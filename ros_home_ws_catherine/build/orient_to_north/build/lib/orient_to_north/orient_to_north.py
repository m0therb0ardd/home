# #!/usr/bin/env python3

# import math
# import rclpy
# from rclpy.node import Node
# from nuturtlebot_msgs.msg import SensorData, WheelCommands

# class OrientToNorthNode(Node):
#     def __init__(self):
#         super().__init__('orient_to_north')

#         # Publishers and Subscribers
#         self.sensor_subscriber = self.create_subscription(
#             SensorData, 'sensor_data', self.sensor_callback, 10)
#         self.wheel_publisher = self.create_publisher(WheelCommands, 'wheel_cmd', 10)

#         # Parameters
#         self.target_heading = 0.0  # North is 0 degrees
#         self.current_heading = None

#         self.get_logger().info("OrientToNorthNode initialized. Waiting for sensor data...")
#         #self.last_log_time = self.get_clock().now()

    

#     def align_to_north(self):
#         if self.current_heading is None:
#             return

#         # Calculate the error between current heading and target (north = 0 degrees)
#         error = self.target_heading - self.current_heading

#         # Normalize error to [-180, 180] for shortest rotation
#         if error > 180:
#             error -= 360
#         elif error < -180:
#             error += 360

#         self.get_logger().info(f"Heading error: {error:.2f}°")

#         # If error is small enough, stop
#         if abs(error) < 5:  # 5 degrees tolerance
#             self.publish_wheel_command(0, 0)  # Stop the wheels
#             self.get_logger().info("Aligned with North!")
#             return

#         # Rotate left or right based on error
#         rotation_speed = 100  # Speed in mcu units
#         if error > 0:
#             self.publish_wheel_command(-rotation_speed, rotation_speed)  # Rotate right
#         else:
#             self.publish_wheel_command(rotation_speed, -rotation_speed)  # Rotate left

#     def publish_wheel_command(self, left_velocity, right_velocity):
#         wheel_cmd = WheelCommands()
#         wheel_cmd.left_velocity = left_velocity
#         wheel_cmd.right_velocity = right_velocity
#         self.wheel_publisher.publish(wheel_cmd)

# def main(args=None):
#     rclpy.init(args=args)
#     node = OrientToNorthNode()
#     rclpy.spin(node)
#     rclpy.shutdown()

# if __name__ == '__main__':
#     main()



#!/usr/bin/env python3

import math
import rclpy
import sys
from rclpy.node import Node
from nuturtlebot_msgs.msg import SensorData, WheelCommands  
from nav_msgs.msg import Odometry
from transforms3d.euler import quat2euler
from math import degrees



class OrientToNorthNode(Node):
    def __init__(self):
        super().__init__('orient_to_north')
        self.sensor_subscriber = self.create_subscription(
            SensorData, 'sensor_data', self.sensor_callback, 10)
        self.wheel_publisher = self.create_publisher(WheelCommands, 'wheel_cmd', 10)

        self.target_heading = 0.0
        self.current_heading = None
        self.filtered_mag_x = None
        self.filtered_mag_y = None
        self.alpha = 0.2  # Smoothing factor
        self.get_logger().info("OrientToNorthNode initialized. Waiting for sensor data...")

    def sensor_callback(self, msg):
        mag_x, mag_y = msg.mag_x, msg.mag_y
        if mag_x == 0 and mag_y == 0:
            return

        if self.filtered_mag_x is None or self.filtered_mag_y is None:
            self.filtered_mag_x, self.filtered_mag_y = mag_x, mag_y
        else:
            self.filtered_mag_x = self.alpha * mag_x + (1 - self.alpha) * self.filtered_mag_x
            self.filtered_mag_y = self.alpha * mag_y + (1 - self.alpha) * self.filtered_mag_y

        heading = math.atan2(self.filtered_mag_y, self.filtered_mag_x)
        heading_degrees = math.degrees(heading)
        if heading_degrees < 0:
            heading_degrees += 360

        self.current_heading = heading_degrees
        self.get_logger().info(f"Smoothed heading: {heading_degrees:.2f}°")
        self.align_to_north()

    def align_to_north(self):
        if self.current_heading is None:
            return

        error = self.target_heading - self.current_heading
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360

        self.get_logger().info(f"Heading error: {error:.2f}°")
        # if abs(error) < 5:
        #     self.publish_wheel_command(0, 0)
        #     self.get_logger().info("Aligned with North!")
        #     return

        # rotation_speed = max(30, min(100, abs(error) * 2))
        # if error > 0:
        #     self.publish_wheel_command(-rotation_speed, rotation_speed)
        # else:
        #     self.publish_wheel_command(rotation_speed, -rotation_speed)

    # def publish_wheel_command(self, left_velocity, right_velocity):
    #     wheel_cmd = WheelCommands()
    #     wheel_cmd.left_velocity = int(left_velocity)  # Ensure integer type
    #     wheel_cmd.right_velocity = int(right_velocity)  # Ensure integer type
    #     self.get_logger().info(f"Publishing wheel command: left={int(left_velocity)}, right={int(right_velocity)}")
    #     self.wheel_publisher.publish(wheel_cmd)


class OrientToHomeNode(Node):
    def __init__(self):
        super().__init__('orient_to_home')
        self.odom_subscriber = self.create_subscription(
            Odometry, '/odom', self.odom_callback, 10
        )
        self.wheel_publisher = self.create_publisher(WheelCommands, '/wheel_cmd', 10)

        self.home_x = 5.0
        self.home_y = 3.0
        self.current_position = {'x': 0.0, 'y': 0.0, 'theta': 0.0}

    def odom_callback(self, msg):
        # Extract position and orientation
        self.current_position['x'] = msg.pose.pose.position.x
        self.current_position['y'] = msg.pose.pose.position.y


        yaw, pitch, roll = quat2euler([q.w, q.x, q.y, q.z])  # Note the order of w, x, y, z
        yaw_degrees = degrees(yaw)  # Convert yaw to degrees if needed
        self.current_position['theta'] = math.degrees(yaw)

        # Orient towards home
        self.orient_towards_home()

    def calculate_heading_to_home(self, current_x, current_y, home_x, home_y):
        dx = home_x - current_x
        dy = home_y - current_y
        desired_heading = math.atan2(dy, dx)  # Result in radians
        return math.degrees(desired_heading)  # Convert to degrees if needed
    
    def calculate_heading_error(self, current_heading, desired_heading):
        error = desired_heading - current_heading
        # Normalize error to [-180, 180] for shortest rotation
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360
        return error


    def orient_towards_home(self):
        current_x = self.current_position['x']
        current_y = self.current_position['y']
        current_heading = self.current_position['theta']

        desired_heading = calculate_heading_to_home(current_x, current_y, self.home_x, self.home_y)
        heading_error = calculate_heading_error(current_heading, desired_heading)

        self.get_logger().info(f"Desired heading: {desired_heading:.2f}°")
        self.get_logger().info(f"Heading error: {heading_error:.2f}°")

        if abs(heading_error) > 5:
            rotation_speed = 100
            if heading_error > 0:
                self.publish_wheel_command(-rotation_speed, rotation_speed)
            else:
                self.publish_wheel_command(rotation_speed, -rotation_speed)
        else:
            self.publish_wheel_command(0, 0)
            self.get_logger().info("Aligned towards home!")

    def publish_wheel_command(self, left_velocity, right_velocity):
        cmd = WheelCommands()
        cmd.left_velocity = int(left_velocity)
        cmd.right_velocity = int(right_velocity)
        self.wheel_publisher.publish(cmd)



def main(args=None):
    rclpy.init(args=args)

    # Check for command-line arguments to select the node
    if len(sys.argv) > 1:
        selected_node = sys.argv[1].lower()
    else:
        selected_node = "north"  # Default to OrientToNorthNode

    if selected_node == "north":
        node = OrientToNorthNode()
        print("Running OrientToNorthNode...")
    elif selected_node == "home":
        node = OrientToHomeNode()
        print("Running OrientToHomeNode...")
    else:
        print(f"Invalid argument: {selected_node}")
        print("Usage: ros2 run <package_name> <script_name> [north|home]")
        rclpy.shutdown()
        return

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        print("Shutting down...")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

# import math
# import rclpy
# from rclpy.node import Node
# from sensor_msgs.msg import LaserScan
# from geometry_msgs.msg import Twist
# from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

# class MoveToOpenSpaceNode(Node):
#     def __init__(self):
#         super().__init__('move_to_open_space')

#         # Set QoS policy for LaserScan to BEST_EFFORT
#         qos = QoSProfile(
#             reliability=ReliabilityPolicy.BEST_EFFORT,  # Match LiDAR's QoS
#             history=HistoryPolicy.KEEP_LAST,
#             depth=10
#         )

#         # LiDAR Subscriber
#         self.scan_subscriber = self.create_subscription(
#             LaserScan,
#             '/scan',
#             self.scan_callback,
#             qos
#         )

#         # Velocity Command Publisher
#         self.cmd_publisher = self.create_publisher(Twist, '/cmd_vel', 10)

#         self.get_logger().info("MoveToOpenSpaceNode initialized!")
#         self.get_logger().info("MoveToOpenSpaceNode initialized!")

#     def scan_callback(self, msg):
#         # Divide ranges into sectors
#         ranges = msg.ranges
#         num_sectors = 36  # Divide 360° into 10° sectors
#         sector_size = len(ranges) // num_sectors

#         max_distance = 0
#         best_sector_index = 0

#         for i in range(num_sectors):
#             sector = ranges[i * sector_size:(i + 1) * sector_size]
#             avg_distance = sum(sector) / len(sector)
#             if avg_distance > max_distance:
#                 max_distance = avg_distance
#                 best_sector_index = i

#         # Calculate angle to the emptiest sector
#         angle = best_sector_index * (360 / num_sectors)
#         self.get_logger().info(f"Emptiest space at angle: {angle:.2f}°, max distance: {max_distance:.2f}m")

#         self.move_towards(angle)

#     def move_towards(self, angle):
#         twist = Twist()

#         # Normalize angle to [-180, 180]
#         if angle > 180:
#             angle -= 360

#         # Rotate proportional to the angle
#         twist.angular.z = math.radians(angle) * 0.5  # Scale angular speed

#         # Move forward if the angle is small (nearly aligned)
#         if abs(angle) < 15:
#             twist.linear.x = 0.2  # Adjust forward speed as needed
#         else:
#             twist.linear.x = 0.0

#         # Publish the Twist command
#         self.get_logger().info(f"Moving towards angle: {angle:.2f}°")
#         self.cmd_publisher.publish(twist)


# def main(args=None):
#     rclpy.init(args=args)
#     node = MoveToOpenSpaceNode()
#     try:
#         rclpy.spin(node)
#     except KeyboardInterrupt:
#         pass
#     finally:
#         node.destroy_node()
#         rclpy.shutdown()

# if __name__ == '__main__':
#     main()

import math
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from nuturtlebot_msgs.msg import WheelCommands  # Import WheelCommands
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy

class MoveToOpenSpaceNode(Node):
    def __init__(self):
        super().__init__('move_to_open_space')

        # Set QoS policy for LaserScan to BEST_EFFORT
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10
        )

        # LiDAR Subscriber
        self.scan_subscriber = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos
        )

        # Wheel Command Publisher
        self.wheel_publisher = self.create_publisher(WheelCommands, '/wheel_cmd', 10)

        self.get_logger().info("MoveToOpenSpaceNode initialized!")

    def scan_callback(self, msg):
        # Divide ranges into sectors
        ranges = msg.ranges
        num_sectors = 36  # Divide 360° into 10° sectors
        sector_size = len(ranges) // num_sectors

        max_distance = 0
        best_sector_index = 0

        for i in range(num_sectors):
            sector = ranges[i * sector_size:(i + 1) * sector_size]
            avg_distance = sum(sector) / len(sector)
            if avg_distance > max_distance:
                max_distance = avg_distance
                best_sector_index = i

        # Calculate angle to the emptiest sector
        angle = best_sector_index * (360 / num_sectors)
        self.get_logger().info(f"Emptiest space at angle: {angle:.2f}°, max distance: {max_distance:.2f}m")

        self.move_towards(angle)

    def move_towards(self, angle):
        # Normalize angle to [-180, 180]
        if angle > 180:
            angle -= 360

        wheel_cmd = WheelCommands()

        # If angle is small, move forward
        if abs(angle) < 15:
            wheel_cmd.left_velocity = 100  # Adjust speed as needed
            wheel_cmd.right_velocity = 100
        else:  # Rotate towards the target direction
            rotation_speed = 50  # Adjust rotation speed as needed
            if angle > 0:
                # Turn left
                wheel_cmd.left_velocity = -rotation_speed
                wheel_cmd.right_velocity = rotation_speed
            else:
                # Turn right
                wheel_cmd.left_velocity = rotation_speed
                wheel_cmd.right_velocity = -rotation_speed

        self.get_logger().info(f"Publishing WheelCommands: left={wheel_cmd.left_velocity}, right={wheel_cmd.right_velocity}")
        self.wheel_publisher.publish(wheel_cmd)


def main(args=None):
    rclpy.init(args=args)
    node = MoveToOpenSpaceNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()


#!/usr/bin/env python3

import math
import rclpy
from rclpy.node import Node
from nuturtlebot_msgs.msg import SensorData, WheelCommands

class OrientToNorthNode(Node):
    def __init__(self):
        super().__init__('orient_to_north')

        # Publishers and Subscribers
        self.sensor_subscriber = self.create_subscription(
            SensorData, 'sensor_data', self.sensor_callback, 10)
        self.wheel_publisher = self.create_publisher(WheelCommands, 'wheel_cmd', 10)

        # Parameters
        self.target_heading = 0.0  # North is 0 degrees
        self.current_heading = None

        self.get_logger().info("OrientToNorthNode initialized. Waiting for sensor data...")
        #self.last_log_time = self.get_clock().now()

    def sensor_callback(self, msg):
        mag_x = msg.mag_x
        mag_y = msg.mag_y

        # Filter: Only process and log if either mag_x or mag_y is non-zero
        if mag_x == 0 and mag_y == 0:
            return  # Skip processing if magnetometer values are zero

        self.get_logger().info(f"In sensor callback... Raw data: {msg}")
        self.get_logger().info(f"Extracted magnetometer data: x={mag_x}, y={mag_y}")

        # Calculate the current heading in radians
        heading = math.atan2(mag_y, mag_x)

        # Convert to degrees and normalize to [0, 360]
        heading_degrees = math.degrees(heading)
        if heading_degrees < 0:
            heading_degrees += 360

        self.current_heading = heading_degrees
        self.get_logger().info(f"Current heading: {heading_degrees:.2f}°")

        # Decide on motion
        self.align_to_north()

    def align_to_north(self):
        if self.current_heading is None:
            return

        # Calculate the error between current heading and target (north = 0 degrees)
        error = self.target_heading - self.current_heading

        # Normalize error to [-180, 180] for shortest rotation
        if error > 180:
            error -= 360
        elif error < -180:
            error += 360

        self.get_logger().info(f"Heading error: {error:.2f}°")

        # If error is small enough, stop
        if abs(error) < 5:  # 5 degrees tolerance
            self.publish_wheel_command(0, 0)  # Stop the wheels
            self.get_logger().info("Aligned with North!")
            return

        # Rotate left or right based on error
        rotation_speed = 100  # Speed in mcu units
        if error > 0:
            self.publish_wheel_command(-rotation_speed, rotation_speed)  # Rotate right
        else:
            self.publish_wheel_command(rotation_speed, -rotation_speed)  # Rotate left

    def publish_wheel_command(self, left_velocity, right_velocity):
        wheel_cmd = WheelCommands()
        wheel_cmd.left_velocity = left_velocity
        wheel_cmd.right_velocity = right_velocity
        self.wheel_publisher.publish(wheel_cmd)

def main(args=None):
    rclpy.init(args=args)
    node = OrientToNorthNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from rclpy.qos import QoSProfile, ReliabilityPolicy, HistoryPolicy


class SimpleLidarTest(Node):
    def __init__(self):
        super().__init__('simple_lidar_test')
        
        # Define QoS with Best Effort reliability and required parameters
        qos = QoSProfile(
            reliability=ReliabilityPolicy.BEST_EFFORT,
            history=HistoryPolicy.KEEP_LAST,
            depth=10  # Buffer size for messages
        )
        
        self.subscription = self.create_subscription(
            LaserScan,
            '/scan',
            self.scan_callback,
            qos)  # Pass QoS profile
        self.get_logger().info("SimpleLidarTest initialized. Listening to /scan...")

    def scan_callback(self, msg):
        # Print a sample of ranges
        self.get_logger().info(f"Ranges: {msg.ranges[:10]}")  # First 10 range values

def main(args=None):
    rclpy.init(args=args)
    node = SimpleLidarTest()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

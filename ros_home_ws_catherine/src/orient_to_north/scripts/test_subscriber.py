import rclpy
from rclpy.node import Node
from nuturtlebot_msgs.msg import SensorData

class TestSubscriber(Node):
    def __init__(self):
        super().__init__('test_subscriber')
        self.create_subscription(SensorData, '/sensor_data', self.callback, 10)

    def callback(self, msg):
        self.get_logger().info(f"Received: {msg}")

def main(args=None):
    rclpy.init(args=args)
    node = TestSubscriber()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()

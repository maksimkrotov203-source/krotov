#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class OverflowListener(Node):
    """
    Слушает топик /overflow и выводит предупреждение о переполнении.
    """

    def __init__(self):
        super().__init__('overflow_listener')

        self.subscription = self.create_subscription(
            Int32,
            '/overflow',
            self.listener_callback,
            10)
        self.subscription  # для устранения предупреждения

        self.get_logger().info("👂 Узел overflow_listener запущен и слушает /overflow...")

    def listener_callback(self, msg):
        self.get_logger().warn(f'🔥 !!! ПЕРЕПОЛНЕНИЕ !!! Получено значение: {msg.data}')

def main(args=None):
    rclpy.init(args=args)
    node = OverflowListener()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("🛑 Узел остановлен")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

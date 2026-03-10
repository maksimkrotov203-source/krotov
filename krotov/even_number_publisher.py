#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    """
    Публикует чётные числа от 0 до 98 в /even_numbers (10 Гц).
    При достижении 100 публикует 100 в /overflow и сбрасывает счётчик.
    """

    def __init__(self):
        # Имя узла: even_pub (как в задании)
        super().__init__('even_pub')

        # --- Издатели ---
        self.even_publisher = self.create_publisher(Int32, '/even_numbers', 10)
        self.overflow_publisher = self.create_publisher(Int32, '/overflow', 10)

        # --- Состояние ---
        self.counter = 0
        self.max_value = 100

        # --- Таймер на 10 Гц (0.1 сек) ---
        self.timer = self.create_timer(0.1, self.timer_callback)

        self.get_logger().info("✅ Узел even_pub запущен. Публикация чётных чисел...")

    def timer_callback(self):
        # 1. Публикуем текущее чётное число
        msg = Int32()
        msg.data = self.counter
        self.even_publisher.publish(msg)
        self.get_logger().info(f'📤 Чётное: {msg.data}')

        # 2. Проверка переполнения
        if self.counter >= self.max_value:
            overflow_msg = Int32()
            overflow_msg.data = self.counter
            self.overflow_publisher.publish(overflow_msg)
            self.get_logger().warn(f'❗ ПЕРЕПОЛНЕНИЕ! Сброс. Отправлено: {overflow_msg.data}')
            self.counter = 0  # Сброс
        else:
            # Следующее чётное число
            self.counter += 2

def main(args=None):
    rclpy.init(args=args)
    node = EvenNumberPublisher()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info("🛑 Узел остановлен")
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()

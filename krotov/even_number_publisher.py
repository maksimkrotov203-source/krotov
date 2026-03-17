#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Int32

class EvenNumberPublisher(Node):
    def __init__(self):
        super().__init__('even_pub') # Имя узла

        # --- ОБЪЯВЛЯЕМ ПАРАМЕТРЫ (как в методичке) ---
        self.declare_parameter('publish_frequency', 10.0) # Значение по умолчанию
        self.declare_parameter('overflow_threshold', 100)
        self.declare_parameter('topic_name', '/even_numbers')

        # --- ЧИТАЕМ ЗНАЧЕНИЯ ПАРАМЕТРОВ ---
        self.freq = self.get_parameter('publish_frequency').value
        self.threshold = self.get_parameter('overflow_threshold').value
        self.topic = self.get_parameter('topic_name').value

        # Логируем, какие параметры загружены (для проверки)
        self.get_logger().info(f'Параметры: частота={self.freq} Гц, порог={self.threshold}, топик="{self.topic}"')

        # --- ИЗДАТЕЛИ ---
        self.even_publisher = self.create_publisher(Int32, self.topic, 10)
        self.overflow_publisher = self.create_publisher(Int32, '/overflow', 10)

        # --- СОСТОЯНИЕ ---
        self.counter = 0

        # --- ТАЙМЕР (используем параметр self.freq) ---
        timer_period = 1.0 / self.freq
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.get_logger().info("✅ Узел even_pub запущен и готов к работе.")

    def timer_callback(self):
        # ... (ваш код публикации и проверки переполнения БЕЗ ИЗМЕНЕНИЙ) ...
        msg = Int32()
        msg.data = self.counter
        self.even_publisher.publish(msg)
        self.get_logger().info(f'📤 Чётное: {msg.data}')

        if self.counter >= self.threshold: # Используем параметр self.threshold
            overflow_msg = Int32()
            overflow_msg.data = self.counter
            self.overflow_publisher.publish(overflow_msg)
            self.get_logger().warn(f'❗ ПЕРЕПОЛНЕНИЕ! Сброс. Отправлено: {overflow_msg.data}')
            self.counter = 0
        else:
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

#!/usr/bin/env python3
"""Узел вывода текущего времени каждые 5 секунд"""

import rclpy
from rclpy.node import Node
from datetime import datetime

class TimePrinter(Node):
    def __init__(self):
        super().__init__('time_printer_node')
        # Создаём таймер, который вызывает callback каждые 5 секунд (5000 мс)
        self.timer = self.create_timer(5.0, self.timer_callback)
    
    def timer_callback(self):
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.get_logger().info(f'Текущее время: {current_time} 🕐')

def main(args=None):
    rclpy.init(args=args)
    node = TimePrinter()
    rclpy.spin(node)  # Запускаем цикл обработки
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from std_msgs.msg import String


class car(Node):
    """
    Узел-подписчик, который реагирует на сигнал светофора (цвет)
    """

    def __init__(self):
        super().__init__('car')

        # Создаём Subscriber
        self.subscriber_ = self.create_subscription(
            String,  # тип сообщения
            'traffic_light',  # имя топика
            self.light_callback,  # функция обработки
            9  # размер очереди
        )

        self.get_logger().info('car готов к движению!')

    def light_callback(self, msg):
        """
        Функция обработки сообщений от светофора.
        """
        light_color = msg.data

        # Реагируем в зависимости от цвета
        if light_color == 'RED':
            self.get_logger().info('Остановка!')
        elif light_color == 'YELLOW':
            self.get_logger().info('Замедляюсь...')
        elif light_color == 'GREEN':
            self.get_logger().info('Еду!')


def main(args=None):
    rclpy.init(args=args)
    node = car()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
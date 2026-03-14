import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, Bool


class TemperatureSensor(Node):
    """
    Симулятор температуры процессора.

    """

    def __init__(self):
        super().__init__('temperature_sensor')

        # Начальные параметры
        self.temperature = 25.0  # температура
        self.is_robot_moving = False  # движется ли робот

        # Publisher для уровня батареи
        self.temp_publisher = self.create_publisher(
            Float32,
            '/temperature',
            10
        )

        # Subscriber для состояния моторов
        self.motor_subscriber = self.create_subscription(
            Bool,
            '/motor_state',
            self.motor_state_callback,
            10
        )

        # Таймер для смены температуры (каждые 2 секунды)
        self.timer = self.create_timer(2.0, self.update_temperature)

        self.get_logger().info('temperature Sensor started - Initial charge: 25.0 C')

    def motor_state_callback(self, msg):
        """
        Получаем информацию о состоянии моторов.
        """
        self.is_robot_moving = msg.data
        state = "MOVING" if self.is_robot_moving else "IDLE"
        self.get_logger().info(f'Motor state changed: {state}')

    def update_temperature(self):
        """
        Обновление температуры у процессора.
        """
        if self.temperature < 25.0:
            self.temperature = 25.0
            self.get_logger().info('Температура достигла минимума: 25.0 C')
        elif self.temperature > 80.0:
            self.temperature = 80.0
            self.get_logger().info('Температура достигла максимума: 80.0 C')

        # Температура процессора зависит от состояния моторов
        if self.is_robot_moving:
            self.temperature += 2.0  # +2 при движении
            self.get_logger().warn(f'Температура повышается (moving): {self.temperature:.1f}С')
        else:
            self.temperature -= 1.0  # -1 в покое
            self.get_logger().warn(f'Температура понижается (idle): {self.temperature:.1f}С')

        # Публикуем текущий уровень
        msg = Float32()
        msg.data = self.temperature
        self.temp_publisher.publish(msg)

        # Предупреждения о высокой температуры
        if self.temperature > 70.0:
            self.get_logger().warn(f'Слишком высокая температура: {self.temperature:.1f}C !!!')
        elif self.temperature > 25.0:
            self.get_logger().info(f'Температура: {self.temperature:.1f}C')


def main(args=None):
    rclpy.init(args=args)
    node = TemperatureSensor()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
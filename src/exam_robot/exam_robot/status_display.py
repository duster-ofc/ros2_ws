import rclpy
from rclpy.node import Node
from std_msgs.msg import Float32, String


class StatusDisplay(Node):
    def __init__(self):
        super().__init__('status_display')

        # Состояния
        self.battery = 100.0
        self.distance = 3.0
        self.current_status = ""

        # Подписки
        self.sub_battery = self.create_subscription(
            Float32,
            'battery_level',
            self.battery_cb,
            10
        )
        self.sub_distance = self.create_subscription(
            Float32,
            'distance',
            self.distance_cb,
            10
        )

        # Публикация
        self.publisher_ = self.create_publisher(
            String,
            'robot_status',
            10
        )

        # Таймер на 2 Hz
        self.timer = self.create_timer(0.5, self.timer_callback)

        self.get_logger().info('Status Display started')

    def battery_cb(self, msg):
        self.battery = msg.data

    def distance_cb(self, msg):
        self.distance = msg.data

    def timer_callback(self):
        # Определяем статус (от самого критичного к нормальному)
        if self.battery < 10.0 or self.distance < 0.7:
            new_status = "CRITICAL"
        elif self.battery < 20.0:
            new_status = "WARNING: Low battery"
        elif self.distance < 1.0:
            new_status = "WARNING: Obstacle close"
        else:
            new_status = "ALL OK"

        # Логируем изменения
        if new_status != self.current_status:
            self.get_logger().info(f'Status changed: {self.current_status} -> {new_status}')
            self.current_status = new_status

        # Публикуем текущий статус
        msg = String()
        msg.data = self.current_status
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = StatusDisplay()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
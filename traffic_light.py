import rclpy
from rclpy.node import Node
from std_msgs.msg import String # Импортируем тип сообщения

class traffic_light(Node):
     """
     Узел-издатель, который публикует новости робота.
     """

     def __init__(self):
         super().__init__('traffic_light')

         # Создаём Publisher
         self.publisher_ = self.create_publisher(
            String, # тип сообщения
            'traffic_light', # имя топика
            9 # размер очереди
         )

         # Таймер для публикации каждые 3 секунды
         self.timer = self.create_timer(3.0, self.publish_light_state)

         # Цвета
         self.colors = ['RED', 'YELLOW', 'GREEN']
         self.current_color_index = 0

         self.get_logger().info('Traffic Light запущен!')

     def publish_light_state(self):
         """
         Функция публикации цвета.
         """
         # Берём текущий цвет по индексу
         current_color = self.colors[self.current_color_index]

         # Создаём сообщение
         msg = String()
         msg.data = current_color

         # Публикуем сообщение
         self.publisher_.publish(msg)

         # Выводим в лог
         self.get_logger().info(f'Светофор: {msg.data}')

         # Переходим к следующему цвету
         self.current_color_index = (self.current_color_index + 1) % len(self.colors)

def main(args=None):
    rclpy.init(args=args)
    node = traffic_light()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()
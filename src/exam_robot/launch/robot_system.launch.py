import os
from launch import LaunchDescription
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    """
    Launch-файл для запуска всей системы робота.
    Запускает все 4 узла exam_robot и robot_state_publisher с URDF моделью.
    """

    # Получаем путь к директории установленного пакета
    pkg_share = get_package_share_directory('exam_robot')

    # Формируем полный путь к URDF файлу
    urdf_file = os.path.join(pkg_share, 'urdf', 'exam_robot.urdf')

    # Читаем содержимое URDF файла
    with open(urdf_file, 'r') as infp:
        robot_description = infp.read()

    # Создаём и возвращаем описание запуска
    return LaunchDescription([
        # 1. battery_node
        Node(
            package='exam_robot',
            executable='battery_node',
            name='battery_node',
            output='screen',
        ),

        # 2. distance_sensor
        Node(
            package='exam_robot',
            executable='distance_sensor',
            name='distance_sensor',
            output='screen',
        ),

        # 3. status_display
        Node(
            package='exam_robot',
            executable='status_display',
            name='status_display',
            output='screen',
        ),

        # 4. robot_controller
        Node(
            package='exam_robot',
            executable='robot_controller',
            name='robot_controller',
            output='screen',
        ),

        # 5. Узел robot_state_publisher (публикует состояние робота по URDF)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{'robot_description': robot_description}],
            output='screen',
        ),
    ])

from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="meu_drone",
                executable="movimentacao",
                name="movimentacao",
                output="screen",
            ),
            Node(
                package="meu_drone",
                executable="posicao_drone",
                name="posicao_drone",
                output="screen",
            ),
            Node(
                package="meu_drone",
                executable="obstaculo",
                name="obstaculo",
                output="screen",
            ),
        ]
    )

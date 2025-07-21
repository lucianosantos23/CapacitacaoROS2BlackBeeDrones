#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import math
from std_msgs.msg import Float32MultiArray  # Alterado para MultiArray


# NÓ QUE ATRAVÉS DA VELOCIDADE ESTIMA A POSIÇÃO
class PosicaoEstimadaNode(Node):
    def __init__(self):
        super().__init__("posicao_estimada")

        self.subscription = self.create_subscription(
            Twist, "movimentos", self.twist_callback, 10
        )  # recebe as velocidades de "movimentos" e chama a funçao twist_callback

        self.publisher = self.create_publisher(
            Float32MultiArray, "posicao", 10
        )  # publica qual a posição estimada do drone

        self.create_timer(
            0.1, self.posicaoAtual
        )  # a cada 0.1seg chama a função posicaoAtual

        self.x = 0.0
        self.y = 1.0
        self.z = 0.0
        self.yaw = 0.0

        self.last_time = self.get_clock().now()

    def twist_callback(self, msg: Twist):
        now = self.get_clock().now()  # retorna o tempo atual
        dt = (
            now - self.last_time
        ).nanoseconds / 1e9  # faz o delta t para cálculo da distância
        self.last_time = now  # atualiza o valor de last time

        if dt > 1:  # tempo mt grande entre as execuções, nao houve movimentação
            return  # sai da função

        self.x += msg.linear.x * dt
        self.y = max(0, self.y + msg.linear.y * dt)  # nao tem como y < 0
        self.z += msg.linear.z * dt

        yaw_rad = math.atan2(self.z, self.x)
        yaw_deg = math.degrees(yaw_rad)  # transforma em graus

        self.get_logger().info(
            f"Posição estimada -> x: {self.x:.2f}, y: {self.y:.2f}, z: {self.z:.2f}, theta(yaw): {yaw_deg:.2f}"
        )

    def posicaoAtual(self):
        msg = Float32MultiArray()
        msg.data = [
            float(self.x),
            float(self.y),
            float(self.z),
        ]  # converte para float32
        self.publisher.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = PosicaoEstimadaNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from .drone import Drone

# NÓ QUE MANDA O DRONE PRA FRENTE E DESVIA DO OBJETO


class Movimentacao(Node):

    def __init__(self):
        super().__init__("movimentacao")
        self.drone = Drone()
        self.desviando = False

        self.movimentos_pub = self.create_publisher(
            Twist, "movimentos", 10
        )  # publica quais movimentos está fazendo

        self.movimentos_sub = self.create_subscription(
            Twist, "desvia", self.desvia_callback, 10
        )  # recebe informação se precisa desviar

        self.create_timer(
            0.1, self.movimento_padrao
        )  # chama a função movimento_padrao(drone pra frente) a cada 0.1

        self.create_timer(0.1, self.motores)  # chama a função motores a cada 0.1

        self.create_timer(0.1, self.resetar_desvio)

    def desvia_callback(self, msg: Twist):
        self.desviando = True
        self.drone.up()
        self.movimentos_pub.publish(msg)

    def resetar_desvio(self):
        self.desviando = False

    def movimento_padrao(self):  # manda o drone pra frente
        if self.desviando:
            self.drone.m1 = 30
            self.drone.m2 = 30
            return
        msg = Twist()
        msg.linear.x = 1.0
        self.drone.frente()
        self.movimentos_pub.publish(msg)

    def sobe_drone(self):  # take off
        msg = Twist()
        msg.linear.z = 1.0
        self.drone.up()
        self.movimentos_pub.publish(msg)

    def motores(self):
        self.get_logger().info(
            f"M1 = {self.drone.m1}, M2 = {self.drone.m2}, M3 = {self.drone.m3}, M4 = {self.drone.m4}"
        )


def main(args=None):
    rclpy.init(args=args)
    node = Movimentacao()
    rclpy.spin(node)
    node.drone.land()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_msgs.msg import Float32MultiArray
import random
import os


# NÓ PARA AFERIR DISTÂNCIA DE OBSTÁCULO E AVISAR PARA DESVIAR
class Obstaculo(Node):
    def __init__(self):
        super().__init__("obstaculo")
        self.obstaculo_sub = self.create_subscription(
            Float32MultiArray, "posicao", self.obs_callback, 10
        )  # recebe a pos do drone
        self.aviso_pub = self.create_publisher(
            Twist, "desvia", 10
        )  # avisa pra mover o drone para cima

        self.obsx = random.randint(8, 25)  # para o obstáculo vir em algum lugar random
        self.obsAltura = random.uniform(1.5, 3)
        self.distancia_seguranca = 2.5 * self.obsAltura
        self.velocidade_subida = 1.0
        self.limpeza_feita = False  # usado para limpar o terminal após desviar o objeto

    def obs_callback(self, msg: Float32MultiArray):
        desvio = Twist()  # criar um dado do tipo Twist para enviar para "desvia"
        x, y, z = msg.data[0], msg.data[1], msg.data[2]

        if (
            abs(x - self.obsx) > 0 and abs(x - self.obsx) < 0.5 and y < self.obsAltura
        ):  # se estiver com a distancia menos de 0.5m, colidiu
            self.get_logger().warn("Colisão!!!")

        elif (
            abs(x - self.obsx) < self.distancia_seguranca and y < self.obsAltura
        ):  # se está mais próximo que a distância segura, avisa
            desvio.linear.y = self.velocidade_subida
            self.aviso_pub.publish(desvio)
            self.get_logger().warn(f"Objeto a {abs(x - self.obsx):.2f} metros")
            self.limpeza_feita = False

        elif (
            not self.limpeza_feita and x > self.obsx + 2
        ):  # para limpar o terminal, se ja me afastei e a distância é maior que 2m, limpa
            os.system("clear")
            self.limpeza_feita = True

        elif not self.limpeza_feita and x < self.obsx - 2:
            os.system("clear")
            self.limpeza_feita = True

        elif abs(x - self.obsx) < self.distancia_seguranca:
            self.limpeza_feita = False


def main(args=None):
    rclpy.init(args=args)
    node = Obstaculo()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == "__main__":
    main()

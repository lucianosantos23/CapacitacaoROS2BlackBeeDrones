#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from .drone import Drone
import curses  # nova lib para capturar teclado

# NÓ PARA CONTROLAR O DRONE PELO TECLADO


class DroneKeyboardControl(Node):
    def __init__(self):
        super().__init__("drone_keyboard_control")
        self.drone = Drone()
        self.movimentos_pub = self.create_publisher(Twist, "movimentos", 10)

        # configuração do curses
        self.stdscr = curses.initscr()
        curses.cbreak()
        self.stdscr.keypad(True)
        self.stdscr.nodelay(True)

        self.timer = self.create_timer(
            0.01, self.check_keyboard
        )  # a cada 0.01 seg chama a função check_keyboard

    def check_keyboard(self):
        msg = Twist()

        key = self.stdscr.getch()  # pega oq foi digitado e executa o movimento

        if key == -1:
            return

        if key == ord("w") or key == ord("W"):
            self.drone.frente()
            msg.linear.x = 1.0
        elif key == ord("s") or key == ord("S"):
            self.drone.tras()
            msg.linear.x = -1.0

        if key == ord("q") or key == ord("Q"):
            self.drone.esquerda()
            msg.linear.z = 1.0
        elif key == ord("e") or key == ord("E"):
            self.drone.direita()
            msg.linear.z = -1.0

        if key == ord("d") or key == ord("D"):
            self.drone.up()
            msg.linear.y = 1.0
        elif key == ord("a") or key == ord("A"):
            self.drone.down()
            msg.linear.y = -1.0

        if key == ord("y") or key == ord("Y"):
            self.drone.girar_esquerda()
            msg.angular.z = 1.0
        elif key == ord("u") or key == ord("U"):
            self.drone.girar_direita()
            msg.angular.z = -1.0

        if key == ord("p") or key == ord("P"):
            self.drone.pousar()

        self.movimentos_pub.publish(
            msg
        )  # envia qual foi o movimento para o topic "movimentos"


def main(args=None):
    rclpy.init(args=args)
    node = DroneKeyboardControl()
    rclpy.spin(node)
    node.cleanup()
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()

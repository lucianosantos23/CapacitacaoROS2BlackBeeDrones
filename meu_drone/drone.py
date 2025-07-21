import time

ajuste = 1.5


class Drone:
    def __init__(self, raio=1):
        self.x = 5
        self.y = 10
        self.z = 4
        self.LiDAR = 0
        self.m1 = self.m2 = self.m3 = self.m4 = 70
        self.roll = self.yaw = self.pitch = 0
        self.raio = raio
        self.alturas = []
        self.trajetoria = []

    def limitar_potencias(self):
        for m in ["m1", "m2", "m3", "m4"]:
            setattr(self, m, max(30, min(100, getattr(self, m))))

    def esquerda(self):
        self.roll = max(-30, self.roll - 3)
        self.m1 -= ajuste
        self.m3 -= ajuste
        self.m2 += ajuste
        self.m4 += ajuste
        if self.roll < -5:
            self.x = max(0, self.x - 1)
        self.limitar_potencias()

    def direita(self):
        self.roll = min(30, self.roll + 3)
        self.m1 += ajuste
        self.m3 += ajuste
        self.m2 -= ajuste
        self.m4 -= ajuste
        if self.roll > 5:
            self.x = min(10, self.x + 1)
        self.limitar_potencias()

    def frente(self):
        self.pitch = max(-30, self.pitch - 3)
        self.m1 += ajuste
        self.m2 += ajuste
        self.m3 -= ajuste
        self.m4 -= ajuste
        self.z = min(10, self.z + 1)
        self.limitar_potencias()

    def tras(self):
        self.pitch = min(30, self.pitch + 3)
        self.m1 -= ajuste
        self.m2 -= ajuste
        self.m3 += ajuste
        self.m4 += ajuste
        self.z = max(0, self.z - 1)
        self.limitar_potencias()

    def up(self, quant=1):
        self.y = min(10, self.y + quant)
        self.m1 += ajuste
        self.m2 += ajuste
        self.m3 += ajuste
        self.m4 += ajuste
        self.alturas.append(self.y)
        self.limitar_potencias()

    def down(self, quant=1):
        self.y = max(0, self.y - quant)
        self.m1 -= ajuste
        self.m2 -= ajuste
        self.m3 -= ajuste
        self.m4 -= ajuste
        self.alturas.append(self.y)
        self.limitar_potencias()

    def girar_direita(self):
        self.yaw = (self.yaw + 10) % 360
        self.m1 += ajuste
        self.m3 += ajuste
        self.m2 -= ajuste
        self.m4 -= ajuste
        self.limitar_potencias()

    def girar_esquerda(self):
        self.yaw = (self.yaw - 10) % 360
        self.m2 += ajuste
        self.m4 += ajuste
        self.m1 -= ajuste
        self.m3 -= ajuste
        self.limitar_potencias()

    def pousar(self):
        print("Drone pousando...")
        while self.y > 0:
            self.down()

    def parar(self):
        self.pitch = self.roll = 0
        self.m1 = self.m2 = self.m3 = self.m4 = 70
        self.limitar_potencias()

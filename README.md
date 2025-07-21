# Projeto de Controle de Drone com ROS2

Sistema para controle de drone com ROS2, incluindo navegação manual, detecção de obstáculos e controle autônomo.

Os codigós dos nós e a classe Drone estão em: src/meu_drone/meu_drone

🚀 Nós Implementados

  1. `controle_drone.py` - Controle Manual por Teclado
	- Comandos:
	  - W/S: Frente/Trás
	  - A/D: Desce/Sobe
	  - Q/E: Esquerda/Direita
	  - Y/U: Girar esquerda/direita
	  - P: Pousar
	  - Publica: Tópico `movimentos` (Twist)

 2. `drone.py` - Modelo Físico do Drone
	 - Simula comportamento físico com:
	  - Controle de motores (M1-M4)
	  - Limitação de potências
	  - Cálculo de rotação (roll, pitch, yaw)

 3. `movimentacao.py` - Controle Autônomo
	- Movimento padrão para frente
	- Sistema de desvio de obstáculos
	- Subscreve: Tópico `desvia` (Twist)
	- Publica: Tópico `movimentos` (Twist)

 4. `obstaculo.py` - Detecção de Colisão
	- Gera obstáculos aleatórios
	- Calcula distância de segurança
	- Publica: Alertas no tópico `desvia` (Twist)

 5. `posicao_drone.py` - Estimativa de Posição
	- Calcula posição com base na velocidade
	- Publica: Tópico `posicao` (Float32MultiArray)

 🔌 Tópicos ROS2

| Tópico         | Tipo               | Descrição                     |
|----------------|--------------------|-------------------------------|
| `movimentos`   | Twist              | Comandos de movimento         |
| `desvia`       | Twist              | Alertas de obstáculo          |
| `posicao`      | Float32MultiArray  | Posição estimada do drone     |

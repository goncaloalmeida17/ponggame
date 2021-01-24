from kivy.app import App
from kivy.uix.widget import Widget
from kivy.properties import NumericProperty, ReferenceListProperty, ObjectProperty
from kivy.vector import Vector
from kivy.clock import Clock
from random import randint


class PongPaddle(Widget):
    score = NumericProperty(0)

    def bounce_ball(self, ball):
        if self.collide_widget(ball):  # O self refere-se à PongPaddle
            ball.velocity_x *= -1  # Se diminuirmos para -2 por exemplo, a velocidade da bola aumenta


class PongBall(Widget):
    velocity_x = NumericProperty(0)  # Valor inteiro
    velocity_y = NumericProperty(0)
    velocity = ReferenceListProperty(velocity_x,
                                     velocity_y)  # Dá para aceder aos dois tipos de velocidade, como se fosse uma tuple

    # Latest Position = Current velocity + Current Position
    def move(self):
        self.pos = Vector(*self.velocity) + self.pos


# Update - Moving the ball by calling the move() and other stuff
class PongGame(Widget):  # Criação do jogo
    ball = ObjectProperty(None)  # Objeto
    player1 = ObjectProperty(None)
    player2 = ObjectProperty(None)

    def serve_ball(self):
        self.ball.velocity = Vector(4, 0).rotate(randint(0, 360))  # Alteração da variável velocity que se refere à velocidade e direção da bola, sendo que avança 4px

    def update(self, dt):  # A cada segundo esta função é chamada 60 vezes (linha 2 da função build da class PongApp)
        self.ball.move()  # Isto funciona pois no ficheiro pong.kv a bola está associada a um id que está associado à class PongBall
        num = 50  # Criei esta variável por causa do erro causado pelo bouncing da bola na parte cima e na parte da direita, sendo este número o tamanho da bola

        # bounce off top and bottom
        if (self.ball.y < 0) or (self.ball.y > self.height - num):
            self.ball.velocity_y *= -1  # Faz 180 menos o ângulo que bateu na borda

        # bounce off left
        if self.ball.x < 0:
            self.ball.velocity_x *= -1  # Faz 180 menos o ângulo que bateu na borda
            self.player1.score += 1

        # bounce off right
        if self.ball.x > self.width - num:
            self.ball.velocity_x *= -1
            self.player2.score += 1

        self.player1.bounce_ball(self.ball)
        self.player2.bounce_ball(self.ball)

    def on_touch_move(self, touch):
        if touch.x < self.width / 1 / 4:
            self.player1.center_y = touch.y
        if touch.x > self.width * 3 / 4:
            self.player2.center_y = touch.y


class PongApp(App):  # Criação da aplicação
    def build(self):
        game = PongGame()
        game.serve_ball()
        Clock.schedule_interval(game.update, 1.0 / 60.0)  # 1seg = 60 imagens (60fps)
        return game


PongApp().run()  # Iniciar o jogo

# self.height -> altura da preprint janela
# root.top - 50 -> margem de 50px do topo da janela
# size: self.size -> fazemos isto e não definimos diretamente o tamanho pois a bola não ficaria centrada no canvas
# self.parent.center -> É o centro do PongGame que é o parente de PongBall
# velocity tem direção e velocidade e speed só tem velocidade
# root.width - self.width -> Desenha o retângulo o mais à esquerda possível mas toda a paddle é apresentada daí a subtração

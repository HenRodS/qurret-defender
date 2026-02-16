import pygame

class player(object):
    def __init__(self, pos, size, color):
        self.pos = pos
        self.size = size
        self.color = color
        self.speed = 300
        self.direction = pygame.Vector2(0, 0)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def update(self, dt):
        self.direction = pygame.mouse.get_pos() - self.pos
        self.direction = self.direction.normalize()

    def draw_mira(self, screen):
        if self.direction.length() > 0:
            distancia_mira = 40
            tamanho_triangulo = 10
            
            ponta = self.pos + self.direction * distancia_mira
            ortogonal = pygame.Vector2(-self.direction.y, self.direction.x) * (tamanho_triangulo / 2)
            base_esq = (self.pos + self.direction * (distancia_mira - 10)) + ortogonal
            base_dir = (self.pos + self.direction * (distancia_mira - 10)) - ortogonal

            pygame.draw.polygon(screen, (255, 255, 255), [ponta, base_esq, base_dir])


# Projétil - vai sair da posição do jogador e avançar em direção à mira
class projectile(object):
    def __init__(self, pos, size, color, direction):
        self.pos = pos
        self.size = size
        self.color = color
        self.direction = direction
        self.vel = 8 * direction
        self.distancia_percorrida = 0
        self.range = 100
        self.active = True

    # verificar se está bom (HENRIQUE)
    # NAO ESQUECE DE COLOCAR O PROJETO NO GIT
    def update(self, dt):
        self.pos += self.vel * dt
        self.distancia_percorrida += self.vel.length() * dt
        if self.distancia_percorrida >= self.range:
            self.active = False

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)
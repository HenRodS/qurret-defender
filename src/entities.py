import pygame

class player(object):
    def __init__(self, pos, size, life, color):
        self.life = life
        self.pos = pos
        self.size = size
        self.color = color
        self.speed = 300
        self.direction = pygame.Vector2(0, 0)
        self.active = True
        self.projectiles = []
        self.can_shoot = True
        self.shoot_timer = 0
        self.shoot_cooldown = 0.5
        self.hitbox = pygame.Rect(0, 0, self.size * 2, self.size * 2)
        self.hitbox.center = self.pos
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)

    def update(self, dt):
        self.direction = pygame.mouse.get_pos() - self.pos

        if self.direction.length() > 0:
            self.direction = self.direction.normalize()

        # Atualiza os projéteis do player
        for projectile in self.projectiles:
            projectile.update(dt)

        # Verifica se já passou o tempo de recarga
        if not self.can_shoot:
            self.shoot_timer += dt
            if self.shoot_timer >= self.shoot_cooldown:
                self.can_shoot = True
                self.shoot_timer = 0

        # Centraliza o retangulo do player
        self.hitbox.center = self.pos

    def draw_mira(self, screen):
        if self.direction.length() > 0:
            distancia_mira = 40
            tamanho_triangulo = 10
            
            ponta = self.pos + self.direction * distancia_mira
            ortogonal = pygame.Vector2(-self.direction.y, self.direction.x) * (tamanho_triangulo / 2)
            base_esq = (self.pos + self.direction * (distancia_mira - 10)) + ortogonal
            base_dir = (self.pos + self.direction * (distancia_mira - 10)) - ortogonal

            pygame.draw.polygon(screen, (255, 255, 255), [ponta, base_esq, base_dir])
        
    def shoot(self):
        if self.can_shoot:
            self.projectiles.append(projectile(self.pos.copy(), self.size / 2, (255, 0, 0), self.direction.copy()))
            self.can_shoot = False


# Projétil - vai sair da posição do jogador e avançar em direção à mira
class projectile(object):
    def __init__(self, pos, size, color, direction):
        self.pos = pos
        self.size = size
        self.color = color
        self.direction = direction
        self.vel = 200 * direction
        self.distancia_percorrida = 0
        self.range = 500
        self.active = True
        self.hitbox = pygame.Rect(0, 0, self.size * 2, self.size * 2)
        self.hitbox.center = self.pos
        self.damage = 25

    # verificar se está bom (HENRIQUE)
    def update(self, dt):
        self.pos += self.vel * dt
        self.distancia_percorrida += self.vel.length() * dt
        if self.distancia_percorrida >= self.range:
            self.active = False

        # Centraliza o retangulo do projetil
        self.hitbox.center = self.pos


    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)


class enemy(object):
    def __init__(self, pos, stats):

        self.pos = pos
        self.size, self.life, self.speed, self.color, self.is_boss = stats
        self.direction = pygame.Vector2(0, 0)
        self.active = True
        self.hitbox = pygame.Rect(0, 0, self.size * 2, self.size * 2)
        self.hitbox.center = self.pos

        #Variaveis de vida
        self.max_life = self.life
        self.show_health = True
    
    def update(self, dt, player):
        self.direction = player.pos - self.pos
        self.direction = self.direction.normalize()
        self.pos += self.speed * dt * self.direction

        # Centraliza o retangulo do inimigo
        self.hitbox.center = self.pos

        # atualiza a barra de vida
        if self.life < self.max_life:
            self.show_health = True
        else:
            self.show_health = False

        # verifica se está vivo ou não
        if self.life <= 0:
            self.active = False
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.pos, self.size)
        self.draw_health_bar(screen)

    def draw_health_bar(self, screen):
        if self.show_health:
            pygame.draw.rect(screen, (255, 0, 0), (self.pos.x - self.size, self.pos.y - self.size - 10, self.size * 2, 5))
            pygame.draw.rect(screen, (0, 255, 0), (self.pos.x - self.size, self.pos.y - self.size - 10, self.size * 2 * (self.life / self.max_life), 5))
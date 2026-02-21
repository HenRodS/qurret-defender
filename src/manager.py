import pygame
import random
import math
from src.entities import enemy

class Manager:
    def __init__(self):
        self.state = "PLAYING"
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0

    def update(self, dt, player):
        # 1. Logica de spawn
        self.spawn_timer -= dt
        if self.spawn_timer <= 0:
            self.spawn_enemy(player.pos)
            self.spawn_timer = self.spawn_cooldown

        # 2. Atualiza os inimigos
        for enemy in self.enemies:
            enemy.update(dt, player)

        # 3. Checa colisao
        self.check_collision(player)

        # 

        # 4. Remove os inimigos mortos
        self.enemies = [enemy for enemy in self.enemies if enemy.active]

    def spawn_enemy(self, player_pos):
        # Cria um vetor que aponta para a direita
        spawn_vec = pygame.math.Vector2(800, 0) # raio de 800 (fora da tela)

        # Rotaciona o vetor aleatoriamente entre 0 e 360 graus
        angle = random.uniform(0, 360)
        spawn_vec = spawn_vec.rotate(angle)

        # A posição final é a posição do player + o vetor de spawn
        final_pos = player_pos + spawn_vec

        # Cria o inimigo e adiciona na lista
        new_enemy = enemy(final_pos, 20, 100, (0, 255, 0))
        self.enemies.append(new_enemy)

    def draw(self, screen):
        for enemy  in self.enemies:
            enemy.draw(screen)

    # checa a colisao entre projetil e inimigo (tbm deleta o projetil e inimigo)
    # (nao sei se devo fazer isso em uma funcao separada)
    def check_collision(self, player):
        for enemy in self.enemies:
            # Colisão entre inimigo-projetil
            for projectile in player.projectiles:
                if enemy.hitbox.colliderect(projectile.hitbox):
                    # enemy.active = False
                    self.enemies_defeated += 1
                    projectile.active = False
                    enemy.life -= projectile.damage

            # Colisão entre inimigo-jogador
            if enemy.hitbox.colliderect(player.hitbox):
                player.active = False
                enemy.active = False
                self.state = "GAMEOVER"


    def reset(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0
        self.state = "PLAYING"

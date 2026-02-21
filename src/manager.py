import pygame
import random
from src.entities import enemy

class Manager:
    def __init__(self):
        self.state = "PLAYING"
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0
        self.meta = 2
        self.progress = 0
        self.boss_spawned = False

    def update(self, dt, player):
        # 1. Logica de spawn
        self.spawn_timer -= dt
        if self.spawn_timer <= 0 and not self.boss_spawned:
            self.spawn_enemy(player.pos)
            self.spawn_timer = self.spawn_cooldown

        # 2. Atualiza os inimigos
        for enemy in self.enemies:
            enemy.update(dt, player)

        # 3. Checa colisao
        self.check_collision(player)

        # 4. Checa se os inimigos morreram
        self.check_enemy_death()

        # 5. Remove os inimigos mortos
        self.enemies = [enemy for enemy in self.enemies if enemy.active]

        # 6. Atualiza a barra de progresso
        self.progress = self.enemies_defeated / self.meta

        # 6. Verifica se chegou no boss
        if self.progress >= 1:
            self.enemies = []
            self.spawn_boss(player.pos)
            self.progress = 0
            self.meta = 1
            self.enemies_defeated = 0
            self.boss_spawned = True


    def spawn_boss(self, player_pos):
        # Cria um vetor que aponta para a direita
        spawn_vec = pygame.math.Vector2(150, 0) # raio de 800 (fora da tela)

        # Rotaciona o vetor aleatoriamente entre 0 e 360 graus
        angle = random.uniform(0, 360)
        spawn_vec = spawn_vec.rotate(angle)

        # A posição final é a posição do player + o vetor de spawn
        final_pos = player_pos + spawn_vec

        boss_stats = (50, 500, 100, (255, 0, 0), True)
        new_boss = enemy(final_pos, boss_stats)
        self.enemies.append(new_boss)

    def spawn_enemy(self, player_pos):
        # Cria um vetor que aponta para a direita
        spawn_vec = pygame.math.Vector2(800, 0) # raio de 800 (fora da tela)

        # Rotaciona o vetor aleatoriamente entre 0 e 360 graus
        angle = random.uniform(0, 360)
        spawn_vec = spawn_vec.rotate(angle)

        # A posição final é a posição do player + o vetor de spawn
        final_pos = player_pos + spawn_vec

        # Cria o inimigo e adiciona na lista
        # stats = (size, life, speed, color)
        heavy_stats = (30, 150, 60, (0, 100, 0), False)      # verde escuro
        normal_stats = (20, 100, 100, (0, 170, 0), False)    # verde médio
        fast_stats = (10, 50, 200, (120, 255, 120), False)   # verde claro

        # probabilidade de spawn
        spawn_normal = 0.7
        spawn_fast = 0.2
        spawn_heavy = 0.1

        # escolhe o tipo de inimigo
        spawn_type = random.choices(["normal", "fast", "heavy"], [spawn_normal, spawn_fast, spawn_heavy])[0]

        if spawn_type == "normal":
            new_enemy = enemy(final_pos, normal_stats)
        elif spawn_type == "fast":
            new_enemy = enemy(final_pos, fast_stats)
        elif spawn_type == "heavy":
            new_enemy = enemy(final_pos, heavy_stats)

        self.enemies.append(new_enemy)

    def draw(self, screen):
        for enemy  in self.enemies:
            enemy.draw(screen)

        # Desenha a barra de progresso
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 200 * self.progress, 20))

    # checa a colisao entre projetil e inimigo (tbm deleta o projetil e inimigo)
    # (nao sei se devo fazer isso em uma funcao separada)
    def check_collision(self, player):
        for enemy in self.enemies:
            # Colisão entre inimigo-projetil
            for projectile in player.projectiles:
                if enemy.hitbox.colliderect(projectile.hitbox):
                    projectile.active = False
                    enemy.life -= projectile.damage

            # Colisão entre inimigo-jogador
            if enemy.hitbox.colliderect(player.hitbox):
                player.active = False
                enemy.active = False
                self.state = "GAMEOVER"

    def check_enemy_death(self):
        for enemy in self.enemies:
            if enemy.life <= 0:
                if enemy.is_boss:
                    self.state = "GAMEOVER"
                enemy.active = False
                self.enemies_defeated += 1


    def reset(self):
        self.enemies = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0
        self.state = "PLAYING"

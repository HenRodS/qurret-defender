import pygame
import random
import src.config as config
from src.entities import enemy, turret

class Manager:
    def __init__(self):
        self.state = "PLAYING"
        self.enemies = []
        self.turrets = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0
        self.meta = 10
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

        # 7. Muda o spawn-rate conforme avança
        if self.progress <= 0.5:
            self.spawn_cooldown = 2.0
        elif self.progress <= 0.75:
            self.spawn_cooldown = 1.5
        elif self.progress < 1:
            self.spawn_cooldown = 1.0
        
        # 7. Verifica se chegou no boss
        if self.progress >= 1:
            self.enemies = []
            self.spawn_boss(player.pos)
            self.progress = 0
            self.meta = 1
            self.enemies_defeated = 0
            self.boss_spawned = True

        # lida com as torretas do jogador
        for t in self.turrets:
            t.update(dt, self.enemies)
        self.turrets = [turret for turret in self.turrets if turret.active]


    def spawn_boss(self, player_pos):
        # Cria um vetor que aponta para a direita
        spawn_vec = pygame.math.Vector2(800, 0) # raio de 800 (fora da tela)

        # Rotaciona o vetor aleatoriamente entre 0 e 360 graus
        angle = random.uniform(0, 360)
        spawn_vec = spawn_vec.rotate(angle)

        # A posição final é a posição do player + o vetor de spawn
        final_pos = player_pos + spawn_vec

        new_boss = enemy(final_pos, config.BOSS_STATS)
        self.enemies.append(new_boss)

    def spawn_enemy(self, player_pos):
        # mesmos comandos que a função anterior
        spawn_vec = pygame.math.Vector2(800, 0) # raio de 800 (fora da tela)
        angle = random.uniform(0, 360)
        spawn_vec = spawn_vec.rotate(angle)
        final_pos = player_pos + spawn_vec

        # probabilidade de spawn
        spawn_normal = 0.7
        spawn_fast = 0.2
        spawn_heavy = 0.1

        # escolhe o tipo de inimigo
        spawn_type = random.choices(["normal", "fast", "heavy"], [spawn_normal, spawn_fast, spawn_heavy])[0]

        # Cria o inimigo e adiciona na lista
        if spawn_type == "normal":
            new_enemy = enemy(final_pos, config.NORMAL_STATS)
        elif spawn_type == "fast":
            new_enemy = enemy(final_pos, config.FAST_STATS)
        elif spawn_type == "heavy":
            new_enemy = enemy(final_pos, config.HEAVY_STATS)

        self.enemies.append(new_enemy)

    def draw(self, screen):
        for turret in self.turrets:
            turret.draw(screen)

        for enemy  in self.enemies:
            enemy.draw(screen)

        # Desenha a barra de progresso
        pygame.draw.rect(screen, (255, 255, 255), (10, 10, 200, 20))
        pygame.draw.rect(screen, (0, 255, 0), (10, 10, 200 * self.progress, 20))

    # checa a colisao entre projetil e inimigo (tbm deleta o projetil e inimigo)
    # (nao sei se devo fazer isso em uma funcao separada)
    def check_collision(self, player):
        for enemy in self.enemies:
            # 1. Tiros do Jogador
            for projectile in player.projectiles:
                if enemy.hitbox.colliderect(projectile.hitbox):
                    projectile.active = False
                    enemy.life -= projectile.damage

            # 2. Tiros das Torretas
            for t in self.turrets:
                for p in t.projectiles:
                    if enemy.hitbox.colliderect(p.hitbox):
                        p.active = False
                        enemy.life -= p.damage

            # Colisão entre inimigo-jogador
            if enemy.hitbox.colliderect(player.hitbox):
                player.active = False
                enemy.active = False
                self.state = "GAMEOVER"

    def check_enemy_death(self):
        for enemy in self.enemies:
            if enemy.life <= 0:
                if enemy.is_boss:
                    self.state = "GAMEOVER" # TODO: mudar para vitoria  
                enemy.active = False
                self.enemies_defeated += 1

    def spawn_turret(self, player):
        if not len(self.turrets) >= config.MAX_TURRETS:
            new_turret = turret(player.pos.copy(), config.COLOR_TURRET, config.TURRET_SIZE)
            self.turrets.append(new_turret)


    def reset(self):
        self.enemies = []
        self.turrets = []
        self.spawn_timer = 0
        self.spawn_cooldown = 2.0
        self.enemies_defeated = 0
        self.state = "PLAYING"

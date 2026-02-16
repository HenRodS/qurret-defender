import pygame
import src.config as config
import src.models as models

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
enemy_can_spawn = True

player = models.player(pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2), config.PLAYER_SIZE, config.COLOR_PLAYER)
dt = 0

enemies = []

# Loop Principal
# ORDEM IMPORTANTE: EVENTOS, LÓGICA, DESENHO, FINALIZAÇÃO
while running:
    # 1. EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. LÓGICA / UPDATE
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.pos.y -= config.PLAYER_SPEED * dt
    if keys[pygame.K_s]: player.pos.y += config.PLAYER_SPEED * dt
    if keys[pygame.K_a]: player.pos.x -= config.PLAYER_SPEED * dt
    if keys[pygame.K_d]: player.pos.x += config.PLAYER_SPEED * dt
    if keys[pygame.K_SPACE]: player.shoot()

    # 3. DESENHO (DRAW)
    screen.fill("purple") # Limpa a tela primeiro

    # Desenha o Jogador
    player.draw(screen)

    # Desenha a Mira (Triângulo)
    player.draw_mira(screen)

    # Atualiza o Jogador
    player.update(dt)

    # Desenha e atualiza os projeteis
    for projectile in player.projectiles:
        projectile.draw(screen)
        projectile.update(dt)
        if not projectile.active:
            player.projectiles.remove(projectile)
    
    # Cria inimigos
    if enemy_can_spawn:
        enemy = models.enemy(pygame.Vector2(screen.get_width() / 3, screen.get_height() / 3), config.PLAYER_SIZE, config.COLOR_ENEMY)
        enemies.append(enemy)
        enemy_can_spawn = False
    # Desenha os inimigos
    for enemy in enemies:
        enemy.draw(screen)
        enemy.update(dt, player)


    # 4. FINALIZAÇÃO
    pygame.display.flip() # Só chama o flip DEPOIS de desenhar tudo
    dt = clock.tick(60) / 1000

pygame.quit()
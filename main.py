import pygame
import src.config as config
import src.entities as entities
from src.manager import Manager

# pygame setup
pygame.init()
screen = pygame.display.set_mode((config.SCREEN_WIDTH, config.SCREEN_HEIGHT))
clock = pygame.time.Clock()
dt = 0

player = entities.player(pygame.Vector2(config.START_POS), config.PLAYER_SIZE, config.PLAYER_LIFE, config.PLAYER_COLOR)
manager = Manager()

# Loop Principal
# ORDEM IMPORTANTE: EVENTOS, LÓGICA, DESENHO, FINALIZAÇÃO
running = True
while running:
    # 1. EVENTOS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_e:
                manager.spawn_turret(player)


    # 2. teclas
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]: player.pos.y -= config.PLAYER_SPEED * dt
    if keys[pygame.K_s]: player.pos.y += config.PLAYER_SPEED * dt
    if keys[pygame.K_a]: player.pos.x -= config.PLAYER_SPEED * dt
    if keys[pygame.K_d]: player.pos.x += config.PLAYER_SPEED * dt
    if keys[pygame.K_SPACE]: player.shoot()

    if manager.state == "PLAYING":
        manager.update(dt, player)
        player.update(dt)

        # 3. DESENHO (DRAW)
        screen.fill("purple") # Limpa a tela primeiro

        player.draw(screen)
        player.draw_mira(screen)
        manager.draw(screen)

        # Desenha e atualiza os projeteis
        for projectile in player.projectiles:
            projectile.draw(screen)
            projectile.update(dt)
            if not projectile.active:
                player.projectiles.remove(projectile)

    if manager.state == "GAMEOVER":
        screen.fill("black")

        if keys[pygame.K_SPACE]: manager.reset()

    # 4. FINALIZAÇÃO
    pygame.display.flip() # Só chama o flip DEPOIS de desenhar tudo
    dt = clock.tick(60) / 1000

pygame.quit()
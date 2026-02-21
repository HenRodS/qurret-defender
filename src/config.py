# Configurações de Display
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
FPS = 60

# Configurações de Gameplay
SPAWN_RADIUS = 600      # Distância mínima para inimigos aparecerem
MAX_TURRETS = 3         # Limite inicial de 'a' a 'e'
BOSS_DISTANCE = 10000   # Pontos/Distância necessária para o Boss (100%)

# Cores (se não usar letras) ou Cores das Letras
COLOR_ENEMY = (0, 100, 0)      # Verde Escuro
COLOR_TURRET = (255, 255, 255) # Branco

# Configurações do Jogador
PLAYER_SPEED = 300
PLAYER_SIZE = 10
PLAYER_COLOR = (139, 69, 19)   # Marrom
PLAYER_LIFE = 100

# Configurações de INICIO
START_POS = (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)

# configurações dos inimigos
# stats = (size, life, speed, color)
HEAVY_STATS = (30, 150, 60, (0, 100, 0), False)      # verde escuro
NORMAL_STATS = (20, 100, 100, (0, 170, 0), False)    # verde médio
FAST_STATS = (10, 50, 200, (120, 255, 120), False)   # verde claro

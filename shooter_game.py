from pygame import *
from random import randint

# Inicialización de fuentes y sonidos
font.init()
mixer.init()

# Cargar música de fondo y efectos de sonido
mixer.music.load('space.ogg') if False else None  # Puedes agregar música si tienes el archivo
fire_sound = mixer.Sound('fire.ogg')

# Fuentes de texto
font1 = font.SysFont('Arial', 36)
font_win = font.SysFont('Arial', 60)

# Ventana del juego
win_width = 600
win_height = 900
window = display.set_mode((win_width, win_height))
display.set_caption("Shooter Espacial")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))

# Variables del juego
score = 0      # Naves destruidas
lost = 0       # Naves pasadas
max_lost = 3   # Límite de naves perdidas antes de perder
goal = 10      # Naves necesarias para ganar


# Clase padre para sprites
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


# Clase del jugador principal
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 85:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx - 7, self.rect.top, 15, 30, 15)
        bullets.add(bullet)
        fire_sound.play()


# Clase de los enemigos (UFO)
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            lost += 1


# Clase de los proyectiles
class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


# Creación de objetos
ship = Player('rocket.png', win_width // 2 - 40, win_height - 100, 80, 100, 10)

monsters = sprite.Group()
for i in range(5):
    monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
    monsters.add(monster)

bullets = sprite.Group()

# Bucle principal
run = True
finish = False
clock = time.Clock()
FPS = 60

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and not finish:
                ship.fire()

    if not finish:
        # Dibujar fondo
        window.blit(background, (0, 0))

        # Movimiento de sprites
        ship.update()
        monsters.update()
        bullets.update()

        # Dibujar sprites
        ship.reset()
        monsters.draw(window)
        bullets.draw(window)

        # Detección de colisiones: balas con enemigos
        collides = sprite.groupcollide(monsters, bullets, True, True)
        for c in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, win_width - 80), -40, 80, 50, randint(1, 4))
            monsters.add(monster)

        # Condición de derrota: colisión con jugador o demasiados ovnis perdidos
        if sprite.spritecollide(ship, monsters, False) or lost >= max_lost:
            finish = True
            lose_txt = font_win.render('¡HAS PERDIDO!', True, (255, 0, 0))
            window.blit(lose_txt, (win_width // 2 - 160, win_height // 2 - 30))

        # Condición de victoria
        if score >= goal:
            finish = True
            win_txt = font_win.render('¡HAS GANADO!', True, (0, 255, 0))
            window.blit(win_txt, (win_width // 2 - 160, win_height // 2 - 30))

        # Marcadores
        text_score = font1.render(f"Puntos: {score}", True, (255, 255, 255))
        text_lost = font1.render(f"Perdidos: {lost}", True, (255, 255, 255))
        window.blit(text_score, (10, 20))
        window.blit(text_lost, (10, 55))

    display.update()
    clock.tick(FPS)
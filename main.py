import pygame
import random

# Bildschirmgröße
WIDTH = 800
HEIGHT = 400

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Initialisierung
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

# Schlägerklasse
class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 60))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.velocity = 0

    def update(self):
        self.rect.y += self.velocity
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

# Ballklasse
class Ball(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.centery = HEIGHT // 2
        self.velocity_x = random.choice([-2, 2])
        self.velocity_y = random.choice([-2, 2])

    def update(self):
        self.rect.x += self.velocity_x
        self.rect.y += self.velocity_y

        # Kollision mit den Wänden
        if self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.velocity_y *= -1

# Spielobjekte erstellen
paddle_left = Paddle(30, HEIGHT // 2)
paddle_right = Paddle(WIDTH - 30, HEIGHT // 2)
ball = Ball()

# Punktzähler
score_left = 0
score_right = 0
font = pygame.font.Font(None, 36)

# Alle Sprites gruppieren
all_sprites = pygame.sprite.Group()
all_sprites.add(paddle_left, paddle_right, ball)

# Spielhauptschleife
running = True
while running:
    # Ereignisse verarbeiten
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                paddle_right.velocity = -3
            elif event.key == pygame.K_DOWN:
                paddle_right.velocity = 3
            elif event.key == pygame.K_w:
                paddle_left.velocity = -3
            elif event.key == pygame.K_s:
                paddle_left.velocity = 3
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                paddle_right.velocity = 0
            elif event.key == pygame.K_w or event.key == pygame.K_s:
                paddle_left.velocity = 0

    # Spiellogik aktualisieren
    all_sprites.update()

    # Kollision mit den Schlägern
    if pygame.sprite.collide_rect(ball, paddle_left) or pygame.sprite.collide_rect(ball, paddle_right):
        ball.velocity_x *= -1

    # Punktzähler aktualisieren
    if ball.rect.left <= 0:
        score_right += 1
        if score_right >= 5:
            running = False
    elif ball.rect.right >= WIDTH:
        score_left += 1
        if score_left >= 5:
            running = False

    # Spieloberfläche zeichnen
    screen.fill(BLACK)
    all_sprites.draw(screen)
    score_text = font.render(str(score_left) + " : " + str(score_right), True, WHITE)
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 10))

    pygame.display.flip()
    clock.tick(60)

# Spiel beenden
pygame.quit()

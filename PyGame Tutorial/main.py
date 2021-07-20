import pygame
import os
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("PyGame Tutorial")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
ORANGE = (255, 100, 0)
GREEN = (0, 255, 0)

BORDER = pygame.Rect((WIDTH//2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Grenade+1.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'Gun+Silencer.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 5
BULLET_VEL = 10
MAX_BULLETS = 5
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 50, 40

RED_HIT = pygame.USEREVENT + 1
BLUE_HIT = pygame.USEREVENT + 2

# YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))

RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

BLUE_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_blue.png'))
BLUE_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(BLUE_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'space.png')), (WIDTH, HEIGHT))

def draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health):
    #WIN.fill(WHITE)
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)
    red_health_text = HEALTH_FONT.render("Health: " + str(red_health), 1, ORANGE)
    blue_health_text = HEALTH_FONT.render("Health: " + str(blue_health), 1, GREEN)
    WIN.blit(red_health_text, (10, 10))
    WIN.blit(blue_health_text, (WIDTH - blue_health_text.get_width() - 10, 10))
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    WIN.blit(BLUE_SPACESHIP, (blue.x, blue.y))
    for bullet in red_bullets:
        pygame.draw.rect(WIN, ORANGE, bullet)
    for bullet in blue_bullets:
        pygame.draw.rect(WIN, GREEN, bullet)
    pygame.display.update()

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_a] and red.x - VEL >= 0: #LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_d] and red.x + VEL <= (BORDER.x - red.height): #RIGHT
        red.x += VEL
    if keys_pressed[pygame.K_w] and red.y - VEL >= 0: #UP
        red.y -= VEL
    if keys_pressed[pygame.K_s] and red.y + VEL <= (HEIGHT - red.width): #DOWN
        red.y += VEL

def blue_handle_movement(keys_pressed, blue):
    if keys_pressed[pygame.K_LEFT] and blue.x - VEL >= (BORDER.x + 10): #LEFT
        blue.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and blue.x + VEL <= (WIDTH - blue.height): #RIGHT
        blue.x += VEL
    if keys_pressed[pygame.K_UP] and blue.y - VEL >= 0: #UP
        blue.y -= VEL
    if keys_pressed[pygame.K_DOWN] and blue.y + VEL <= (HEIGHT - blue.width): #DOWN
        blue.y += VEL

def handle_bullets(red_bullets, blue_bullets, red, blue):
    for bullet in red_bullets:
        bullet.x += BULLET_VEL
        if blue.colliderect(bullet):
            pygame.event.post(pygame.event.Event(BLUE_HIT))
            red_bullets.remove(bullet)
        elif bullet.x >= WIDTH:
            red_bullets.remove(bullet)
    for bullet in blue_bullets:
        bullet.x -= BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            blue_bullets.remove(bullet)
        elif bullet.x + 10 <= 0:
            blue_bullets.remove(bullet)

def draw_winner(text):
    if text == "Red Wins!":
        draw_text = WINNER_FONT.render(text, 1, ORANGE)
    elif text == "Blue Wins!":
        draw_text = WINNER_FONT.render(text, 1, GREEN)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(3000)

def main():
    red = pygame.Rect(300, 150, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    blue = pygame.Rect(560, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    red_bullets = []
    blue_bullets = []

    red_health = 10
    blue_health = 10

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LSHIFT and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x + red.height, red.y + (red.width//2) - 2, 10, 4)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_RSHIFT and len(blue_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(blue.x - 10, blue.y + (blue.width//2) - 2, 10, 4)
                    blue_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == BLUE_HIT:
                blue_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()

        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        blue_handle_movement(keys_pressed, blue)
        handle_bullets(red_bullets, blue_bullets, red, blue)
        draw_window(red, blue, red_bullets, blue_bullets, red_health, blue_health)

        winner_text = ""
        if red_health <= 0:
            winner_text = "Blue Wins!"
        if blue_health <= 0:
            winner_text = "Red Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break
    main()

if __name__ == "__main__":
    main()
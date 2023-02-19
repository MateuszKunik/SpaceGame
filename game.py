import pygame as pg
import os
os.chdir("./SpaceGame")

pg.font.init()

WIDTH, HEIGHT = 900, 500
#WIDTH, HEIGHT = 1920, 1080
SCREEN = pg.display.set_mode(
    size = (WIDTH, HEIGHT)
)

pg.display.set_caption("First Game!")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
FPS = 60

BORDER = pg.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)
HEALTH_FONT = pg.font.SysFont("comicsans", 40)
WINNER_FONT = pg.font.SysFont("comicsens", 100)

YELLOW_HIT = pg.USEREVENT + 1
RED_HIT = pg.USEREVENT + 2

vel = 5
bullet_vel = 7
max_bullets = 3

space = pg.transform.scale(
    surface = pg.image.load(
        os.path.join("Assets", "space.png")),
    size = (WIDTH, HEIGHT)
)


spaceship_width, spaceship_height = 55, 40
yellow_spaceship_image = pg.image.load(
    os.path.join("Assets", "spaceship_yellow.png")
)
yellow_spaceship = pg.transform.rotate(
    pg.transform.scale(
        surface = yellow_spaceship_image,
        size = (spaceship_width, spaceship_height)),
    angle = 90
)

red_spaceship_image = pg.image.load(
    os.path.join("Assets", "spaceship_red.png")
)
red_spaceship = pg.transform.rotate(
    pg.transform.scale(
        surface = red_spaceship_image,
        size = (spaceship_width, spaceship_height)),
    angle = 270
)


def draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health):
    SCREEN.blit(space, (0, 0))
    pg.draw.rect(SCREEN, BLACK, BORDER)
    yellow_health_text = HEALTH_FONT.render(
        "Health: " + str(yellow_health),
        1,
        WHITE
    )

    red_health_text = HEALTH_FONT.render(
        "Health: " + str(red_health),
        1,
        WHITE
    )

    SCREEN.blit(yellow_health_text, (10, 10))
    SCREEN.blit(red_health_text, (WIDTH - yellow_health_text.get_width() - 10, 10))
    SCREEN.blit(yellow_spaceship, (yellow.x, yellow.y))
    SCREEN.blit(red_spaceship, (red.x, red.y))

    for bullet in yellow_bullets:
        pg.draw.rect(surface = SCREEN, color = YELLOW, rect = bullet)
    for bullet in red_bullets:
        pg.draw.rect(surface = SCREEN, color = RED, rect = bullet)

    pg.display.update()


def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pg.K_w] and yellow.y - vel > 0:
        yellow.y -= vel
    if keys_pressed[pg.K_s] and yellow.y + vel + yellow.height < HEIGHT - 20:
        yellow.y += vel
    if keys_pressed[pg.K_a] and yellow.x - vel > 0:
        yellow.x -= vel
    if keys_pressed[pg.K_d] and yellow.x + vel + yellow.width < BORDER.x :
        yellow.x += vel


def red_handle_movement(keys_pressed, red):
    if keys_pressed[pg.K_UP] and red.y - vel > 0:
        red.y -= vel
    if keys_pressed[pg.K_DOWN] and red.y + vel + red.height < HEIGHT - 20:
        red.y += vel
    if keys_pressed[pg.K_LEFT] and red.x - vel > BORDER.x + BORDER.width:
        red.x -= vel
    if keys_pressed[pg.K_RIGHT] and red.x + vel + red.width < WIDTH:
        red.x += vel


def handle_bullets(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += bullet_vel
        if red.colliderect(bullet):
            pg.event.post(pg.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= bullet_vel
        if yellow.colliderect(bullet):
            pg.event.post(pg.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)    
        elif bullet.x < 0:
            red_bullets.remove(bullet)


def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    SCREEN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pg.display.update()
    pg.time.delay(5000)


def main():
    yellow = pg.Rect(250, 200, spaceship_width, spaceship_height)
    yellow_bullets = []

    red = pg.Rect(650, 200, spaceship_width, spaceship_height)
    red_bullets = []
    
    yellow_health, red_health = 10, 10


    clock = pg.time.Clock()
    run = True

    while run:
        clock.tick(FPS)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
                pg.quit()

            if event.type == pg.KEYDOWN:
                if event.key == pg.K_LCTRL and len(yellow_bullets) < max_bullets:
                    bullet = pg.Rect(
                        yellow.x + yellow.width - 10, yellow.y + yellow.height//2 - 2, 10, 5
                    )
                    yellow_bullets.append(bullet)

                if event.key == pg.K_RCTRL and len(red_bullets) < max_bullets:
                    bullet = pg.Rect(
                        red.x, red.y + red.height//2 - 2, 10, 5
                    )
                    red_bullets.append(bullet)

            if event.type == YELLOW_HIT:
                yellow_health -= 1

            if event.type == RED_HIT:
                red_health -= 1

        winner_text = ""

        if yellow_health <= 0:
            winner_text = "Red Wins!"

        if red_health <= 0:
            winner_text = "Yellow Wins!"

        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pg.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)
        handle_bullets(yellow_bullets, red_bullets, yellow, red)

        draw_window(yellow, red, yellow_bullets, red_bullets, yellow_health, red_health)

    main()



if __name__ == "__main__":
    main()
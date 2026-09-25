import pygame
import os
import random

pygame.init()
pygame.mixer.init()

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.play(-1)

WIDTH = 1000
HEIGHT = 700

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Game")

clock = pygame.time.Clock()

font = pygame.font.Font(None, 42)
small_font = pygame.font.Font(None, 32)

player_path = "player"

music_volume = 0.5
sound_volume = 0.5
rain_volume = 0.5
weather = "clear"

fullscreen = False

pygame.mixer.music.load("music.mp3")
pygame.mixer.music.set_volume(music_volume)
pygame.mixer.music.play(-1)


def remove_background(image):
    image = image.convert_alpha()
    image.set_colorkey((0, 0, 0))
    return image


def load_player(filename):
    path = os.path.join(player_path, filename)

    image = pygame.image.load(path)
    image = remove_background(image)

    return image


def resize_player(image):
    width = int(image.get_width() / 3.75)
    height = int(image.get_height() / 3.75)

    return pygame.transform.scale(
        image,
        (width, height)
    )


idle_side = resize_player(
    load_player("idle_side.png")
)

walk_1 = resize_player(
    load_player("walk_1.png")
)

walk_2 = resize_player(
    load_player("walk_2.png")
)

jump_1 = resize_player(
    load_player("jump_1.png")
)

jump_2 = resize_player(
    load_player("jump_2.png")
)

jump_3 = resize_player(
    load_player("jump_3.png")
)

fall = resize_player(
    load_player("fall.png")
)

attack = resize_player(
    load_player("attack_1.png")
)


stage = pygame.image.load("stage1.png").convert()

stage = pygame.transform.scale(
    stage,
    (1600, 700)
)

snow_stage = pygame.image.load("weather/snow.png").convert()
snow_stage = pygame.transform.scale(snow_stage, (1600, 700))

rain_stage = pygame.image.load("weather/rain.png").convert()
rain_stage = pygame.transform.scale(rain_stage, (1600, 700))

snowflake = pygame.image.load("weather/snowflake.png").convert_alpha()
snowdrift = pygame.image.load("weather/snowdrift.png").convert_alpha()

rain_sound = pygame.mixer.Sound("weather/rain.mp3")
rain_sound.set_volume(rain_volume)


player_x = WIDTH // 2
player_y = 615

world_x = 0

player_speed = 3

velocity_y = 0
gravity = 0.8
jump_power = -14

on_ground = True
facing_right = True

walk_timer = 0
walk_frame = 0

attacking = False
attack_timer = 0

inventory_open = False
menu_open = False
settings_open = False
code_window = False

experimental_enabled = False
code_input = ""

running = True

touch_left = False
touch_right = False

snowflakes = [
    [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(1, 3)]
    for _ in range(80)
]

rain_drops = [
    [random.randint(0, WIDTH), random.randint(0, HEIGHT), random.randint(8, 16)]
    for _ in range(140)
]

left_button = pygame.Rect(35, HEIGHT - 145, 90, 90)
right_button = pygame.Rect(140, HEIGHT - 145, 90, 90)
jump_button = pygame.Rect(WIDTH - 230, HEIGHT - 145, 90, 90)
attack_button = pygame.Rect(WIDTH - 125, HEIGHT - 145, 90, 90)
inventory_button = pygame.Rect(WIDTH - 125, HEIGHT - 250, 90, 80)


def draw_touch_button(text, rect, pressed=False):
    if pressed:
        pygame.draw.rect(
            screen,
            (100, 100, 100),
            rect,
            border_radius=18
        )
    else:
        pygame.draw.rect(
            screen,
            (55, 55, 55),
            rect,
            border_radius=18
        )

    pygame.draw.rect(
        screen,
        (180, 180, 180),
        rect,
        2,
        border_radius=18
    )

    text_surface = small_font.render(
        text,
        True,
        (255, 255, 255)
    )

    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        )
    )


def draw_touch_controls():
    pressed_left = False
    pressed_right = False

    mouse_pos = pygame.mouse.get_pos()

    if pygame.mouse.get_pressed()[0]:
        pressed_left = left_button.collidepoint(mouse_pos)
        pressed_right = right_button.collidepoint(mouse_pos)

    draw_touch_button("←", left_button, pressed_left)
    draw_touch_button("→", right_button, pressed_right)
    draw_touch_button("↑", jump_button)
    draw_touch_button("⚔", attack_button)
    draw_touch_button("E", inventory_button)


def draw_button(text, rect):
    mouse_pos = pygame.mouse.get_pos()

    if rect.collidepoint(mouse_pos):

        pygame.draw.rect(
            screen,
            (100, 100, 100),
            rect
        )

        pygame.draw.rect(
            screen,
            (220, 220, 220),
            rect,
            3
        )

    else:

        pygame.draw.rect(
            screen,
            (55, 55, 55),
            rect
        )

        pygame.draw.rect(
            screen,
            (140, 140, 140),
            rect,
            2
        )

    text_surface = font.render(
        text,
        True,
        (255, 255, 255)
    )

    screen.blit(
        text_surface,
        (
            rect.centerx - text_surface.get_width() // 2,
            rect.centery - text_surface.get_height() // 2
        )
    )


def draw_slider(x, y, width, value):

    pygame.draw.rect(
        screen,
        (60, 60, 60),
        (x, y, width, 8)
    )

    pygame.draw.rect(
        screen,
        (180, 180, 180),
        (
            x,
            y,
            int(width * value),
            8
        )
    )

    pygame.draw.circle(
        screen,
        (255, 255, 255),
        (
            x + int(width * value),
            y + 4
        ),
        10
    )


def draw_menu():

    screen.fill((25, 25, 30))

    title = font.render(
        "MAIN MENU",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            80
        )
    )

    continue_button = pygame.Rect(
        350,
        180,
        300,
        60
    )

    settings_button = pygame.Rect(
        350,
        260,
        300,
        60
    )

    experimental_button = pygame.Rect(
        350,
        340,
        300,
        60
    )

    exit_button = pygame.Rect(
        350,
        420,
        300,
        60
    )

    draw_button(
        "Continue",
        continue_button
    )

    draw_button(
        "Settings",
        settings_button
    )

    draw_button(
        "Experimental",
        experimental_button
    )

    draw_button(
        "Exit",
        exit_button
    )
def draw_settings():

    screen.fill((25, 25, 30))

    title = font.render(
        "SETTINGS",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            70
        )
    )

    music_text = font.render(
        "Music Volume",
        True,
        (255, 255, 255)
    )

    screen.blit(
        music_text,
        (250, 180)
    )

    draw_slider(
        250,
        230,
        500,
        music_volume
    )

    music_percent = small_font.render(
        str(int(music_volume * 100)) + "%",
        True,
        (200, 200, 200)
    )

    screen.blit(
        music_percent,
        (770, 215)
    )

    sound_text = font.render(
        "Sound Volume",
        True,
        (255, 255, 255)
    )

    screen.blit(
        sound_text,
        (250, 300)
    )

    draw_slider(
        250,
        350,
        500,
        sound_volume
    )

    sound_percent = small_font.render(
        str(int(sound_volume * 100)) + "%",
        True,
        (200, 200, 200)
    )

    screen.blit(
        sound_percent,
        (770, 335)
    )

    rain_text = font.render(
        "Rain Volume",
        True,
        (255, 255, 255)
    )

    screen.blit(
        rain_text,
        (250, 390)
    )

    draw_slider(
        250,
        440,
        500,
        rain_volume
    )

    rain_percent = small_font.render(
        str(int(rain_volume * 100)) + "%",
        True,
        (200, 200, 200)
    )

    screen.blit(
        rain_percent,
        (770, 425)
    )

    draw_button("Clear", pygame.Rect(250, 475, 150, 45))
    draw_button("Rain", pygame.Rect(425, 475, 150, 45))
    draw_button("Snow", pygame.Rect(600, 475, 150, 45))

    fullscreen_button = pygame.Rect(
        350,
        540,
        300,
        60
    )

    if fullscreen:

        draw_button(
            "Fullscreen: ON",
            fullscreen_button
        )

    else:

        draw_button(
            "Fullscreen: OFF",
            fullscreen_button
        )

    back_button = pygame.Rect(
        350,
        620,
        300,
        60
    )

    draw_button(
        "Back",
        back_button
    )


def draw_inventory():

    screen.fill((20, 20, 25))

    title = font.render(
        "INVENTORY",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            60
        )
    )

    for row in range(4):

        for column in range(7):

            x = 250 + column * 75
            y = 150 + row * 75

            pygame.draw.rect(
                screen,
                (45, 45, 50),
                (x, y, 60, 60)
            )

            pygame.draw.rect(
                screen,
                (120, 120, 120),
                (x, y, 60, 60),
                2
            )

    text = small_font.render(
        "Press E to close",
        True,
        (180, 180, 180)
    )

    screen.blit(
        text,
        (
            WIDTH // 2 - text.get_width() // 2,
            500
        )
    )


def draw_code_window():

    screen.fill((20, 20, 25))

    title = font.render(
        "EXPERIMENTAL",
        True,
        (255, 255, 255)
    )

    screen.blit(
        title,
        (
            WIDTH // 2 - title.get_width() // 2,
            130
        )
    )

    text = small_font.render(
        "Enter code:",
        True,
        (220, 220, 220)
    )

    screen.blit(
        text,
        (350, 220)
    )

    box = pygame.Rect(
        350,
        260,
        300,
        60
    )

    pygame.draw.rect(
        screen,
        (45, 45, 50),
        box
    )

    pygame.draw.rect(
        screen,
        (180, 180, 180),
        box,
        2
    )

    code_text = font.render(
        code_input,
        True,
        (255, 255, 255)
    )

    screen.blit(
        code_text,
        (
            box.x + 15,
            box.y + 10
        )
    )

    hint = small_font.render(
        "Press Enter to confirm",
        True,
        (160, 160, 160)
    )

    screen.blit(
        hint,
        (
            WIDTH // 2 - hint.get_width() // 2,
            350
        )
    )


while running:

    clock.tick(60)

    for event in pygame.event.get():

        if event.type == pygame.QUIT:

            running = False

        if not menu_open and not settings_open and not code_window and not inventory_open:
            if event.type == pygame.MOUSEBUTTONDOWN:
                touch_pos = event.pos

                if left_button.collidepoint(touch_pos):
                    touch_left = True

                elif right_button.collidepoint(touch_pos):
                    touch_right = True

                elif jump_button.collidepoint(touch_pos):
                    if on_ground:
                        velocity_y = jump_power
                        on_ground = False

                elif attack_button.collidepoint(touch_pos):
                    attacking = True
                    attack_timer = 20

                elif inventory_button.collidepoint(touch_pos):
                    inventory_open = True

            elif event.type == pygame.MOUSEBUTTONUP:
                touch_left = False
                touch_right = False

        if menu_open:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    menu_open = False

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()
                continue_button = pygame.Rect(
                    350,
                    180,
                    300,
                    60
                )

                settings_button = pygame.Rect(
                    350,
                    260,
                    300,
                    60
                )

                experimental_button = pygame.Rect(
                    350,
                    340,
                    300,
                    60
                )

                exit_button = pygame.Rect(
                    350,
                    420,
                    300,
                    60
                )

                if continue_button.collidepoint(mouse_pos):

                    menu_open = False

                elif settings_button.collidepoint(mouse_pos):

                    settings_open = True
                    menu_open = False

                elif experimental_button.collidepoint(mouse_pos):

                    code_window = True
                    menu_open = False
                    code_input = ""

                elif exit_button.collidepoint(mouse_pos):

                    running = False

        elif settings_open:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    settings_open = False
                    menu_open = True

            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_x, mouse_y = pygame.mouse.get_pos()

                if 250 <= mouse_x <= 750 and 210 <= mouse_y <= 250:

                    music_volume = (
                        mouse_x - 250
                    ) / 500

                    music_volume = max(
                        0,
                        min(1, music_volume)
                    )

                    pygame.mixer.music.set_volume(
                        music_volume
                    )

                elif 250 <= mouse_x <= 750 and 330 <= mouse_y <= 370:

                    sound_volume = (
                        mouse_x - 250
                    ) / 500

                    sound_volume = max(
                        0,
                        min(1, sound_volume)
                    )

                elif 250 <= mouse_x <= 750 and 420 <= mouse_y <= 460:

                    rain_volume = (
                        mouse_x - 250
                    ) / 500

                    rain_volume = max(
                        0,
                        min(1, rain_volume)
                    )

                    rain_sound.set_volume(rain_volume)

                elif pygame.Rect(250, 475, 150, 45).collidepoint(mouse_x, mouse_y):

                    weather = "clear"
                    rain_sound.stop()

                elif pygame.Rect(425, 475, 150, 45).collidepoint(mouse_x, mouse_y):

                    weather = "rain"
                    rain_sound.set_volume(rain_volume)
                    rain_sound.play(-1)

                elif pygame.Rect(600, 475, 150, 45).collidepoint(mouse_x, mouse_y):

                    weather = "snow"
                    rain_sound.stop()

                elif pygame.Rect(
                    350,
                    540,
                    300,
                    60
                ).collidepoint(mouse_x, mouse_y):

                    fullscreen = not fullscreen

                    if fullscreen:

                        screen = pygame.display.set_mode(
                            (WIDTH, HEIGHT),
                            pygame.FULLSCREEN
                        )

                    else:

                        screen = pygame.display.set_mode(
                            (WIDTH, HEIGHT)
                        )

                elif pygame.Rect(
                    350,
                    620,
                    300,
                    60
                ).collidepoint(mouse_x, mouse_y):

                    settings_open = False
                    menu_open = True

        elif code_window:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:

                    code_window = False
                    menu_open = True

                elif event.key == pygame.K_BACKSPACE:

                    code_input = code_input[:-1]

                elif event.key == pygame.K_RETURN:

                    if code_input == "1221":

                        experimental_enabled = True

                    code_input = ""
                    code_window = False
                    menu_open = True

                elif event.unicode.isdigit():

                    if len(code_input) < 10:

                        code_input += event.unicode

        elif inventory_open:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_e:

                    inventory_open = False

        else:

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    menu_open = True

                elif event.key == pygame.K_e:

                    inventory_open = True

                elif event.key == pygame.K_SPACE:

                    if on_ground:

                        velocity_y = jump_power
                        on_ground = False

                elif event.key == pygame.K_f:

                    attacking = True
                    attack_timer = 20

    if menu_open:

        draw_menu()
        pygame.display.flip()
        continue

    if settings_open:

        draw_settings()
        pygame.display.flip()
        continue

    if code_window:

        draw_code_window()
        pygame.display.flip()
        continue

    if inventory_open:

        draw_inventory()
        pygame.display.flip()
        continue

    keys = pygame.key.get_pressed()

    moving = False

    if keys[pygame.K_a] or keys[pygame.K_LEFT] or touch_left:

        world_x += player_speed

        moving = True
        facing_right = False

    if keys[pygame.K_d] or keys[pygame.K_RIGHT] or touch_right:

        world_x -= player_speed

        moving = True
        facing_right = True

    if world_x > 0:

        world_x = 0

    if world_x < WIDTH - stage.get_width():

        world_x = WIDTH - stage.get_width()

    velocity_y += gravity

    player_y += velocity_y

    ground_y = 615

    if player_y >= ground_y:

        player_y = ground_y
        velocity_y = 0
        on_ground = True

    if attacking:

        player = attack

        attack_timer -= 1

        if attack_timer <= 0:

            attacking = False

    elif not on_ground:

        if velocity_y < -5:

            player = jump_1

        elif velocity_y < 3:

            player = jump_2

        elif velocity_y < 7:

            player = jump_3

        else:

            player = fall

    elif moving:

        walk_timer += 1

        if walk_timer >= 10:

            walk_timer = 0
            walk_frame = 1 - walk_frame

        if walk_frame == 0:

            player = walk_1

        else:

            player = walk_2

    else:

        player = idle_side

    if not facing_right:

        player = pygame.transform.flip(
            player,
            True,
            False
        )

    screen.fill((0, 0, 0))

    if weather == "snow":
        current_stage = snow_stage
    elif weather == "rain":
        current_stage = rain_stage
    else:
        current_stage = stage

    screen.blit(
        current_stage,
        (world_x, 0)
    )

    if weather == "snow":
        for flake in snowflakes:
            flake[1] += flake[2]
            flake[0] += 0.5

            if flake[1] > HEIGHT:
                flake[0] = random.randint(0, WIDTH)
                flake[1] = -20

            size = max(4, flake[2] * 5)
            flake_image = pygame.transform.scale(
                snowflake,
                (size, size)
            )
            screen.blit(flake_image, (flake[0], flake[1]))

    elif weather == "rain":
        for drop in rain_drops:
            drop[1] += drop[2]

            if drop[1] > HEIGHT:
                drop[0] = random.randint(0, WIDTH)
                drop[1] = -20

            pygame.draw.line(
                screen,
                (150, 180, 220),
                (drop[0], drop[1]),
                (drop[0] - 2, drop[1] + drop[2]),
                1
            )

    screen.blit(
        player,
        (
            player_x - player.get_width() // 2,
            player_y - player.get_height()
        )
    )

    draw_touch_controls()

    pygame.display.flip()


pygame.quit()

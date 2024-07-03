import pygame
import random
import sys

pygame.init()
W, H = 800, 600
FPS = 60

screen = pygame.display.set_mode((W, H), pygame.RESIZABLE)
clock = pygame.time.Clock()
done = False
bg = (255, 255, 255)
paused = False
in_settings = False

#Paddle
paddleW = 300
paddleH = 20
paddleSpeed = 25
paddle = pygame.Rect(W // 2 - paddleW // 2, H - paddleH - 30, paddleW, paddleH)

#Ball
ballRadius = 15
ballSpeed = 7
ball_rect = int(ballRadius * 2 ** 0.5)
ball = pygame.Rect(random.randrange(ball_rect, W - ball_rect), H // 2, ball_rect, ball_rect)
dx, dy = 1, -1

#Brick
brick_rows = 4
brick_cols = 10
brick_padding = 10
brick_width = (W - (brick_cols + 1) * brick_padding) // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    brick_row = []
    for col in range(brick_cols):
        brick_x = col * (brick_width + brick_padding) + brick_padding
        brick_y = row * (brick_height + brick_padding) + 50
        brick = pygame.Rect(brick_x, brick_y, brick_width, brick_height)

        if row == 3:
            if random.random() < 0.3:  # 30% chance for each brick to be unbreakable
                brick_type = 'unbreakable'
                brick_color = (0, 0, 0)
            else:
                brick_type = 'normal'
                brick_color = [random.randint(0, 255) for _ in range(3)]
        else:
            brick_type = 'normal'
            if random.random() < 0.9:
                brick_type = 'bonus'
                brick_color = (255, 215, 0)
            else:
                brick_color = [random.randint(0, 255) for _ in range(3)]

        brick_row.append((brick, brick_color, brick_type))
    bricks.append(brick_row)

#Game over and winning texts
font = pygame.font.SysFont('comicsansms', 40)
game_over_text = font.render('Game Over', True, (255, 255, 255))
game_over_text_rect = game_over_text.get_rect()
game_over_text_rect.center = (W // 2, H // 2)

win_text = font.render('You Win!', True, (255, 255, 255))
win_text_rect = win_text.get_rect()
win_text_rect.center = (W // 2, H // 2)

#Pause menu
menu_font = pygame.font.SysFont('comicsansms', 30)
pause_menu_options = ['Continue', 'Settings']
settings_options = ['Ball Speed: ', 'Shrink Paddle: ']
current_menu_option = 0
current_settings_option = 0
ball_speed_modifier = 1.0
shrink_paddle = True

#Timer to increase ball speed and shrink paddle
pygame.time.set_timer(pygame.USEREVENT + 1, 5000)

def draw_menu(options, current_option):
    for i, option in enumerate(options):
        color = (255, 0, 0) if i == current_option else (255, 255, 255)
        option_text = menu_font.render(option, True, color)
        screen.blit(option_text, (W // 2 - option_text.get_width() // 2, H // 2 + i * 40))

def draw_settings():
    for i, option in enumerate(settings_options):
        color = (255, 0, 0) if i == current_settings_option else (255, 255, 255)
        if i == 0:
            option_text = menu_font.render(f'{option}{ball_speed_modifier:.1f}', True, color)
        else:
            option_text = menu_font.render(f'{option}{"On" if shrink_paddle else "Off"}', True, color)
        screen.blit(option_text, (W // 2 - option_text.get_width() // 2, H // 2 + i * 40))

#Game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                if in_settings:
                    in_settings = False
                else:
                    paused = not paused
            elif event.key == pygame.K_w:
                if paused and not in_settings:
                    current_menu_option = (current_menu_option - 1) % len(pause_menu_options)
                elif in_settings:
                    current_settings_option = (current_settings_option - 1) % len(settings_options)
            elif event.key == pygame.K_s:
                if paused and not in_settings:
                    current_menu_option = (current_menu_option + 1) % len(pause_menu_options)
                elif in_settings:
                    current_settings_option = (current_settings_option + 1) % len(settings_options)
            elif event.key == pygame.K_a:
                if in_settings:
                    if current_settings_option == 0:
                        ball_speed_modifier = max(0.5, ball_speed_modifier - 0.1)
                    elif current_settings_option == 1:
                        shrink_paddle = not shrink_paddle
            elif event.key == pygame.K_d:
                if in_settings:
                    if current_settings_option == 0:
                        ball_speed_modifier = min(1.3, ball_speed_modifier + 0.1)
                    elif current_settings_option == 1:
                        shrink_paddle = not shrink_paddle
            elif event.key == pygame.K_RETURN:
                if paused and not in_settings:
                    if current_menu_option == 0:
                        paused = False
                    elif current_menu_option == 1:
                        in_settings = True
                elif in_settings:
                    if current_settings_option == 0:
                        ball_speed_modifier = max(0.5, min(1.3, ball_speed_modifier))
                    elif current_settings_option == 1:
                        shrink_paddle = not shrink_paddle
        elif event.type == pygame.USEREVENT + 1:
            ballSpeed += 0.4 * ball_speed_modifier
            if shrink_paddle and paddle.width > 50:
                paddle.width -= 20

    if paused:
        screen.fill((0, 0, 0))
        if in_settings:
            draw_settings()
        else:
            draw_menu(pause_menu_options, current_menu_option)
    else:
        screen.fill(bg)

        #Draw paddle
        pygame.draw.rect(screen, pygame.Color(0, 0, 0), paddle)
        #Draw ball
        pygame.draw.circle(screen, pygame.Color(0, 0, 128), ball.center, ballRadius)

        #Draw bricks
        for brick_row in bricks:
            for brick, color, brick_type in brick_row:
                pygame.draw.rect(screen, color, brick)

        #Controls
        key = pygame.key.get_pressed()
        if key[pygame.K_a] and paddle.left > 0:
            paddle.left -= paddleSpeed
        if key[pygame.K_d] and paddle.right < W:
            paddle.right += paddleSpeed

        #Ball movement
        ball.x += ballSpeed * dx
        ball.y += ballSpeed * dy

        #Collision with walls
        if ball.centerx < ballRadius or ball.centerx > W - ballRadius:
            dx = -dx
        if ball.centery < ballRadius + 50:
            dy = -dy
        #Collision with paddle
        if ball.colliderect(paddle) and dy > 0:
            dy = -dy

        #Collision with bricks
        for brick_row in bricks:
            for brick, color, brick_type in brick_row:
                if ball.colliderect(brick):
                    if brick_type != 'unbreakable':
                        brick_row.remove((brick, color, brick_type))
                        dy = -dy
                        if brick_type == 'bonus':
                            paddle.width = min(paddle.width + 30, W)
                    else:
                        dx = -dx if ball.centerx < brick.left or ball.centerx > brick.right else dx
                        dy = -dy if ball.centery < brick.top or ball.centery > brick.bottom else dy
                    break

        #Win
        breakable_bricks_remaining = any(
            brick_type != 'unbreakable' 
            for brick_row in bricks 
            for _, _, brick_type in brick_row
        )
        if not breakable_bricks_remaining:
            screen.fill((0, 0, 0))
            screen.blit(win_text, win_text_rect)

        #Gameover
        if ball.y > H:
            screen.fill((0, 0, 0))
            screen.blit(game_over_text, game_over_text_rect)

    pygame.display.update()
    clock.tick(FPS)

pygame.quit()
sys.exit()

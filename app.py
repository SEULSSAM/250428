import pygame
import sys
import random

# 초기화
pygame.init()

# 화면 설정
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("벽돌 깨기 게임")

# 색상 정의
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)

# 패들 설정
paddle_width = 100
paddle_height = 15
paddle_x = WIDTH // 2 - paddle_width // 2
paddle_y = HEIGHT - 30
paddle_speed = 8

# 공 설정
ball_radius = 10
ball_x = WIDTH // 2
ball_y = HEIGHT // 2
ball_dx = 5
ball_dy = -5

# 벽돌 설정
brick_width = 80
brick_height = 30
brick_rows = 5
brick_cols = 10
brick_gap = 5
bricks = []

# 벽돌 초기화
def init_bricks():
    colors = [RED, ORANGE, YELLOW, GREEN, BLUE]
    for row in range(brick_rows):
        for col in range(brick_cols):
            brick_x = col * (brick_width + brick_gap) + brick_gap
            brick_y = row * (brick_height + brick_gap) + brick_gap + 50
            bricks.append({
                'rect': pygame.Rect(brick_x, brick_y, brick_width, brick_height),
                'color': colors[row % len(colors)],
                'visible': True
            })

# 게임 초기화
init_bricks()
score = 0
lives = 3

# 한글 폰트 설정
font_path = "C:/Windows/Fonts/malgun.ttf"  # 한글 폰트 경로
font = pygame.font.Font(font_path, 24)

game_over = False
game_won = False

# 게임 루프
clock = pygame.time.Clock()
running = True

while running:
    # 이벤트 처리
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and (game_over or game_won):
                # 게임 재시작
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = 5 * (1 if random.random() > 0.5 else -1)
                ball_dy = -5
                paddle_x = WIDTH // 2 - paddle_width // 2
                init_bricks()
                score = 0
                lives = 3
                game_over = False
                game_won = False

    if not game_over and not game_won:
        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_x < WIDTH - paddle_width:
            paddle_x += paddle_speed

        # 공 이동
        ball_x += ball_dx
        ball_y += ball_dy

        # 벽 충돌 처리
        if ball_x <= ball_radius or ball_x >= WIDTH - ball_radius:
            ball_dx = -ball_dx
        if ball_y <= ball_radius:
            ball_dy = -ball_dy

        # 패들 충돌 처리
        if (ball_y + ball_radius >= paddle_y and 
            ball_x >= paddle_x and ball_x <= paddle_x + paddle_width):
            ball_dy = -abs(ball_dy)  # 항상 위로 튕기도록
            # 패들의 어느 부분에 맞았는지에 따라 x 방향 속도 조정
            relative_x = (ball_x - paddle_x) / paddle_width
            ball_dx = 8 * (2 * relative_x - 1)  # -1에서 1 사이의 값으로 변환 후 속도 조정

        # 벽돌 충돌 처리
        for brick in bricks:
            if brick['visible'] and brick['rect'].collidepoint(ball_x, ball_y):
                brick['visible'] = False
                ball_dy = -ball_dy
                score += 10
                break

        # 바닥에 공이 떨어졌을 때
        if ball_y >= HEIGHT:
            lives -= 1
            if lives <= 0:
                game_over = True
            else:
                # 공 위치 초기화
                ball_x = WIDTH // 2
                ball_y = HEIGHT // 2
                ball_dx = 5 * (1 if random.random() > 0.5 else -1)
                ball_dy = -5
                paddle_x = WIDTH // 2 - paddle_width // 2

        # 모든 벽돌이 깨졌는지 확인
        if all(not brick['visible'] for brick in bricks):
            game_won = True

    # 화면 그리기
    screen.fill(BLACK)

    # 패들 그리기
    pygame.draw.rect(screen, WHITE, (paddle_x, paddle_y, paddle_width, paddle_height))

    # 공 그리기
    pygame.draw.circle(screen, WHITE, (int(ball_x), int(ball_y)), ball_radius)

    # 벽돌 그리기
    for brick in bricks:
        if brick['visible']:
            pygame.draw.rect(screen, brick['color'], brick['rect'])

    # 점수와 생명 표시
    score_text = font.render(f'점수: {score}', True, WHITE)
    lives_text = font.render(f'생명: {lives}', True, WHITE)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 100, 10))

    # 게임 오버 메시지
    if game_over:
        game_over_text = font.render('게임 오버! R키를 눌러 재시작', True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - 180, HEIGHT // 2))

    # 게임 승리 메시지
    if game_won:
        game_won_text = font.render('승리! R키를 눌러 재시작', True, GREEN)
        screen.blit(game_won_text, (WIDTH // 2 - 150, HEIGHT // 2))

    # 화면 업데이트
    pygame.display.flip()
    clock.tick(60)

# 게임 종료
pygame.quit()
sys.exit()

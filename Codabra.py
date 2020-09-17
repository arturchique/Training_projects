import pygame
import random
import sys
import time


def change_direction():
    """ Сверяем, можем ли мы изменить направление на заданное пользователем """
    global direction, change_to # меняем значения переменных, существующих вне функции
    if change_to == 'UP' and direction != 'DOWN':
        direction = 'UP'
    if change_to == 'DOWN' and direction != 'UP':
        direction = 'DOWN'
    if change_to == 'LEFT' and direction != 'RIGHT':
        direction = 'LEFT'
    if change_to == 'RIGHT' and direction != 'LEFT':
        direction = 'RIGHT'


def move_head():
    """ Меняем координаты головы при движении в зависимости от направления """
    if direction == "RIGHT":
        snake_head[0] += 10
    elif direction == "LEFT":
        snake_head[0] -= 10
    elif direction == "UP":
        snake_head[1] -= 10
    elif direction == "DOWN":
        snake_head[1] += 10


def draw_snake():
    """ Вырисовываем все "блоки" змеи, предварительно заливая всю область
    коричневым цветом, чтобы на каждоом кадре была актуальная змея """
    game_display.fill(BROWN)
    for pos in snake_body:
        pygame.draw.rect(game_display, GREEN, (pos[0], pos[1], 9, 9))


def draw_food():
    """ Вырисовываем еду """
    pygame.draw.rect(game_display, RED, (food[0], food[1], 9, 9))


def check_for_crash():
    """ Рассматриваем все условия, при которых игра закончится
     и вызываем функцию game_over() """
    if snake_head[0] < 0 or snake_head[0] > window_width - 10 or snake_head[1] < 0 or snake_head[1] > window_height - 10:
        game_over()
    for body in snake_body[1:]:
        if snake_head[0] == body[0] and snake_head[1] == body[1]:
            game_over()


def check_for_food():
    """ Проверка, не столкнулась ли змея с едой """
    global food, score # работаем с переменными, существующими вне функции
    snake_body.insert(0, snake_head.copy())
    if snake_head[0] == food[0] and snake_head[1] == food[1]:
        # если столкнулась с едой, то увеличим число очков и зададим новый координаты для еды
        score += 1
        food = [random.randrange(1, (window_width // 10)) * 10, random.randrange(1, (window_height // 10)) * 10]
    else:
        # если не столкнулась, то удалим элемент с хвоста, так как змея будет двигаться
        # за счет изменения координат головы
        snake_body.pop()


def show_score():
    """ Отрисовываем количество очков """
    score_font = pygame.font.SysFont("arial", 15)
    score_surface = score_font.render(f"Счёт : {score}", True, WHITE)
    score_rect = score_surface.get_rect()
    game_display.blit(score_surface, score_rect)


def game_over():
    """ Отрисовываем экран конца игры """
    go_font = pygame.font.SysFont("arial", 50)
    go_surface = go_font.render(f"Вы проиграли со счетом: {score}", True, RED)
    go_rect = go_surface.get_rect()
    go_rect.midtop = (window_width // 2, window_height // 2 - 35)
    game_display.fill(BLACK)
    game_display.blit(go_surface, go_rect)
    pygame.display.update()
    time.sleep(3)
    pygame.quit()
    sys.exit()


# Определяем цвета по их кодам
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (59, 48, 36)

# Задаем параметры окна с игрой
window_width = 800
window_height = 600

# Создаем окно с игрой
pygame.init()
game_display = pygame.display.set_mode((window_width, window_height))
pygame.display.set_caption("The Snake")

# Задаем параметры будущей скорости обновления кадров
clock = pygame.time.Clock()
FPS = 25

# Параметры шрифта, которым будут писаться все
font = pygame.font.SysFont(None, 25, bold=True)

# Начальные координаты и переменные для Змеи
snake_head = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
direction = 'RIGHT'
change_to = direction
score = 0

# Начальные координаты для еды
food = [random.randrange(1, (window_width//10)) * 10, random.randrange(1, (window_height//10)) * 10]
append_food = True

# Далее -- основной цикл программы
while True:
    # Обрабатываем все возможные события
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                change_to = "LEFT"
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                change_to = "RIGHT"
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                change_to = "UP"
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                change_to = "DOWN"

    # Изменяем направление змеи
    change_direction()
    # Двигаем голову змеи в соответствии с направлением
    move_head()
    # Поведение змеи если она съела еду и если еда не была съедена
    check_for_food()
    # Отрисовка змеи
    draw_snake()
    # Отрисовка еды
    draw_food()
    # Поведение змеи при аварии
    check_for_crash()

    show_score()
    pygame.display.update()
    clock.tick(FPS)
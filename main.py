import pygame

BACKGROUND_COLOR = (0, 255, 255)
FPS = 150

pygame.init()
window = pygame.display.set_mode((500, 500))
window.fill(BACKGROUND_COLOR)
clock = pygame.time.Clock()


class Area:
    def __init__(self, x=0, y=0, width=10, height=10):
        self.rect = pygame.Rect(x, y, width, height)

    def colliderect(self, rect):
        return self.rect.colliderect(rect)


class Picture(Area):
    def __init__(self, x=0, y=0, width=10, height=10, filename='img/enemy.png'):
        super().__init__(x, y, width, height)
        self.image = pygame.image.load(filename)

    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


def reset_game():
    """ Функция для сброса игры до начального состояния """
    global ball, platform, monsters, speed_x, speed_y, game
    # Сбрасываем позиции объектов
    ball.rect.x, ball.rect.y = 250, 250
    platform.rect.x = 200
    speed_x, speed_y = 2, 2

    # Восстанавливаем монстров
    monsters.clear()
    for row in range(3):
        for i in range(9 - row):
            monsters.append(Picture(10 + row * 25 + i * 55, 10 + row * 60, 50, 50))

    game = True


monsters = []
for row in range(3):
    for i in range(9 - row):
        monsters.append(Picture(10 + row * 25 + i * 55, 10 + row * 60, 50, 50))

platform = Picture(200, 475, 99, 25, 'img/platform.png')
ball = Picture(250, 250, 50, 50, 'img/ball.png')

run = True
game = False
move_right, move_left = False, False
speed_x, speed_y = 2, 2


# Функция для отображения стартового экрана
def start_screen():
    window.fill(BACKGROUND_COLOR)
    font = pygame.font.SysFont('verdana', 40)
    text = font.render('Press SPACE to Start', True, (0, 0, 0))

    text_rect = text.get_rect(center=(window.get_width() // 2, window.get_height() // 2))

    window.blit(text, text_rect)
    pygame.display.update()


while run:
    if not game:
        start_screen()

        # Ждем, пока пользователь нажмет на пробел для старта
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                reset_game()  # Сброс игры
                game = True  # Начинаем игру

    if game:
        clock.tick(FPS)

        # Логика конца игры при проигрыше
        if ball.rect.y > platform.rect.y + 35:
            font1 = pygame.font.SysFont('verdana', 40)
            text = font1.render('YOU LOSE', True, (255, 0, 0))
            window.blit(text, (180, 200))
            pygame.display.update()
            game = False
        if len(monsters) == 0:
            font1 = pygame.font.SysFont('verdana', 40)
            text = font1.render('YOU WIN!!!', True, (255, 0, 0))
            window.blit(text, (180, 200))
            pygame.display.update()
            game = False
            FPS += 50  # Увеличение FPS при победе

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    move_left = True
                if event.key == pygame.K_d:
                    move_right = True
                if event.key == pygame.K_ESCAPE:
                    run = False
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    move_left = False
                if event.key == pygame.K_d:
                    move_right = False

        # Основная логика игры
        if game:
            window.fill(BACKGROUND_COLOR)
            ball.rect.x += speed_x
            ball.rect.y += speed_y

            if move_left and platform.rect.x > 0:
                platform.rect.x -= 5
            if move_right and platform.rect.x < 401:
                platform.rect.x += 5

            if ball.rect.x > 450 or ball.rect.x < 0:
                speed_x *= -1
            if ball.rect.y <= 0:
                speed_y *= -1
            if ball.colliderect(platform.rect):
                speed_y = -speed_y

            ball.draw()
            platform.draw()
            for monster in monsters:
                if ball.colliderect(monster):
                    monsters.remove(monster)
                    speed_y *= -1
                else:
                    monster.draw()

        pygame.display.update()

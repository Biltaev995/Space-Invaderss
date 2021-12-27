import pygame
import random

# Настройки окна
WIDTH = 500
HEIGHT = 500
FPS = 60

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Инициализация
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Space Invaders')

clock = pygame.time.Clock()

# Время
last_time = 0
current_time = 0

# Персонаж
x = WIDTH // 2
y = HEIGHT // 2
hero = pygame.Rect(x, y, 60, 50)
hero_img = pygame.image.load('assets/spaceship.png')
hero_hp = 3
points = 0

# Противники
enemies = []

green_enemy_img = pygame.image.load('assets/enemies/green_invader.png').convert()
red_enemy_img = pygame.image.load('assets/enemies/red_invader.png').convert()
yellow_enemy_img = pygame.image.load('assets/enemies/yellow_invader.png').convert()
blue_enemy_img = pygame.image.load('assets/enemies/blue_invader.png').convert()
enemies_imgs = [green_enemy_img, red_enemy_img, yellow_enemy_img, blue_enemy_img]
enemy_img = random.choice(enemies_imgs)

enemy_rect = green_enemy_img.get_rect()
enemy_width = enemy_rect.width
enemy_height = enemy_rect.height
enemy_cd = 5
enemy_speed = 2
enemy_damage = 1

# Звезды
stars = []
star_cd = 10
star_img = pygame.image.load('assets/star.png')
star_rect = star_img.get_rect()
star_width = enemy_rect.width
star_height = enemy_rect.height
star_speed = 4

# Пули
bullet_width = 2
bullet_height = 5
bullet_img = pygame.image.load("assets/bullet.png")
bullets = []
is_shot = False

# Шрифты
DEFAULT_FONT = 'comic sans ms'
menu_font = pygame.font.SysFont(DEFAULT_FONT, 18)
points_font = pygame.font.SysFont(DEFAULT_FONT, 14)
gameover_points_font = pygame.font.SysFont(DEFAULT_FONT, 30)
gameover_font = pygame.font.SysFont(DEFAULT_FONT, 60)

# Текст
gameover_text = gameover_font.render("GAME OVER", True, WHITE)
play_text = menu_font.render("Играть", True, BLACK)
exit_text = menu_font.render("Выйти", True, BLACK)
back_to_menu_text = menu_font.render("В меню", True, BLACK)

# Условия для игрового цикла
moving = ''
running = True
block_hp = False
game_mode = 'MENU'

# Основной цикл отрисовки игры
while running:
    screen.fill(BLACK)

    # Меню игры
    if game_mode == 'MENU':
        # Обрабатываем события, произошедшие за кадр
        for event in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла
            if event.type == pygame.QUIT:
                running = False

            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                # В области зеленой кнопки - начинаем игру
                if 170 < event.pos[0] < 160 + 170 and 100 < event.pos[1] < 100 + 50:
                    game_mode = 'GAME'
                # В области желтой кнопки - изменяем сложность
                if 170 < event.pos[0] < 160 + 170 and 200 < event.pos[1] < 200 + 50:
                    # ЛКМ
                    if event.button == 1:
                        # Минимальная сложность (скорость движения врагов) = 2
                        if enemy_speed > 2:
                            enemy_speed -= 1
                    # ПКМ
                    if event.button == 3:
                        # Максимальная сложность (скорость движения врагов) = 5
                        if enemy_speed < 5:
                            enemy_speed += 1
                # В области красной кнопки - закрываем игру (выходим из цикла)
                if 170 < event.pos[0] < 160 + 170 and 300 < event.pos[1] < 300 + 50:
                    running = False

        # Отрисовываем кнопки
        pygame.draw.rect(screen, GREEN, (170, 100, 160, 50))
        pygame.draw.rect(screen, YELLOW, (170, 200, 160, 50))
        pygame.draw.rect(screen, RED, (170, 300, 160, 50))

        # Отрисовываем текст на кнопках
        screen.blit(play_text, (220, 112))
        difficulty_text = menu_font.render("Сложность: " + str(enemy_speed), True, BLACK)
        screen.blit(difficulty_text, (193, 212))
        difficulty_hint_text = points_font.render("ПКМ - увеличить сложность, ЛКМ - уменьшить", True, WHITE)
        screen.blit(difficulty_hint_text, (93, 262))
        screen.blit(exit_text, (220, 312))

    # Сам процесс игры
    if game_mode == 'GAME':
        # Обрабатываем события, произошедшие за кадр
        for event in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла
            if event.type == pygame.QUIT:
                running = False

            # Обработка событий нажатия клавиш клавиатуры
            if event.type == pygame.KEYDOWN:
                # Нажатие клавиш со стрелками = перемещение в соответствующую сторону
                if event.key == pygame.K_LEFT:
                    moving = 'LEFT'
                if event.key == pygame.K_RIGHT:
                    moving = 'RIGHT'
                if event.key == pygame.K_UP:
                    moving = 'UP'
                if event.key == pygame.K_DOWN:
                    moving = 'DOWN'
                # Нажатие на пробел = выстрел
                if event.key == pygame.K_SPACE:
                    is_shot = True

            # Прекращаем движение при отжатии клавиш со стрелками
            # Без этого условия при однократном нажатии будет бесконечное движение в выбранном направлении
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                    moving = 'STOP'

        # Передвижение персонажа
        if moving == 'LEFT' and hero.left > 0:
            hero.left -= 5
        if moving == 'RIGHT' and hero.right < WIDTH:
            hero.left += 5
        if moving == 'UP' and hero.top > 0:
            hero.top -= 5
        if moving == 'DOWN' and hero.bottom < HEIGHT:
            hero.top += 5

        # СТОЛКНОВЕНИЯ
        # Противник с героем
        for enemy in enemies:
            if hero.colliderect(enemy) and not block_hp:
                # отнимаем 1 жизнь
                hero_hp -= enemy_damage
                block_hp = True

                if hero_hp <= 0:
                    game_mode = "GAME OVER"

        # Противник с пулей
        for bullet in bullets:
            for enemy in enemies:
                # Если пуля попала во врага - +1 очко и удаляем пулю и врага
                if bullet.colliderect(enemy):
                    points += 1
                    bullets.remove(bullet)
                    enemies.remove(enemy)

        # ПУЛИ
        # Создание пуль
        if is_shot:
            bullet_rect = pygame.Rect(hero.left + 33, hero.top + 5, bullet_width, bullet_height)
            bullets.append(bullet_rect)
            # блокируем дудос выстрелами
            is_shot = False

        # Отрисовка пуль
        for bullet in bullets:
            screen.blit(bullet_img, (bullet.left, bullet.top))
            bullet.top -= 5

        # Удаление пуль
        index_bul = 0
        for b in bullets:
            if b.bottom < -5:
                bullets.pop(index_bul)
            index_bul += 1

        # ПРОТИВНИКИ
        current_time = pygame.time.get_ticks()
        # Создание противников раз в рандомный промежуток времени
        if current_time - last_time > enemy_cd:
            x_enemy = random.randint(enemy_width, WIDTH - enemy_width)
            enemies.append(pygame.Rect(x_enemy, -enemy_height, enemy_width, enemy_height))
            last_time = current_time
            enemy_cd = random.randint(100, 5000)

        # Отрисовка противников
        for enemy in enemies:
            screen.blit(enemy_img, (enemy.left, enemy.top))
            enemy.top += enemy_speed

        index_enemy = 0
        # Удаление противников
        for enemy in enemies:
            # Если противник ушел за пределы экрана,
            # больше его не отрисовываем, чтобы игра не висла
            if enemy.top > HEIGHT:
                del enemies[index_enemy]
                block_hp = False
                enemy_img = random.choice(enemies_imgs)

        # Отрисовка счета и жизней
        hp_text = points_font.render("Здоровье: " + str(hero_hp), True, WHITE)
        points_text = points_font.render("Очки: " + str(points), True, WHITE)
        screen.blit(hp_text, (410, 10))
        screen.blit(points_text, (10, 10))

        # ЗВЕЗДЫ
        star_cd -= 1
        # Создание звезд
        if star_cd < 0:
            x_star = random.randint(0, WIDTH - star_width)
            star = pygame.Rect(x_star, -star_height, star_width, star_height)
            stars.append(star)
            star_cd = random.randint(20, 40)

        # Отрисовка звезд
        for star in stars:
            screen.blit(star_img, (star.left, star.top))
            star.top += star_speed

            # Удаление звезд
            if star.top > HEIGHT:
                stars.remove(star)

        # Отрисовка персонажа
        screen.blit(hero_img, (hero.left, hero.top))

    # Если конец игры - отрисовываем экран с надписью "GAME OVER"
    if game_mode == 'GAME OVER':
        screen.fill(BLACK)

        screen.blit(gameover_text, (70, 200))

        final_points_text = gameover_points_font.render("Очки: " + str(points), True, WHITE)
        screen.blit(final_points_text, (180, 280))

        # Кнопка возврата в меню
        pygame.draw.rect(screen, GREEN, (170, 100, 160, 50))
        screen.blit(back_to_menu_text, (220, 112))

        # Обрабатываем события, произошедшие за кадр
        for event in pygame.event.get():
            # Если нажали на крестик (на окне игры) - выходим из цикла
            if event.type == pygame.QUIT:
                running = False

            # Если нажали на кнопку мыши
            if event.type == pygame.MOUSEBUTTONDOWN:
                # В области зеленой кнопки - возвращаемся в меню
                if 170 < event.pos[0] < 160 + 170 and 100 < event.pos[1] < 100 + 50:
                    hero_hp = 3
                    points = 0
                    hero = pygame.Rect(x, y, 60, 50)
                    moving = ''

                    game_mode = 'MENU'

    pygame.display.update()
    clock.tick(FPS)
pygame.quit()

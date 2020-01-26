import pygame
import random
from os import path
from PIL import Image
# Импортирование библиотек
img_dir = path.join(path.dirname(__file__), 'img')
snd_dir = path.join(path.dirname(__file__), 'snd')
# Загрузка директорий
# Установка констант
WIDTH = 700
HEIGHT = 700
FPS = 60
POWERUP_TIME = 5000

# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Изменение размеров моделек персонажей
img = Image.open('img/lifestealer.png')
width = 200
height = 1000
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/lifestealer_.png')

img = Image.open('img/shar.png')
width = 32
height = 32
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/shar_small.png')

img = Image.open('img/hero1.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_1.png')

img = Image.open('img/hero2.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_2.png')

img = Image.open('img/hero3.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_3.png')

img = Image.open('img/hero4.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_4.png')

img = Image.open('img/hero5.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_5.png')

img = Image.open('img/hero6.png')
width = 90
height = 90
resized_img = img.resize((width, height), Image.ANTIALIAS)
resized_img.save('img/hero_6.png')


# Создаем игру и окно
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("LIFESTEALER")  # Название окна
clock = pygame.time.Clock()

font_name = pygame.font.match_font('arial')  # Установка шрифта


def dr_txt(surf, text, size, x, y):  # функция установки текста
    # и подача аргументов
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)


def newVRAG():
    m = VRAG()
    all_sprites.add(m)
    VRAGs.add(m)


def dr_shield(surf, x, y, gl):  # Панель здоровья
    if gl < 0:
        gl = 0
    the_bar_len = 100
    the_bar_high = 10
    fill = (gl / 100) * the_bar_len
    outline_rect = pygame.Rect(x, y, the_bar_len, the_bar_high)
    fill_rect = pygame.Rect(x, y, fill, the_bar_high)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)  # Отрисовка панели


def draw_lives(surf, x, y, lives, img):  # Панель жизней
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)


def show_go_screen():  # Отрисовка главного экрана/текста
    screen.blit(background, background_rect)
    dr_txt(screen, "GUNSHOOTER demo!", 58, WIDTH / 2, HEIGHT / 4)
    dr_txt(screen, "move by keys ←→↓↑, Space to fire", 22,
              WIDTH / 2, HEIGHT / 2)
    dr_txt(screen, "Press a key to begin", 22, WIDTH / 2, HEIGHT * 2.2 / 4)
    dr_txt(screen, "made by Vladislav Pismanik", 18, WIDTH / 2, HEIGHT * 3.5 / 4)
    pygame.display.flip()
    running = True
    while running:  # Часть игрового цикла
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                running = False


class Player(pygame.sprite.Sprite): # Создание главного объекта LIFESTEALER
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(player_img, (112, 115))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = HEIGHT - 10
        self.speedx = 0
        self.shield = 100
        self.shoot_delay = 250
        self.last_shot = pygame.time.get_ticks()
        self.lives = 3
        self.hidden = False
        self.hide_timer = pygame.time.get_ticks()
        self.power = 1
        self.power_time = pygame.time.get_ticks()

    def update(self):
        # задржка
        if self.power >= 2 and pygame.time.get_ticks() - self.power_time > POWERUP_TIME:
            self.power -= 1
            self.power_time = pygame.time.get_ticks()

        # показать, если скрыто
        if self.hidden and pygame.time.get_ticks() - self.hide_timer > 1000:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10

        self.speedx = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:  # Игровой цикл для перемещения и стрельбы + проверка границ
            self.speedx = -8
        if keystate[pygame.K_RIGHT]:
            self.speedx = 8
        if keystate[pygame.K_SPACE]:
            self.shoot()
        self.rect.x += self.speedx
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def powerup(self):
        self.power += 1
        self.power_time = pygame.time.get_ticks()

    def shoot(self):  # Стрельба
        now = pygame.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            if self.power == 1:
                bullet = Bullet(self.rect.centerx, self.rect.top)
                all_sprites.add(bullet)
                bullets.add(bullet)
            if self.power >= 2:
                bullet1 = Bullet(self.rect.left, self.rect.centery)
                bullet2 = Bullet(self.rect.right, self.rect.centery)
                all_sprites.add(bullet1)
                all_sprites.add(bullet2)
                bullets.add(bullet1)
                bullets.add(bullet2)

    def hide(self):
        # временно скрыть игрока
        self.hidden = True
        self.hide_timer = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 200)


class VRAG(pygame.sprite.Sprite):  # Моб врага
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image_orig = random.choice(dota_heroes)
        self.image_orig.set_colorkey(BLACK)
        self.image = self.image_orig.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width * .85 / 2)
        # pygame.draw.circle(self.image, RED, self.rect.center, self.radius) отслеживание врага по красному кругу
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-150, -100)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
        self.rot = 0
        self.rot_speed = random.randrange(-8, 8)
        self.last_update = pygame.time.get_ticks()

    def rotate(self):  # Повороты объектов
        now = pygame.time.get_ticks()
        if now - self.last_update > 50:
            self.last_update = now
            self.rot = (self.rot + self.rot_speed) % 360
            new_image = pygame.transform.rotate(self.image_orig, self.rot)
            old_center = self.rect.center
            self.image = new_image
            self.rect = self.image.get_rect()
            self.rect.center = old_center

    def update(self):
        self.rotate()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)

class Bullet(pygame.sprite.Sprite):  # Класс и спрайт шара-пули
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()


class Pow(pygame.sprite.Sprite):  # Класс Бонусов
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.image = powerup_images[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 2

    def update(self):
        self.rect.y += self.speedy
        # убить, если он сдвинется с нижней части экрана
        if self.rect.top > HEIGHT:
            self.kill()


class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.image = explosion_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim[self.size]):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.size][self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center


# Загрузка всей игровой графики
background = pygame.image.load(path.join(img_dir, "FON GREEN.jpg")).convert()
background_rect = background.get_rect()
player_img = pygame.image.load(path.join(img_dir, "lifestealer_.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
bullet_img = pygame.image.load(path.join(img_dir, "shar_small.png")).convert()
# Загрузка спрайтов врагов
dota_heroes = []
meteor_list =['hero_1.png',
              'hero_2.png', 'hero_3.png',
              'hero_4.png', 'hero_5.png',
              'hero_6.png',
              'meteorBrown_tiny1.png']
for img in meteor_list:
    dota_heroes.append(pygame.image.load(path.join(img_dir, img)).convert())

explosion_anim = {}
explosion_anim['lg'] = []
explosion_anim['sm'] = []
explosion_anim['player'] = []
for i in range(9):  # Загрузка игрвых Анимациий
    filename = 'regularExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    img_lg = pygame.transform.scale(img, (75, 75))
    explosion_anim['lg'].append(img_lg)
    img_sm = pygame.transform.scale(img, (32, 32))
    explosion_anim['sm'].append(img_sm)
    filename = 'sonicExplosion0{}.png'.format(i)
    img = pygame.image.load(path.join(img_dir, filename)).convert()
    img.set_colorkey(BLACK)
    explosion_anim['player'].append(img)
powerup_images = {}
powerup_images['shield'] = pygame.image.load(path.join(img_dir, 'shield1.png')).convert()
powerup_images['gun'] = pygame.image.load(path.join(img_dir, 'star1.png')).convert()

all_sprites = pygame.sprite.Group()  # Объединение спрайтов в группу
VRAGs = pygame.sprite.Group()
bullets = pygame.sprite.Group()
powerups = pygame.sprite.Group()
player = Player()
all_sprites.add(player)
for i in range(8):
    newVRAG()
score = 0  # Объявление очков

# Цикл игры
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        VRAGs = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        powerups = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for i in range(8):
            newVRAG()
        score = 0

    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # проверка для закрытия окна
        if event.type == pygame.QUIT:
            running = False

    # Обновление
    all_sprites.update()

    # проверьте, не попала ли пуля в моб
    hits = pygame.sprite.groupcollide(VRAGs, bullets, True, True)
    for hit in hits:
        score += 50 - hit.radius
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        if random.random() > 0.9:
            pow = Pow(hit.rect.center)
            all_sprites.add(pow)
            powerups.add(pow)
        newVRAG()

    #  Проверка, не ударил ли моб игрока
    hits = pygame.sprite.spritecollide(player, VRAGs, True, pygame.sprite.collide_circle)
    for hit in hits:
        player.shield -= hit.radius * 2
        expl = Explosion(hit.rect.center, 'sm')
        all_sprites.add(expl)
        newVRAG()
        if player.shield <= 0:
            death_explosion = Explosion(player.rect.center, 'player')
            all_sprites.add(death_explosion)
            player.hide()
            player.lives -= 1
            player.shield = 100

    # Проверка столкновений игрока и улучшения
    hits = pygame.sprite.spritecollide(player, powerups, True)
    for hit in hits:
        if hit.type == 'shield':
            player.shield += random.randrange(10, 30)
            if player.shield >= 100:
                player.shield = 100
        if hit.type == 'gun':
            player.powerup()

    # Если игрок умер, игра окончена
    if player.lives == 0 and not death_explosion.alive():
        game_over = True

    # Рендеринг
    screen.fill(BLACK)
    screen.blit(background, background_rect)
    all_sprites.draw(screen)
    dr_txt(screen, str(score), 18, WIDTH / 2, 10)
    dr_shield(screen, 5, 5, player.shield)
    draw_lives(screen, WIDTH - 100, 5, player.lives,
               player_mini_img)
    # После отрисовки всего, переворачиваем экран
    pygame.display.flip()

pygame.quit()

#Создай собственный Шутер!

from pygame import *
from random import randint
from time import time as timer

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play(-1)
mixer.music.set_volume(0.1)

font.init()
font1 = font.SysFont('Arial', 35)
font2 = font.SysFont('Arial', 60)

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self,player_image, player_x, player_y, size_x, size_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x,size_y))
        self.rect = self.image.get_rect()
        self.speed = player_speed
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys[K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys[K_DOWN] and self.rect.y < 435:
            self.rect.y += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15,20,15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1

class Asteroid(GameSprite):
    def update (self):
        self.rect.y += self.speed
        if self.rect.y > 500:
            self.rect.y = 0
            self.rect.x = randint(80, 620)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


window = display.set_mode((700, 500))
display.set_caption('играй')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))

ship = Player('rocket.png', 5, 400, 85, 100, 7)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(5):
    monster = Enemy('ufo.png', randint(80, 620), -30, 80, 100, randint(1,5))
    monsters.add(monster)

for i in range(3):
    asteroid = Asteroid('asteroid.png', randint(80, 620), -30, 80, 100, randint(1,5))
    asteroids.add(asteroid)

game = True
finish = False
fire_sound = mixer.Sound('fire.ogg')
num_fire = 0
life = 3
rel_time = False
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire_sound.play()
                    ship.fire()
                    num_fire += 1
                
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    last_time = timer()


    if not finish:
        window.blit(background, (0,0))

        text = font1.render(f'Счет: {score}', True, (255,255,255))
        window.blit(text,(10,20))

        text_lose = font1.render(f'Пропущено: {lost}', True, (255,255,255))
        window.blit(text_lose,(10,50))

        win = font2.render('YOU WIN', True, (0,255,0))
        lose = font2.render('YOU LOSE', True, (255,0,0))

        ship.reset()
        ship.update()
        monsters.draw(window)
        monsters.update()
        bullets.draw(window)
        bullets.update()
        asteroids.draw(window)
        asteroids.update()
        collides = sprite.groupcollide(monsters, bullets, True, False)

        if rel_time:
            now_time = timer()
            if now_time - last_time < 3:
                reload = font1.render("Перезарядка!", True, (0, 255, 0))
                window.blit(reload,(250,450))
            else:
                num_fire = 0
                rel_time = False

        for i in collides:
            score += 1
            monster = Enemy('ufo.png', randint(80, 620), -30,80,100, randint (1,5))
            monsters.add(monster)
        
        if sprite.spritecollide(ship, monsters, False) or lost > 20:
            finish = True
            window.blit(lose,(200,200))

        if sprite.spritecollide(ship, asteroids, True) or lost > 20:
            life -= 1

        if score > 30:
            finish = True
            window.blit(win,(200,200))
        life_text = font1.render(f'Жизни: {life}', True ,(0,255,0))
        if life < 1:
            finish = True
            window.blit(lose, (200,200))
    
    else:
        finish = False
        score = 0
        lost = 0
        rel_time = False
        num_fire = 0
        life = 3
        for m in monsters:
            m.kill()
        for b in bullets:
            b.kill()
        for a in asteroids:
            a.kill()
        time.delay(3000)
        for i in range (5):
            monster = Enemy('ufo.png', randint(80, 620), -30,80,100, randint (1,5))
            monsters.add(monster)
        for i in range(3):
            asteroid = Asteroid('asteroid.png', randint(80, 620), -30, 80, 100, randint(1,5))
            asteroids.add(asteroid)

    display.update()
    time.delay(20)

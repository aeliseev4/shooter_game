from pygame import *
from random import *

class GameSprite(sprite.Sprite):
    def __init__(self, img, x, y, speed, w, h):
        super().__init__()
        self.image = transform.scale(image.load(img), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x >= 0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x <= 600:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet("bullet.png", self.rect.x, self.rect.y, 1.5, 25, 25)
        bullets.add(bullet)

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.rect.y = 500
            self.kill()

class Monster(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 500:
            x_x = randint(0, 500)
            self.rect.x = x_x
            self.rect.y = -150
            lost += 1
        
monsters = sprite.Group()

bullets = sprite.Group()

lost = 0

font.init()
font = font.SysFont(None, 28)

for i in range(5):
    x_x = randint(0, 500)
    m = Monster("ufo.png", x_x, 1, 1.25, 70, 50)
    monsters.add(m)

window = display.set_mode((700, 500))
display.set_caption("Шутер")

background = transform.scale(image.load('galaxy.jpg'), (700, 500))
mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

player = Player("rocket.png", 300, 400, 4, 60, 80)

score = 0

clock = time.Clock()
FPS = 60

fire_sound = mixer.Sound("fire.ogg")

game = True
finish = False

while game:
    clock.tick(FPS)
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()
    if not finish:
        window.blit(background, (0,0))
        player.reset()
        player.update()
        monsters.draw(window)
        bullets.draw(window)
        monsters.update()
        bullets.update()
        missed_enemies = font.render("Пропущенные враги: " + str(lost), True, (255, 0, 0))
        window.blit(missed_enemies, (20, 20))
        result = sprite.groupcollide(monsters, bullets, True, True)
        for m in result:
            score += 1
            x_x = randint(0, 500)
            m = Monster("ufo.png", x_x, 1, 1.25, 70, 50)
            monsters.add(m)
        hitting = font.render("Попадания: " + str(score), True, (255, 255, 255))
        window.blit(hitting, (20, 50))
        display.update()

        if lost >= 5:
            finish = True

        if sprite.spritecollide(player, monsters, False):
            finish = True
    
      


# Разработай свою игру в этом файле!

from pygame import *
mw=display.set_mode((700,500))
back=(0, 0, 255)
display.set_caption('Лабиринт')
class GameSprite(sprite.Sprite):
    def __init__(self,  picture, x, y, w, h):
        super().__init__()
        self.image=transform.scale(image.load(picture), (w, h))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))
        
class Player(GameSprite):
    def __init__(self, player, x, y, w, h, speed_x, speed_y):
       GameSprite.__init__(self, player, x, y, w, h)
       self.speed_x = speed_x
       self.speed_y = speed_y
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        platform_touched = sprite.spritecollide(self, bar, False)
        if self.speed_x > 0:
            for p in platform_touched:
                self.rect.right = min(self.rect.right, p.rect.left)
        elif self.speed_y < 0:
            for p in platform_touched:
                self.rect.left = max(self.rect.left, p.rect.right)
        if self.speed_y > 0:
            for p in platform_touched:
                self.rect.bottom = min(self.rect.bottom, p.rect.top)
        elif self.speed_y < 0:
            for p in platform_touched:
                self.rect.top = max(self.rect.top, p.rect.bottom)

    def fire(self):
        bullet=Bullet('weapon.png', self.rect.right, self.rect.centery, 10, 20, 10)
        bullets.add(bullet)
class Enemy(GameSprite):
    d = 'top'
    def __init__(self,player, x, y, w, h, speed):
        GameSprite.__init__(self, player, x, y, w, h)
        self.speed = speed
    def update(self):
        if self.rect.y <= 0:
            self.d = "buttom"
        if self.rect.y >= 400:
            self.d = "top"
        if self.d == "top":
            self.rect.y -= self.speed
        else:
            self.rect.y += self.speed

    
class Bullet(GameSprite):
    def __init__(self,player, x, y, w, h, speed):
        GameSprite.__init__(self, player, x, y, w, h)
        self.speed = speed
    def update(self):
        self.rect.x+=self.speed
        if self.rect.x>700:
            self.kill()
     

hero=Player('shutterstock_783589810_frame-43.png', 75, 250, 70, 100, 0, 0)
flag= True
wall_1=GameSprite('platform_v.png', 180, 230, 50, 180)
wall_2=GameSprite('platform_h.png', 0, 370, 190, 50)
wall_3=GameSprite('platform_h.png', 75, 184, 160, 50)
wall_4=GameSprite('platform_h.png', 230, 300, 400, 50)
bar = sprite.Group()
bullets=sprite.Group()
enemys=sprite.Group()
bar.add(wall_1)
bar.add(wall_2)
bar.add(wall_3)
bar.add(wall_4)

final=GameSprite('1-2.png', 10, 430, 70, 70)
enemy=GameSprite('Asset 4@4x.png', 400, 200, 70, 100)
win=transform.scale(image.load('winner_1.jpg'), (700, 500))
lose=transform.scale(image.load('game-over_1.png'), (700, 500))
enemys.add(enemy)

finish=False
while flag:
    mw.fill(back)
    time.delay(50)

    for e in event.get():
        if e.type == QUIT:
            flag=False
        elif e.type == KEYDOWN:
            if e.key == K_LEFT:
                hero.speed_x = -5
            elif e.key == K_RIGHT:
                hero.speed_x = 5
            elif e.key == K_UP:
                hero.speed_y = -5
            elif e.key == K_DOWN:
               hero.speed_y = 5
            elif e.key == K_SPACE:
                hero.fire()
        elif e.type == KEYUP:
           if e.key == K_LEFT:
               hero.speed_x = 0
           elif e.key == K_RIGHT:
               hero.speed_x = 0
           elif e.key == K_UP:
               hero.speed_y = 0
           elif e.key == K_DOWN:
               hero.speed_y = 0
    sprite.groupcollide(bullets, bar, True, False)
    sprite.groupcollide(bullets, enemys, True, True)
    bullets.update()
    bullets.draw(mw)
    bar.update()
    bar.draw(mw)
    hero.update()
    hero.reset()
    enemys.update()
    enemys.draw(mw)
    final.reset()
    if sprite.collide_rect(hero, final):
        finish=True
        mw.blit(win, (0, 0))
    if sprite.spritecollide(hero, enemys, False):
        finish=True
        mw.blit(lose, (0, 0))
    display.update()
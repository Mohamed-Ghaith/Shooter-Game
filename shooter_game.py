from pygame import *
from random import randint
from time import time as timer
# this is a new commit/change
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed, width=65, height=65):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.player_image = player_image
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_UP] and self.rect.y >0 :
            self.rect.y -= self.speed
        if keys_pressed[K_DOWN] and self.rect.y < 425:
            self.rect.y += self.speed
        if keys_pressed[K_LEFT] and self.rect.x >0:
            self.rect.x -= self.speed
        if keys_pressed[K_RIGHT] and self.rect.x <620:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet2.png', self.rect.centerx, self.rect .top,20, 20, 20 )
        Bullets.add(bullet)


class Enemy(GameSprite):
    def update(self):
      global lost
      self.rect.y += self.speed
        
      if self.rect.y >= win_height:
        if "asteroid2.png" in self.player_image:
          lost += 1
          self.rect.y = 0
          self.rect.x = randint(0, win_width - 100)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y <= 0:
            self.kill()       

#Game Scene 
win_width = 700
win_height = 500
window = display.set_mode((win_width,win_height))
display.set_caption('Shooter')
background = transform.scale(image.load('galazy.jpg'),(win_width,win_height))
sp1 = Player('rocket1.png',0,400,5)
e1 = Enemy('asteroid2.png', randint(0, win_width - 100),2,3)
e2 = Enemy('asteroid2.png', randint(0, win_width - 100),3,1)
e3 = Enemy('asteroid2.png', randint(0, win_width - 100),6,2)
e4 = Enemy('asteroid2.png', randint(0, win_width - 100),4,2)
asteroids1 = Enemy('asteroid.png', randint(0, win_width - 100),2,3)
asteroids20 = Enemy('asteroid.png', randint(0, win_width - 100),3,1)
asteroids3 = Enemy('asteroid.png', randint(0, win_width - 100),6,2)

monsters = sprite.Group()
monsters.add(e1)
monsters.add(e2)
monsters.add(e3)
monsters.add(e4)

asteroids = sprite.Group()
asteroids.add(asteroids1)
asteroids.add(asteroids20)
asteroids.add(asteroids3)





Bullets = sprite.Group()


#Music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
Shoot = mixer.Sound('laserShoot.wav')



#Font
font.init()
font1 = font.SysFont('Arial', 70)  
font2 = font.SysFont('Arial', 36)
win = font1.render('YOU WIN!', True, (0,255,0))
win2 = font1.render('YOU LOSE!', True, (255,0,0))

miss = font2.render('Missed:'+str(lost), True, (255,255,255))
score = font2.render('Score: 0', True, (255,255,255))

num_fire = 5
rel_time = False  

points = 0
# Game loop data 
game = True
finish = False
FPS = 60
clock = time.Clock()
#Game loop
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:

                if num_fire > 0 and rel_time == False:
                    sp1.fire()
                    Shoot.play()
                    num_fire -= 1

                if num_fire <= 0 and rel_time == False:
                    rel_time = True
                    start_time = timer()
                
    if finish != True:
        window.blit(background,(0,0))

        #reloading logic
        if rel_time == True:
            now_time  = timer( )
            if now_time - start_time < 3:
              reloading_txt = font2.render('Wait, Reload...', 1, (150,0,0))
              window.blit(reloading_txt, (260, 460))
            else: 
                num_fire = 5
                rel_time = False

              


        # collsion monesters with bullets
        collided_list = sprite.groupcollide(monsters, Bullets, True, True)
        if len(collided_list) > 0 :
            for m in collided_list:
                points += 1
                e = Enemy('asteroid2.png', randint(0, win_width - 100),2,randint(1,5)) 
                monsters.add(e)
                print(points) 


        #win and lose logic
        if points >= 10:
            #win
            finish = True 
            window.blit(win, (230, 230))


        #lose
        if lost >= 3 or sprite.spritecollide(sp1, monsters, False) or sprite.spritecollide(sp1, asteroids, False):
            finish =True 
            window.blit(win2, (230,230))

        
        miss = font2.render('Missed:'+str(lost), True, (255,255,255))
        score = font2.render('Score:' + str (points), True, (255,255,255))




        window.blit(miss, (10,10))
        window.blit(score, (10,40))


        sp1.reset()
        sp1.update()
        monsters.draw(window)
        monsters.update()
        asteroids.draw(window)
        asteroids.update()
        Bullets.draw(window)
        Bullets.update()

    display.update()
    clock.tick(FPS)
    

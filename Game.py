import pygame

from abc import ABC, abstractmethod
from time import sleep
from pygame.locals import*
from random import randrange

class Sprite(ABC):
    def __init__(self, x, y, w, h, m):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.model = m
        self.vert_velocity = 0.0
    
    @abstractmethod
    def update(self):
        pass
    
    @abstractmethod
    def isBrick(self):
        return False
    
    @abstractmethod
    def isMario(self):
        return False
    
    @abstractmethod
    def isCoinBlock(self):
        return False
     
    #checks to see if Mario is colliding with obstacle
    def isColliding(self, sprite):
        if (self.x + self.w < sprite.x):      #Not a Left collision
            return False
        if (self.x > sprite.x + sprite.w):    #Not a Right collision
            return False
        if (self.y + self.h < sprite.y):       #Not Top collision
            return False
        if (self.y > sprite.y + sprite.h):      #Not Under the brick collision 
            return False  
        return True

    def getOutOfTheObstacle(self, sprite): 
        if (self.x <= sprite.x + sprite.w and self.prev_x >= sprite.x + sprite.w):      #Right Side Collision
            self.x = sprite.x + sprite.w
        elif (self.x + self.w >= sprite.x and self.prev_x + self.w <= sprite.x):  #Left side collision
            self.x = sprite.x - self.w
        elif (self.y + self.h >= sprite.y and self.prev_y + self.h <= sprite.y + sprite.h):  #Top Collision
            self.y = sprite.y - self.h
            self.jumpFrame = 0
            self.vert_velocity = 2.1
            self.coinPop = 0
        elif self.y <= sprite.y + sprite.h and self.prev_y >= sprite.h:          #Under the Brick collision
            self.y = sprite.y + sprite.h
            self.vert_velocity = 0.0
            if (sprite.isCoinBlock() and self.coinPop == 0):                                         
                self.coinPop += 1                     
                if sprite.coinLimit < 5:
                    sprite.addCoins()

class Model():    
    def __init__(self):
        self.mario = Mario(self)
        self.sprites = []
        self.sprites.append(self.mario)
        self.sprites.append(Brick(450, 350, self))
        self.sprites.append(Brick(-120, 305, self))
        self.sprites.append(Brick(118, 145, self))
        self.sprites.append(Brick(217, 220, self))
        self.sprites.append(Brick(78, 335, self))
        self.sprites.append(Brick(884, 216, self))
        self.sprites.append(Brick(984, 322, self))
        self.sprites.append(Brick(800, 275, self))
        
        self.sprites.append(CoinBlock(610, 300, self))
        self.sprites.append(CoinBlock(1220, 300, self))
        self.sprites.append(CoinBlock(1830, 300, self))
       
    def removeCoin(self, coin):
        self.sprites.remove(coin)
    
    def update(self):
        for s in self.sprites:
            if s.isBrick() or s.isCoinBlock():
                if self.mario.isColliding(s):
                    self.mario.getOutOfTheObstacle(s)
            #uses polymorphism to call the update() of either Mario, CoinBlock, Coin, or Brick
            s.update()
    
class Brick(Sprite):
    def __init__(self, X, Y, m):
        super().__init__(X, Y, 89, 60, m)
        self.img = pygame.image.load("brick.png")
    
    def draw(self, screen):
        screen.blit(pygame.transform.scale(self.img, (self.w, self.h)), (self.x - self.model.mario.x + self.model.mario.marioScreenLocation, self.y))
    
    def update(self):
        pass
    
    def isMario(self):
        return False
    
    def isBrick(self):
        return True
    
    def isCoinBlock(self):
        return False
            
class Mario(Sprite):
    def __init__(self, m):
        super().__init__(0, 0, 60, 95, m)
        self.marioScreenLocation = 150
        self.jumpFrame = 0
        self.vert_velocity = 0
        
        self.mario_imagesLeft, self.mario_imagesRight = [], []
        self.leftImgCounter, self.rightImgCounter = 0, 0 
        self.moveMarioLeft, self.moveMarioRight = False, False 
        self.defaultPos = -1
        
        self.mario_img = pygame.image.load("marioRight1.png")
        self.mario_imagesLeft.append(pygame.image.load("marioLeft1.png"))
        self.mario_imagesLeft.append(pygame.image.load("marioLeft2.png"))
        self.mario_imagesLeft.append(pygame.image.load("marioLeft3.png"))
        self.mario_imagesLeft.append(pygame.image.load("marioLeft4.png"))
        self.mario_imagesLeft.append(pygame.image.load("marioLeft5.png"))
        self.mario_imagesRight.append(pygame.image.load("marioRight1.png"))
        self.mario_imagesRight.append(pygame.image.load("marioRight2.png"))
        self.mario_imagesRight.append(pygame.image.load("marioRight3.png"))
        self.mario_imagesRight.append(pygame.image.load("marioRight4.png"))
        self.mario_imagesRight.append(pygame.image.load("marioRight5.png"))
        
    def prev_destination(self):
        self.prev_x = self.x
        self.prev_y = self.y
    
    def draw(self, screen):
        if self.moveMarioRight:
            self.mario_img = self.mario_imagesRight[self.rightImgCounter]
            self.rightImgCounter += 1
            
            if self.rightImgCounter == 5:
                self.rightImgCounter = 0
            self.defaultPos = 1
        elif self.moveMarioLeft:
            self.mario_img = self.mario_imagesLeft[self.leftImgCounter]
            self.leftImgCounter += 1
            
            if self.leftImgCounter == 5:
                self.leftImgCounter = 0
            self.defaultPos = 0
        elif self.defaultPos == 1:
            self.mario_img = self.mario_imagesRight[self.rightImgCounter]
        elif self.defaultPos == 0:
            self.mario_img = self.mario_imagesLeft[self.leftImgCounter]
        else:
            self.mario_img = self.mario_imagesRight[self.rightImgCounter]
        screen.blit(self.mario_img, (self.marioScreenLocation, self.y))
    
    def update(self):
        if self.y < 420: 
            self.vert_velocity += 1.2 #gravity - release Mario gradually from air to ground
            self.y += self.vert_velocity
            self.jumpFrame += 1
        else:                        #stop Mario at ground 
            self.vert_velocity = 0.0
            self.y = 420
            self.jumpFrame = 0
            self.coinPop = 0
    
    def isMario(self):
        return True
    
    def isBrick(self):
        return False
    
    def isCoinBlock(self):
        return False
    
class CoinBlock(Sprite):
    def __init__(self, X, Y, m):
        super().__init__(X, Y, 89, 83, m)
        self.coinLimit = 0
        self.coinBrick = pygame.image.load("coinBlock.png")
        self.coinBrickEmpty = pygame.image.load("coinBlockEmpty.png")

    def addCoins(self):
        # more coins can be added if less than 5 coins have popped out of block
        self.coinLimit += 1   
        # create new coin object and add it to sprites list
        self.coin = Coin(self.x, self.y - 60, self.model)     
        self.model.sprites.append(self.coin)
    
    def update(self):
        pass
      
    def draw(self, screen):
        if self.coinLimit < 5:
            screen.blit(pygame.transform.scale(self.coinBrick, (self.w, self.h)), (self.x - self.model.mario.x + self.model.mario.marioScreenLocation, self.y))
        # change coin block image to being empty after 5 coins have popped out of it
        else:
            screen.blit(pygame.transform.scale(self.coinBrickEmpty, (self.w, self.h)), (self.x - self.model.mario.x + self.model.mario.marioScreenLocation, self.y))
    
    def isMario(self):
        return False
    
    def isBrick(self):
        return False
    
    def isCoinBlock(self):
        return True

class Coin(Sprite):
    def __init__(self, X, Y, m):          
        super().__init__(X, Y, 60, 60, m)                       
        self.vert_velocity = -20.0   # accelerates coin by constant amount first upwards, then down
        self.horiz_velocity = randrange(25) - 12  #accelerates coin by random horizontal amount
  
        self.coin = pygame.image.load("coin.png")
    
    def isMario(self):
        return False
    
    def isBrick(self):
        return False
    
    def isCoinBlock(self):
        return False
    
    def draw(self, screen):
        screen.blit(self.coin, (self.x - self.model.mario.x + self.model.mario.marioScreenLocation, self.y))

    def update(self):
        if (self.y < 500):     #if coin is above ground      
            self.x += self.horiz_velocity 
        
            self.vert_velocity += 1 # to make coin rise
            self.y += self.vert_velocity 
            self.vert_velocity += 1.6    # to make coin fall
            self.y += self.vert_velocity
        
        # remove coin if it hits ground
        else: 
            self.model.removeCoin(self)
            self.y = 500
      
class Controller():
    def __init__(self, model):
        self.model = model
        self.keep_going = True
        
    def update(self):
        self.model.mario.prev_destination()
        for event in pygame.event.get():
            if event.type == QUIT:
                self.keep_going = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.keep_going = False
                if event.key == K_LEFT:
                    self.model.mario.moveMarioLeft = True
                if event.key == K_RIGHT:
                    self.model.mario.moveMarioRight = True
            # elif event.type == pygame.MOUSEBUTTONUP:
            #     self.model.set_dest(pygame.mouse.get_pos())
            elif event.type == KEYUP:
                if event.key == K_RIGHT:
                    self.model.mario.moveMarioRight = False
                if event.key == K_LEFT:
                    self.model.mario.moveMarioLeft = False
        keys = pygame.key.get_pressed()
        
        if keys[K_LEFT]:
            self.model.mario.x -= 10
        if keys[K_RIGHT]:
            self.model.mario.x += 10
        if keys[K_SPACE]:
            if self.model.mario.jumpFrame < 5:
                self.model.mario.vert_velocity -= 6.0
                self.model.mario.y += self.model.mario.vert_velocity
        # if keys[K_DOWN]:
        #     self.model.mario.y += 10
                  
class View():
    def __init__(self, model):
        screen_size = (800,600)
        self.screen = pygame.display.set_mode(screen_size, 32)
        self.background_image = pygame.image.load("background.png")
        
        self.model = model
        
    def update(self):    
        self.screen.fill([0,200,100])
        
        #draws background image that scrolls as Mario runs
        for i in range(5):            
            self.screen.blit(pygame.transform.scale(self.background_image, (800, 600)), (i*700 - (self.model.mario.x - self.model.mario.marioScreenLocation) / 10, 0))
        
        for s in self.model.sprites: # iterate through sprites
            s.draw(self.screen)    # uses polymorphism to call the draw() of either Mario, Brick, CoinBlock, or Coin

        pygame.display.flip()
                    
print("Use the arrow keys to move. Press Esc to quit.")
pygame.init()
m = Model()
v = View(m)
c = Controller(m)
while c.keep_going:
    c.update()
    m.update()
    v.update()
    sleep(0.04)
print("Goodbye")
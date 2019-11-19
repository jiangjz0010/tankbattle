# -*- coding: utf-8 -*-
import pygame
import time
SCREEN_WIDTH = 23*26
SCREEN_HEIGHT = 23*26
BG_COLOR = pygame.Color(0,0,0)
TEXT_COLOR = pygame.Color(255,0,0)
class MainGame():
    window = None
    my_tank = None
    enemytank_list=[]
    def __init__(self):
        pass
    def StartGame(self):
        #初始化窗口
        pygame.display.init()
        #设置窗口大小及显示
        MainGame.window = pygame.display.set_mode([SCREEN_WIDTH,SCREEN_HEIGHT])
        #设置窗口的标题
        pygame.display.set_caption('坦克大战')
        #初始化我方坦克
        MainGame.my_tank = Mytank(23*8,23*24)
        wood_wall = wood() #设置墙
        wood_wall.setwall(5,5,6,6)
        iron_wall = iron()
        iron_wall.setwall(7,8,9,10)
        MainGame.explode = Explode()
        set_enemytank(10,10)
        set_enemytank(50,10)
        set_enemytank(100,10)
        set_enemytank(150,10)
        set_enemytank(200,10)
        set_enemytank(250,10)
        set_enemytank(300,10)
        set_enemytank(350,10)
        set_enemytank(360,10)
        set_enemytank(370,10)
        while True:
            # time.sleep(0.0001)
            #给窗口填充色
            MainGame.window.fill(BG_COLOR)
            #获取事件
            self.getEvent()
            #调用坦克显示的方法
            MainGame.my_tank.displayTank()
            #坦克移动
            if not MainGame.my_tank.stop: 
                 MainGame.my_tank.move()
            wood_wall.displaywood() #展示木头_墙
            iron_wall.displayicon() #展示钢铁_墙
            if MainGame.my_tank.ifbullet:
                MainGame.my_tank.bullet.displayBullet()
                MainGame.my_tank.bullet.move()
            for i in MainGame.enemytank_list:
                i.displayTank()
                i.move()
            pygame.display.update()
    def EndGame(self):
        print('thank you for using')
        exit()
    def getEvent(self):
        eventList = pygame.event.get()
        #遍历事件
        for event in eventList:
            #判断按下的是键盘还是关关闭
            if event.type == pygame.QUIT:
                self.EndGame()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    MainGame.my_tank.direction = 'L'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_RIGHT:
                    MainGame.my_tank.direction = 'R'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_UP:
                    MainGame.my_tank.direction = 'U'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_DOWN:
                    MainGame.my_tank.direction = 'D'
                    MainGame.my_tank.stop = False
                elif event.key == pygame.K_SPACE:
                    if not MainGame.my_tank.ifbullet:
                        MainGame.my_tank.shot()
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_DOWN or event.key == pygame.K_UP:
                    MainGame.my_tank.stop = True
class Tank():
    def __init__(self):
        pass
    def move(self):
        pass
    def shot(self):
        pass
    def displayTank(self):
        #获取展示的对象
        self.image = self.images[self.direction]
        #调用blit方法展示
        MainGame.window.blit(self.image,self.rect)
    def notinwall(self):
        if self.direction == 'U':
            if ([self.rect.left,self.rect.top-23] in wood.woodplace_list) or ([self.rect.left+23,self.rect.top-23] in wood.woodplace_list) or ([self.rect.left,self.rect.top-23] in iron.ironplace_list) or ([self.rect.left+23,self.rect.top-23] in iron.ironplace_list) :
                return False
            else:
                return True
        elif self.direction == 'D':
            if ([self.rect.left,self.rect.top+46] in wood.woodplace_list) or ([self.rect.left+23,self.rect.top+46] in wood.woodplace_list) or ([self.rect.left,self.rect.top+46] in iron.ironplace_list) or ([self.rect.left+23,self.rect.top+46] in iron.ironplace_list):
                return False
            else:
                return True
        elif self.direction == 'L':
            if ([self.rect.left-23,self.rect.top] in wood.woodplace_list) or ([self.rect.left-23,self.rect.top+23] in wood.woodplace_list) or ([self.rect.left-23,self.rect.top] in iron.ironplace_list) or ([self.rect.left-23,self.rect.top+23] in iron.ironplace_list):
                return False
            else:
                return True
        else:
            if ([self.rect.left+46,self.rect.top] in wood.woodplace_list) or ([self.rect.left+46,self.rect.top+23] in wood.woodplace_list) or ([self.rect.left+46,self.rect.top] in iron.ironplace_list) or ([self.rect.left+46,self.rect.top+23] in iron.ironplace_list):
                return False
            else:
                return True
class Mytank(Tank):
    stop = True
    def __init__(self,left,top):
        self.bullet = None
        self.ifbullet = False
        #保存加载的图片
        self.images = {
            'U':pygame.image.load("90/a.png"),
            'D':pygame.image.load("90/ab.png"),
            'L':pygame.image.load("90/al.png"),
            'R':pygame.image.load("90/ar.png"),
            }
        #方向
        self.direction = 'U'
        #根据方向获取图片
        self.image = self.images[self.direction]
        #根据图片获取区域
        self.rect = self.image.get_rect()
        #设置区域的left,top
        self.rect.left = left
        self.rect.top = top
    def shot(self):
        self.ifbullet = True
        self.bullet = Bullet(self.direction,self.rect.left,self.rect.top)
        MainGame.window.blit(self.bullet.image,self.rect)
        pygame.display.update()
    def move(self):
        self.speed = 1
        pygame.time.delay(25)
        if self.direction == 'U' and self.notinwall():
            if self.rect.top - self.speed*23 >= 0:
                self.rect.top -= self.speed*23
        elif self.direction == 'D' and self.notinwall():
            if self.rect.top+self.rect.height+self.speed*23 <= SCREEN_HEIGHT:
                self.rect.top += self.speed*23
        elif self.direction == 'L' and self.notinwall():
            if self.rect.left-self.speed*23 >= 0:
                self.rect.left -= self.speed*23
        else:
            if self.notinwall():
                if self.rect.left+self.rect.height+self.speed*23 <= SCREEN_WIDTH:
                    self.rect.left += self.speed*23

class Enemytank(Tank):
    enemytank_placelist = []
    def __init__(self,left,top):
        self.bullet = None
        self.ifbullet = False
        #保存加载的图片
        self.images = {
            'U':pygame.image.load("90/enemybf00.png"),
            'D':pygame.image.load("90/enemybb00.png"),
            'L':pygame.image.load("90/enemybl00.png"),
            'R':pygame.image.load("90/enemybr00.png"),
            }
        #方向
        self.direction = 'D'
        #根据方向获取图片
        self.image = self.images[self.direction]
        #根据图片获取区域
        self.rect = self.image.get_rect()
        #设置区域的left,top
        self.rect.left = left
        self.rect.top = top
    def shot(self):
        self.ifbullet = True
        self.bullet = Bullet(self.direction,self.rect.left,self.rect.top)
        MainGame.window.blit(self.bullet.image,self.rect)
        pygame.display.update()
    def move(self):
        self.speed = 1
        pygame.time.delay(35)
        if self.direction == 'U' and self.notinwall():
            if self.rect.top - self.speed*23 >= 0:
                self.rect.top -= self.speed*23
        elif self.direction == 'D' and self.notinwall():
            if self.rect.top+self.rect.height+self.speed*23 <= SCREEN_HEIGHT:
                self.rect.top += self.speed*23
        elif self.direction == 'L' and self.notinwall():
            if self.rect.left-self.speed*23 >= 0:
                self.rect.left -= self.speed*23
        else:
            if self.notinwall():
                if self.rect.left+self.rect.height+self.speed*23 <= SCREEN_WIDTH:
                    self.rect.left += self.speed*23
def set_enemytank(x,y):
    a = Enemytank(x,y)
    MainGame.enemytank_list.append(a)
class Wall():
    def __init__(self):
        pass
    def setwall(self):
        pass
class Bullet():
    def __init__(self,direction,left,top):
        self.image = pygame.image.load('90/pao.jpg')
        self.direction = direction
        self.rect = self.image.get_rect()
        if self.direction == 'U':
            self.rect.left = left+18
            self.rect.top = top
        elif self.direction == 'D':
            self.rect.left = left+18
            self.rect.top = top+46
        elif self.direction == 'L':
            self.rect.left = left
            self.rect.top = top + 18
        else:
            self.rect.left = left+46
            self.rect.top = top+18
    def move(self):
        pygame.time.delay(17)
        if self.ifexplode():
            MainGame.explode.displayExplode(self.rect.left,self.rect.top)
            MainGame.my_tank.ifbullet = False
        if self.direction == 'U':
            self.rect.top -=23
        elif self.direction == 'D':
            self.rect.top +=23
        elif self.direction == 'L':
            self.rect.left -= 23
        else:
            self.rect.left += 23
    def displayBullet(self):
        MainGame.window.blit(self.image,self.rect)
    def ifexplode(self):
        if self.rect.left <=0 or self.rect.left >= SCREEN_WIDTH or self.rect.top <= 0 or self.rect.top >= SCREEN_HEIGHT:
            return True
        if self.direction == 'U':
            if [self.rect.left-18,self.rect.top-23] in wood.woodplace_list or [self.rect.left+5,self.rect.top-23] in wood.woodplace_list:
                if [self.rect.left-18,self.rect.top-23] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left-18,self.rect.top-23])
                if [self.rect.left+5,self.rect.top-23] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left+5,self.rect.top-23])
                return True
            elif [self.rect.left-18,self.rect.top-23] in iron.ironplace_list or [self.rect.left+5,self.rect.top-23] in iron.ironplace_list:
                return True
        elif self.direction == 'D':
            if [self.rect.left-18,self.rect.top] in wood.woodplace_list or [self.rect.left+5,self.rect.top] in wood.woodplace_list:
                if [self.rect.left-18,self.rect.top] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left-18,self.rect.top])
                if [self.rect.left+5,self.rect.top] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left+5,self.rect.top])
                return True
            elif [self.rect.left-18,self.rect.top] in iron.ironplace_list or [self.rect.left+5,self.rect.top] in iron.ironplace_list:
                return True
        elif self.direction == 'L':
            if [self.rect.left-23,self.rect.top-18] in wood.woodplace_list or [self.rect.left-23,self.rect.top+5] in wood.woodplace_list:
                if [self.rect.left-23,self.rect.top-18] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left-23,self.rect.top-18])
                if [self.rect.left-23,self.rect.top+5] in wood.woodplace_list:
                    wood.woodplace_list.remove( [self.rect.left-23,self.rect.top+5])
                return True
            elif [self.rect.left-23,self.rect.top-18] in iron.ironplace_list or [self.rect.left-23,self.rect.top+5] in iron.ironplace_list:
                return True
        else:
            if [self.rect.left,self.rect.top-18] in wood.woodplace_list or [self.rect.left,self.rect.top+5] in wood.woodplace_list:
                if [self.rect.left,self.rect.top-18] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left,self.rect.top-18])
                if [self.rect.left,self.rect.top+5] in wood.woodplace_list:
                    wood.woodplace_list.remove([self.rect.left,self.rect.top+5])
                return True
            elif [self.rect.left,self.rect.top-18] in iron.ironplace_list or [self.rect.left,self.rect.top+5] in iron.ironplace_list:
                return True 
        return False

class Music():
    def __init__(self):
        pass
    def paly(self):
        pass
class Explode():
    def __init__(self):
        self.image = pygame.image.load('90/boom.png')
        self.rect = self.image.get_rect()
    def displayExplode(self,left,top):
        if left <= 0 or left >= SCREEN_WIDTH or top <= 0 or top >= SCREEN_HEIGHT:
            if left <= 0:
                self.rect.left = 0
                self.rect.top = top
            elif left >=SCREEN_WIDTH:
                self.rect.left = SCREEN_WIDTH-28
                self.rect.top = top
            elif top <= 0:
                self.rect.left = left
                self.rect.top = 0
            else:
                self.rect.left = left
                self.rect.top = SCREEN_HEIGHT-28
        else:
            self.rect.left = left
            self.rect.top = top
        MainGame.window.blit(self.image,self.rect)
        pygame.display.update()
        pygame.time.delay(40)
class wood(Wall):
    woodplace_list = []
    def setwall(self,x0,y0,x1,y1):
        for i in range(x0,x1+1,):
            for j in range(y0,y1+1):
                # MainGame.window.blit(self.image,(i*23,j*23))
                self.woodplace_list.append([i*23,j*23])
    def __init__(self):
        self.image = pygame.image.load('90/wood.jpg')
    def displaywood(self):
        for i in self.woodplace_list:
            MainGame.window.blit(self.image,(i[0],i[1]))

class iron(Wall):
    ironplace_list = []
    def setwall(self,x0,y0,x1,y1):
        for i in range(x0,x1+1,):
            for j in range(y0,y1+1):
                # MainGame.window.blit(self.image,(i*23,j*23))
                self.ironplace_list.append([i*23,j*23])
    def __init__(self):
        self.image = pygame.image.load('90/iron.jpg')
    def displayicon(self):
        for i in self.ironplace_list:
            MainGame.window.blit(self.image,(i[0],i[1]))
if __name__=='__main__':
    MainGame().StartGame()
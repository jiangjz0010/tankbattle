# -*- coding: utf-8 -*-
import pygame
import time
import random
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
        wood_wall.setwall(1,3,2,10)
        wood_wall.setwall(5,3,6,10)
        wood_wall.setwall(11,3,12,10)
        wood_wall.setwall(17,3,18,10)
        wood_wall.setwall(23,3,24,10)
        wood_wall.setwall(2,13,3,23)
        wood_wall.setwall(6,13,7,20)
        wood_wall.setwall(10,13,11,20)
        wood_wall.setwall(11,15,14,16)
        wood_wall.setwall(14,13,15,20)
        wood_wall.setwall(18,13,19,20)
        wood_wall.setwall(22,13,23,23)
        # wood_wall.setwall(10,23,10,26)
        # wood_wall.setwall(11,23,14,23)
        # wood_wall.setwall(14,23,14,26)
        iron_wall = iron()
        iron_wall.setwall(14,8,15,9)
        iron_wall.setwall(0,13,1,13)
        iron_wall.setwall(24,13,26,13)
        iron_wall.setwall(10,23,10,26)
        iron_wall.setwall(11,23,14,23)
        iron_wall.setwall(14,23,14,26)
        MainGame.explode = Explode()
        set_enemytank(23*1,23*1)        
        set_enemytank(23*3,23*1)        
        set_enemytank(23*5,23*1)
        while True:
            time.sleep(0.1)
            image = pygame.image.load("90/bird.jpg")
            #给窗口填充色
            MainGame.window.fill(BG_COLOR)
            MainGame.bird()
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
                MainGame.my_tank.bullet.move()
                if MainGame.my_tank.bullet.ifexplode():
                    MainGame.explode.displayExplode(MainGame.my_tank.bullet.rect.left,MainGame.my_tank.bullet.rect.top)
                    MainGame.my_tank.ifbullet = False
                MainGame.my_tank.bullettouchbullet()     
                MainGame.my_tank.bulletattacktank()
            for i in MainGame.enemytank_list:
                i.displayTank()
                i.move()
                i.changedirection()
                if not i.ifbullet:
                    i.shot()
                else:
                    i.bullet.move()
                    i.bullet.move()
                    i.bullet.displayBullet()
                    if i.bulletattacktank():
                        pygame.event.get()
                        time.sleep(5)
                        MainGame.EndGame()
                    if i.bullet.ifexplode():
                        MainGame.explode.displayExplode(i.bullet.rect.left,i.bullet.rect.top)
                        i.ifbullet = False
                        i.bullet = None
            pygame.display.update()
    def EndGame():
        print('thank you for using')
        exit()
    def bird():
        image = pygame.image.load("90/bird.jpg")
        MainGame.window.blit(image,(23*11.5,23*24))
    def getEvent(self):
        eventList = pygame.event.get()
        #遍历事件
        for event in eventList:
            #判断按下的是键盘还是关关闭
            if event.type == pygame.QUIT:
                MainGame.EndGame()
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
        self.ifbullet = True
        self.bullet = Bullet(self.direction,self.rect.left,self.rect.top)
        MainGame.window.blit(self.bullet.image,self.rect)
        pygame.display.update()
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
    def notinborder(self):
        if self.rect.left == 0 or self.rect.left+46 == SCREEN_WIDTH or self.rect.top == 0 or self.rect.top+46 == SCREEN_HEIGHT:
            return False
        else:
            return True
    def notintank(self):
        pass
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
    def move(self):
        self.speed = 1
        if self.direction == 'U' and self.notinwall() and self.notintank():
            if self.rect.top - self.speed*23 >= 0:
                self.rect.top -= self.speed*23
        elif self.direction == 'D' and self.notinwall() and self.notintank():
            if self.rect.top+self.rect.height+self.speed*23 <= SCREEN_HEIGHT:
                self.rect.top += self.speed*23
        elif self.direction == 'L' and self.notinwall() and self.notintank():
            if self.rect.left-self.speed*23 >= 0:
                self.rect.left -= self.speed*23
        elif self.direction == 'R' and self.notinwall() and self.notintank():
            if self.notinwall():
                if self.rect.left+self.rect.height+self.speed*23 <= SCREEN_WIDTH:
                    self.rect.left += self.speed*23
    def notintank(self):
        for i in MainGame.enemytank_list:
            if self.direction == 'U':
                if (self.rect.left,self.rect.top-46) == (i.rect.left,i.rect.top) or (self.rect.left+23,self.rect.top-46) == (i.rect.left,i.rect.top) or (self.rect.left-23,self.rect.top-46) == (i.rect.left,i.rect.top):
                    return False
            elif self.direction == 'D':
                if (self.rect.left,self.rect.top+46) == (i.rect.left,i.rect.top) or (self.rect.left-23,self.rect.top+46) == (i.rect.left,i.rect.top) or (self.rect.left+23,self.rect.top+46) == (i.rect.left,i.rect.top):
                    return False
            elif self.direction == 'L':
                if (self.rect.left-46,self.rect.top) == (i.rect.left,i.rect.top) or (self.rect.left-46,self.rect.top+23) == (i.rect.left,i.rect.top) or (self.rect.left-46,self.rect.top-23) == (i.rect.left,i.rect.top):
                   return False 
            elif self.direction == 'R':
                if (self.rect.left+46,self.rect.top) == (i.rect.left,i.rect.top) or (self.rect.left+46,self.rect.top-23) == (i.rect.left,i.rect.top) or (self.rect.left+46,self.rect.top+23) == (i.rect.left,i.rect.top):
                    return False
        return True
    def bulletattacktank(self):
        if self.ifbullet == True:
            for i in MainGame.enemytank_list:
                if self.bullet.direction == 'U':
                    if (self.bullet.rect.left-18,self.bullet.rect.top-46) == (i.rect.left,i.rect.top):
                        MainGame.enemytank_list.remove(i)
                elif self.bullet.direction == 'D':
                    if (self.bullet.rect.left-18,self.bullet.rect.top+46) == (i.rect.left,i.rect.top):
                        MainGame.enemytank_list.remove(i)
                elif self.bullet.direction == 'L':
                    if (self.bullet.rect.left-46,self.bullet.rect.top-18) == (i.rect.left,i.rect.top):
                        MainGame.enemytank_list.remove(i)
                elif self.bullet.direction == 'R':
                    if (self.bullet.rect.left+46,self.bullet.rect.top-18) == (i.rect.left,i.rect.top):
                        MainGame.enemytank_list.remove(i)
    def bullettouchbullet(self):
        if self.ifbullet == True:
            for i in MainGame.enemytank_list:
                if i.ifbullet == True:
                    if self.bullet == i.bullet:
                        self.bullet.displayExplode()
                        self.ifbullet = False
                        i.ifbullet = False
class Enemytank(Tank):
    enemytank_placelist = []
    def __init__(self,left,top):
        self.bullet = None
        self.ifbullet = False
        #保存加载的图片
        self.images1 = {
            'U':pygame.image.load("90/enemybf00.png"),
            'D':pygame.image.load("90/enemybb00.png"),
            'L':pygame.image.load("90/enemybl00.png"),
            'R':pygame.image.load("90/enemybr00.png"),
            }
        self.images2 = {
            'U':pygame.image.load("90/enemydf10.png"),
            'D':pygame.image.load("90/enemydb10.png"),
            'L':pygame.image.load("90/enemydl10.png"),
            'R':pygame.image.load("90/enemydr10.png"),
            }
        self.images3 = {
            'U':pygame.image.load("90/enemydf30.png"),
            'D':pygame.image.load("90/enemydb30.png"),
            'L':pygame.image.load("90/enemydl30.png"),
            'R':pygame.image.load("90/enemydr30.png"),
            }
        choceimage = random.randint(1,3)
        if choceimage == 1:
            self.images = self.images1
        elif choceimage == 2:
            self.images= self.images2
        elif choceimage == 3:
            self.images  = self.images3  
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
        if self.direction == 'U' and self.notinwall() and self.notintank():
            if self.rect.top - self.speed*23 >= 0:
                self.rect.top -= self.speed*23
        elif self.direction == 'D' and self.notinwall() and self.notintank():
            if self.rect.top+self.rect.height+self.speed*23 <= SCREEN_HEIGHT:
                self.rect.top += self.speed*23
        elif self.direction == 'L' and self.notinwall() and self.notintank():
            if self.rect.left-self.speed*23 >= 0:
                self.rect.left -= self.speed*23
        elif self.direction == 'R' and self.notinwall() and self.notintank():
            if self.rect.left+self.rect.width+self.speed*23 <= SCREEN_WIDTH:
                self.rect.left += self.speed*23
    def changedirection(self):
        if not self.notinwall() or not self.notinborder():
            flag = random.randint(0,3)
            if flag == 0:
                self.direction = 'U'
            elif flag == 1:
                self.direction = 'D'
            elif flag == 2:
                self.direction = 'L'
            else:
                self.direction = 'R'
    def notintank(self):
        for i in MainGame.enemytank_list:
            if self != i :
                if self.direction == 'U':
                    if (self.rect.left,self.rect.top-46) == (i.rect.left,i.rect.top) or (self.rect.left+23,self.rect.top-46) == (i.rect.left,i.rect.top) or (self.rect.left-23,self.rect.top-46) == (i.rect.left,i.rect.top):
                        self.direction = 'D'
                        return False
                elif self.direction == 'D':
                        if (self.rect.left,self.rect.top+46) == (i.rect.left,i.rect.top) or (self.rect.left-23,self.rect.top+46) == (i.rect.left,i.rect.top) or (self.rect.left+23,self.rect.top+46) == (i.rect.left,i.rect.top):
                            self.direction = 'U'
                            return False
                elif self.direction == 'L':
                        if (self.rect.left-46,self.rect.top) == (i.rect.left,i.rect.top) or (self.rect.left-46,self.rect.top+23) == (i.rect.left,i.rect.top) or (self.rect.left-46,self.rect.top-23) == (i.rect.left,i.rect.top):
                            self.direction = 'R'
                            return False 
                elif self.direction == 'R':
                        if (self.rect.left+46,self.rect.top) == (i.rect.left,i.rect.top) or (self.rect.left+46,self.rect.top-23) == (i.rect.left,i.rect.top) or (self.rect.left+46,self.rect.top+23) == (i.rect.left,i.rect.top):
                            self.direction = 'L'
                            return False
        if self.direction == 'U':
            if (self.rect.left,self.rect.top-46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left+23,self.rect.top-46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left-23,self.rect.top-46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                return False
        elif self.direction == 'D':
            if (self.rect.left,self.rect.top+46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left-23,self.rect.top+46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left+23,self.rect.top+46) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                return False
        elif self.direction == 'L':
            if (self.rect.left-46,self.rect.top) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left-46,self.rect.top+23) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left-46,self.rect.top-23) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                return False
        elif self.direction == 'R':
            if (self.rect.left+46,self.rect.top) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left+46,self.rect.top-23) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top) or (self.rect.left+46,self.rect.top+23) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                return False
        return True
    def bulletattacktank(self):
        if self.bullet.direction == 'U':
            if (self.bullet.rect.left-18,self.bullet.rect.top-23) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                gameover = pygame.image.load('90/over.png')
                MainGame.window.blit(gameover,(23*6,23*6))
                pygame.display.flip()
                return True
        elif self.bullet.direction == 'D':
            if (self.bullet.rect.left-18,self.bullet.rect.top) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                gameover = pygame.image.load('90/over.png')
                MainGame.window.blit(gameover,(23*7,23*8))
                pygame.display.flip()
                return True
        elif self.bullet.direction == 'L':
            if (self.bullet.rect.left-23,self.bullet.rect.top-18) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                gameover = pygame.image.load('90/over.png')
                MainGame.window.blit(gameover,(23*6,23*6))
                pygame.display.flip()
                return True
        elif self.bullet.direction == 'R':
            if (self.bullet.rect.left+23,self.bullet.rect.top-18) == (MainGame.my_tank.rect.left,MainGame.my_tank.rect.top):
                gameover = pygame.image.load('90/over.png')
                MainGame.window.blit(gameover,(23*4,23*5))
                pygame.display.flip()
                return True
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
        if self.direction == 'U':
            self.rect.top -= 23
        elif self.direction == 'D':
            self.rect.top += 23
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
        # pygame.time.delay(40)
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
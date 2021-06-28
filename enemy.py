from PIL import Image
import random

cartman = Image.open("./image/chineseCartman.png").convert("RGBA")
kenny = Image.open("./image/kenny.png").convert("RGBA")
kyle = Image.open("./image/kyle.png").convert("RGBA")
stan = Image.open("./image/stan.png").convert("RGBA")
wendy = Image.open("./image/wendy.png").convert("RGBA")

img_list = [cartman, kenny, kyle, stan, wendy]

WIDTH = 240 # width of screen
HEIGHT = 240 # height of screen
        
class Enemy:
    def __init__(self):
        self.width = 30
        self.height = 30
        self.x = WIDTH
        self.y = HEIGHT - self.height
        self.dx = 20 # x-axis speed 
        self.img = random.choice(img_list)
    def left(self):
            self.x -= self.dx
    def draw(self, canvas):
        self.img = self.img.resize((self.width, self.height))
        canvas.paste(self.img, (self.x, self.y), self.img)
    
class EnemyList:
    def __init__(self):
        self.enemy_list = []
        self.rm_list = []
        self.rate = 5 # appearing rate
    def append(self):
        if random.randint(1, 101) <= self.rate:
            e = Enemy()
            self.enemy_list.append(e)
    def move(self):
        for i in self.enemy_list:
            i.left()
            if i.x < 0:
                self.rm_list.append(i)
    def draw(self, canvas):
        for i in self.enemy_list:
            i.draw(canvas)
    def remove(self):
        for i in self.rm_list:
            if i in self.enemy_list:
                self.enemy_list.remove(i)
        self.rm_list.clear()

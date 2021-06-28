from PIL import Image
import random

doge = Image.open("./image/doge.png").convert("RGBA")
doge = doge.resize((25, 25))

WIDTH = 240
        
class Doge:
    def __init__(self,x):
        self.width = 25
        self.height = 25
        self.x = x
        self.y = -self.height
        self.dy = 25
    def down(self):
            self.y += self.dy
    def draw(self, canvas):
        canvas.paste(doge, (self.x, self.y), doge)
    
class DogeList:
    def __init__(self):
        self.doge_list = []
        self.rm_list = []
        self.rate = 10 # appearing rate
    def append(self):
        if random.randint(1, 101) <= self.rate:
            x = random.randrange(0, WIDTH - 24)
            doge = Doge(x)
            self.doge_list.append(doge)
    def move(self):
        for i in self.doge_list:
            i.down()
            if i.y > WIDTH:
                self.rm_list.append(i)
    def draw(self, canvas):
        for i in self.doge_list:
            i.draw(canvas)
    def remove(self):
        for i in self.rm_list:
            self.doge_list.remove(i)
        self.rm_list.clear()

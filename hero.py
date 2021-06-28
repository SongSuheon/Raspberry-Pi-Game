from PIL import Image

GRAVITY = 15
GROUND = 240
WIDTH = 240 # width of screen

musk_img = Image.open("./image/elonmusk.png")
musk_img = musk_img.resize((40, 80))

class ElonMusk:
    def __init__(self):
        self.width = 40
        self.height = 80
        self.x = 120 - (self.width // 2) 
        self.y = GROUND - self.height
        self.dx = 20
        self.dy = -45
        self.is_jump = False
    def left(self):
        if self.x - self.dx >= 0:
            self.x -= self.dx
    def right(self):
         if self.x + self.dx <= WIDTH:
            self.x += self.dx
    def jump(self):
        if self.is_jump == True:
            self.dy += GRAVITY
            self.y += self.dy

        if self.y > GROUND - self.height:
            self.y = GROUND - self.height
            self.dy = -45
            self.is_jump = False
                              
    def draw(self, canvas):
        canvas.paste(musk_img,(self.x, self.y), musk_img)

import time
import random
import math
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

# Create the display
cs_pin = DigitalInOut(board.CE0)
dc_pin = DigitalInOut(board.D25)
reset_pin = DigitalInOut(board.D24)
BAUDRATE = 24000000

spi = board.SPI()
disp = st7789.ST7789(
    spi,
    height=240,
    y_offset=80,
    rotation=180,
    cs=cs_pin,
    dc=dc_pin,
    rst=reset_pin,
    baudrate=BAUDRATE,
)

# Input pins:
button_A = DigitalInOut(board.D5)
button_A.direction = Direction.INPUT

button_B = DigitalInOut(board.D6)
button_B.direction = Direction.INPUT

button_L = DigitalInOut(board.D27)
button_L.direction = Direction.INPUT

button_R = DigitalInOut(board.D23)
button_R.direction = Direction.INPUT

button_U = DigitalInOut(board.D17)
button_U.direction = Direction.INPUT

button_D = DigitalInOut(board.D22)
button_D.direction = Direction.INPUT

button_C = DigitalInOut(board.D4)
button_C.direction = Direction.INPUT

# Turn on the Backlight
backlight = DigitalInOut(board.D26)
backlight.switch_to_output()
backlight.value = True

# Create blank image for drawing.
# Make sure to create image with mode 'RGB' for color.
width = disp.width
height = disp.height
image = Image.new("RGB", (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Clear display.
draw.rectangle((0, 0, width, height), outline=0, fill=(255, 0, 0))
disp.image(image)

fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

class circle:
    def __init__(self):
        self.x = 120 
        self.y = 180
        self.radius = 10
        self.color = '#FF0000' #default color is red
        self.speed = 10

    def move(self, direction):
        
        global width, height
        
        if direction == 'left' and self.x - self.radius - self.speed >=0:
            self.x -= self.speed
        elif direction == 'right' and  self.x + self.radius + self.speed <= width:
            self.x += self.speed
        elif direction == 'up' and self.y - self.radius - self.speed >=0:
            self.y -= self.speed    
        elif direction == 'down'and self.y + self.radius + self.speed <= height:
            self.y += self.speed
                
    def draw(self):
        draw.arc([(self.x - self.radius, self.y - self.radius),(self.x + self.radius, self.y + self.radius)],
            0,360,fill=self.color, width=10)

class bullet:
    def __init__(self, x, y, r):  #  x-axis of center, y-axis of center , radius of circle
        self.width = 5
        self.height = 9
        self.speed = 30
        self.x = x - (self.width / 2)
        self.y = y - r - self.height + (self.speed - 10)
        self.color = '#00FF00' # default color is green
        
    def draw(self):
         draw.rectangle((self.x, self.y, 
            self.x + self.width , self.y + self.height), outline=self.color, fill=self.color, width=2)

class enemy:
    def __init__(self, x):
        self.x = x 
        self.y = 7
        self.radius = self.y
        self.color = '#FFFFFF'
        self.speed = 5
                
    def draw(self):
        
        draw.arc([(self.x - self.radius, self.y - self.radius),(self.x + self.radius, self.y + self.radius)],
            0,360,fill=self.color, width=10)


def clear_all():
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)

# not yet
def crash(e, o): # enemy, object 
    if math.sqrt( (e.x - o.x)**2 + (e.x - o.y)**2 ) < e.radius + o.radius:
        return True
 
    else: 
        return False

 

c = circle()
magazine  = [] # house of bullet
num_of_bullet = 0

enemies = []
num_of_enemy = 0

while True:
    clear_all()

    # circle

    if not button_U.value: 
       c.move('up')
    elif not button_D.value:
       c.move('down')         
    elif not button_L.value:
       c.move('left') 
    elif not button_R.value:
       c.move('right')
    
    c.draw()

    # enemy

    rate = 10
    if random.randint(1, 100) <= rate:
        e = enemy(random.randrange(7, width - 7))
        enemies.append(e)
        num_of_enemy += 1

    rm_e_list = [] # enemy to remove
    rm_e_num = 0 # number of enemy to remove

    for i in range(num_of_enemy):
        if enemies[i].y + enemies[i].speed  >= height :
            rm_e_list.append(i)
            rm_e_num += 1
            continue
 
        else:
            enemies[i].y += enemies[i].speed
            enemies[i].draw()
    
    for i in range(rm_e_num-1, -1, -1):
            del enemies[rm_e_list[i]]
            num_of_enemy -= 1

    # bullet

    if not button_A.value: # fire a bullet
       b = bullet(c.x, c.y, c.radius)
       magazine.append(b)
       num_of_bullet += 1
    
    elif not button_B.value: # fire two bullets
       b1 = bullet(c.x - 5, c.y, c.radius)
       b1.color = "#0000AA"
       magazine.append(b1)
       b2 = bullet(c.x + 5, c.y, c.radius)
       b2.color = "#0000AA"
       magazine.append(b2)
       num_of_bullet += 2
    
    rm_b_list = [] # bullet to remove
    rm_b_num = 0 # number of bullet to remove

    for i in range(num_of_bullet):
        if magazine[i].y - magazine[i].speed  < -magazine[i].height:
            rm_b_list.append(i)
            rm_b_num += 1
            continue
        else:
            magazine[i].y -= magazine[i].speed
            magazine[i].draw()

            
    for i in range(rm_b_num-1, -1, -1):
            del magazine[rm_b_list[i]]
            num_of_bullet -= 1


    # crash
            

    disp.image(image)
    time.sleep(0.02)

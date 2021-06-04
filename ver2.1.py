import time
import random
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
   
    def chang_size(self, radius):
        self.radius = radius
    
    def change_color(self, color):
        self.color = color
    
    def change_speed(self, speed):
        self.speed = speed

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
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 5
        self.height = 9
        self.color = '#00FF00' # default color is green
        self.speed = 30

    def set_init_location(self,circle_x, circle_y, radius): #  x-axis of circle's center, y-axis of circle's center
        self.x = circle_x - (self.width / 2)
        self.y = circle_y - radius - self.height

    def draw(self):
         draw.rectangle((self.x, self.y, 
            self.x + self.width , self.y + self.height), outline=self.color, fill=self.color, width=2)
                   
def clear_all():
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
        

magazine  = [] # house of bullet
num_of_bullet = 0
c = circle()

while True:
    clear_all()
        
    if not button_U.value: 
       c.move('up')
    elif not button_D.value:
       c.move('down')         
    elif not button_L.value:
       c.move('left') 
    elif not button_R.value:
       c.move('right')
    
    c.draw()

    if not button_A.value: # #5 button
       b = bullet()
       b.set_init_location(c.x, c.y, c.radius)
       magazine.append(b)
       num_of_bullet += 1

    elif not button_B.value: # #6 button 
       b = bullet()
       b.set_init_location(c.x, c.y, c.radius)
       # change color and size
       b.color = '#0000FF'
       b.width *= 2
       magazine.append(b)
       num_of_bullet += 1
    
    remove = []
    rm_num = 0

    for i in range(num_of_bullet):
        if magazine[i].y - magazine[i].speed  < -magazine[i].height:
            remove.append(i)
            rm_num += 1
            continue
        else:
            magazine[i].y -= magazine[i].speed
            magazine[i].draw()

            
    for i in range(rm_num-1, -1, -1):
            del magazine[remove[i]]
            num_of_bullet -= 1
            

    disp.image(image)
    time.sleep(0.02)

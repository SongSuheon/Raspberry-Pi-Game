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

#fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)

class circle:
    def __init__(self):
        self.center_x = 120 
        self.center_y = 180
        self.radius = 10
        self.color = '#FF0000' #default color is red
        self.speed = 0
   
    def chang_size(self, radius):
        self.radius = radius
    
    def change_color(self, color):
        self.color = color
    
    def change_speed(self, speed):
        self.speed = speed

    def move(self, direction):
        if((self.center_x - self.radius + x_mvt >=0 && self.center_x + self.radius + x_mvt < width &&
            (self.center_y - self.radius - y_mvt >=0 && self.center_y + slef.radius + y_mvt < height))

            if(direction == 'up')
                self.center_y -= self.speed    
            elif(direction == 'down')
                self.center_y += self.speed
            elif(direction == 'left')
                self.center_x -= self.speed
            elif(direction == 'right')
                self.center_x += self.speed
                
    def draw(self):
        draw.arc([(self.center_x - self.radius, self.center_y - self.radius),(self.center_x + self.radius, slef.center_y + self.radius)],
            0,360,fill=self.color, width=10)

class bullet1:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 5
        self.height = 9
        self.color = '#00FF00' # default color is green
        self.speed = 10

    def set_init_location(self,circle_x, circle_y, radius): #  x-axis of circle's center, y-axis of circle's center
        self.x = circle_x - (self.width / 2)
        self.y = circle_y - radius - self.height
    
    def draw(self):
         draw.rectangle((self.x, self.y, 
            self.x + self.width , self.y + self.height), outline=self.color, fill=self.color, width=2)
    
class bulltet2:
   def __init__(self):
        self.x = 0
        self.y = 0
        self.width = 2.5
        self.height = 4.5
        self.color = '#0000FF' # default color is blue
        self.speed = 20

    def set_init_location(self,circle_x, circle_y, radius): #  x-axis of circle's center, y-axis of circle's center
        self.x = circle_x - (self.width / 2)
        self.y = circle_y - radius - self.height
        
    def draw(self):
        draw.rectangle((self.x, self.y, 
            self.x + self.width , self.y + self.height), outline=self.color, fill=self.color, width=2)



                   
def clear_all():
    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
        
        



           


while True:
    drawCircle()
    front_bullet_x = circle_x1 - width_of_bullet
    front_bullet_y = (circle_y1 + circle_y2) / 2 - (height_of_bullet / 2)
    rear_bullet_x = circle_x2
    rear_bullet_y = (circle_y1 + circle_y2) / 2 - (height_of_bullet / 2)
    
    if not button_U.value:
        moveCircle(0,-circle_mvt)
        drawCircle()

    if not button_D.value:
        moveCircle(0,circle_mvt)
        drawCircle()
        
    if not button_L.value:
        moveCircle(-circle_mvt,0)
        drawCircle()

    if not button_R.value:
        moveCircle(circle_mvt,0)
        drawCircle()
    
    if not button_A.value:
        shootRearBulletAt(rear_bullet_x, rear_bullet_y)

    if not button_B.value:
        shootFrontBulletAt(front_bullet_x, front_bullet_y)

    disp.image(image)


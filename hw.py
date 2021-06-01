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

#state of circle
circle_diameter = 20
circle_mvt = 15

circle_x1 = (width / 2) - (circle_diameter / 2)
circle_y1 = (height / 2) - (circle_diameter / 2)
circle_x2 = (width / 2) + (circle_diameter / 2)
circle_y2 = (height / 2) + (circle_diameter/ 2)

#state of bullet
width_of_bullet = 8.5
height_of_bullet = 5
bullet_speed = 20

front_bullet_x = circle_x1 - width_of_bullet
front_bullet_y = (circle_y1 + circle_y2) / 2 - (height_of_bullet / 2)
rear_bullet_x = circle_x2
rear_bullet_y = (circle_y1 + circle_y2) / 2 - (height_of_bullet / 2)


#function of circle
def drawCircle():
    global circle_x1, circle_y1, circle_x2, circle_y2, circle_diameter, width, height

    draw = ImageDraw.Draw(image)
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    draw.arc([(circle_x1, circle_y1),(circle_x2, circle_y2)],0,360,fill='red', width=10)

def moveCircle(x_mvt, y_mvt):
    global circle_x1, circle_y1, circle_x2, circle_y2, circle_diameter,circle_mvt, width, height

    if ((circle_x1 + x_mvt >= 0 and circle_x1 + x_mvt <= width - circle_diameter)
        and (circle_y1 + y_mvt >= 0 and circle_y1 + y_mvt <= height - circle_diameter)):
        circle_x1 += x_mvt; circle_x2 += x_mvt;
        circle_y1 += y_mvt; circle_y2 += y_mvt;


#function of bullet
def shootFrontBulletAt(front_bullet_x, front_bullet_y):
    global  width_of_bullet, height_of_bullet, bullet_speed, circle_mvt

    while(front_bullet_x > 0):
        if not button_U.value:
            moveCircle(0,-circle_mvt)

        if not button_D.value:
            moveCircle(0,circle_mvt)
        
        if not button_L.value:
            moveCircle(-circle_mvt,0)

        if not button_R.value:
            moveCircle(circle_mvt,0)

        drawCircle()
        draw.rectangle((front_bullet_x, front_bullet_y, 
            front_bullet_x - width_of_bullet , front_bullet_y + height_of_bullet), outline='blue', fill='blue', width=2)
        disp.image(image)
        front_bullet_x -= bullet_speed
        
def shootRearBulletAt(rear_bullet_x, rear_bullet_y):
    global  width_of_bullet, height_of_bullet, bullet_speed, circle_mvt

    while(rear_bullet_x < width):
        if not button_U.value:
            moveCircle(0,-circle_mvt)

        if not button_D.value:
            moveCircle(0,circle_mvt)
        
        if not button_L.value:
            moveCircle(-circle_mvt,0)

        if not button_R.value:
            moveCircle(circle_mvt,0)

        drawCircle()
        draw.rectangle((rear_bullet_x, rear_bullet_y, 
            rear_bullet_x + width_of_bullet , rear_bullet_y + height_of_bullet), outline='blue', fill='blue', width=2)
        disp.image(image)
        rear_bullet_x += bullet_speed


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


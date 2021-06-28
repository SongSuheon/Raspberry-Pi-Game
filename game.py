import time
from colorsys import hsv_to_rgb
import board
from digitalio import DigitalInOut, Direction
from PIL import Image, ImageDraw, ImageFont
import adafruit_rgb_display.st7789 as st7789

import hero
import enemy
import missile
import coin
import utility as u

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
canvas = Image.new("RGBA", (width, height),(255,255,255,0))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(canvas)

# Get opening img and font
st_bgd = Image.open("./image/opening.png").convert("RGBA")
st_bgd = st_bgd.resize((width, height))
st_fnt1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 25)
st_fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 17)

# Get ingame img and font
in_bgd = Image.open("./image/background.png").convert("RGBA")
in_fnt = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
score = None
life = None

# Get ending img and font
end_bgd = Image.open('./image/black.png').convert("RGBA")
end_fnt1 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
end_fnt2 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 30)
end_fnt3 = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
dancing_cartman = Image.open('./image/dancing2.gif','r')
img_list = []

try:
    while 1:
        img = dancing_cartman.copy()
        img = img.convert("RGBA")
        img = img.resize((100,100))
        img_list.append(img)
        dancing_cartman.seek(len(img_list))
except EOFError:
    pass

# show start screen
def show_st_screen():
    blink = 1 # if blink is even number make text blink
    
    while True:
        u.clear_all(canvas, st_bgd)
        canvas.paste(st_bgd, (0, 0))
        draw.text((7,0), "Doge To The Mars", font = st_fnt1)
        if blink % 2 == 0:
            draw.text((25,180), "Press Any Key to Start", font = st_fnt2)
        disp.image(canvas)
        
        if ((not button_U.value) or (not button_D.value) or (not button_L.value) or
        (not button_R.value) or (not button_A.value) or (not button_B.value)):
                break
        blink += 1
        
        time.sleep(0.01)

# show ingame screen
def show_ingame_screen():
    global score
    score = 0
    life = 3
    is_over = False

    h = hero.ElonMusk()
    e = enemy.EnemyList()
    m = missile.TweetList()
    c = coin.DogeList()

    while True:
        u.clear_all(canvas, in_bgd)
            
        draw.text((175,20), "coin: " + str(score), font = in_fnt)
        draw.text((175,40), "life: " + str(life), font = in_fnt)
                      
        if not button_L.value:
            h.left()
        elif not button_R.value:
            h.right()
        if not button_A.value: # jump
            if h.is_jump == False:
                h.is_jump = True
        if not button_B.value: # shoot
            x = h.x + h.width
            y = h.y + 50
            m.append(x, y)
                
        if h.is_jump == True:
            h.jump()

        h.draw(canvas)

        e.append()
        e.move()

        m.move()
        
        c.append()
        c.move()
            
        # score
        for i in c.doge_list:
            if u.crash(i, h) == True:
                c.rm_list.append(i)
                score += 1

        # tweet remove enemy
        for i in m.tweet_list:
            for j in e.enemy_list:
                if u.crash(i, j) == True:
                    if (i not in e.rm_list) and (j not in m.rm_list):
                        m.rm_list.append(i)
                        e.rm_list.append(j)
                        
        # crash with enemy (condition of game over)
        for i in e.enemy_list:
            if u.crash(i, h) == True:
                life -= 1
                e.rm_list.append(i)
                draw.text((i.x, i.y), "CRASH" , font = in_fnt, fill = 'red')
            if life == 0: 
                is_over = True

        if is_over == True:
            break
                        
        e.remove()
        e.draw(canvas)

        m.remove()
        m.draw(canvas)

        c.remove()
        c.draw(canvas)
                    
        disp.image(canvas)
        time.sleep(0.01)

# show ending screen        
def show_end_screen():
    is_restart = False
    while True:
        u.clear_all(canvas, end_bgd)
        draw.text((0,120), "Your Score: " + str(score), font = end_fnt1)
        draw.text((0,150), "GAME OVER", font = end_fnt2, fill = 'red')
        draw.text((0,180), "Press up key to retry", font = end_fnt3, fill = 'blue')
        for i in img_list:
            canvas.paste(i,(70,0),i)
            disp.image(canvas)
        if not button_U.value:
            is_restart = True

        if is_restart == True:
            break

        time.sleep(0.01)
    

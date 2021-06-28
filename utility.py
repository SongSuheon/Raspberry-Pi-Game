from PIL import Image, ImageDraw

def clear_all(canvas, background):
    draw = ImageDraw.Draw(canvas)
    background = background.resize((240,240))
    canvas.paste(background,(0,0))

def crash(obj1, obj2):
    x1 = obj1.x; y1 = obj1.y; w1 = obj1.width; h1 = obj1.height;
    x2 = obj2.x; y2 = obj2.y; w2 = obj2.width; h2 = obj2.height;

    if(x1 < x2 + w2 and x1 + w1 > x2 and y1 + h1 > y2 and y1 < y2 + h2):
        return True
    else:
        return False

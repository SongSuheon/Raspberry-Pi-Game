from PIL import Image

twitter = Image.open("./image/t5.png").convert("RGBA")
twitter = twitter.resize((20, 20))

class Tweet:
    def __init__(self, x, y):
        self.width = 20
        self.height = 20
        self.x = x
        self.y = y
        self.dx = 20 # x-axis speed of tweet
    def right(self):
        if self.x + self.dx <= 240:
            self.x += self.dx
    def draw(self, canvas):
        global twitter
        canvas.paste(twitter, (self.x, self.y), twitter)
        
class TweetList:
    def __init__(self):
        self.tweet_list = []
        self.rm_list = []
    def append(self, x, y):
        t = Tweet(x, y)
        self.tweet_list.append(t)
    def move(self):
        for i in self.tweet_list:
            i.right()
            if i.x >= 240:
                self.rm_list.append(i)
    def draw(self, canvas):
        for i in self.tweet_list:
            i.draw(canvas)
    def remove(self):
        for i in self.rm_list:
            if i in self.tweet_list:
                self.tweet_list.remove(i)
        self.rm_list.clear()


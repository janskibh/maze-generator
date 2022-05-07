from PIL import Image, ImageDraw
import random
from datetime import datetime, date
import os
#import seaborn
#import os
#from instabot import Bot

#seaborn.set_theme()
#colors = seaborn.hls_palette(10, l=.5, s=.8).as_hex()

path = os.getcwd()

palettes = [
    ["#2d363d","#b32e49","#8f7b62","#f25b22","#e9d84c"], #orange
    ["#e9d84c","#d21e2d","#d2691e","#eab903","#f7f1cf"], #yellow/red
    ["#15174f","#1639bf","#6749dc","#ad51f3","#f64cd5"], #purple/blue
    ["#f3f6f4","#6497b1","#005b96","#03396c","#011f4b"], #blue
    ["#859382","#3e4839","#f4f1f0","#678044","#131312"], #green/grey
    ["#f4cccc","#b6d7a8","#ffe599","#6aa84f","#38761d"], #light-green
    ["#d7f0ed","#93ede1","#4acbbb","#247674","#1e4d66"], #light-blue
    ["#64f187","#104b6b","#eeeeeb","#18194e","#e8d7ef"], #white/green/blue
    #["#25020d","#180b3c","#3b0404","#240b3c","#2f061e"], #dark-blue/dark-red
    #["#5b167e","#41167e","#27167e","#161f7e","#061183"], #purple
    ["#061106","#133412","#1f561d","#2c7929","#4c9949"], #green/black
    ["#c86e9d","#efb2d1","#cf3a88","#e0d0d8","#1d0813"], #pink
    #["#f3c5c5","#ffdcdc","#fff1c4","#d5e8ea","#bfd0e3"], #pink/blue creme
    ["#efcd65","#937737","#efc40e","#c7cc58","#c9b218"], #yellow/green
    ["#ffe599","#2e1114","#64485c","#83677b","#adadad"], #purple/grey
    ["#e2a36b","#ffa500","#7c0d0e","#26453e","#f3f6f4"], #brey/red/yellow
]
#palette = ["#e2a36b","#ffa500","#7c0d0e","#26453e","#f3f6f4"]
palette_id = int(input(f"Map number : (1, {len(palettes)}) : ")) - 1

map_nb = int(palette_id) + 1

palette =  palettes[int(palette_id)] #palettes[random.randint(0,len(palettes) - 1)]

def random_color(): 
    return (palette[random.randint(0,len(palette) - 1)])


def generate():
    print("Generating image...")

    now = datetime.now()
    today = date.today()


    class IMG():
        width = 320
        height = 240
        bg = (10,10,10)
        padding = 0
        name = now.strftime("%H%M%S")

    class Squares():
        number = 100
        size = 100

    squares = []

    image = Image.new(
        "RGB",
        size=(IMG.width, IMG.height),
        color=IMG.bg
    )
    
    draw = ImageDraw.Draw(image)

    size = Squares.size

    for i in range(Squares.number):
        squares.append(
            [
                (random.randint(IMG.padding, IMG.width - IMG.padding),
                random.randint(IMG.padding, IMG.height - IMG.padding)),
                size
            ]
        )
        size -= round(Squares.size/Squares.number)

    for point in squares:
        draw.rectangle(((point[0][0] - point[1]/2, point[0][1] - point[1]/2), (point[0][0] + point[1]/2, point[0][1] + point[1]/2)), fill=(random_color()))
    
    """if not os.path.isdir(os.path.abspath("images")+"/"+today.strftime("%Y")):
        os.mkdir(os.path.abspath("images")+"/"+today.strftime("%Y"))
    
    if not os.path.isdir(os.path.abspath("images")+"/"+today.strftime("%Y")+"/"+today.strftime("%m")):
        os.mkdir(os.path.abspath("images")+"/"+today.strftime("%Y")+"/"+today.strftime("%m"))
    
    if not os.path.isdir(os.path.abspath("images")+"/"+today.strftime("%Y")+"/"+today.strftime("%m")+"/"+today.strftime("%d")):
        os.mkdir(os.path.abspath("images")+"/"+today.strftime("%Y")+"/"+today.strftime("%m")+"/"+today.strftime("%d"))

    path = os.path.abspath("images")+"/"+today.strftime("%Y")+"/"+today.strftime("%m")+"/"+today.strftime("%d")+"/"
"""
    image.save(f"{path}\maps\RandomMap{map_nb}.png")

    print("Done !")

if __name__ == "__main__":
    generate()

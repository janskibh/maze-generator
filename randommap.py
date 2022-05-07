import json
import random
import os
from prettytable import PrettyTable
import math

os.system('cls' if os.name == 'nt' else 'clear')

path = os.getcwd()


m = open(path + "/map.json", 'r')
data = json.loads(m.read())

si = 0

cubes = []

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

palette_id = int(input(f"Map number : (1, {len(palettes)}) : ")) - 1

map_size = int(input("Map size : "))
map_height = int(input("Map height : "))
block_height = int(input("Block height : "))

print(f"Map size : {map_size} x {map_size}, Map height : {map_height}")

data["camPos"] = [0, map_height, 0, 0, False, 0]

map_nb = int(palette_id) + 1

palette = palettes[int(palette_id)]

data["name"] = "RandomMap" + str(map_nb)
data["welMsg"] = f"Welcome to RandomMap{str(map_nb)}, a randomly generated map by Xenoy_"

sp = round(map_size/3)

p = [[sp * -1, map_height + 2, sp * -1], [sp, map_height + 2, sp * -1], [sp, map_height + 2, sp], [sp * -1, map_height + 2, sp]]
xyz = [20,block_height,20]
bxyz = [12,18,12]

for d, i in enumerate(p):
    data["objects"].append({"p": i, "t": 5, "ci": si, "si": si})
    data["colors"].append(palette[random.randint(0, len(palette) - 1)].upper())
    data["spawns"].append([i[0], i[1] + block_height, i[2], 0, d, 0])
    for k in xyz:
        data["xyz"].append(k)
    si += 1

for i in p:
    data["objects"].append({"p": [i[0], i[1] + block_height, i[2], 0, d, 0], "t": 5, "o": 0.3, "ci": si, "si": si})
    data["colors"].append(palette[random.randint(0, len(palette) - 1)].upper())
    for l in bxyz:
        data["xyz"].append(l)
    si += 1

u = 2

class Position:
    max_xz = round(map_size / (2 * u))
    min_xz = round(0/u)
    #max_y = round(-20/u)
    #min_y = round(-80/u)

class Size:
    max_xz = round(map_size/u * 0.2)
    min_xz = round(round(math.sqrt(map_height))/u)
    #max_y = round(20/u)
    #min_y = round(5/u)

for i in range(map_height):
    size = random.randint(Size.min_xz * u, Size.max_xz * u)
    #height = random.randint(Size.min_y * u, Size.max_y * u)

    p = [
        random.randint(Position.min_xz * u, Position.max_xz * u) * random.choice([-1, 1]),
        #random.randint(Position.min_y * u, Position.max_y * u),
        i,
        random.randint(Position.min_xz * u, Position.max_xz * u) * random.choice([-1, 1])
    ]
    xyz = [size,block_height,size]

    '''
    if len(cubes) > 1:
        for c in cubes:
            if p[1] + height == c[5][1]:
                height += 1
                print(f"Changed height for cube {si} ({height - 1} => {height}) [{c[0]}]")
    '''

    cubes.append([si, size, block_height, p, [p[0] + size/2, p[1], p[2] + size/2], [p[0] - size/2, p[1] + block_height, p[2] - size/2]])
    data["objects"].append({"p": p, "t": 5, "ci": si, "si": si})
    color = palette[random.randint(0, len(palette) - 1)].upper()
    data["colors"].append(color)
    for i in xyz:
        data["xyz"].append(i)

    si += 1

    #print(f"\033[37m ID = {si} \033[37m | Position : \033[32m {str(p)} \033[37m | Size : \033[33m {size} \033[37m | Color : \033[31m {color} \033[37m")

with open(path + f"/maps/RandomMap{map_nb}.json", "w") as m:
    json.dump(data, m)
    m.close()
    print(f"RandomMap{map_nb} successfully generated")
    print("A randomly generated map")

cubetable = PrettyTable()
cubetable.field_names = ["ID", "Size", "Height", "Position", "From", "To"]

for cube in cubes:
    cubetable.add_row([f"\033[34m{cube[0]}\033[37m", f"\033[32m{cube[1]} x {cube[1]}\033[37m", f"\033[33m{cube[2]}\033[37m", f"\033[31m{cube[3]}\033[37m", f"\033[36m{cube[4]}\033[37m", f"\033[36m{cube[5]}\033[37m"])

#print(cubetable)

#json.dump(json_string, mapfile)
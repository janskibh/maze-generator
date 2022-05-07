import json
import random
import time
import os
import math
from PIL import Image, ImageDraw


os.system('cls' if os.name == 'nt' else 'clear')

dossier = "D:/DATA JAN/_Python/krunker-map"

m = open(dossier + "/map.json", 'r')
data = json.loads(m.read())

cubes = []
darkwood_color = 0
lightwood_color = 1
dirt_color = 2
wall_color = 3
border_color = 4

objects_nbr = 0


data['colors'].append("#5D5B5B")
data['colors'].append("#B0B0B0")
data['colors'].append("#A8AFC3")
data['colors'].append("#797575")
data['colors'].append("#444444")

choice_method = int(input("Auto options ( No : 0, Yes : 1) : "))

if choice_method == 1:
    cell_width = 50
    map_size = 50 * cell_width
    nb_towers = 6
    nb_spawns = 6
    border_height = 80
    wall_height = 60
    towers_height = wall_height + 40
    wall_width = 5
    border_width = wall_width + 2
else:
    cell_width = int(input("Corridor width : "))
    map_size = int(input("Map size (cells) : ")) * cell_width
    nb_towers = int(input("Number of towers : "))
    nb_spawns = int(input("Number of spawnpoints : "))
    border_height = int(input("Borders height : "))
    wall_height = int(input("Walls height : "))
    towers_height = wall_height + 40
    wall_width = int(input("Walls_width : "))
    border_width = wall_width + 2


image_size = (1280, 660)

wall_list = [[],[]]

for i in wall_list:
    for x in range(1, round(map_size / cell_width) + 1):
        for y in range(1, round(map_size / cell_width) + 1):
            i.append((x, y))

'''for i, u in enumerate(wall_list):
    print(i)
    print(wall_list[i][0])
    print(wall_list[i][len(wall_list[i]) - 1])'''

#print(wall_list)

image = Image.new(
    "RGB",
    size = image_size,
    color = (255,255,255)
)

padding = image_size[1] / (map_size / cell_width)
pixel_size = round((image_size[1] - padding * 2) / (map_size / cell_width))

maze_pict = map_size / cell_width * pixel_size

draw = ImageDraw.Draw(image)

xyz = [map_size, 5, map_size]
for i in xyz:
    data['xyz'].append(i)
data['objects'].append({"p": [map_size/2, -5, map_size/2],"t": 1, "ci": dirt_color, "si": 0})
data['objects'].append({"p": [map_size/2, -10, map_size/2],"t": 1, "ci": dirt_color, "si": 0})


walls_1 = [
    [map_size/2, 0, 0], 
    [map_size/2, 0, map_size], 
]
    
walls_2 = [
    [map_size, 0, map_size / 2],
    [0, 0, map_size/2]
]

sizes = [[map_size, border_height, border_width], [border_width, border_height, map_size]]

for s in range(2):
    for i in sizes[int(s)]:
        data['xyz'].append(i)

print("Creating borders...")

for p in walls_1:
    data['objects'].append({"p": p, "t": 11,"bo": 1, "ci": border_color, "si": 1})
    objects_nbr += 1

for p in walls_2:
    data['objects'].append({"p": p, "t": 11,"bo": 1, "ci": border_color, "si": 2})
    objects_nbr +=1

print("Generating spawns...")

decalage = image_size[0] / 2 - maze_pict / 2 - padding/2 - pixel_size
for i in range(nb_spawns):
    x = random.randint(2, map_size / cell_width - 2) * cell_width + cell_width/2
    y = random.randint(2, map_size / cell_width - 2) * cell_width + cell_width/2
    data['spawns'].append([
        x,
        0,
        y,
        0,random.randint(0,4),0
    ])
    position_x = x / cell_width * pixel_size + decalage + pixel_size/2
    position_y = y / cell_width * pixel_size - pixel_size + 2 * pixel_size + 2

    draw.rectangle(
        (
            (position_x + round(pixel_size / 5), position_y + round(pixel_size / 5) - pixel_size / 2), 
            (position_x + pixel_size - round(pixel_size / 5), position_y + pixel_size/2 - round(pixel_size / 5))
        ), 
        fill=(0,200,0)
    )

x = 0
y = 0

grid = []
stack_list = []
closed_list = []

path = {}

#Width, Height = map_size, map_size

print(f"Map size : {map_size} x {map_size}")

data["camPos"] = [map_size/2, wall_height + 20, map_size/2, 0, False, 0]

map_Name = input("Map Name : ")

data["name"] = map_Name
data["welMsg"] = "Welcome to " + map_Name

time.sleep(2)

def build_grid(x, y):
    for n in range(round(map_size / cell_width)):
        x = cell_width
        y = y + cell_width
        for m in range(round(map_size / cell_width)):
            grid.append((x, y))
            x = x + cell_width
    #print(grid)

def Maze(x, y, data):
    stack_list.append((x, y))
    closed_list.append((x, y))

    walls = 0

    print("Generating maze...")

    while len(stack_list) > 0:
        #print((x, y))
        cell = []

        if(x + cell_width, y) not in closed_list and (x + cell_width, y) in grid:
            cell.append("West")

        if (x - cell_width, y) not in closed_list and (x - cell_width, y) in grid:
            cell.append("East")

        if (x , y + cell_width) not in closed_list and (x , y + cell_width) in grid:
            cell.append("North")

        if (x, y - cell_width) not in closed_list and (x , y - cell_width) in grid:
            cell.append("South") 

        if len(cell) > 0:
            wall_px = 1

            current_cell = (random.choice(cell))
            
            if current_cell == "East":
                wx, wy = round(x / cell_width) - 1, round(y / cell_width)

                if (wx, wy) in wall_list[0]:
                    #print(f"destroyed East wall at {(wx, wy)} , {x}, {y}")
                    wall_list[0].remove((wx, wy))
                path[(x - cell_width, y)] = x, y
                x = x - cell_width
                '''decalage = image_size[0] / 2 - maze_pict / 2

                position_x = x / cell_width * pixel_size + decalage
                position_y = y / cell_width * pixel_size
                draw.rectangle(
                    (
                        (position_x + pixel_size, position_y), 
                        (position_x + pixel_size + wall_px, position_y + pixel_size)
                    ), 
                    fill=(0,0,0)
                )
                
                data['objects'].append({"p": [x + cell_width/2, 0, y],"t": 11, "ci": wall_color, "si": 3})
                walls += 1'''

                '''for wall in v_walls[0]:
                    if wall == (x, y):
                        v_walls[0].remove(wall)'''

                closed_list.append((x, y))
                stack_list.append((x, y))


            elif current_cell == "West":
                wx, wy = round(x / cell_width), round(y / cell_width)

                if (wx, wy) in wall_list[0]:
                    #print(f"destroyed West wall at {(wx - 1, wy)} , {x}, {y}")
                    wall_list[0].remove((wx, wy))
                path[(x + cell_width, y)] = x, y
                x = x + cell_width
                '''decalage = image_size[0] / 2 - maze_pict / 2

                position_x = x / cell_width * pixel_size + decalage
                position_y = y / cell_width * pixel_size
                draw.rectangle(
                    (
                        (position_x, position_y), 
                        (position_x + wall_px, position_y + pixel_size)
                    ), 
                    fill=(0,0,0)
                )
                
                data['objects'].append({"p": [x - cell_width/2, 0, y],"t": 11, "ci": wall_color, "si": 3})'''
                '''for wall in v_walls[1]:
                    if wall == (x, y):
                        v_walls[1].remove(wall)'''

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "North":
                wx, wy = round(x / cell_width), round(y / cell_width) + 1

                if (wx, wy) in wall_list[1]:
                    #print(f"destroyed North wall at {(wx, wy)} , {x}, {y}")
                    wall_list[1].remove((wx, wy))
                path[(x , y + cell_width)] = x, y
                y = y + cell_width
                '''decalage = image_size[0] / 2 - maze_pict / 2

                position_x = x / cell_width * pixel_size + decalage
                position_y = y / cell_width * pixel_size
                draw.rectangle(
                    (
                        (position_x, position_y - pixel_size), 
                        (position_x + pixel_size, position_y + wall_px - pixel_size)
                    ), 
                    fill=(0,0,0)
                )
                
                data['objects'].append({"p": [x, 0, y + cell_width/2],"t": 11, "ci": wall_color, "si": 4})
                walls += 1'''

                '''for wall in h_walls[0]:
                    if wall == (x, y):
                        h_walls[0].remove(wall)'''

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "South":
                wx, wy = round(x / cell_width), round(y / cell_width)
                if (wx, wy) in wall_list[1]:
                    #print(f"destroyed South wall at {(wx, wy + 1)} , {x}, {y}")
                    wall_list[1].remove((wx, wy))

                path[(x , y - cell_width)] = x, y
                y = y - cell_width
                '''decalage = image_size[0] / 2 - maze_pict / 2

                position_x = x / cell_width * pixel_size + decalage
                position_y = y / cell_width * pixel_size
                draw.rectangle(
                    (
                        (position_x, position_y + pixel_size - pixel_size), 
                        (position_x + pixel_size, position_y + pixel_size + wall_px - pixel_size)
                    ), 
                    fill=(0,0,0)
                )

                data['objects'].append({"p": [x, 0, y - cell_width/2],"t": 11, "ci": wall_color, "si": 4})
                walls += 1'''
                '''for wall in h_walls[1]:
                    if wall == (x, y):
                        h_walls[1].remove(wall)'''

                closed_list.append((x, y))
                stack_list.append((x, y))

        else:
            x, y = stack_list.pop()

    #print(f"Number of walls : {walls}")
    decalage = image_size[0] / 2 - maze_pict / 2 - padding/2 - pixel_size
    draw.rectangle(
        (
            (decalage + pixel_size - 2, pixel_size - 2), 
            (maze_pict + decalage + pixel_size + 2, maze_pict + pixel_size + 2)
        ), 
        width = 8,
        outline=(0,0,0)
    )

x, y = cell_width, cell_width
build_grid(cell_width, 0)
Maze(x, y, data)

print("Making walls...")

xyz = [cell_width, wall_height, wall_width] #horizontal
for i in xyz:
    data['xyz'].append(i)

xyz = [wall_width, wall_height, cell_width] #vertical
for i in xyz:
    data['xyz'].append(i)

for w in wall_list[0]: #vertical
    data['objects'].append({"p": [w[0] * cell_width, 0, w[1] * cell_width - cell_width/2],"t": 11, "ci": wall_color, "si": 4})
    draw.rectangle(((decalage + w[0] * pixel_size + pixel_size, w[1] * pixel_size), (decalage + w[0] * pixel_size + pixel_size + 4, w[1] * pixel_size + pixel_size)), fill = (0,0,0))
for w in wall_list[1]: #horizontal
    data['objects'].append({"p": [w[0] * cell_width - cell_width/2, 0, w[1] * cell_width - cell_width],"t": 11, "ci": wall_color, "si": 3})
    draw.rectangle(((decalage + w[0] * pixel_size, w[1] * pixel_size), (decalage + w[0] * pixel_size + pixel_size, w[1] * pixel_size + 4)), fill = (0,0,0))


#draw.rectangle(((10,10), (100,12)), fill = (255,0,0))
#draw.rectangle(((10,10), (12,100)), fill = (0,0,255))

xyz = [4,25,4,2,towers_height - 2,4,40,2,10,10,2,20,40,3,40,10,towers_height,10,30,3,30]

for i in xyz:
    data["xyz"].append(i)

towers = []

print("Generating towers...")

for i in range(nb_towers):
    x = (random.randint(2, map_size / cell_width - 2) * cell_width + cell_width/2)
    y = (random.randint(2, map_size / cell_width - 2) * cell_width + cell_width/2)

    position_x = x / cell_width * pixel_size + decalage + pixel_size / 2
    position_y = y / cell_width * pixel_size - pixel_size + pixel_size / 2 + pixel_size + 2

    draw.rectangle(
        (
            (position_x + round(pixel_size / 5), position_y + round(pixel_size / 5)), 
            (position_x + pixel_size - round(pixel_size / 5), position_y + pixel_size - round(pixel_size / 5))
        ), 
        fill=(148, 33, 10)
    )

    towers.append((x/cell_width - 0.5, y/cell_width - 0.5))

    objects = [
        {"p":[x - 16, towers_height - 24,y - 16],"t":2,"ci":0,"si":5},
        {"p":[x - 5, 0,y],"i":3,"t":2,"d":2,"si":6},
        {"p":[x + 5, 0,y],"i":3,"t":2,"si":6},
        {"p":[x, 0, y + 5],"i":3,"t":2,"d":1,"si":6},
        {"p":[x, 0, y - 5],"i":3,"t":2,"d":3,"si":6},
        {"p":[x, towers_height - 25, y + 15],"t":2,"ci":1,"si":7},
        {"p":[x, towers_height - 25, y - 15],"t":2,"ci":1,"si":7},
        {"p":[x - 15, towers_height - 25, y],"t":2,"ci":1,"si":8},
        {"p":[x + 15, towers_height - 25, y],"t":2,"ci":1,"si":8},
        {"p":[x, towers_height, y],"t":2,"ci":1,"si":9},
        {"p":[x, 0, y],"t":2,"ci":0,"si":10},
        {"p":[x - 16, towers_height - 24, y + 16],"t":2,"ci":0,"si":5},
        {"p":[x + 16, towers_height - 24, y - 16],"t":2,"ci":0,"si":5},
        {"p":[x + 16, towers_height - 24, y + 16],"t":2,"ci":0,"si":5},
        {"p":[x, towers_height + 3, y],"t":2,"ci":1,"si":11}
    ]

    for o in objects:
        data['objects'].append(o)
        objects_nbr += 1

print("Towers : ", towers)

#print(grid, "\n")
#print(stack_list, "\n")
#print(closed_list, "\n")

#datastr = str(data).replace("'", '"')

#print(datastr.replace("False", "false"))

with open(f"{dossier}/maps/RandomMaze/{map_Name}.json", "w") as m:
    json.dump(data, m)
    m.close()

print("Maze successfully generated")
print(f"number of objects : {str(objects_nbr)}")
image.save(f"D:\DATA JAN\_Python\krunker-map\maps\RandomMaze\{map_Name}_thumb.png")
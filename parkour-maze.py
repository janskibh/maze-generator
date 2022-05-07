import json
import random
import time
import os
import math
from PIL import Image, ImageDraw


os.system('cls' if os.name == 'nt' else 'clear')

dossier = os.getcwd()

m = open(dossier + "/maze_base.json", 'r')
data = json.loads(m.read())

cubes = []

objects_nbr = 0

ci_start = len(data['colors'])
si_start = len(data['xyz']) / 3
print(si_start)

darkwood_color = ci_start
lightwood_color = ci_start + 1
wall_color = ci_start + 2
black = ci_start + 3

data['colors'].append("#5D5B5B")
data['colors'].append("#B0B0B0")
#data['colors'].append("#A8AFC3")
data['colors'].append("#797575")
data['colors'].append("#000000")
#data['colors'].append("#444444")

cell_width = 80
map_size = 60 * cell_width
nb_towers = 12
nb_bouncepads = 15
nb_portals = 15
wall_height = 120
towers_height = wall_height + 40
wall_width = 10
wall_px = 3


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

padding = 2 * image_size[1] / (map_size / cell_width)

pixel_size = round((image_size[1] - padding * 2) / (map_size / cell_width))

maze_pict = map_size / cell_width * pixel_size

draw = ImageDraw.Draw(image)

decalage = image_size[0] / 2 - maze_pict / 2 - padding/2

x = 0
y = 0

grid = []
stack_list = []
closed_list = []

path = {}

#Width, Height = map_size, map_size

print(f"Map size : {map_size} x {map_size}")

map_Nbr = input("Map Number : ")

data['objects'].append({"p":[187,50,-96],"i":30,"r":[1.57,0,1.57],"st":f"Maze_{map_Nbr}","sc":"#FFFFFF","bv":1,"sf":116,"sa":1,"si":9})
data["name"] = "Maze_" + map_Nbr
data["welMsg"] = "Welcome to Maze_" + map_Nbr

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

            current_cell = (random.choice(cell))
            
            if current_cell == "East":
                wx, wy = round(x / cell_width) - 1, round(y / cell_width)

                if (wx, wy) in wall_list[0]:
                    #print(f"destroyed East wall at {(wx, wy)} , {x}, {y}")
                    wall_list[0].remove((wx, wy))
                path[(x - cell_width, y)] = x, y
                x = x - cell_width

                closed_list.append((x, y))
                stack_list.append((x, y))


            elif current_cell == "West":
                wx, wy = round(x / cell_width), round(y / cell_width)

                if (wx, wy) in wall_list[0]:
                    #print(f"destroyed West wall at {(wx - 1, wy)} , {x}, {y}")
                    wall_list[0].remove((wx, wy))
                path[(x + cell_width, y)] = x, y
                x = x + cell_width

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "North":
                wx, wy = round(x / cell_width), round(y / cell_width) + 1

                if (wx, wy) in wall_list[1]:
                    #print(f"destroyed North wall at {(wx, wy)} , {x}, {y}")
                    wall_list[1].remove((wx, wy))
                path[(x , y + cell_width)] = x, y
                y = y + cell_width

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "South":
                wx, wy = round(x / cell_width), round(y / cell_width)
                if (wx, wy) in wall_list[1]:
                    #print(f"destroyed South wall at {(wx, wy + 1)} , {x}, {y}")
                    wall_list[1].remove((wx, wy))

                path[(x , y - cell_width)] = x, y
                y = y - cell_width

                closed_list.append((x, y))
                stack_list.append((x, y))

        else:
            x, y = stack_list.pop()

    #print(f"Number of walls : {walls}")

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
    data['objects'].append({"p": [w[0] * cell_width, 0, w[1] * cell_width - cell_width/2],"t": 11, "ci": wall_color, "si": si_start + 1})
    draw.rectangle(((decalage + w[0] * pixel_size + pixel_size, w[1] * pixel_size + padding), (decalage + w[0] * pixel_size + pixel_size + wall_px, w[1] * pixel_size + pixel_size + wall_px + padding)), fill = (0,0,0))
for w in wall_list[1]: #horizontal
    data['objects'].append({"p": [w[0] * cell_width - cell_width/2, 0, w[1] * cell_width - cell_width],"t": 11, "ci": wall_color, "si": si_start})
    draw.rectangle(((decalage + w[0] * pixel_size, w[1] * pixel_size + padding), (decalage + w[0] * pixel_size + pixel_size + wall_px, w[1] * pixel_size + wall_px + padding)), fill = (0,0,0))

xyz = [4,25,4,2,towers_height - 2,4,40,2,10,10,2,20,40,3,40,10,towers_height,10,30,3,30]

for i in xyz:
    data["xyz"].append(i)

print("Generating towers...")

for i in range(nb_towers):
    x = (random.randint(0, map_size / cell_width - 2) * cell_width + cell_width/2)
    y = (random.randint(0, map_size / cell_width - 2) * cell_width + cell_width/2)

    position_x = x / cell_width * pixel_size + decalage + pixel_size / 2
    position_y = y / cell_width * pixel_size - pixel_size + pixel_size / 2 + pixel_size + 2

    draw.rectangle(
        (
            (position_x + round(pixel_size / 10) + 2, position_y + round(pixel_size / 10) + padding), 
            (position_x + pixel_size - round(pixel_size / 10) + 2, position_y + pixel_size - round(pixel_size / 10) + padding)
        ), 
        fill=(255, 55, 10)
    )

    objects = [
        {"p":[x - 16, towers_height - 24,y - 16],"t":2,"ci":darkwood_color,"si":si_start + 2},
        {"p":[x - 5, 0,y],"i":3,"t":2,"d":2,"si":si_start + 3},
        {"p":[x + 5, 0,y],"i":3,"t":2,"si":si_start + 3},
        {"p":[x, 0, y + 5],"i":3,"t":2,"d":1,"si":si_start + 3},
        {"p":[x, 0, y - 5],"i":3,"t":2,"d":3,"si":si_start + 3},
        {"p":[x, towers_height - 25, y + 15],"t":2,"ci":lightwood_color,"si":si_start + 4},
        {"p":[x, towers_height - 25, y - 15],"t":2,"ci":lightwood_color,"si":si_start + 4},
        {"p":[x - 15, towers_height - 25, y],"t":2,"ci":lightwood_color,"si":si_start + 5},
        {"p":[x + 15, towers_height - 25, y],"t":2,"ci":lightwood_color,"si":si_start + 5},
        {"p":[x, towers_height, y],"t":2,"ci":lightwood_color,"si":si_start + 6},
        {"p":[x, 0, y],"t":2,"ci":darkwood_color,"si":si_start + 7},
        {"p":[x - 16, towers_height - 24, y + 16],"t":2,"ci":darkwood_color,"si":si_start + 2},
        {"p":[x + 16, towers_height - 24, y - 16],"t":2,"ci":darkwood_color,"si":si_start + 2},
        {"p":[x + 16, towers_height - 24, y + 16],"t":2,"ci":darkwood_color,"si":si_start + 2},
        {"p":[x, towers_height + 3, y],"t":2,"ci":lightwood_color,"si":si_start + 8}
    ]

    for o in objects:
        data['objects'].append(o)
        objects_nbr += 1

print("Generating bounce pads...")

xyz = [10,0.5,10]
for i in xyz:
    data['xyz'].append(i)

for i in range(nb_bouncepads):
    x = (random.randint(0, map_size / cell_width - 2) * cell_width + cell_width/2)
    y = (random.randint(0, map_size / cell_width - 2) * cell_width + cell_width/2)
    position_x = x / cell_width * pixel_size + decalage + pixel_size / 2
    position_y = y / cell_width * pixel_size - pixel_size + pixel_size / 2 + pixel_size + 2

    draw.rectangle(
        (
            (position_x + round(pixel_size / 10) + 2, position_y + round(pixel_size / 10) + padding), 
            (position_x + pixel_size - round(pixel_size / 10) + 2, position_y + pixel_size - round(pixel_size / 10) + padding)
        ), 
        fill=(19, 222, 237)
    )
    data['objects'].append({"p":[x,0,y],"i":46,"bm":2.3,"si":si_start + 9})

print("Generating portals...")

xyz = [12,20,3,2,20,3,16,2,3]
for i in xyz:
    data['xyz'].append(i)

xyz = [3,20,12,3,20,2,3,2,16]
for i in xyz:
    data['xyz'].append(i)

channel = 0

for i in range(nb_portals):
    channel += 1
    xy = []
    for j in range(2):
        wall = random.choice((0,1))
        position = random.choice(wall_list[wall])
        while position[0] < 2 or position[0] > map_size/cell_width - 2 or position[1] < 2 or position[1] > map_size/cell_width - 2:
            position = random.choice(wall_list[wall])
                
                
        if wall == 1:
            x = (position[0] * cell_width - cell_width/2)
            y = (position[1] * cell_width - cell_width/2 - cell_width)
        else:
            x = (position[0] * cell_width + cell_width / 2)
            y = (position[1] * cell_width - cell_width/2)
        position_x = x / cell_width * pixel_size + decalage + pixel_size / 2
        position_y = y / cell_width * pixel_size - pixel_size + pixel_size / 2 + pixel_size + 2
        xy.append((position_x + round(pixel_size / 2) + 2, position_y + round(pixel_size / 2) + padding))
        if wall == 1:
            draw.rectangle(
                (
                    (position_x + round(pixel_size / 10) + 2, position_y + pixel_size - pixel_size/2 + padding), 
                    (position_x + pixel_size - round(pixel_size / 10) + 2, position_y + pixel_size - round(pixel_size / 10) + padding)
                ), 
                fill=(21, 214, 44)
            )
        else:
            draw.rectangle(
                (
                    (position_x + pixel_size/2 + 2, position_y + round(pixel_size / 10) + padding), 
                    (position_x + round(pixel_size / 10) + 2, position_y + pixel_size - round(pixel_size / 10) + padding)
                ), 
                fill=(21, 214, 44)
            )

        if j == 1:
            draw.line(xy, fill = (21, 214, 44), width = 3)
        if wall == 1:
            objects = [
                {"p":[x, 0, y + 36],"i":27,"d":3,"fd":1,"tm":0,"ch":channel,"n":2,"m":1,"si":si_start + 10},
                {"p":[x, 0, y + 36],"l":1,"t":5,"ci":black,"si":si_start + 10},
                {"p":[x + 7, 0, y + 35],"t":11,"ci":wall_color,"si":si_start + 11},
                {"p":[x - 7, 0, y + 35],"t":11,"ci":wall_color,"si":si_start + 11},
                {"p":[x, 20, y + 35],"t":11,"ci":wall_color,"si":si_start + 12}
            ]
        else:
            objects = [
                {"p":[x - 36, 0, y],"i":27,"fd":1,"tm":0,"ch":channel,"n":2,"m":1, "si":si_start + 13},
                {"p":[x - 36, 0, y],"l":1,"t":5,"ci":black,"si":si_start + 13},
                {"p":[x - 35, 0, y + 7],"t":11,"ci":wall_color,"si":si_start + 14},
                {"p":[x - 35, 0, y - 7],"t":11,"ci":wall_color,"si":si_start + 14},
                {"p":[x - 35, 20, y],"t":11,"ci":wall_color,"si":si_start + 15},
            ]

        for o in objects:
            data['objects'].append(o)



draw.rectangle(
        (
            (decalage + pixel_size - wall_px, pixel_size - wall_px + padding), 
            (maze_pict + decalage + pixel_size + wall_px * 2, maze_pict + pixel_size + wall_px * 2 + padding)
        ), 
        width = wall_px * 2,
        outline=(0,0,0)
    )

draw.rectangle(
        (
            (decalage - 10, padding - 10), 
            (decalage + pixel_size * 2 - 2, padding + pixel_size * 2 - 2)
        ), 
        fill = (36, 65, 150)
    )

draw.rectangle(
        (
            (maze_pict + decalage + 3, maze_pict + padding + 3), 
            (maze_pict + decalage + pixel_size * 2 + 13, maze_pict + padding + pixel_size * 2 + 13)
        ), 
        fill = (227, 181, 14)
    )


with open(f"{dossier}/maps/ParkourMaze/Maze_{map_Nbr}.json", "w") as m:
    json.dump(data, m)
    m.close()

print("Maze successfully generated")
print(f"number of objects : {str(objects_nbr)}")
image.save(f"{dossier}/maps/ParkourMaze/Maze_{map_Nbr}_thumb.png")

def Path_tracker(x, y):
    position_x = x / cell_width * pixel_size + decalage + 1
    position_y = y / cell_width * pixel_size - pixel_size + pixel_size + 2
    draw.rectangle(
        (
            (position_x + round(pixel_size / 5) , position_y + padding + round(pixel_size / 5)), 
            (position_x + pixel_size - round(pixel_size / 5), position_y + pixel_size + padding - round(pixel_size / 5))
        ), 
        fill=(20, 217, 44)
    )

def path_tracer(x, y):
    Path_tracker(x,y)
    while (x, y) != (cell_width, cell_width):
        x, y = path[x, y]
        Path_tracker(x,y)

path_tracer(map_size, map_size)

image.save(f"{dossier}/maps/ParkourMaze/Maze_{map_Nbr}_solved.png")
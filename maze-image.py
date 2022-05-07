import json
import random
import time
import os
import math
from PIL import Image, ImageDraw


os.system('cls' if os.name == 'nt' else 'clear')

dossier = os.getcwd()

map_size = 60
nb_towers = 6
wall_height = 120
towers_height = wall_height + 40
wall_width = 10
wall_px = 3


image_size = (1920, 1080)

wall_list = [[],[]]

for i in wall_list:
    for x in range(1, round(map_size) + 1):
        for y in range(1, round(map_size) + 1):
            i.append((x, y))

#print(wall_list)

image = Image.new(
    "RGB",
    size = image_size,
    color = (255,255,255)
)

padding = 2 * image_size[1] / map_size

pixel_size = round((image_size[1] - padding * 2) / map_size)

maze_pict = map_size * pixel_size

draw = ImageDraw.Draw(image)

decalage = image_size[0] / 2 - maze_pict / 2 - padding/2

x = 0
y = 0

grid = []
stack_list = []
closed_list = []

path = {}

print(f"Map size : {map_size} x {map_size}")

map_Name = input("Map Number : ")

time.sleep(2)

def build_grid(x, y):
    for n in range(map_size):
        x = 1
        y += 1
        for m in range(map_size):
            grid.append((x, y))
            x += 1

def Maze(x, y):
    stack_list.append((x, y))
    closed_list.append((x, y))

    walls = 0

    print("Generating maze...")

    while len(stack_list) > 0:
        #print((x, y))
        cell = []

        if(x + 1, y) not in closed_list and (x + 1, y) in grid:
            cell.append("West")

        if (x - 1, y) not in closed_list and (x - 1, y) in grid:
            cell.append("East")

        if (x , y + 1) not in closed_list and (x , y + 1) in grid:
            cell.append("North")

        if (x, y - 1) not in closed_list and (x , y - 1) in grid:
            cell.append("South") 

        if len(cell) > 0:

            current_cell = (random.choice(cell))
            
            if current_cell == "East":
                wx, wy = x - 1, y

                if (wx, wy) in wall_list[0]:
                    wall_list[0].remove((wx, wy))
                path[(x - 1, y)] = x, y
                x = x - 1

                closed_list.append((x, y))
                stack_list.append((x, y))


            elif current_cell == "West":
                wx, wy = x, y

                if (wx, wy) in wall_list[0]:
                    wall_list[0].remove((wx, wy))
                path[(x + 1, y)] = x, y
                x = x + 1

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "North":
                wx, wy = x, y + 1

                if (wx, wy) in wall_list[1]:
                    wall_list[1].remove((wx, wy))
                path[(x , y + 1)] = x, y
                y = y + 1

                closed_list.append((x, y))
                stack_list.append((x, y))

            elif current_cell == "South":
                wx, wy = x, y
                if (wx, wy) in wall_list[1]:
                    wall_list[1].remove((wx, wy))

                path[(x , y - 1)] = x, y
                y = y - 1

                closed_list.append((x, y))
                stack_list.append((x, y))

        else:
            x, y = stack_list.pop()


x, y = 1, 1

build_grid(1, 0)
Maze(x, y)

print("Making walls...")

for w in wall_list[0]: #vertical
    draw.rectangle(((decalage + w[0] * pixel_size + pixel_size, w[1] * pixel_size + pixel_size), (decalage + w[0] * pixel_size + pixel_size + wall_px, w[1] * pixel_size + pixel_size + wall_px + pixel_size)), fill = (0,0,0))
for w in wall_list[1]: #horizontal
    draw.rectangle(((decalage + w[0] * pixel_size, w[1] * pixel_size + pixel_size), (decalage + w[0] * pixel_size + pixel_size + wall_px, w[1] * pixel_size + wall_px + pixel_size)), fill = (0,0,0))

draw.rectangle(
        (
            (decalage + pixel_size - wall_px, pixel_size - wall_px + pixel_size), 
            (maze_pict + decalage + pixel_size + wall_px * 2, maze_pict + pixel_size + wall_px * 2 + pixel_size)
        ), 
        width = wall_px * 2,
        outline=(0,0,0)
    )

draw.rectangle(
        (
            (decalage - 10, pixel_size - 10), 
            (decalage + pixel_size * 2 - 2, pixel_size + pixel_size * 2 - 2)
        ), 
        fill = (255, 255, 255)
    )

draw.rectangle(
        (
            (maze_pict + decalage + 3, maze_pict + pixel_size + 3), 
            (maze_pict + decalage + pixel_size * 2 + 13, maze_pict + pixel_size + pixel_size * 2 + 13)
        ), 
        fill = (255, 255, 255)
    )

print("Maze successfully generated")
image.save(f"{dossier}/images/Maze_{map_Name}.png")

def Path_tracker(x, y):
    position_x = x * pixel_size + decalage + 1
    position_y = y * pixel_size - pixel_size + pixel_size + 2
    draw.rectangle(
        (
            (position_x + round(pixel_size / 5) , position_y + pixel_size + round(pixel_size / 5)), 
            (position_x + pixel_size - round(pixel_size / 5), position_y + pixel_size + pixel_size - round(pixel_size / 5))
        ), 
        fill=(20, 217, 44)
    )

def path_tracer(x, y):
    Path_tracker(x,y)
    while (x, y) != (1, 1):
        x, y = path[x, y]
        Path_tracker(x,y)

path_tracer(map_size, map_size)

image.save(f"{dossier}/images/solved/Maze_{map_Name}.png")
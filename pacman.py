import pygame
import math
import random
from queue import Queue

pygame.init()
screen = pygame.display.set_mode((1000,850))
clock = pygame.time.Clock()
running = True
maze = []
Pacman = pygame.transform.scale(pygame.image.load("assets/player_images/1.png"), (40, 40))
BlueGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/blue.png"), (40, 40))
RedGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/red.png"), (40, 40))
PinkGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/pink.png"), (40, 40))
OrangeGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/orange.png"), (40, 40))

def Maze_Init():
    file = open("maze.txt", "r")
    for line in file:
        int_list = []
        for i in line.strip().split():
            int_list.append(int(i))
        maze.append(int_list)
    file.close()

def Gen_PandG():
    gen = True
    while gen:
        Ghost_posx = random.randint(2, 30)
        Ghost_posy = random.randint(2, 27)
        Pacman_posx = random.randint(2, 30)
        Pacman_posy = random.randint(2, 27)
        if maze[Ghost_posx][Ghost_posy] == 0 and maze[Pacman_posx][Pacman_posy] == 0 and (Ghost_posx, Ghost_posy) != (Pacman_posx, Pacman_posy):
            print(Pacman_posx, Pacman_posy)
            print(Ghost_posx, Ghost_posy)
            maze[Pacman_posx][Pacman_posy] = 1
            maze[Ghost_posx][Ghost_posy] = 2
            gen = False


def Draw_Maze():
    center = 125
    PI = math.pi
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 3:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25), 3)
            elif maze[i][j] == 4:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)
            elif maze[i][j] == 5:
                pygame.draw.arc(screen, "blue", pygame.Rect(j * 25 - 25*0.5 + center, i * 25 + 25*0.5, 25, 25), 0, PI/2, 3)
            elif maze[i][j] == 6:
                pygame.draw.arc(screen, "blue", pygame.Rect(j * 25 + 25*0.5 + center, i * 25 + 25*0.5, 25, 25), PI/2, PI, 3)
            elif maze[i][j] == 7:
                pygame.draw.arc(screen, "blue", pygame.Rect(j * 25 + 25*0.5 + center, i * 25 - 25*0.5, 25, 25), PI, 3*PI/2, 3)
            elif maze[i][j] == 8:
                pygame.draw.arc(screen, "blue", pygame.Rect(j * 25 - 25*0.5 + center, i * 25 - 25*0.5, 25, 25), 3*PI/2, 0, 3)
            elif maze[i][j] == 9:
                pygame.draw.line(screen, "white", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)
            elif maze[i][j] == 1:
                screen.blit(Pacman, (j * 25 - 7 + center, i * 25 - 5))
            elif maze[i][j] == 2:
                screen.blit(BlueGhost, (j * 25 - 7 + center, i * 25 - 5))



Maze_Init()

Gen_PandG()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    screen.fill("black")

    Draw_Maze()

    pygame.display.update()

    clock.tick(60)

pygame.quit()
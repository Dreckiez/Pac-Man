import pygame
import math
import random
from queue import Queue
import sys

pygame.init()
screen = pygame.display.set_mode((1000,850))
clock = pygame.time.Clock()
running = True
maze = []
Pacman_Img = pygame.transform.scale(pygame.image.load("Pac-Man/assets/player_images/1.png"), (40, 40))
BlueGhost = pygame.transform.scale(pygame.image.load("Pac-Man/assets/ghost_images/blue.png"), (40, 40))
RedGhost = pygame.transform.scale(pygame.image.load("Pac-Man/assets/ghost_images/red.png"), (40, 40))
PinkGhost = pygame.transform.scale(pygame.image.load("Pac-Man/assets/ghost_images/pink.png"), (40, 40))
OrangeGhost = pygame.transform.scale(pygame.image.load("Pac-Man/assets/ghost_images/orange.png"), (40, 40))

Pacman_pos_cases = [(9,7), (2, 3), (6,22), (2,2), (21,10)]
Ghost_pos_cases = [(27,7), (2,8), (6,2), (30,27), (14,7)]

def Maze_Init():
    file = open("Pac-Man/maze.txt", "r")
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
    return (Ghost_posx, Ghost_posy), (Pacman_posx, Pacman_posy)

def BFS(Ghost, Pacman):
    traversal=[]
    q = Queue()
    visited = set()
    parent = {}
    path = []

    visited.add(Ghost)
    parent[Ghost] = None
    q.put(Ghost)

    while not q.empty():
        front = q.get()
        traversal.append(front)

        up = (front[0] - 1, front[1])
        down = (front[0] + 1, front[1])
        left = (front[0], front[1] - 1)
        right = (front[0], front[1] + 1)

        if maze[up[0]][up[1]] == 0 and not up in visited:
            visited.add(up)
            parent[up] = front
            q.put(up)
        elif up == Pacman:
            parent[up] = front
            traversal.append(up)
            break

        if maze[left[0]][left[1]] == 0 and not left in visited:
            visited.add(left)
            parent[left] = front
            q.put(left)
        elif left == Pacman:
            parent[left] = front
            traversal.append(left)
            break

        if maze[down[0]][down[1]] == 0 and not down in visited:
            visited.add(down)
            parent[down] = front
            q.put(down)
        elif down == Pacman:
            parent[down] = front
            traversal.append(down)
            break

        if maze[right[0]][right[1]] == 0 and not right in visited:
            visited.add(right)
            parent[right] = front
            q.put(right)
        elif right == Pacman:
            parent[right] = front
            traversal.append(right)
            break
    
    current = Pacman
    while current != None:
        path.append(current)
        current = parent[current]
    path.remove(Pacman)
    path.remove(Ghost)
    path.reverse()

    traversal.remove(Ghost)
    traversal.remove(Pacman)

    return traversal, path

def DFS(Ghost, Pacman):
    traversal = []
    stack = [Ghost]
    visited = set()
    parent = {}
    path = []

    visited.add(Ghost)
    parent[Ghost] = None

    while stack:
        front = stack.pop()
        traversal.append(front)

        if front == Pacman:
            break

        up = (front[0] - 1, front[1])
        down = (front[0] + 1, front[1])
        left = (front[0], front[1] - 1)
        right = (front[0], front[1] + 1)

        for move in [up, down, left, right]:
            if 0 <= move[0] < len(maze) and 0 <= move[1] < len(maze[0]) and maze[move[0]][move[1]] == 0:
                if move not in visited:
                    visited.add(move)
                    parent[move] = front
                    stack.append(move)

    # Tạo đường đi từ Ghost đến Pacman
    current = Pacman
    while current and current in parent:
        path.append(current)
        current = parent[current]
    
    if path:
        path.remove(Pacman)
        path.reverse()

    traversal.remove(Ghost)

    return traversal, path

def Draw_Search(traverse):
    for coors in traverse:
        pygame.draw.circle(screen, "red", (coors[1] * 25 + 25 * 0.5 + 125, coors[0] * 25 + 25 * 0.5), 5)

def Draw_Path(path):
    for coors in path:
        pygame.draw.circle(screen, "white", (coors[1] * 25 + 25 * 0.5 + 125, coors[0] * 25 + 25 * 0.5), 5)

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
                screen.blit(Pacman_Img, (j * 25 - 7 + center, i * 25 - 5))
            elif maze[i][j] == 2:
                screen.blit(BlueGhost, (j * 25 - 7 + center, i * 25 - 5))



Maze_Init()

Ghost_coors, Pacman_coors = Gen_PandG()

traverses = BFS(Ghost_coors, Pacman_coors)

traverses = []
path = []

argument_number = len(sys.argv)


if argument_number == 3:

    Pacman_pos = ()
    Ghost_pos = ()

    if int(sys.argv[2]) == 1: # Vertical Search
        Pacman_pos = Pacman_pos_cases[0]
        Ghost_pos = Ghost_pos_cases[0]
    elif int(sys.argv[2]) == 2: # Neighboring
        Pacman_pos = Pacman_pos_cases[1]
        Ghost_pos = Ghost_pos_cases[1]
    elif int(sys.argv[2]) == 3: # Horizontal Search
        Pacman_pos = Pacman_pos_cases[2]
        Ghost_pos = Ghost_pos_cases[2]
    elif int(sys.argv[2]) == 4: # Across
        Pacman_pos = Pacman_pos_cases[3]
        Ghost_pos = Ghost_pos_cases[3]
    elif int(sys.argv[2]) == 5: # Some Obstacles
        Pacman_pos = Pacman_pos_cases[4]
        Ghost_pos = Ghost_pos_cases[4]
    else:
        print("Invalid Test Case")
        sys.exit()

    maze[Pacman_pos[0]][Pacman_pos[1]] = 1
    maze[Ghost_pos[0]][Ghost_pos[1]] = 2

    if sys.argv[1] == "BFS":
        traverses, path = BFS(Ghost_pos, Pacman_pos)
    elif sys.argv[1] == "DFS":
        traverses, path = DFS(Ghost_pos, Pacman_pos)
    else:
        print("Invalid Search Algorithm")
        sys.exit()
    """ 
    elif sys.argv[1] == "UCS":
    elif sys.argv[1] == "A*": """

current_cells = 0
visualize_search = []
visualize_path = []


Draw_Search_Event = pygame.USEREVENT + 1
Draw_Path_Event = pygame.USEREVENT + 2

pygame.time.set_timer(Draw_Search_Event, 300)

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == Draw_Search_Event:
            visualize_search.append(traverses[current_cells])
            if len(visualize_search) == len(traverses):
                pygame.time.set_timer(Draw_Search_Event, 0)
                pygame.time.set_timer(Draw_Path_Event, 100)
                current_cells -= current_cells 
            else:
                current_cells += 1
        elif event.type == Draw_Path_Event:
            visualize_path.append(path[current_cells])
            if len(visualize_path) == len(path):
                pygame.time.set_timer(Draw_Path_Event, 0)
            else:
                current_cells += 1


    screen.fill("black")

    Draw_Maze()

    Draw_Search(visualize_search)

    Draw_Path(visualize_path)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
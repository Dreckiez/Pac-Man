import pygame
import math
import random
from queue import Queue
from queue import PriorityQueue
import sys

pygame.init()
screen = pygame.display.set_mode((1000,850))
clock = pygame.time.Clock()
running = True
maze = []
Pacman_Img = pygame.transform.scale(pygame.image.load("assets/player_images/1.png"), (40, 40))
BlueGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/blue.png"), (40, 40))
RedGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/red.png"), (40, 40))
PinkGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/pink.png"), (40, 40))
OrangeGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/orange.png"), (40, 40))

Pacman_pos_cases = [(9,7), (2, 3), (6,22), (2,2), (21,10)]
Ghost_pos_cases = [(27,7), (2,8), (6,2), (30,27), (14,7)]


def Maze_Init():
    file = open("maze.txt", "r")
    for line in file:
        int_list = []
        for i in line.strip().split():
            int_list.append(int(i))
        maze.append(int_list)
    file.close()

# def Gen_PandG():
#     gen = True
#     while gen:
#         Ghost_posx = random.randint(2, 30)
#         Ghost_posy = random.randint(2, 27)
#         Pacman_posx = random.randint(2, 30)
#         Pacman_posy = random.randint(2, 27)
#         if maze[Ghost_posx][Ghost_posy] == 0 and maze[Pacman_posx][Pacman_posy] == 0 and (Ghost_posx, Ghost_posy) != (Pacman_posx, Pacman_posy):
#             print(Pacman_posx, Pacman_posy)
#             print(Ghost_posx, Ghost_posy)
#             maze[Pacman_posx][Pacman_posy] = 1
#             maze[Ghost_posx][Ghost_posy] = 2
#             gen = False
#     return (Ghost_posx, Ghost_posy), (Pacman_posx, Pacman_posy)


def get_neighbors(pos):
    """Trả về danh sách ô có thể đi được xung quanh một vị trí."""
    x, y = pos
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    neighbors = []
    for dx, dy in directions:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(maze) and 0 <= ny < len(maze[0]) and maze[nx][ny] in [0, 1]:
            neighbors.append((nx, ny))
    return neighbors

def BFS(Ghost, Pacman):
    queue = Queue()
    queue.put(Ghost)
    parent = {Ghost: None}
    traversal = []
    while not queue.empty():
        current = queue.get()
        traversal.append(current)
        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                if neighbor == Pacman:  # Nếu gặp Pac-Man thì dừng ngay
                    parent[neighbor] = current
                    traversal.append(neighbor)
                    return traversal,reconstruct_path(parent, Ghost, Pacman)
                parent[neighbor] = current
                queue.put(neighbor)
    
    return traversal, reconstruct_path(parent, Ghost, Pacman)

def UCS(Ghost, Pacman):
    pq = PriorityQueue()
    pq.put((0, Ghost))
    parent = {Ghost: None}
    cost = {Ghost: 0}
    traversal = []
    while not pq.empty():
        current_cost, current_node = pq.get()
        traversal.append(current_node)
        if current_node == Pacman:
            break
        for neighbor in get_neighbors(current_node):
            new_cost = current_cost + 1
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                pq.put((new_cost, neighbor))
                parent[neighbor] = current_node
    
    return traversal, reconstruct_path(parent, Ghost, Pacman)

def DFS(Ghost, Pacman):
    stack = [Ghost]
    parent = {Ghost: None}
    traversal = []
    while stack:
        current = stack.pop()
        traversal.append(current)
        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                if neighbor == Pacman:  # Nếu gặp Pac-Man thì dừng ngay
                    parent[neighbor]= current
                    traversal.append(neighbor)
                    return traversal,reconstruct_path(parent, Ghost, Pacman)
                parent[neighbor] = current
                stack.append(neighbor)
    
    return traversal,reconstruct_path(parent, Ghost, Pacman)

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current and current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path[1:] if len(path) > 1 else []

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
            elif maze[i][j] == 'B':
                screen.blit(BlueGhost, (j * 25 - 7 + center, i * 25 - 5))
            elif maze[i][j] == 'O':
                screen.blit(OrangeGhost, (j * 25 - 7 + center, i * 25 - 5))
            elif maze[i][j] == 'P':
                screen.blit(PinkGhost, (j * 25 - 7 + center, i * 25 - 5))




Maze_Init()

# Ghost_coors, Pacman_coors = Gen_PandG()

# traverses = BFS(Ghost_coors, Pacman_coors)

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
    

    if sys.argv[1] == "BFS":
        maze[Ghost_pos[0]][Ghost_pos[1]] = 'B'
        traverses, path = BFS(Ghost_pos, Pacman_pos)
    elif sys.argv[1] == "UCS":
        maze[Ghost_pos[0]][Ghost_pos[1]] = 'O'
        traverses, path = UCS (Ghost_pos, Pacman_pos)
    elif sys.argv[1] == "DFS":
        maze[Ghost_pos[0]][Ghost_pos[1]] = 'P'
        traverses, path = DFS (Ghost_pos, Pacman_pos)
    else:
        print("Invalid Search Algorithm")
        sys.exit()
    
    
    """ elif sys.argv[1] == "DFS":
    elif sys.argv[1] == "A*": """

current_cells = 0
visualize_search = []
visualize_path = []


Draw_Search_Event = pygame.USEREVENT + 1
Draw_Path_Event = pygame.USEREVENT + 2

pygame.time.set_timer(Draw_Search_Event, 50)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == Draw_Search_Event:
            if current_cells < len(traverses): #Add this check
                visualize_search.append(traverses[current_cells])
                if len(visualize_search) == len(traverses):
                    pygame.time.set_timer(Draw_Search_Event, 0)
                    pygame.time.set_timer(Draw_Path_Event, 10)
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



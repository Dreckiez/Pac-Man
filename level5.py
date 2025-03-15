import pygame
import math
import random
from queue import Queue, PriorityQueue
import sys

# Khởi tạo Pygame
pygame.init()
screen = pygame.display.set_mode((1000, 850))
clock = pygame.time.Clock()

# Tải hình ảnh
Pacman_Img = pygame.transform.scale(pygame.image.load("assets/player_images/1.png"), (40, 40))
BlueGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/blue.png"), (40, 40))
RedGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/red.png"), (40, 40))
PinkGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/pink.png"), (40, 40))
OrangeGhost = pygame.transform.scale(pygame.image.load("assets/ghost_images/orange.png"), (40, 40))

# Khởi tạo tọa độ ban đầu
Pacman_pos_cases = [(9, 7), (2, 3), (6, 22), (2, 2), (21, 10)]
Ghost_pos_cases = [(27, 7), (2, 8), (6, 2), (30, 27), (14, 7)]

# Khởi tạo maze
maze = []
def Draw_Path(path):
    for coors in path:
        pygame.draw.circle(screen, "white", (coors[1] * 25 + 25 * 0.5 + 125, coors[0] * 25 + 25 * 0.5), 5)
def Maze_Init():
    global maze
    with open("maze.txt", "r") as file:
        maze = [list(map(int, line.strip().split())) for line in file]

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
    
    while not queue.empty():
        current = queue.get()
        if current == Pacman:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                queue.put(neighbor)
    
    return reconstruct_path(parent, Ghost, Pacman)

def UCS(Ghost, Pacman):
    pq = PriorityQueue()
    pq.put((0, Ghost))
    parent = {Ghost: None}
    cost = {Ghost: 0}

    while not pq.empty():
        current_cost, current_node = pq.get()
        if current_node == Pacman:
            break
        for neighbor in get_neighbors(current_node):
            new_cost = current_cost + 1
            if neighbor not in cost or new_cost < cost[neighbor]:
                cost[neighbor] = new_cost
                pq.put((new_cost, neighbor))
                parent[neighbor] = current_node
    
    return reconstruct_path(parent, Ghost, Pacman)

def DFS(Ghost, Pacman):
    stack = [Ghost]
    parent = {Ghost: None}

    while stack:
        current = stack.pop()
        if current == Pacman:
            break
        for neighbor in get_neighbors(current):
            if neighbor not in parent:
                parent[neighbor] = current
                stack.append(neighbor)
    
    return reconstruct_path(parent, Ghost, Pacman)

def reconstruct_path(parent, start, end):
    path = []
    current = end
    while current and current in parent:
        path.append(current)
        current = parent[current]
    path.reverse()
    return path[1:] if len(path) > 1 else []

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



def isOccupied(*positions):
    """Kiểm tra xem có ít nhất hai ma trùng vị trí không."""
    seen = set()
    duplicates = set()
    for pos in positions:
        if pos in seen:
            duplicates.add(pos)
        seen.add(pos)
    return duplicates  # Trả về tập hợp các vị trí bị trùng
# Khởi tạo trò chơi
Maze_Init()
found = False
#case 2 works
#case 0 works
#cas 3 2 ghost stuck when same ocupied is pacman

Pacman = Pacman_pos_cases[1]
maze[Pacman[0]][Pacman[1]] = 1
UCS_pos = Ghost_pos_cases[0]
BFS_pos = Ghost_pos_cases[1]
DFS_pos = Ghost_pos_cases[2]
maze[UCS_pos[0]][UCS_pos[1]] = 'O'
maze[BFS_pos[0]][BFS_pos[1]] = 'B'
maze[DFS_pos[0]][DFS_pos[1]] = 'P'
UCS_Path = UCS(UCS_pos, Pacman)
BFS_Path = BFS(BFS_pos, Pacman)
DFS_Path = DFS(DFS_pos, Pacman)
Draw_Path(BFS_Path)
Draw_Path(DFS_Path)
Draw_Path(UCS_Path)
Draw_Maze()

UPDATE_PATH_EVENT = pygame.USEREVENT + 1
CHASING = pygame.USEREVENT + 2
pygame.time.set_timer(UPDATE_PATH_EVENT, 100)
pygame.time.set_timer(CHASING, 500)
UPDATE_PATH_EVERY_2S = pygame.USEREVENT + 3
pygame.time.set_timer(UPDATE_PATH_EVERY_2S, 2000)
while not found:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == UPDATE_PATH_EVENT:
            UCS_Path = UCS(UCS_pos, Pacman)
            BFS_Path = BFS(BFS_pos, Pacman)
            DFS_Path = DFS(DFS_pos, Pacman)
        elif event.type == UPDATE_PATH_EVERY_2S:
            UCS_Path = UCS(UCS_pos, Pacman)
            BFS_Path = BFS(BFS_pos, Pacman)
            DFS_Path = DFS(DFS_pos, Pacman)
            print("Cập nhật đường đi sau 2 giây")
        elif event.type == CHASING:
            maze[UCS_pos[0]][UCS_pos[1]] = 0
            maze[BFS_pos[0]][BFS_pos[1]] = 0
            maze[DFS_pos[0]][DFS_pos[1]] = 0
            
            next_UCS = UCS_Path[0] if UCS_Path else UCS_pos
            next_BFS = BFS_Path[0] if BFS_Path else BFS_pos
            next_DFS = DFS_Path[0] if DFS_Path else DFS_pos
            print (next_UCS,next_BFS,next_DFS)
            print (Pacman)
            duplicates = []
            if (next_UCS != Pacman and next_BFS != Pacman and next_DFS != Pacman):
                duplicates = isOccupied(next_UCS, next_BFS, next_DFS)
            
            if not duplicates:
                if UCS_Path:
                    UCS_pos = UCS_Path.pop(0)
                if BFS_Path:
                    BFS_pos = BFS_Path.pop(0)
                if DFS_Path:
                    DFS_pos = DFS_Path.pop(0)
            else:    
                if next_UCS in duplicates:
                        maze[next_UCS[0]][next_UCS[1]] = -1
                        UCS_Path = UCS(UCS_pos, Pacman)
                        maze[next_UCS[0]][next_UCS[1]] = 0
                        if UCS_Path:
                            UCS_pos = UCS_Path.pop(0)
                if next_BFS in duplicates :
                        maze[next_BFS[0]][next_BFS[1]] = -1
                        BFS_Path = BFS(BFS_pos, Pacman)
                        maze[next_BFS[0]][next_BFS[1]] = 0
                        if BFS_Path:
                            BFS_pos = BFS_Path.pop(0)
                if next_DFS in duplicates:
                    maze[next_DFS[0]][next_DFS[1]] = -1
                    DFS_Path = DFS(DFS_pos, Pacman)
                    maze[next_BFS[0]][next_BFS[1]] = 0
                    if DFS_Path:
                        DFS_pos = DFS_Path.pop(0)
                
            maze[UCS_pos[0]][UCS_pos[1]] = 'O'
            maze[BFS_pos[0]][BFS_pos[1]] = 'B'
            maze[DFS_pos[0]][DFS_pos[1]] = 'P'

            # Nếu ma trùng vị trí, cập nhật lại đường đi
            
            

    # Kiểm tra nếu có va chạm với Pacman
    if UCS_pos == Pacman or BFS_pos == Pacman or DFS_pos == Pacman:
        found = True
        print("Pacman bị bắt!")

    # Vẽ lại maze
    screen.fill("black")
    Draw_Maze()
    Draw_Path(BFS_Path)
    Draw_Path(DFS_Path)
    Draw_Path(UCS_Path)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

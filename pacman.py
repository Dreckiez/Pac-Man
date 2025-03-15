import pygame
import time
import sys
import tracemalloc
import search
import utils
import draw

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

Draw_Search_Event = pygame.USEREVENT + 1
Draw_Path_Event = pygame.USEREVENT + 2
Draw_Ghost_Move = pygame.USEREVENT + 3

Pacman_pos_cases = [(9,7), (2, 3), (6,22), (2,2), (21,10)]
Ghost_pos_cases = [(27,7), (2,8), (6,2), (30,27), (14,7)]


utils.Maze_Init(maze)

# Ghost_coors, Pacman_coors = Gen_PandG()

# traverses = BFS(Ghost_coors, Pacman_coors)

traverses = []
path = []

argument_number = len(sys.argv)

Pacman_pos = ()
Ghosts_pos = [(0,0),(0,0),(0,0),(0,0)]

if argument_number == 2:
    if sys.argv[1] == "all":
        Pacman_pos, Ghosts_pos = utils.Gen_PandG(maze)
        traverses, temp_path = search.BFS(Ghosts_pos[0], Pacman_pos, maze)
        path.append(temp_path)
        
        traverses, temp_path = search.DFS(Ghosts_pos[1], Pacman_pos, maze)
        path.append(temp_path)

        traverses, temp_path = search.UCS(Ghosts_pos[2], Pacman_pos, maze)
        path.append(temp_path)

        traverses, temp_path = search.A_star(Ghosts_pos[3], Pacman_pos, maze)
        path.append(temp_path)

        pygame.time.set_timer(Draw_Ghost_Move, 300)
    else:
        print("Invalid Test Case")
        sys.exit()
elif argument_number == 3:
    Temp_pos = ()

    if int(sys.argv[2]) == 1: # Vertical Search
        Pacman_pos = Pacman_pos_cases[0]
        Temp_pos = Ghost_pos_cases[0]
    elif int(sys.argv[2]) == 2: # Neighboring
        Pacman_pos = Pacman_pos_cases[1]
        Temp_pos = Ghost_pos_cases[1]
    elif int(sys.argv[2]) == 3: # Horizontal Search
        Pacman_pos = Pacman_pos_cases[2]
        Temp_pos = Ghost_pos_cases[2]
    elif int(sys.argv[2]) == 4: # Across
        Pacman_pos = Pacman_pos_cases[3]
        Temp_pos = Ghost_pos_cases[3]
    elif int(sys.argv[2]) == 5: # Some Obstacles
        Pacman_pos = Pacman_pos_cases[4]
        Temp_pos = Ghost_pos_cases[4]
    else:
        print("Invalid Test Case")
        sys.exit()

    maze[Pacman_pos[0]][Pacman_pos[1]] = 1

    if sys.argv[1] == "BFS":
        Ghosts_pos[0] = Temp_pos
        maze[Ghosts_pos[0][0]][Ghosts_pos[0][1]] = 11
        tracemalloc.start()
        start = time.perf_counter()

        traverses, path = search.BFS(Ghosts_pos[0], Pacman_pos, maze)
        
        end = time.perf_counter()
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("BFS")
        print(f"Memory Usage: {peak/1024: .2f} KB")
        print(f"Runtime: {end - start: .6f} seconds")
        print("Expanded Nodes: ", len(traverses) - 1) # Early Stopping
    elif sys.argv[1] == "DFS":
        Ghosts_pos[1] = Temp_pos
        maze[Ghosts_pos[1][0]][Ghosts_pos[1][1]] = 12
        tracemalloc.start()
        start = time.perf_counter()

        traverses, path = search.DFS(Ghosts_pos[1], Pacman_pos, maze)
        
        end = time.perf_counter()
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("DFS")
        print(f"Memory Usage: {peak/1024: .2f} KB")
        print(f"Runtime: {end - start: .6f} seconds")
        print("Expanded Nodes: ", len(traverses) - 1) # Early Stopping
    elif sys.argv[1] == "UCS":
        Ghosts_pos[2] = Temp_pos
        maze[Ghosts_pos[2][0]][Ghosts_pos[2][1]] = 13
        tracemalloc.start()
        start = time.perf_counter()

        traverses, path = search.UCS(Ghosts_pos[2], Pacman_pos, maze)
        
        end = time.perf_counter()
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("UCS")
        print(f"Memory Usage: {peak/1024: .2f} KB")
        print(f"Runtime: {end - start: .6f} seconds")
        print("Expanded Nodes: ", len(traverses))
    elif sys.argv[1] == "A*":
        Ghosts_pos[3] = Temp_pos
        maze[Ghosts_pos[3][0]][Ghosts_pos[3][1]] = 13
        tracemalloc.start()
        start = time.perf_counter()

        traverses, path = search.A_star(Ghosts_pos[3], Pacman_pos, maze)
        
        end = time.perf_counter()
        cur, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print("A*")
        print(f"Memory Usage: {peak/1024: .2f} KB")
        print(f"Runtime: {end - start: .6f} seconds")
        print("Expanded Nodes: ", len(traverses))
    else:
        print("Invalid Search Algorithm")
        sys.exit()
    
    pygame.time.set_timer(Draw_Search_Event, 300)

current_cells = 0
visualize_search = []
visualize_path = []
visualize_move = []

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
        elif event.type == Draw_Ghost_Move:
            if current_cells < len(path[0]):
                Ghosts_pos[0] = path[0][current_cells]
            if current_cells < len(path[1]):
                Ghosts_pos[1] = path[1][current_cells]
            if current_cells < len(path[2]):
                Ghosts_pos[2] = path[2][current_cells]
            if current_cells < len(path[3]):
                Ghosts_pos[3] = path[3][current_cells]
            current_cells += 1

    screen.fill("black")

    draw.Draw_Maze(screen, maze)
    draw.Draw_Pacman(screen, Pacman_Img, Pacman_pos)
    draw.Draw_Ghosts(screen, BlueGhost, PinkGhost, OrangeGhost, RedGhost, Ghosts_pos)

    draw.Draw_Search(screen, visualize_search)

    draw.Draw_Path(screen, visualize_path)

    pygame.display.update()

    clock.tick(60)

pygame.quit()
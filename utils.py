import random

def Maze_Init(maze):
    file = open("maze.txt", "r")
    for line in file:
        int_list = []
        for i in line.strip().split():
            int_list.append(int(i))
        maze.append(int_list)
    file.close()

def Gen_PandG(maze):
    playable_pos = []
    rows = len(maze)
    cols = len(maze[0])

    for r in range(0, rows):
        for c in range(0, cols):
            if maze[r][c] == 0:
                playable_pos.append((r, c))
    
    selected = random.sample(playable_pos, 5)
    pacman_pos = selected[0]
    ghosts_pos = selected[1:]
    
    maze[pacman_pos[0]][pacman_pos[1]] = 1

    for g, i in zip(ghosts_pos, [1,2,3,4]):
        maze[g[0]][g[1]] = 10 + i
    
    return pacman_pos, ghosts_pos

def Move_Pacman(maze, pos, direction):
    new_r, new_c = pos

    if direction == 0:
        new_c += 1
    elif direction == 1:
        new_r -= 1
    elif direction == 2:
        new_c -= 1
    elif direction == 3:
        new_r += 1
    else:
        return pos

    if maze[new_r][new_c] != 0:
        return pos

    return (new_r, new_c)
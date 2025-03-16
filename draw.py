import pygame

def Draw_Search(screen, traverse):
    for coors in traverse:
        pygame.draw.circle(screen, "red", (coors[1] * 25 + 25 * 0.5 + 125, coors[0] * 25 + 25 * 0.5), 5)

def Draw_Path(screen, path):
    for coors in path:
        pygame.draw.circle(screen, "white", (coors[1] * 25 + 25 * 0.5 + 125, coors[0] * 25 + 25 * 0.5), 5)

def Draw_Maze(screen, maze):
    center = 125
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 3:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25), 3)
            elif maze[i][j] == 4:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)
            elif maze[i][j] == 5:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), 3)
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25), 3)
            elif maze[i][j] == 6:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25), 3)
            elif maze[i][j] == 7:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), 3)
            elif maze[i][j] == 8:
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), 3)
                pygame.draw.line(screen, "blue", pygame.Vector2(j * 25 + 25*0.5 + center, i * 25), pygame.Vector2(j * 25 + 25*0.5 + center, i * 25 + 25*0.5), 3)
            elif maze[i][j] == 9:
                pygame.draw.line(screen, "white", pygame.Vector2(j * 25 + center, i * 25 + 25*0.5), pygame.Vector2(j * 25 + 25 + center, i * 25 + 25*0.5), 3)

def Draw_Pacman(screen, img, pos, direction):
    center = 125
    # direction = 0 - Right, 1 - Up, 2 - Left, 3 - Down
    if direction == 0:
        screen.blit(img, (pos[1] * 25 - 7 + center, pos[0] * 25 - 5))
    elif direction == 1:
        screen.blit(pygame.transform.rotate(img, 90), (pos[1] * 25 - 7 + center, pos[0] * 25 - 5))
    elif direction == 2:
        screen.blit(pygame.transform.flip(img, True, False), (pos[1] * 25 - 7 + center, pos[0] * 25 - 5))
    elif direction == 3:
        screen.blit(pygame.transform.rotate(img, 270), (pos[1] * 25 - 7 + center, pos[0] * 25 - 5))


def Draw_Ghosts(screen, BlueGhost, PinkGhost, OrangeGhost, RedGhost, GhostPos):
    center = 125
    if GhostPos[0] != (0,0):
        screen.blit(BlueGhost, (GhostPos[0][1] * 25 - 7 + center, GhostPos[0][0] * 25 - 5))
    if GhostPos[1] != (0,0):
        screen.blit(PinkGhost, (GhostPos[1][1] * 25 - 7 + center, GhostPos[1][0] * 25 - 5))
    if GhostPos[2] != (0,0):
        screen.blit(OrangeGhost, (GhostPos[2][1] * 25 - 7 + center, GhostPos[2][0] * 25 - 5))
    if GhostPos[3] != (0,0):
        screen.blit(RedGhost, (GhostPos[3][1] * 25 - 7 + center, GhostPos[3][0] * 25 - 5))
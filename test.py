from queue import Queue
import random

maze=[]

file = open("maze.txt", "r")
for line in file:
    int_list = []
    for i in line.strip().split():
        int_list.append(int(i))
    maze.append(int_list)
file.close()


""" gen = True
while gen:
    Ghost_posx = random.randint(2, 30)
    Ghost_posy = random.randint(2, 27)
    Pacman_posx = random.randint(2, 30)
    Pacman_posy = random.randint(2, 27)
    if maze[Ghost_posx - 1][Ghost_posy - 1] == 0 and maze[26][25] == 0 and Ghost_posx != Pacman_posx and Ghost_posy != Pacman_posy:
        print(Pacman_posx, Pacman_posy)
        print(Ghost_posx, Ghost_posy)
        maze[26][25] = 1
        maze[Ghost_posx - 1][Ghost_posy - 1] = 2
        gen = False """

maze[26][25] = 1
maze[21][13] = 2


traversal=[]
q = Queue()
visited = {(0,0)}

visited.add((21,13))
q.put([21,13])

# print(visited)
# print(q.get())


while not q.empty():
    front = q.get()
    traversal.append(front)

    up = (front[0] - 1, front[1])
    down = (front[0] + 1, front[1])
    left = (front[0], front[1] - 1)
    right = (front[0], front[1] + 1)
    """ print("Front: ", front, maze[front[0]][front[1]])
    print("Up: ", up, maze[up[0]][up[1]])
    print("Left: ", left, maze[left[0]][left[1]])
    print("Down: ", down, maze[down[0]][down[1]])
    print("Right: ", right, maze[right[0]][right[1]]) """

    if up[0] > 2 and up[1] < 30 and maze[up[0]][up[1]] == 0 and not up in visited:
        visited.add(up)
        if up[0] == 26 and up[1] == 25:
            traversal.append(up)
            break
        q.put(up)
    if left[0] > 2 and left[1] < 27 and maze[left[0]][left[1]] == 0 and not left in visited:
        visited.add(left)
        if left[0] == 26 and left[1] == 25:
            traversal.append(left)
            break
        q.put(left)
    if down[0] > 2 and down[1] < 30 and maze[down[0]][down[1]] == 0 and not down in visited:
        visited.add(down)
        if down[0] == 26 and down[1] == 25:
            traversal.append(down)
            break
        q.put(down)
    if right[0] > 2 and right[1] < 27 and maze[right[0]][right[1]] == 0 and not right in visited:
        print("Front: ", front, maze[front[0]][front[1]])
        print("Right: ", right, maze[right[0]][right[1]])
        visited.add(right)
        if right[0] == 26 and right[1] == 25:
            traversal.append(right)
            break
        q.put(right)

print(traversal)
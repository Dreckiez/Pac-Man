from queue import Queue
from queue import PriorityQueue

def BFS(Ghost, Pacman, maze):
    traversal=[]
    q = Queue()
    visited = set()
    parent = {}
    path = []

    visited.add(Ghost)
    parent[Ghost] = None
    q.put(Ghost)

    found = False

    while not q.empty() and not found:
        front = q.get()
        traversal.append(front)

        up = (front[0] - 1, front[1])
        down = (front[0] + 1, front[1])
        left = (front[0], front[1] - 1)
        right = (front[0], front[1] + 1)

        for move in [up, left, down, right]:
            if maze[move[0]][move[1]] in [0, 9] and not move in visited:
                visited.add(move)
                parent[move] = front
                q.put(move)
            if move == Pacman:
                parent[move] = front
                traversal.append(move)
                found = True
                break
    
    current = Pacman
    while current != None:
        path.append(current)
        current = parent[current]
    path.reverse()

    return traversal, path

def DFS(Ghost, Pacman, maze):
    traversal = []
    stack = [Ghost]
    visited = set()
    parent = {}
    path = []

    visited.add(Ghost)
    parent[Ghost] = None
    found = False

    while stack and not found:
        front = stack.pop()
        traversal.append(front)

        up = (front[0] - 1, front[1])
        down = (front[0] + 1, front[1])
        left = (front[0], front[1] - 1)
        right = (front[0], front[1] + 1)

        for move in [up, down, left, right]:
            if maze[move[0]][move[1]] in [0, 9] and move not in visited:
                visited.add(move)
                parent[move] = front
                stack.append(move)
            if move == Pacman:
                parent[move] = front
                traversal.append(move)
                found = True
                break

    # Tạo đường đi từ Ghost đến Pacman
    current = Pacman
    while current and current in parent:
        path.append(current)
        current = parent[current]
    
    if path:
        path.reverse()

    return traversal, path

def UCS(Ghost, Pacman, maze):
    traversal = []
    path = []
    parent = {}
    pq = PriorityQueue()
    visited = set()
    cost = {Ghost: 0}
    pq.put((0, Ghost))
    visited.add(Ghost)
    parent[Ghost] = None

    while not pq.empty():
        current_cost, current_node = pq.get()
        traversal.append(current_node)

        if current_node == Pacman:
            break
        
        up = (current_node[0] - 1, current_node[1])
        down = (current_node[0] + 1, current_node[1])
        left = (current_node[0], current_node[1] - 1)
        right = (current_node[0], current_node[1] + 1)

        for neighbor in [up, down, left, right]:
            if maze[neighbor[0]][neighbor[1]] in [0, 1, 9]:
                new_cost = cost[current_node] + 1
                if neighbor not in visited or new_cost < cost.get(neighbor, float('inf')):
                    cost[neighbor] = new_cost
                    pq.put((new_cost, neighbor))
                    parent[neighbor] = current_node
                    visited.add(neighbor)  # Đánh dấu ngay khi thêm vào hàng đợi

    current = Pacman
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()

    return traversal, path

def A_star(Ghost, Pacman, maze):
    def f(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    traversal = []
    path = []
    parent = {}
    pq = PriorityQueue()
    cost = {Ghost: 0}
    parent[Ghost] = None
    pq.put((f(Ghost, Pacman), 0, Ghost))

    while not pq.empty():
        current = pq.get()
        traversal.append(current[2])
        
        if current[2] == Pacman:
            break

        neighbors = [
            (current[2][0] - 1, current[2][1]),
            (current[2][0] + 1, current[2][1]),
            (current[2][0], current[2][1] - 1),
            (current[2][0], current[2][1] + 1)
        ]

        for neighbor in neighbors:
            if maze[neighbor[0]][neighbor[1]] in [0, 1, 9]:
                new_cost = cost[current[2]] + 1

                if neighbor not in cost or new_cost < cost[neighbor]:
                    cost[neighbor] = new_cost
                    f_value = new_cost + f(neighbor, Pacman)
                    pq.put((f_value, new_cost, neighbor))
                    parent[neighbor] = current[2]

    current = Pacman
    while current is not None:
        path.append(current)
        current = parent[current]
    path.reverse()

    return traversal, path
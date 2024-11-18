import heapq


class Environment:
    def __init__(self, grid, start, goal):  
        self.grid = grid  
        self.start = start
        self.goal = goal

    def neighbors(self, node):
        
        moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        result = []
        for move in moves:
            neighbor = (node[0] + move[0], node[1] + move[1])
            if 0 <= neighbor[0] < len(self.grid) and 0 <= neighbor[1] < len(self.grid[0]):
                if self.grid[neighbor[0]][neighbor[1]] == 0: 
                    result.append(neighbor)
        return result


def heuristic(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(environment, start, goal):
    open_list = []
    heapq.heappush(open_list, (0, start))
    
    came_from = {}
    g_score = {start: 0}
    
    while open_list:
        _, current = heapq.heappop(open_list)
        
        if current == goal:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        
        for neighbor in environment.neighbors(current):
            tentative_g_score = g_score[current] + 1
            if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                g_score[neighbor] = tentative_g_score
                f_score = tentative_g_score + heuristic(neighbor, goal)
                heapq.heappush(open_list, (f_score, neighbor))
                came_from[neighbor] = current
                
    return None  

def backward_chaining(environment, goal_conditions):
    current_goal = environment.goal
    chain = [current_goal]
    
    while current_goal not in goal_conditions:
        for neighbor in environment.neighbors(current_goal):
            if neighbor in goal_conditions:
                current_goal = neighbor
                chain.append(current_goal)
                break
    return chain

def hybrid_motion_planning(environment, goal_conditions):
    backward_chain_path = backward_chaining(environment, goal_conditions)
    print("Backward chaining path:", backward_chain_path)
    
    
    subgoal = backward_chain_path[-1] if backward_chain_path else environment.start
    final_path = astar(environment, environment.start, subgoal)
    
    if final_path:
        
        remaining_path = astar(environment, subgoal, environment.goal)
        if remaining_path:
            final_path += remaining_path[1:]  
    else:
        return None
    
    return final_path

grid = [
    [0, 0, 0, 1, 0],
    [1, 1, 0, 1, 0],
    [0, 0, 0, 0, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

start = (0, 0)
goal = (4, 4)
goal_conditions = [(3, 4), (2, 4)]  

env = Environment(grid, start, goal)

path = hybrid_motion_planning(env, goal_conditions)
print("Hybrid path:", path)

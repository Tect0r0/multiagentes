import numpy as np
import heapq
import matplotlib.pyplot as plt
import json

class Node:
    def __init__(self, pos, g_cost, h_cost, parent=None, time_step=0):
        self.pos = pos  # (x, y)
        self.g_cost = g_cost  # Cost from start
        self.h_cost = h_cost  # Heuristic to goal
        self.f_cost = g_cost + h_cost
        self.parent = parent
        self.time_step = time_step
    
    def __lt__(self, other):
        return self.f_cost < other.f_cost

class MultiAgentPathfinding:
    def __init__(self, grid):
        self.grid = grid
        self.grid_size = grid.shape[0]
        self.reservation_table = {}  # (x, y, time_step): agent_id
    
    def manhattan_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
    
    def get_neighbors(self, pos):
        """Get valid neighboring positions"""
        neighbors = []
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        
        for dx, dy in directions:
            new_pos = (pos[0] + dx, pos[1] + dy)
            if (0 <= new_pos[0] < self.grid_size and 
                0 <= new_pos[1] < self.grid_size and 
                self.grid[new_pos] == 0):
                neighbors.append(new_pos)
        return neighbors
    
    def is_position_reserved(self, pos, time_step, agent_id):
        """Check if position is reserved by another agent"""
        if (pos, time_step) in self.reservation_table:
            return self.reservation_table[(pos, time_step)] != agent_id
        return False
    
    def find_path(self, start, goal, agent_id):
        """Find path for single agent considering other agents' reservations"""
        open_set = []
        closed_set = set()
        
        start_node = Node(start, 0, self.manhattan_distance(start, goal))
        heapq.heappush(open_set, start_node)
        
        while open_set:
            current = heapq.heappop(open_set)
            
            if current.pos == goal:
                path = []
                while current:
                    path.append(current.pos)
                    current = current.parent
                return path[::-1]
            
            closed_set.add((current.pos, current.time_step))
            
            for next_pos in self.get_neighbors(current.pos):
                if (next_pos, current.time_step + 1) in closed_set:
                    continue
                
                if self.is_position_reserved(next_pos, current.time_step + 1, agent_id):
                    continue
                
                g_cost = current.g_cost + 1
                h_cost = self.manhattan_distance(next_pos, goal)
                
                neighbor = Node(next_pos, g_cost, h_cost, current, current.time_step + 1)
                
                heapq.heappush(open_set, neighbor)
        
        return None
    
    def find_paths_for_agents(self, starts, goals):
        """Find paths for all agents"""
        paths = []
        for i, (start, goal) in enumerate(zip(starts, goals)):
            path = self.find_path(start, goal, i)
            if path:
                # Reserve positions along the path
                for t, pos in enumerate(path):
                    self.reservation_table[(pos, t)] = i
                paths.append(path)
            else:
                print(f"No path found for agent {i}")
        return paths

    def visualize(self, paths):
        """Visualize the grid and paths"""
        plt.figure(figsize=(13, 13))
        
        # Plot obstacles
        obstacle_positions = np.where(self.grid == 1)
        marker_size = 500 / self.grid_size  # Adjust marker size based on grid size
        plt.scatter(obstacle_positions[1], obstacle_positions[0], 
                   color='gray', marker='s', s=marker_size)
        
        # Plot paths
        colors = ['blue', 'red', 'green', 'purple']
        for i, path in enumerate(paths):
            path_array = np.array(path)
            plt.plot(path_array[:, 1], path_array[:, 0], 
                    color=colors[i], linewidth=2, label=f'Agent {i+1}')
            
            # Mark start and end points
            plt.scatter(path[0][1], path[0][0], color=colors[i], 
                      marker='o', s=marker_size, label=f'Start {i+1}')
            plt.scatter(path[-1][1], path[-1][0], color=colors[i], 
                      marker='x', s=marker_size, label=f'Goal {i+1}')
        
        plt.grid(True)
        plt.legend()
        plt.xlim(-1, self.grid_size + 40)
        plt.ylim(-1, self.grid_size)
        plt.show()

# Read grid from map.txt
def read_grid_from_file(filename):
    with open(filename, 'r') as file:
        grid = []
        for line in file:
            grid.append([int(x) for x in line.strip()])
    grid = np.array(grid)
    return np.flipud(grid)  # Reverse the grid on its x-axis (flip vertically)

# Extract obstacle coordinates from the grid
def extract_obstacles(grid):
    obstacles = []
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            if grid[i, j] == 1:
                obstacles.append((i, j))
    return obstacles

# Example usage
grid = read_grid_from_file('map.txt')
obstacles = extract_obstacles(grid)

pathfinder = MultiAgentPathfinding(grid)

# Define start and goal positions for four agents
starts = [(0, 0), (0, 3), (0, 5), (0, 7)]
goals = [(80, 80), (76, 80), (72, 80), (68, 80)]

# Find paths
paths = pathfinder.find_paths_for_agents(starts, goals)

# Variables
k = 50
n = 3
T = 100
b = 2

# Generate JSON output
output_data = {
    "k": k,
    "n": n,
    "T": T,
    "b": b,
    "LGVs": []
}

for i, path in enumerate(paths):
    # Invert x and y coordinates of the path
    #inverted_path = [[pos[1], pos[0]] for pos in path]
    agent_data = {
        "id": i + 1,
        "initial_position": [starts[i][1], starts[i][0]],  # Invert initial position
        "path": path
    }
    output_data["LGVs"].append(agent_data)

# Write JSON to file
with open('simulation_output.json', 'w') as json_file:
    json.dump(output_data, json_file, indent=4)

# Visualize
if all(paths):
    pathfinder.visualize(paths)
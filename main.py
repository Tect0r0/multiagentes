import json
import heapq
from typing import List, Tuple, Dict
import numpy as np

class WarehouseAgent:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.obstacles = set()
        self.start = None
        self.goal = None

    def set_obstacles(self, obstacles: List[Tuple[int, int]]):
        """Define los obstáculos en el almacén (estanterías, cajas, etc)"""
        self.obstacles = set(obstacles)

    def set_start_goal(self, start: Tuple[int, int], goal: Tuple[int, int]):
        """Define el punto inicial y final para el agente"""
        self.start = start
        self.goal = goal

    def get_neighbors(self, pos: Tuple[int, int]) -> List[Tuple[int, int]]:
        """Obtiene las posiciones vecinas válidas para una posición dada"""
        x, y = pos
        possible_neighbors = [
            (x+1, y), (x-1, y), (x, y+1), (x, y-1),
            (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)  # Diagonales
        ]

        return [(x, y) for (x, y) in possible_neighbors 
                if 0 <= x < self.width 
                and 0 <= y < self.height 
                and (x, y) not in self.obstacles]

    def heuristic(self, pos: Tuple[int, int]) -> float:
        """Calcula la heurística (distancia euclidiana) al objetivo"""
        return np.sqrt((pos[0] - self.goal[0])**2 + (pos[1] - self.goal[1])**2)

    def find_path(self) -> List[Dict[str, float]]:
        """Implementa A* para encontrar el camino óptimo y lo devuelve como lista de posiciones"""
        if not (self.start and self.goal):
            raise ValueError("Start and goal positions must be set")

        frontier = [(0, self.start)]
        came_from = {self.start: None}
        cost_so_far = {self.start: 0}

        while frontier:
            current = heapq.heappop(frontier)[1]

            if current == self.goal:
                break

            for next_pos in self.get_neighbors(current):
                # Calcula el costo del movimiento (1 para ortogonal, √2 para diagonal)
                movement_cost = 1.4 if (next_pos[0] != current[0] and next_pos[1] != current[1]) else 1
                new_cost = cost_so_far[current] + movement_cost

                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + self.heuristic(next_pos)
                    heapq.heappush(frontier, (priority, next_pos))
                    came_from[next_pos] = current

        # Reconstruye el camino
        current = self.goal
        path = []
        while current is not None:
            path.append({
                "x": float(current[0]),
                "y": 0.0,  # Altura (puede ajustarse según necesidades)
                "z": float(current[1])
            })
            current = came_from.get(current)

        path.reverse()
        return path

    def save_path_to_json(self, filename: str = "agent_path.json"):
        """Guarda el camino encontrado en un archivo JSON"""
        path = self.find_path()
        data = {
            "agentPath": path,
            "metadata": {
                "gridWidth": self.width,
                "gridHeight": self.height,
                "startPos": {"x": self.start[0], "y": 0, "z": self.start[1]},
                "goalPos": {"x": self.goal[0], "y": 0, "z": self.goal[1]}
            }
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        return filename

# Ejemplo de uso
if __name__ == "__main__":
    # Crear un almacén de 20x20
    agent = WarehouseAgent(20, 20)

    # Definir algunos obstáculos (ejemplo: estanterías)
    obstacles = [(5,5), (5,6), (5,7), (6,5), (6,6), (6,7),
                (12,12), (12,13), (12,14), (13,12), (13,13), (13,14)]
    agent.set_obstacles(obstacles)

    # Definir punto inicial y objetivo
    agent.set_start_goal((2,2), (18,18))

    # Generar y guardar el camino
    filename = agent.save_path_to_json()
    print(f"Path saved to {filename}")
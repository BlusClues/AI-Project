import pygame
import heapq

from Settings import *
from Tank import Tank

class AITank(Tank):
    def __init__(self, game, x, y, id):
        super().__init__(game, x, y, id, RED_TANK_SPRITE_PATH, RED, RED_BULLET_SPRITE_PATH)
        self.x = x
        self.y = y
        self.path = []
        self.last_enemy_pos = None

    # checking neighbours function
    def check_neighbours(self, x, y):
        possible_neighbours = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
        moveable_neighbours = []
        for nx, ny in possible_neighbours:
            if 0 <= nx < GRIDWIDTH and 0 <= ny < GRIDHEIGHT:
                if (nx, ny) not in self.game.wall_positions:
                    moveable_neighbours.append((nx, ny))

        return moveable_neighbours

    # calculate the shortest distance to goal
    # using manhattan distance calculation
    def heuristic(self, location1, location2):
        return abs(location1[0] - location2[0]) + abs(location1[1] - location2[1])

    # a star algorithm
    def a_star_search(self, start, goal):
        frontier = []
        heapq.heappush(frontier, (0, start))
        came_from = {}
        cost_so_far = {}
        came_from[start] = None
        cost_so_far[start] = 0

        while frontier:
            priority, current_location = heapq.heappop(frontier)

            if current_location == goal:
                break

            for next in self.check_neighbours(current_location[0], current_location[1]):
                new_cost = cost_so_far[current_location] + 1
                if next not in cost_so_far or new_cost < cost_so_far[next]:
                    cost_so_far[next] = new_cost
                    priority = new_cost + self.heuristic(next, goal)
                    heapq.heappush(frontier, (priority, next))
                    came_from[next] = current_location

        return came_from, cost_so_far

    # reconstruct path for tank from algorithm
    def reconstruct_path(self, came_from, goal):
        path = []
        if goal in came_from:
            current = goal
            while current:
                path.append(current)
                current = came_from[current]
            path.reverse()
        return path

    # AI LOOP
    def update(self):
        super().update()
        # update the path if the target moves
        if self.last_enemy_pos != (self.game.player.x, self.game.player.y):
            self.path = []

        # if AI has reached its destination make new path
        if self.path == []:
            goal = (self.game.player.x, self.game.player.y)
            self.last_enemy_pos = goal
            came_from, cost_so_far = self.a_star_search((self.x, self.y), goal)
            self.path = self.reconstruct_path(came_from, goal)
        # if AI is still going calculate movement
        elif self.path != []:
            coordinate_to_move = next(iter(self.path))
            dx = coordinate_to_move[0] - self.x
            dy = coordinate_to_move[1] - self.y
            self.move(dx, dy)
            # remove coordinate once AI has reached it
            if self.x == coordinate_to_move[0] and self.y == coordinate_to_move[1]:
                self.path.pop(0)
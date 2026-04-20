from sys import implementation

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

    # calculates the AIs best flank to change behaviour of AI
    def calculate_flank(self, x, y, distance):
        flank_distance = distance
        possible_flanks = [(x + flank_distance, y), (x - flank_distance, y), (x, y + flank_distance), (x, y - flank_distance)]
        moveable_flanks = []
        closest_difference = float('inf')
        # check that positions are not walls
        for nx, ny in possible_flanks:
            if 0 <= nx < GRIDWIDTH and 0 <= ny < GRIDHEIGHT:
                if (nx, ny) not in self.game.wall_positions:
                    moveable_flanks.append((nx, ny))

        # recursively calls function if all surrounding are walls
        if flank_distance > 1:
            if moveable_flanks == []:
                return self.calculate_flank(x, y, flank_distance - 1)
        else:
            return x, y

        # calculate the closest of the flanks so the AI doesn't drive around enemy
        if len(moveable_flanks) > 1:
            closest_position = moveable_flanks[0]
            for fx, fy in moveable_flanks:
                difference = abs(self.x - fx) + abs(self.y - fy)
                if difference < closest_difference or closest_difference is None:
                    closest_difference = abs(self.x - closest_position[0]) + abs(self.y - closest_position[1])
                    closest_position = (fx, fy)
        elif len(moveable_flanks) == 1:
            closest_position = moveable_flanks[0]

        return closest_position

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
        # start of FSM implementation
        # determine how far enemy is
        distance = self.heuristic((self.x, self.y), (self.game.player.x, self.game.player.y))

        # decide state based on distance
        if distance > 6:
            self.state = "chase"
        else:
            self.state = "flank"

        # get the target based on the state
        if self.state == "chase":
            target = (self.game.player.x, self.game.player.y)
        if self.state == "flank":
            target = self.calculate_flank(self.game.player.x, self.game.player.y, 3)

        # start of a star
        # update the path if the target moves
        if self.last_enemy_pos != (self.game.player.x, self.game.player.y):
            self.path = []

        # if AI has reached its destination make new path
        if self.path == []:
            self.last_enemy_pos = (self.game.player.x, self.game.player.y)
            came_from, cost_so_far = self.a_star_search((self.x, self.y), target)
            self.path = self.reconstruct_path(came_from, target)
        # if AI is still following current path calculate movement
        elif self.path != []:
            coordinate_to_move = next(iter(self.path))
            dx = coordinate_to_move[0] - self.x
            dy = coordinate_to_move[1] - self.y
            self.move(dx, dy)
            # remove coordinate once AI has reached it
            if self.x == coordinate_to_move[0] and self.y == coordinate_to_move[1]:
                self.path.pop(0)
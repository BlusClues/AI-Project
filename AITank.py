import pygame
import heapq
import random

from Settings import *
from Tank import Tank

class AITank(Tank):
    def __init__(self, game, x, y, id, tank_sprite_path, tank_colour, tank_bullet_path, flee_health_limit, flank_distance, health_x_pos, path_recalculation_theshold, flank_offset):
        super().__init__(game, x, y, id, tank_sprite_path, tank_colour, tank_bullet_path)
        self.x = x
        self.y = y
        self.path = []
        self.last_enemy_pos = None
        self.current_angle = 90
        self.target = None
        self.flee_health_limit = flee_health_limit
        self.flank_distance = flank_distance
        self.health_x_pos = health_x_pos
        self.last_state = "chase"
        self.path_recalculation_theshold = path_recalculation_theshold
        self.flank_offset = flank_offset

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
                random_flank = random.randint(1, 6) # role either closest flank or random one
                if random_flank == 1:
                    if difference < closest_difference or closest_difference is None:
                        closest_difference = abs(self.x - closest_position[0]) + abs(self.y - closest_position[1])
                        closest_position = (fx, fy)
                else:
                    return random.choice(moveable_flanks)
        elif len(moveable_flanks) == 1:
            closest_position = moveable_flanks[0]

        return closest_position

    # calculate the position the tank flees to
    def calculate_flee(self, x, y, distance):
        flee_distance = distance
        if self.health == self.flee_health_limit:
            possible_flee_positions = [(x + flee_distance, y + flee_distance), (x - flee_distance, y - flee_distance),
                                       (x - flee_distance, y + flee_distance), (x + flee_distance, y - flee_distance)]
            moveable_flee_positions = []
            closest_difference = float('inf')
            # check that positions are not walls
            for nx, ny in possible_flee_positions:
                if 0 <= nx < GRIDWIDTH and 0 <= ny < GRIDHEIGHT:
                    if (nx, ny) not in self.game.wall_positions:
                        moveable_flee_positions.append((nx, ny))

            # recursive call that checks for a valid flee position with no walls
            if flee_distance > 1:
                if moveable_flee_positions == []:
                    return self.calculate_flee(x, y, flee_distance - 1)
            else:
                return x, y

            # calculate the closest of the flee position so the AI doesn't drive around enemy
            if len(moveable_flee_positions) > 1:
                closest_position = moveable_flee_positions[0]
                for fx, fy in moveable_flee_positions:
                    difference = abs(self.x - fx) + abs(self.y - fy)
                    if difference < closest_difference or closest_difference is None:
                        closest_difference = abs(self.x - closest_position[0]) + abs(self.y - closest_position[1])
                        closest_position = (fx, fy)
            elif len(moveable_flee_positions) == 1:
                closest_position = moveable_flee_positions[0]

            return closest_position
        else:
            return x, y

    # raycast locations ahead of the tank to spot enemy for shooting
    def raycast(self, dx, dy, distance):
        for raycast_distance in range(1, distance):
            current_position = ((dx * raycast_distance) + self.x, (dy * raycast_distance) + self.y)
            if 0 <= current_position[0] < GRIDWIDTH and 0 <= current_position[1] < GRIDHEIGHT:
                if current_position not in self.game.wall_positions:
                    for tank in self.game.tanks:
                        if (current_position[0] == tank.x and current_position[1] == tank.y) and self.id != tank.id:
                            self.shoot()
                else:
                    break
            else:
                break

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
        # Initally add target or if tank is missing one
        if self.target is None or not self.target.alive():
            for tank in self.game.tanks:
                if self.id != tank.id:
                    self.target = tank

        # update the path if the target moves
        if self.target is not None:
            if self.last_enemy_pos is None:
                self.last_enemy_pos = (self.target.x, self.target.y)
                self.path = []
            else:
                distance = self.heuristic(self.last_enemy_pos, (self.target.x, self.target.y))
                if distance > self.path_recalculation_theshold:
                    self.path = []

            # start of FSM implementation
            # determine how far away the enemy is
            distance_to_target = self.heuristic((self.x, self.y), (self.target.x, self.target.y))

            # decide state based on distance
            if distance_to_target > self.flank_distance:
                self.state = "chase"
            elif self.health <= self.flee_health_limit:
                self.state = "flee"
            else:
                self.state = "flank"

            # clear path if state changes
            if self.state != self.last_state:
                self.path = []
                self.last_state = self.state

            # get the target based on the state
            if self.state == "chase":
                target = (self.target.x, self.target.y)
            if self.state == "flank":
                target = self.calculate_flank(self.target.x, self.target.y, self.flank_offset)
            if self.state == "flee":
                target = self.calculate_flee(self.target.x, self.target.y, 5)

            # start of a star
            # if AI has reached its destination make new path
            if self.path == []:
                self.last_enemy_pos = (self.target.x, self.target.y)
                came_from, cost_so_far = self.a_star_search((self.x, self.y), target)
                self.path = self.reconstruct_path(came_from, target)
                self.rotate_sprite(self.current_angle) # not sure if this helps, but I want to believe it does lol
            # if AI is still following current path calculate movement
            elif self.path != []:
                coordinate_to_move = next(iter(self.path))
                dx = coordinate_to_move[0] - self.x
                dy = coordinate_to_move[1] - self.y

                # rotate the sprite before moving
                match (dx, dy):
                    case (1,0):
                        self.current_angle = 180
                        self.rotate_sprite(self.current_angle)
                    case (-1,0):
                        self.current_angle = 0
                        self.rotate_sprite(self.current_angle)
                    case (0,1):
                        self.current_angle = 90
                        self.rotate_sprite(self.current_angle)
                    case (0,-1):
                        self.current_angle = -90
                        self.rotate_sprite(self.current_angle)

                self.raycast(dx, dy, RAYCAST_DISTANCE)
                self.move(dx, dy)
                # remove coordinate once AI has reached it
                if self.x == coordinate_to_move[0] and self.y == coordinate_to_move[1]:
                    self.path.pop(0)
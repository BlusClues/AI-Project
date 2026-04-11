from Settings import *

class Map:
    def __init__(self, filename):
        self.data = []
        with open(filename, 'rt') as f:
            for line in f:
                self.data.append(line)
        n_horizontal_tiles = len(self.data[0])
        n_vertical_tiles = len(self.data)

        self.width = n_horizontal_tiles * TILESIZE
        self.height = n_vertical_tiles * TILESIZE
import pygame
from tile import *
from PIL import Image
from itertools import product
import os
import shutil

class Main:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.screenSize = self.screen.get_size()
        self.clock = pygame.time.Clock()
        self.Running = True
        self.grid:list[list[Slot]] = []
        self.done:bool = False
        self.image = "test_image.png"
        self.image_size:int = 400
        self.base_tile_size = 50
        self.possable_tile_sizes = {"A":120,"B":60,"C":40,"D":30,"E":24,"F":20}
        self.tile_size:int = 120
        self.img_tile_dimentions:int = int(self.image_size/self.base_tile_size)
        self.possibilities:list[Tile] = [] 

    def run(self):
        choice = (input("Which tile size would you like?\nA:120\nB:60\nC:40\nD:30\nE:24\nF:20\n -- ")).upper()
        if choice in self.possable_tile_sizes:
            self.tile_size = self.possable_tile_sizes[choice]
        self.slice(self.image, ".", "images/", self.base_tile_size)
        self.make_possibilities()
        self.grid, self.done = makeGrid(self.screen, self.grid, self.img_tile_dimentions, self.tile_size, self.base_tile_size, self.possibilities)
        while self.Running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.Running = False
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LCTRL]:
                self.Running = False
            if keys[pygame.K_LSHIFT]:
                self.grid, self.done = makeGrid(self.screen, self.grid, self.img_tile_dimentions, self.tile_size, self.base_tile_size, self.possibilities)

            self.screen.fill((0,0,0))

            if not self.done: #type: ignore
                self.done,self.grid = determine_possibilities(self.grid)
                self.grid = collapse(self.img_tile_dimentions, self.grid)

            for i in range(int(self.screen.get_height()/self.tile_size)):
                for j in range(int(self.screen.get_width()/self.tile_size)):
                    self.grid[i][j].draw()

            pygame.display.flip()
        self.clear_folder()

    def slice(self, filename, dir_in, dir_out, d):
        name, ext = os.path.splitext(filename)
        img = Image.open(os.path.join(dir_in, filename))
        w, h = img.size
        
        grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
        for i, j in grid:
            box = (j, i, j+d, i+d)
            out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
            img.crop(box).save(out)
    
    def clear_folder(self):
        folder = "images/"
        for filename in os.listdir(folder):
            file_path = os.path.join(folder, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def make_possibilities(self):
        temp:list[Tile] = []
        for i in range(self.img_tile_dimentions):
            for j in range(self.img_tile_dimentions):
                self.possibilities.append(Tile(i,j,self.base_tile_size))

        pixels = []

        for tile in self.possibilities:
            present = False
            for otherTile in temp:
                if tile.sides == otherTile.sides:
                    present = True
            if not present:
                temp.append(tile)

        # pixels.append(self.possibilities[0].sides) 
        # temp.append(self.possibilities[0])
        # for tile in self.possibilities:
        #     if tile.sides not in pixels:
        #         pixels.append(tile.sides)
        #         temp.append(tile)

        self.possibilities = copy.copy(temp)
        print(len(self.possibilities))
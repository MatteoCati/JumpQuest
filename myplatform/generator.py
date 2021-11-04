import os
from collections import deque, defaultdict
import random
import pickle as pkl
import pygame

from myplatform.constants import default_level, BlockType
from myplatform.objects import GameObject


# noinspection PyAttributeOutsideInit
class LevelGenerator:
    def __init__(self, tile_size, screen_size):
        self.left_stack = deque(maxlen=500)
        self.right_stack = deque(maxlen=500)

        self.tile_size = tile_size
        self.screen_size = screen_size
        self.grass_block_img = pygame.image.load("./images/grass.png")
        self.dirt_block_img = pygame.image.load("./images/dirt.png")

        self.load_levels()

    def load_levels(self):
        self.left_dict = defaultdict(list)
        self.right_dict = defaultdict(list)
        with open("./levels/all_levels.pkl", "rb") as fin:
            levels = pkl.load(fin)
            for level_map in levels:
                l_col = [str(i) for i in level_map[0]]
                r_col = [str(i) for i in level_map[-1]]
                self.left_dict["".join(r_col)].append(level_map)
                self.right_dict["".join(l_col)].append(level_map)

    def load_default(self):
        self.block_list = deque()
        for x, col in enumerate(default_level):
            new_col = []
            for y, block_num in enumerate(col):
                block_type = BlockType(block_num)
                if block_type == BlockType.DIRT:
                    new_col.append(GameObject(self.dirt_block_img, x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
                elif block_type == BlockType.GRASS:
                    new_col.append(GameObject(self.grass_block_img, x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size))
            self.block_list.append(new_col)
        self.left_margin = "".join([str(i) for i in default_level[0]])
        self.right_margin = "".join([str(i) for i in default_level[-1]])
        return self.block_list

    def shift(self, dx):
        for col in self.block_list:
            for block in col:
                block.rect.x += dx

    def create_left_level(self):
        if len(self.left_dict[self.left_margin]) == 0:
            next_level = default_level
            print("Non existing")
        else:
            next_level = random.choice(self.left_dict[self.left_margin])
        # start_x = self.block_list[0][0].rect.x - self.tile_size
        for x in range(len(next_level) - 1, -1, -1):
            new_col = []
            for y, block_num in enumerate(next_level[x]):
                block_type = BlockType(block_num)
                if block_type == BlockType.DIRT:
                    new_col.append(
                        GameObject(self.dirt_block_img, 0, y * self.tile_size, self.tile_size,
                                   self.tile_size))
                elif block_type == BlockType.GRASS:
                    new_col.append(
                        GameObject(self.grass_block_img, 0, y * self.tile_size, self.tile_size,
                                   self.tile_size))
            # start_x -= self.tile_size
            self.left_stack.appendleft(new_col)
        self.left_margin = "".join([str(i) for i in next_level[0]])

    def move_left(self, dx):
        i = 0
        while not self.block_list[i]:
            i += 1
        if self.block_list[i][0].rect.x - dx >= i*self.tile_size:
            # If left stack is empty, add level on the left
            if not self.left_stack:
                self.create_left_level()
            # Update x coordinate for blocks in the column
            column = self.left_stack.pop()
            for block in column:
                block.rect.x = self.block_list[i][0].rect.x - (i+1)*self.tile_size
            # Add columns on the left of block_list
            self.block_list.appendleft(column)
            self.right_stack.append(self.block_list.pop())
        self.shift(-dx)

    def create_right_level(self):
        if len(self.right_dict[self.right_margin]) == 0:
            next_level = default_level
            print("Non existing")
        else:
            next_level = random.choice(self.right_dict[self.right_margin])

        for col in next_level:
            new_col = []
            for y, block_num in enumerate(col):
                block_type = BlockType(block_num)
                if block_type == BlockType.DIRT:
                    new_col.append(
                        GameObject(self.dirt_block_img, 0, y * self.tile_size, self.tile_size,
                                   self.tile_size))
                elif block_type == BlockType.GRASS:
                    new_col.append(
                        GameObject(self.grass_block_img, 0, y * self.tile_size, self.tile_size,
                                   self.tile_size))
            self.right_stack.append(new_col)
            self.right_margin = "".join([str(i) for i in next_level[-1]])

    def move_right(self, dx):
        i = len(self.block_list)-1
        while not self.block_list[i]:
            i -= 1
        if self.block_list[i][0].rect.x - dx < self.screen_size - (len(self.block_list)-i) * self.tile_size:
            # If left stack is empty, add level on the left
            if not self.right_stack:
                self.create_right_level()
            # Update x coordinate for blocks in the column
            column = self.right_stack.pop()
            for block in column:
                block.rect.x = self.block_list[i][0].rect.x + (len(self.block_list)-i) * self.tile_size
            # Add columns on the left of block_list
            self.block_list.append(column)
            self.left_stack.append(self.block_list.popleft())
        self.shift(-dx)

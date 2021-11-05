import os
from collections import deque, defaultdict
import random
import pickle as pkl
import pygame

from myplatform.constants import default_level, BlockType, NUM_BLOCKS
from myplatform.objects import GameObject


# noinspection PyAttributeOutsideInit
class LevelGenerator:
    def __init__(self, tile_size, screen_size):
        # Stack for keeping track of columns out of sight
        self.left_stack = deque(maxlen=500)
        self.right_stack = deque(maxlen=500)

        self.tile_size = tile_size
        self.screen_size = screen_size

        self.load_images()
        self.load_levels()

    def load_images(self):
        """Load images for all blocks"""
        self.images = []
        for i in range(NUM_BLOCKS):
            self.images.append(pygame.image.load(f"./images/block{i + 1}.png"))

    def load_levels(self):
        """Load levels from file"""
        self.left_dict = defaultdict(list)
        self.right_dict = defaultdict(list)
        with open("./levels/all_levels.pkl", "rb") as fin:
            levels = pkl.load(fin)
            for level_map in levels:
                l_col = [str(i) for i in level_map[0]]
                r_col = [str(i) for i in level_map[-1]]
                self.left_dict["".join(r_col)].append(level_map)
                self.right_dict["".join(l_col)].append(level_map)

    def load_default(self) -> deque[list[GameObject]]:
        """Load starting level"""
        self.block_list = deque()
        for x, col in enumerate(default_level):
            new_col = self.convert_to_tiles(col, x)
            self.block_list.append(new_col)

        self.left_margin = "".join([str(i) for i in default_level[0]])
        self.right_margin = "".join([str(i) for i in default_level[-1]])
        return self.block_list

    def convert_to_tiles(self, column: list[int], x=0) -> list[GameObject]:
        """Convert a column to a list of tiles"""
        tiles_col = []
        for y, block_num in enumerate(column):
            if block_num != BlockType.EMPTY.value:
                tiles_col.append(GameObject(self.images[block_num], x * self.tile_size, y * self.tile_size,
                                            self.tile_size, self.tile_size))
        return tiles_col

    def shift(self, dx: int):
        """Move all tiles of dx pixels"""
        for col in self.block_list:
            for block in col:
                block.rect.x += dx

    def create_left_level(self):
        """Add level on the left of the screen"""
        if len(self.left_dict[self.left_margin]) == 0:
            next_level = default_level
            print("Non existing")
        else:
            next_level = random.choice(self.left_dict[self.left_margin])

        for x in range(len(next_level) - 1, -1, -1):
            new_col = self.convert_to_tiles(next_level[x])
            self.left_stack.appendleft(new_col)

        self.left_margin = "".join([str(i) for i in next_level[0]])

    def create_right_level(self):
        """Add new level to the right of the screen"""
        if len(self.right_dict[self.right_margin]) == 0:
            next_level = default_level
            print("Non existing")
        else:
            next_level = random.choice(self.right_dict[self.right_margin])

        for col in next_level:
            new_col = self.convert_to_tiles(col)
            self.right_stack.append(new_col)
        self.right_margin = "".join([str(i) for i in next_level[-1]])

    def move_left(self, dx):
        """Move screen to the left by dx pixels, loading a new column/level if necessary"""
        i = 0
        # Get position of last block on screen
        while not self.block_list[i]:
            i += 1
        if self.block_list[i][0].rect.x - dx >= i * self.tile_size:
            # If left stack is empty, add level on the left
            if not self.left_stack:
                self.create_left_level()
            # Update x coordinate for blocks in the column
            column = self.left_stack.pop()
            for block in column:
                block.rect.x = self.block_list[i][0].rect.x - (i + 1) * self.tile_size
            # Add columns on the left of block_list
            self.block_list.appendleft(column)
            self.right_stack.append(self.block_list.pop())
        self.shift(-dx)

    def move_right(self, dx):
        """Move screen to the right by dx pixels, loading a new column/level if necessary"""
        i = len(self.block_list) - 1
        while not self.block_list[i]:
            i -= 1
        if self.block_list[i][0].rect.x - dx < self.screen_size - (len(self.block_list) - i) * self.tile_size:
            # If right stack is empty, add level on the right stack
            if not self.right_stack:
                self.create_right_level()
            # Update x coordinates for blocks in the column
            column = self.right_stack.pop()
            for block in column:
                block.rect.x = self.block_list[i][0].rect.x + (len(self.block_list) - i) * self.tile_size
            # Add columns on the right of block_list
            self.block_list.append(column)
            self.left_stack.append(self.block_list.popleft())
        self.shift(-dx)

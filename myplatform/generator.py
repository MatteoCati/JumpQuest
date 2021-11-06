from collections import deque, defaultdict
import random
import pickle as pkl
import pygame

from myplatform.constants import default_level, NUM_BLOCKS, TILE_SIZE, BlockType
from myplatform.objects import GameObject, generate_tile, Coin


# noinspection PyAttributeOutsideInit
class LevelGenerator:
    def __init__(self, screen_size):
        # Stack for keeping track of columns out of sight
        self.right_stack = deque(maxlen=500)
        self.left_stack = deque(maxlen=500)
        self.screen_size = screen_size
        self.coin_probability = 1/4

        self.coins_list = pygame.sprite.Group()
        self.load_images()
        self.load_levels()

    def load_images(self):
        """Load images for all blocks"""
        self.images = []
        for i in range(NUM_BLOCKS):
            self.images.append(pygame.image.load(f"./images/block{i + 1}.png"))

    def load_levels(self):
        """Load levels from file"""
        self.creation_dict = defaultdict(list)
        with open("./levels/all_levels.pkl", "rb") as fin:
            levels = pkl.load(fin)
            for level_map in levels:
                l_col = [str(i) for i in level_map[0]]
                self.creation_dict["".join(l_col)].append(level_map)

    def load_default(self) -> deque[list[GameObject]]:
        """Load starting level"""
        self.block_list = deque()
        for x, col in enumerate(default_level):
            new_col = self.convert_to_tiles(col, x)
            self.block_list.append((new_col, col))
            for i in range(0, len(col) - 3):
                if col[i] == BlockType.EMPTY.value and col[i + 1] == BlockType.EMPTY.value and \
                        col[i + 2] != BlockType.EMPTY.value:
                    if random.random() < self.coin_probability:
                        coin = Coin(x, i)
                        self.coins_list.add(coin)
                        break
        self.margin = "".join([str(i) for i in default_level[-1]])
        return self.block_list

    def convert_to_tiles(self, column: list[int], x=0) -> list[GameObject]:
        """Convert a column to a list of tiles"""
        tiles_col = []
        for y, block_num in enumerate(column):
            tile = generate_tile(block_num, x, y, self.images[block_num])
            if tile:
                tiles_col.append(tile)

        return tiles_col

    def shift(self, dx: int):
        """Move all tiles of dx pixels"""
        for (col, _) in self.block_list:
            for block in col:
                block.rect.x += dx
        for coin in self.coins_list:
            coin.rect.x += dx

    def create_right_level(self):
        """Add new level to the right of the screen"""
        if len(self.creation_dict[self.margin]) == 0:
            next_level = default_level
            print("Non existing")
        else:
            next_level = random.choice(self.creation_dict[self.margin])
        for col in next_level:
            new_col = self.convert_to_tiles(col)
            self.right_stack.append((new_col, col))

        self.margin = "".join([str(i) for i in next_level[-1]])

    def move_left(self, dx):
        """Move screen to the left by dx pixels, loading a new column/level if necessary"""
        i = 0
        # Get position of last block on screen
        while not self.block_list[i][0]:
            i += 1
        if self.block_list[i][0][0].rect.x - dx >= i * TILE_SIZE:
            # If left stack is empty, add level on the left
            if not self.left_stack:
                return False

            # Update x coordinate for blocks in the column
            column, map = self.left_stack.pop()
            for block in column:
                block.rect.x = self.block_list[i][0][0].rect.x - (i + 1) * TILE_SIZE
            # Add columns on the left of block_list
            self.block_list.appendleft((column, map))
            self.right_stack.appendleft(self.block_list.pop())
        self.shift(-dx)
        return True

    def move_right(self, dx):
        """Move screen to the right by dx pixels, loading a new column/level if necessary"""
        last = len(self.block_list) - 1
        while not self.block_list[last][0]:
            last -= 1
        if self.block_list[last][0][0].rect.x - dx < self.screen_size - (len(self.block_list) - last) * TILE_SIZE:
            # If right stack is empty, add level on the right stack
            if not self.right_stack:
                self.create_right_level()
            # Update x coordinates for blocks in the column
            column, map = self.right_stack.popleft()
            for block in column:
                block.rect.x = self.block_list[last][0][0].rect.x + (len(self.block_list) - last) * TILE_SIZE
            for i in range(0, len(map) - 3):
                if map[i] == BlockType.EMPTY.value and map[i + 1] == BlockType.EMPTY.value and \
                        map[i + 2] != BlockType.EMPTY.value:
                    if random.random() < self.coin_probability:
                        coin = Coin(0, i)
                        coin.rect.center = (self.block_list[last][0][0].rect.x + (len(self.block_list) - last) * TILE_SIZE + TILE_SIZE//2, coin.rect.center[1])
                        self.coins_list.add(coin)
                        break
            # Add columns on the right of block_list
            self.block_list.append((column, map))
            self.left_stack.append(self.block_list.popleft())
        self.shift(-dx)

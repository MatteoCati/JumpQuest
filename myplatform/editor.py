import logging
import random

import pygame
from myplatform.button import Button
from myplatform.objects import generate_tile
from myplatform.constants import TILE_SIZE, BlockType, NUM_BLOCKS
import pickle as pkl
from collections import defaultdict


# noinspection PyAttributeOutsideInit
class Editor:
    BLACK = (0, 0, 0)
    GREEN = (144, 201, 120)
    WHITE = (255, 255, 255)
    RED = (200, 25, 25)

    def __init__(self, title="Level Editor", size=800, fps=120):
        self.size = size
        self.fps = fps

        self.screen_width = self.size + 300
        self.screen_height = self.size + 200

        pygame.init()
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption(title)

        # The level currently shown on screen
        self.level_map = [[-1 for _ in range(size // TILE_SIZE)] for _ in range(size // TILE_SIZE)]
        self.load_images()  # Load all images
        self.load_columns()  # Load possible margins
        self.add_last_column()  # Add a new columns on the right
        self.add_first_column()  # Add a new column on the left

        self.create_buttons()

        self.clock = pygame.time.Clock()
        self.play()

        pygame.quit()

    def create_buttons(self):
        """Create buttons with each block"""
        self.tile_buttons = []
        self.selected_tile = 0
        for i, tile in enumerate(self.tiles):
            obj = generate_tile(i, 0, 0, tile)
            self.tile_buttons.append(Button.fromGameObject(obj, self.size + 75 + (i % 2) * (TILE_SIZE + 50),
                                                           50 + (i // 2) * (TILE_SIZE + 50) + (
                                                           TILE_SIZE // 2 if i == BlockType.LOW_PLATFORM.value else 0)))
        # Create save button
        self.save_button = Button(self.size // 2, self.screen_height - 50, self.save_img)
        # Create load button
        self.load_button = Button(self.size // 2 + 200, self.screen_height - 50, self.load_img)

    def load_columns(self):
        """Load the columns for beginning / end of screen"""
        with open("./levels/last_columns.pkl", "rb") as fin:
            self.ending_columns = pkl.load(fin)
        self.already_existing_left = defaultdict(lambda: 0)
        self.already_existing_right = defaultdict(lambda: 0)
        i = 1

        with open("./levels/all_levels.pkl", "rb") as fin:
            levels = pkl.load(fin)
            for level_map in levels:
                l_col = [str(i) for i in level_map[0]]
                r_col = [str(i) for i in level_map[-1]]
                self.already_existing_left["".join(l_col)] += 1
                self.already_existing_right["".join(r_col)] += 1
            i += 1

    def add_first_column(self):
        """Change first column at random"""
        minimum = 2000
        index = [0]
        for idx, col in enumerate(self.ending_columns):
            s = "".join([str(i) for i in col])
            if self.already_existing_left[s] < minimum:
                minimum = self.already_existing_left[s]
                index = [idx]
            elif self.already_existing_left[s] == minimum:
                index.append(idx)
        logging.info("Minimum repetition on left side:", minimum, "/", len(self.ending_columns))
        self.level_map[0] = self.ending_columns[random.choice(index)]

    def add_last_column(self):
        """Change last column at random"""
        self.level_map[-1] = random.choice(self.ending_columns)

    def load_images(self):
        """Load all necessary images"""
        self.sun_img = pygame.image.load("./images/sun.png")
        self.background_img = pygame.image.load("./images/background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.size, self.size))
        self.tiles = []
        for i in range(1, NUM_BLOCKS + 1):
            self.tiles.append(pygame.image.load(f"./images/block{i}.png"))
        self.save_img = pygame.image.load('./images/save_btn.png').convert_alpha()
        self.load_img = pygame.image.load('./images/load_btn.png').convert_alpha()

    def draw_grid(self):
        """Draw grid on the screen"""
        for i in range(self.size // TILE_SIZE):
            pygame.draw.line(self.screen, self.BLACK, (TILE_SIZE * i, 0), (TILE_SIZE * i, self.size))
            pygame.draw.line(self.screen, self.BLACK, (TILE_SIZE, TILE_SIZE * i),
                             (self.size - TILE_SIZE, TILE_SIZE * i))

    def draw_background(self):
        """Draw background on screen"""
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.sun_img, (80, 80))
        pygame.draw.rect(self.screen, self.GREEN, (self.size, 0, self.screen_width, self.screen_height))
        pygame.draw.rect(self.screen, self.GREEN, (0, self.size, self.screen_width, self.screen_height))

    def draw_world(self):
        """Draw all tiles on screen"""
        for x in range(self.size // TILE_SIZE):
            for y in range(self.size // TILE_SIZE):
                block = self.level_map[x][y]
                tile = generate_tile(block, x, y, self.tiles[block])
                if tile:
                    tile.draw(self.screen)

    def save_level(self):
        all_levels = []
        with open("./levels/all_levels.pkl", "rb") as fin:
            all_levels = pkl.load(fin)
        all_levels.append(self.level_map)
        with open("./levels/all_levels.pkl", "wb") as fout:
            pkl.dump(all_levels, fout)
        l_col = "".join([str(i) for i in self.level_map[0]])
        r_col = "".join([str(i) for i in self.level_map[-1]])
        self.already_existing_left[l_col] += 1
        self.already_existing_right[r_col] += 1
        logging.info("Saved!")

    def check_buttons(self):
        """Check if any button is being pressed and update it"""
        for i, button in enumerate(self.tile_buttons):
            if button.draw(self.screen):
                self.selected_tile = i
        pygame.draw.rect(self.screen, self.RED, self.tile_buttons[self.selected_tile].rect, 3)

        if self.save_button.draw(self.screen):
            self.save_level()

        if self.load_button.draw(self.screen):
            self.level_map = [[-1 for _ in range(self.size // TILE_SIZE)] for _ in range(self.size // TILE_SIZE)]
            self.add_first_column()
            self.add_last_column()

    def update(self):
        """Update the screen"""
        self.clock.tick(self.fps)

        self.draw_background()
        self.draw_grid()
        self.draw_world()

        self.check_buttons()
        pygame.display.update()

    def play(self):
        """Run the application"""
        run = True
        while run:
            self.update()

            pos = pygame.mouse.get_pos()
            x = pos[0] // TILE_SIZE
            y = pos[1] // TILE_SIZE
            if TILE_SIZE < pos[0] < self.size - TILE_SIZE and pos[1] < self.size:
                if pygame.mouse.get_pressed()[0]:
                    self.level_map[x][y] = self.selected_tile
                if pygame.mouse.get_pressed()[2]:
                    self.level_map[x][y] = -1

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False

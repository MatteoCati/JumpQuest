import pygame
from myplatform.constants import BlockType
from myplatform.objects import GameObject, Player
from collections import deque
from myplatform.generator import LevelGenerator


# noinspection PyAttributeOutsideInit
class Game:
    def __init__(self, title="Platform Game", size=800, fps=60):
        self.size = size
        self.fps = fps
        self.tile_size = 50

        pygame.init()
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption(title)

        self.load_images()
        self.generator = LevelGenerator(self.tile_size, self.size)
        self.block_list = self.generator.load_default()
        self.player = Player(self.size//2, 0, 40, 80)

        self.clock = pygame.time.Clock()
        self.play()
        pygame.quit()

    def play(self):
        run = True
        while run:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            self.update()
            if self.player.rect.y > self.size:
                run = False

    def load_images(self):
        self.sun_img = pygame.image.load("./images/sun.png")
        self.background_img = pygame.image.load("./images/background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.size, self.size))

    def update(self):
        self.clock.tick(self.fps)
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.sun_img, (80, 80))

        self.player.update(self)
        #print(len(self.block_list))
        for col in self.block_list:
            for block in col:
                block.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.update()

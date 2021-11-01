import pygame
from myplatform.constants import default_level, BlockType
from myplatform.objects import GameObject, Player


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
        self.load_level()
        self.player = Player(self.tile_size, self.size - self.tile_size -80, 40, 80)

        self.clock = pygame.time.Clock()
        self.play()

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
        self.grass_block_img = pygame.image.load("./images/grass.png")
        self.dirt_block_img = pygame.image.load("./images/dirt.png")

    def load_level(self):
        self.block_list = []
        for x in range(len(default_level)):
            for y in range(len(default_level)):
                if default_level[x][y] == BlockType.GRASS:
                    obj = GameObject(self.grass_block_img, x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                    self.block_list.append(obj)
                elif default_level[x][y] == BlockType.DIRT:
                    obj = GameObject(self.dirt_block_img, x*self.tile_size, y*self.tile_size, self.tile_size, self.tile_size)
                    self.block_list.append(obj)

    def update(self):
        self.clock.tick(self.fps)
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.sun_img, (80, 80))

        self.player.update(self.block_list, self.size)

        for block in self.block_list:
            block.draw(self.screen)
        self.player.draw(self.screen)
        pygame.display.update()

import pygame
from myplatform.objects import Player
from myplatform.generator import LevelGenerator


# noinspection PyAttributeOutsideInit
class Game:
    def __init__(self, title="Platform Game", size=800, fps=60):
        self.size = size
        self.fps = fps

        pygame.init()
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption(title)

        self.load_images()
        self.generator = LevelGenerator(self.size)
        self.block_list = self.generator.load_default()
        self.player = Player(self.size//2, 0, 40, 80)

        self.clock = pygame.time.Clock()
        self.play()
        pygame.quit()

    def play(self):
        """Play the game"""
        run = True
        while run:
            # Check if window has been closed
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
            # Update screen
            self.update()
            # Check if player has lost
            if self.player.rect.y > self.size:
                run = False

    def load_images(self):
        """Load all necessary images"""
        self.sun_img = pygame.image.load("./images/sun.png")
        self.background_img = pygame.image.load("./images/background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.size, self.size))

    def update(self):
        """Update the screen"""
        self.clock.tick(self.fps)
        # Update background
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.sun_img, (80, 80))
        # Update player position
        self.player.update(self)
        # Draw all tiles
        for col in self.block_list:
            for block in col:
                block.draw(self.screen)
        self.player.draw(self.screen)
        # Show updates on screen
        pygame.display.update()

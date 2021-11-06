import pygame

from myplatform.button import Button
from myplatform.constants import TILE_SIZE
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
        self.load_buttons()
        self.play()
        pygame.quit()

    def start_game(self):
        self.generator = LevelGenerator(self.size)
        self.block_list = self.generator.load_default()
        self.player = Player(self.size // 2, 0, 40, 80)

        self.clock = pygame.time.Clock()
        self.game_over = False

    def load_buttons(self):
        restart_img = pygame.image.load("./images/restart_btn.png").convert_alpha()
        self.restart_btn = Button(self.size//2 - TILE_SIZE, self.size//2, restart_img)

    def play(self):
        """Play the game"""
        run = True

        self.start_game()
        while run:
            # Check if window has been closed

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                    self.game_over = True
            # Update screen
            self.update()
            # Check if player has lost
            if self.player.rect.y > self.size:
                self.game_over = True

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
        if self.game_over:
            if self.restart_btn.draw(self.screen):
                print("restart")
                self.start_game()

        pygame.display.update()

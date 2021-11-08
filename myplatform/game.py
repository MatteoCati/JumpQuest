import logging

import pygame

from myplatform.button import Button
from myplatform.constants import TILE_SIZE
from myplatform.objects import Player
from myplatform.generator import LevelGenerator


# noinspection PyAttributeOutsideInit
class Game:
    BLACK = (0, 0, 0)
    BLUE = (0, 0, 255)

    def __init__(self, title="Jump Quest", size=800, fps=60):
        self.size = size
        self.fps = fps

        pygame.mixer.pre_init()
        pygame.mixer.init()
        pygame.init()
        self.screen = pygame.display.set_mode((size, size))
        pygame.display.set_caption(title)

        self.score_font = pygame.font.SysFont("Bauhaus 92", 30, True)
        self.font = pygame.font.SysFont("Bauhaus 92", 70, True)

        self.load_images()
        self.load_buttons()
        self.load_sounds()
        self.play()
        pygame.quit()

    def start_game(self):
        self.generator = LevelGenerator(self.size)
        self.generator.load_default()
        self.player = Player(self.size // 2, 0, 40, 80)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.score = 0

    def load_sounds(self):
        self.coin_sound = pygame.mixer.Sound("./sounds/sound_coin.wav")
        self.coin_sound.set_volume(0.5)
        self.game_over_sound = pygame.mixer.Sound("./sounds/sound_game_over.wav")
        self.game_over_sound.set_volume(0.5)
        self.jump_sound = pygame.mixer.Sound("./sounds/sound_jump.wav")
        self.jump_sound.set_volume(0.5)

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
            # Update screen
            self.update()
            # Check if player has lost
            if self.player.rect.y > self.size:
                self.lose_game()

    def lose_game(self):
        self.game_over = True
        self.game_over_sound.play()

    def load_images(self):
        """Load all necessary images"""
        self.sun_img = pygame.image.load("./images/sun.png")
        self.background_img = pygame.image.load("./images/background.png")
        self.background_img = pygame.transform.scale(self.background_img, (self.size, self.size))
        icon = pygame.image.load("./images/block1.png")
        pygame.display.set_icon(icon)

    def update(self):
        """Update the screen"""
        self.clock.tick(self.fps)
        # Update background
        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(self.sun_img, (80, 80))
        # Update player position
        self.player.update(self)
        self.generator.enemies_group.update()
        # Draw all tiles
        self.generator.tiles_group.draw(self.screen)
        self.generator.enemies_group.draw(self.screen)
        self.player.draw(self.screen)
        self.generator.coins_group.draw(self.screen)
        # Check collision with coins
        if pygame.sprite.spritecollide(self.player, self.generator.coins_group, True):
            self.score += 1
            self.coin_sound.play()
        # Draw score text
        score_txt = self.score_font.render("Score: " + str(self.score), True, self.BLACK)
        self.screen.blit(score_txt, (25, 25))
        # Show game over screen
        if self.game_over:
            if self.restart_btn.draw(self.screen):
                logging.debug("restart")
                self.start_game()
            gameover_txt = self.font.render("Game Over!", True, self.BLUE)
            txt_pos = (self.size//2 - gameover_txt.get_width()//2, 300)
            self.screen.blit(gameover_txt, txt_pos)
        # Update screen
        pygame.display.update()

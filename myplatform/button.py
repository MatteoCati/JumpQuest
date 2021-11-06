import pygame


# button class
from myplatform.objects import GameObject


class Button:
    def __init__(self, x, y, image):
        """Create a button at position x, y and icon image"""
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.clicked = False

    @classmethod
    def fromGameObject(cls, obj: GameObject, x, y):
        return cls(x, y, obj.image)

    def draw(self, surface):
        """Draw the button on the surface.
        Return True if the button has been clicked, False otherwise."""
        action = False
        # get mouse position
        pos = pygame.mouse.get_pos()
        # check mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        # draw button
        surface.blit(self.image, (self.rect.x, self.rect.y))
        return action

import pygame
from myplatform.constants import Direction


class GameObject:
    def __init__(self, image: pygame.Surface, x: int, y: int, width: int, height: int):
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.image, self.rect)

    def check_collision(self, rectangle):
        return self.rect.colliderect(rectangle)


# noinspection PyAttributeOutsideInit
class Player(GameObject):
    def __init__(self, x, y, width, height):
        self.width = width
        self.height = height

        # Load images
        self.image_idx = 0
        self.load_images()

        # call init
        super().__init__(self.right_images[self.image_idx], x, y, width, height)

        # Movement controls
        self.velocity = [0, 0]
        self.counter = 0
        self.direction = Direction.RIGHT
        self.is_jumping = False

    def update(self, world: list[GameObject], height):
        # Check movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.velocity[0] = -5
            self.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            self.velocity[0] = 5
            self.direction = Direction.RIGHT
        else:
            self.velocity[0] = 0
        if keys[pygame.K_SPACE] and not self.is_jumping:
            self.is_jumping = True
            self.velocity[1] = -15

        self.velocity[1] += 1
        dx = self.velocity[0]
        dy = self.velocity[1]
        for tile in world:
            # check for collision in x direction
            if tile.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                dx = 0
            # check for collision in y direction
            if tile.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                # check if below the ground i.e. jumping
                if self.velocity[1] < 0:
                    dy = tile.rect.bottom - self.rect.top
                    self.velocity[1] = 0
                # check if above the ground i.e. falling
                elif self.velocity[1] >= 0:
                    dy = tile.rect.top - self.rect.bottom
                    self.is_jumping = False
                    self.velocity[1] = 0

        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen):
        # Update image index
        if self.velocity[0] == 0:
            self.image_idx = 0
        else:
            self.counter += 1
            if self.counter == 10:
                self.counter = 0
                self.image_idx = (self.image_idx + 1) % len(self.left_images)

        # Choose image direction
        if self.direction == Direction.LEFT:
            self.image = self.left_images[self.image_idx]
        else:
            self.image = self.right_images[self.image_idx]
        super().draw(screen)

    def load_images(self):
        self.left_images = []
        self.right_images = []
        for i in range(1, 5):
            img = pygame.image.load(f"./images/player{i}.png")
            img = pygame.transform.scale(img, (self.width, self.height))
            self.right_images.append(img)
            self.left_images.append(pygame.transform.flip(img, True, False))

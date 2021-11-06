import pygame
from myplatform.constants import Direction, BlockType, TILE_SIZE


def generate_tile(block_num, x, y, image):
    block_type = BlockType(block_num)
    tile = None
    if block_type == BlockType.GRASS:
        tile = GameObject(image, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    elif block_type == BlockType.DIRT:
        tile = GameObject(image, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    elif block_type == BlockType.PLATFORM:
        tile = GameObject(image, x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE//2)
    elif block_type == BlockType.LOW_PLATFORM:
        tile = GameObject(image, x*TILE_SIZE, y*TILE_SIZE + TILE_SIZE//2, TILE_SIZE, TILE_SIZE//2)
    return tile


class GameObject:
    def __init__(self, image: pygame.Surface, x: int, y: int, width: int, height: int):
        """An object with specified image and position"""
        self.width = width
        self.height = height
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        """Draw the tile on screen"""
        screen.blit(self.image, self.rect)

    def check_collision(self, rectangle: pygame.Surface) -> bool:
        """Check if is colliding with other object"""
        return self.rect.colliderect(rectangle)


# noinspection PyAttributeOutsideInit
class Player(GameObject):
    def __init__(self, x, y, width, height):
        """The object representing the player"""
        self.width = width
        self.height = height

        # Load images
        self.image_idx = 0
        self.load_images()

        # call init of GameObject
        super().__init__(self.right_images[self.image_idx], x, y, width, height)

        # Movement controls
        self.velocity = [0, 0]  # velocity in x and y direction
        self.counter = 0  # counter for checking if image should be updated
        self.direction = Direction.RIGHT  # Current direction
        self.is_jumping = False  # IS player pressing key for jumping
        self.jump_time = 0  # 0=no jump, 1=single jump, 2=double jump

    def update(self, world):
        """Update position of the player"""
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            # Move left
            self.velocity[0] = -5
            self.direction = Direction.LEFT
        elif keys[pygame.K_RIGHT]:
            # Move right
            self.velocity[0] = 5
            self.direction = Direction.RIGHT
        else:
            # Stay still
            self.velocity[0] = 0
        if keys[pygame.K_SPACE] and not self.is_jumping and self.jump_time < 2:
            # Jump
            self.is_jumping = True
            self.jump_time += 1
            self.velocity[1] = -15
        if not keys[pygame.K_SPACE]:
            self.is_jumping = False

        self.velocity[1] += 1  # Add negative velocity (gravity)
        dx = self.velocity[0]
        dy = self.velocity[1]
        for col in world.block_list:
            for tile in col:
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
                        self.jump_time = 0
                        self.velocity[1] = 0
        # If near right border, move background instead
        if self.rect.x + dx > 0.70*world.size:
            world.generator.move_right(dx)
            dx = 0
        # If near left border, move background instead
        elif self.rect.x + dx < 0.3*world.size:
            world.generator.move_left(dx)
            dx = 0
        # Update x and y position
        self.rect.x += dx
        self.rect.y += dy

    def draw(self, screen: pygame.Surface):
        """Draw player on the screen"""
        # Update image index
        if self.velocity[0] == 0:
            self.image_idx = 0
        else:
            self.counter += 1
            # Update image every 10 frames
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
        """Load all images of the player"""
        self.left_images = []
        self.right_images = []
        for i in range(1, 5):
            img = pygame.image.load(f"./images/player{i}.png")
            img = pygame.transform.scale(img, (self.width, self.height))
            self.right_images.append(img)
            self.left_images.append(pygame.transform.flip(img, True, False))

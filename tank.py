import pygame
import os
import math

class Tank:
    def __init__(self, position, speed):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.direction = 90  # 90 degrees mean facing north
        image_path = os.path.join('resources', 'tank.png')
        self.original_image = pygame.image.load(image_path)
        self.image = self.original_image.copy()  # Start without rotation
        
    def update(self, rotation_step, move_forward_steps):
        # Update the direction
        self.direction += rotation_step
        # Ensure the direction stays within 0-360 degrees
        self.direction %= 360

        # Rotate the image
        self.image = pygame.transform.rotate(self.original_image, -self.direction + 90)
        
        # Scale down the image
        self.image = pygame.transform.scale(self.image, (int(self.image.get_width() * 0.6), int(self.image.get_height() * 0.6)))

        # Move the tank
        radian = math.radians(self.direction)
        self.position.x -= move_forward_steps * self.speed * math.cos(radian)
        self.position.y -= move_forward_steps * self.speed * math.sin(radian)  # Negative for moving up

    def draw(self, screen):
        # Correct the position of the image to be centered
        rotated_rect = self.image.get_rect(center=self.position)
        screen.blit(self.image, rotated_rect.topleft)

    def get_position(self):
        return self.position

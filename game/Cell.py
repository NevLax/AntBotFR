import pygame
from game.consts import DEFAULT_IMAGE_SIZE
from game.Robot import Robot

pygame.init()


class Cell:
    colors = {
        'w': (255, 255, 255),  # White
        'b': (199, 210, 225),  # Blue
        'r': (222, 74, 74),  # Red
        'y': (254, 251, 216),  # Yellow
        'a': (187, 219, 181),  # Green
        'g': (200, 200, 194)   # Gray
    }

    def __init__(self, y, x, color='w', target=0, robot=None):
        self.x = x
        self.y = y
        self.color = color
        self.target = target
        self.robot = robot
        self.package = None

        if self.target:
            target_font = pygame.font.SysFont(None, 64)
            self.img = target_font.render(str(self.target), True, (0, 0, 0))

    def display_cell(self, screen):
        pygame.draw.rect(screen, Cell.colors[self.color],
                         ((self.x + 1) * DEFAULT_IMAGE_SIZE[0],
                          (self.y + 1) * DEFAULT_IMAGE_SIZE[1],
                          DEFAULT_IMAGE_SIZE[0],
                          DEFAULT_IMAGE_SIZE[1]))

        pygame.draw.rect(screen, (0, 0, 0),
                         ((self.x + 1) * DEFAULT_IMAGE_SIZE[0],
                          (self.y + 1) * DEFAULT_IMAGE_SIZE[1],
                          DEFAULT_IMAGE_SIZE[0],
                          DEFAULT_IMAGE_SIZE[1]), 1)

        if self.target:
            target_font = pygame.font.SysFont(None, 64)
            img = target_font.render(str(self.target), True, (0, 0, 0))
            screen.blit(img, ((self.x + 1) * DEFAULT_IMAGE_SIZE[0] + (DEFAULT_IMAGE_SIZE[0] - img.get_width()) / 2,
                              (self.y + 1) * DEFAULT_IMAGE_SIZE[1] + (DEFAULT_IMAGE_SIZE[1] - img.get_height()) / 2))

        if self.robot:
            self.robot.RobotAnimator(screen)

        if self.package and self.package.visible:
            package_image = pygame.image.load('images/package.png')
            package_image = pygame.transform.scale(package_image,
                                                   (DEFAULT_IMAGE_SIZE[0] * 2, DEFAULT_IMAGE_SIZE[1] * 2))
            package_pos = (
                (self.x + 1) * DEFAULT_IMAGE_SIZE[0] + (DEFAULT_IMAGE_SIZE[0] - package_image.get_width()) / 2,
                (self.y + 2) * DEFAULT_IMAGE_SIZE[1] - package_image.get_height() / 2
            )
            screen.blit(package_image, package_pos)

            package_number_font = pygame.font.SysFont(None, 48)
            number_img = package_number_font.render(str(self.package.number), True, (0, 0, 0))
            number_pos = (
                package_pos[0] + package_image.get_width() / 2 - number_img.get_width() / 2,
                package_pos[1] + package_image.get_height() / 2 - number_img.get_height() / 2 - 40
            )
            screen.blit(number_img, number_pos)

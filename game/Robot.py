import logging
import random
import pygame
from game.Package import Package
from game.consts import DEFAULT_IMAGE_SIZE


class Robot:
    image_paths = {
        0: 'images/blue_robot.png',     # blue
        1: 'images/red_robot.png',      # red
        2: 'images/green_robot.png',    # green
        3: 'images/orange_robot.png'    # orange
    }

    def __init__(self, pos, index, player, width=DEFAULT_IMAGE_SIZE[0], height=DEFAULT_IMAGE_SIZE[1]):
        self.player = player
        self.number_img = None
        self.pos = pos
        self.package = None
        self.index = index
        self.set_number_image()
        self.image = pygame.transform.scale(pygame.image.load(Robot.image_paths[player.id]), (width, height))
        self.rect = self.image.get_rect(topleft=((pos[0] + 1) * width, (pos[1] + 1) * height))

    def move(self, new_pos):
        self.pos = new_pos
        self.animate_move()

    def animate_move(self, steps=10):
        new_x, new_y = self.pos
        old_rect = self.rect.copy()
        step_x = ((new_x + 1) * DEFAULT_IMAGE_SIZE[0] - old_rect.x) / steps
        step_y = ((new_y + 1) * DEFAULT_IMAGE_SIZE[1] - old_rect.y) / steps
        for i in range(steps):
            self.rect.x = old_rect.x + step_x * (i + 1)
            self.rect.y = old_rect.y + step_y * (i + 1)
            self.player.game_manager.simulator.ScreenAnimator()
            pygame.display.flip()
            pygame.time.delay(5)

    def pick_package(self, package) -> Package:
        self.package = package
        package.pick_up()
        logging.info(
            f"Robot {self.index} of Player {self.player.id + 1} picked up package with number {package.number} at position ({chr(ord('A') + (self.pos[0]))}, {self.pos[1] + 1}).")
        new_package = Package(package.pos)
        new_package.number = random.randint(1, 9)
        return new_package

    def drop_package(self, cell):
        if not self.package:
            return False
        logging.info(
            f"Robot {self.index} of Player {self.player.idx + 1} dropped package with number {self.package.number} at position ({chr(ord('A') + (self.pos[0]))}, {self.pos[1] + 1}).")
        self.package.drop_off()
        self.package = None
        cell.package = None
        return True

    def robot_animator(self, screen):
        screen.blit(self.image, self.rect)
        if self.number_img:
            number_pos = (
                self.rect.x + self.rect.width // 2 - self.number_img.get_width() // 2,
                self.rect.y + self.rect.height // 2 - self.number_img.get_height() // 2
            )
            screen.blit(self.number_img, number_pos)
        if self.package:
            package_image = pygame.image.load('images/package.png')
            package_image = pygame.transform.scale(package_image,
                                                   (DEFAULT_IMAGE_SIZE[0] * 1.3, DEFAULT_IMAGE_SIZE[1] * 1.3))
            package_pos = (
                self.rect.x + self.rect.width // 2 - package_image.get_width() // 2,
                self.rect.y - self.rect.height // 2 + DEFAULT_IMAGE_SIZE[0] * 0.38
            )
            screen.blit(package_image, package_pos)
            package_number_font = pygame.font.SysFont(None, 48)
            number_img = package_number_font.render(str(self.package.number), True, (0, 0, 0))
            number_pos = (
                package_pos[0] + package_image.get_width() // 2 - number_img.get_width() // 2,
                package_pos[1] + package_image.get_height() // 2 - number_img.get_height() * 1.4  # Смещение выше
            )
            screen.blit(number_img, number_pos)

    def set_number_image(self):
        robot_number_font = pygame.font.SysFont(None, 32)
        self.number_img = robot_number_font.render(str(self.index), True, (0, 0, 0))

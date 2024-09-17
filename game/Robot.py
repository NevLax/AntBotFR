import logging
import random
import pygame
from game.Package import Package
from game.consts import DEFAULT_IMAGE_SIZE


class Robot:
    image_paths = {
        'blue': 'images/blue_robot.png',
        'red': 'images/red_robot.png',
        'green': 'images/green_robot.png',
        'orange': 'images/orange_robot.png'
    }

    def __init__(self, color, pos, index, player, width=DEFAULT_IMAGE_SIZE[0], height=DEFAULT_IMAGE_SIZE[1]):
        self.number_img = None
        self.color = color
        self.pos = pos
        self.has_package = False
        self.package = None
        self.index = index
        self.set_number_image()
        image = pygame.image.load(Robot.image_paths[color])
        self.image = pygame.transform.scale(image, (width, height))
        self.rect = self.image.get_rect(topleft=((pos[0] + 1) * width, (pos[1] + 1) * height))
        self.player = player

    def move(self, direction, board, animation_steps=10):
        """Движение роботов"""
        x, y = self.pos
        new_x, new_y = x, y
        if direction == "up" and y > 0:
            new_y = y - 1
        elif direction == "down" and y < board.size - 1:
            new_y = y + 1
        elif direction == "left" and x > 0:
            new_x = x - 1
        elif direction == "right" and x < board.size - 1:
            new_x = x + 1
        else:
            return False
        if 0 <= new_x < board.size and 0 <= new_y < board.size:
            if not board.is_occupied((new_x, new_y)):
                target_cell = board[new_y][new_x]
                if target_cell.color == 'r':
                    logging.info(
                        f"Robot {self.index} of Player {self.player.idx + 1} tried to move to a red cell at ({chr(ord('A') + new_x)}, {new_y + 1}). Move cancelled.")
                    return False
                if target_cell.target > 0 and (not self.package or self.package.number != target_cell.target):
                    logging.info(
                        f"Robot {self.index} of Player {self.player.idx + 1} tried to move to a target cell with "
                        f"incompatible package at ({chr(ord('A') + new_x)}, {new_y + 1}). Move cancelled.")
                    return False
                old_rect = self.rect.copy()
                self.animate_move(old_rect, new_x, new_y, animation_steps, board)
                board.update_position(self.pos, (new_x, new_y))
                self.pos = (new_x, new_y)
                self.rect.topleft = ((new_x + 1) * DEFAULT_IMAGE_SIZE[0], (new_y + 1) * DEFAULT_IMAGE_SIZE[1])
                logging.info(
                    f"Player {self.player.idx + 1} moved robot {self.index} {direction} to ({chr(ord('A') + new_x)}, {new_y + 1}).")
                # Execute additional actions after movement
                if target_cell.target and self.package and target_cell.target == self.package.number:
                    self.drop_package(target_cell)
                if not self.has_package:
                    if target_cell.color == 'a':
                        below_cell = board[new_y + 1][new_x]
                        if below_cell.color == 'r' and below_cell.package and not below_cell.package.picked_up:
                            self.pick_package(below_cell.package, board)
                if self.package:
                    self.package.set_position(self.pos)
                return True
        return False

    def animate_move(self, old_rect, new_x, new_y, steps, board):
        """Анимация движения: Анимация движения робота, чтобы робот двигался плавно"""
        step_x = ((new_x + 1) * DEFAULT_IMAGE_SIZE[0] - old_rect.x) / steps
        step_y = ((new_y + 1) * DEFAULT_IMAGE_SIZE[1] - old_rect.y) / steps
        for i in range(steps):
            self.rect.x = old_rect.x + step_x * (i + 1)
            self.rect.y = old_rect.y + step_y * (i + 1)
            self.player.game_manager.simulator.ScreenAnimator()
            pygame.display.flip()
            pygame.time.delay(5)

    def pick_package(self, package, board):
        """Робот поднял посылку с зеленой клетки"""
        self.has_package = True
        self.package = package
        package.pick_up()
        logging.info(
            f"Robot {self.index} of Player {self.player.idx + 1} picked up package with number {package.number} at position ({chr(ord('A') + (self.pos[0]))}, {self.pos[1] + 1}).")
        new_package = Package(package.pos)
        new_package.number = random.randint(1, 9)
        board[package.pos[1]][package.pos[0]].package = new_package

    def drop_package(self, cell):
        """Робот сдал посылку с соответствующим номером в пункт приема отмеченной цифрой"""
        if not self.has_package:
            return False
        logging.info(
            f"Robot {self.index} of Player {self.player.idx + 1} dropped package with number {self.package.number} at position ({chr(ord('A') + (self.pos[0]))}, {self.pos[1] + 1}).")
        self.player.increase_score(self.package.number, self.player.game_manager)
        self.package.drop_off()
        self.package = None
        self.has_package = False
        cell.package = None
        return True

    def RobotAnimator(self, screen):
        """Анимирует робота"""
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

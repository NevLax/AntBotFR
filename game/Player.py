import pygame
import logging
from game.Robot import Robot


class Player:
    def __init__(self, color):
        self.id = color
        self.robots = []
        self.score = 0

    def add_robot(self, robot):
        self.robots.append(robot)

    def draw_robots(self, screen):
        for robot in self.robots:
            robot.RobotAnimator(screen)

    def increase_score(self, points):
        self.score += points
        logging.info(f"Player's {self.id + 1} score is now {self.score}.")

    def win(self):
        logging.info(f"Player {self.id + 1} reached the winning score. Resetting the game.")

    def draw_score(self, screen, position):
        font = pygame.font.SysFont(None, 36)
        score_text = f"({self.id + 1}) Player: {self.score} points"
        img = font.render(score_text, True, (0, 0, 0))
        screen.blit(img, position)

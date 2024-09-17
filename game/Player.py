import pygame
import logging
from game.Robot import Robot


class Player:
    def __init__(self, color, num_robots, idx, move_limit_per_turn, game_manager):
        self.color = color
        self.idx = idx
        self.num_robots = num_robots
        self.robots = []
        self.score = 0
        self.move_limit_per_turn = move_limit_per_turn
        self.remaining_moves = move_limit_per_turn
        self.game_manager = game_manager

    def reset_moves(self):
        """Сброс ходов: Сбрасывает количество оставшихся ходов до начального значения"""
        self.remaining_moves = self.move_limit_per_turn

    def place_robot(self, pos, board, robot_index):
        """Размещение робота: Устанавливает робота на доске"""
        if not board.is_occupied(pos) and board[pos[0]][pos[1]].color == 'w':
            board.occupied(pos)
            robot = Robot(self.color, pos, robot_index + 1, self)
            self.robots.append(robot)
            return True
        return False

    def move_robot(self, robot_index, direction, board):
        """Движение робота: Перемещает робота в указанном направлении"""
        if 0 <= robot_index < len(self.robots) and self.remaining_moves > 0:
            if self.robots[robot_index].move(direction, board):
                self.remaining_moves -= 1
                return True
        return False

    def draw_robots(self, screen):
        """Отображение роботов: Рисует роботов на экране"""
        for robot in self.robots:
            robot.RobotAnimator(screen)

    def increase_score(self, points, game_manager):
        """Отображение роботов: Рисует роботов на экране"""
        self.score += points
        logging.info(f"Player's {self.idx + 1} score is now {self.score}.")
        if self.score >= game_manager.config.win_score:
            logging.info(f"Player {self.idx + 1} reached the winning score. Resetting the game.")
            game_manager.reset_game()

    def draw_score(self, screen, position):
        """Отображение счета: Рисует счет игрока на экране"""
        font = pygame.font.SysFont(None, 36)
        score_text = f"{self.color.capitalize()} ({self.idx + 1}) Player: {self.score} points"
        img = font.render(score_text, True, (0, 0, 0))
        screen.blit(img, position)

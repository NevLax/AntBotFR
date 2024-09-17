import pygame
import logging
from game.consts import DEFAULT_IMAGE_SIZE
import time


def index_to_letter(index):
    return chr(ord('A') + index)


class PlayerSimulator:
    def __init__(self, players, board, screen, game_manager):
        self.players = players
        self.board = board
        self.screen = screen
        self.current_player = 0
        self.current_robot_index = 0
        self.current_robot_counts = [0] * len(players)
        self.total_robots_to_place = len(players) * players[0].num_robots
        self.robots_placed = 0
        self.placing_phase = True
        self.place_initial_packages()

    def place_initial_packages(self):
        """Начальный этап: Размещение начальных посылок на доске"""
        red_cells = self.board.get_cells_by_color('r')
        for i, cell in enumerate(red_cells):
            package = self.board.place_package((cell.x, cell.y))
            package.visible = False

    def update_package_visibility(self, placing_phase):
        """Обновление видимости: Обновление видимости пакетов в зависимости от фазы размещения"""
        self.placing_phase = placing_phase
        for row in self.board.cells:
            for cell in row:
                if cell.package:
                    cell.package.visible = not placing_phase

    def place_robot_at_position(self, cell_x, cell_y):
        """Размещение робота: Размещение робота на доске, функция - в которой сейчас проблемы. Я не знаю,
        как их решать, если поставить if-условие размещения всех роботов - после размещения всех роботов игра встает
        и никуда не двигается. Видимо, дело в placing phase. А может и нет, слабо понимаю, что происходит"""
        if 0 <= cell_x < self.board.size and 0 <= cell_y < self.board.size:
            current_player = self.players[self.current_player]  # Используем current_player из GameManager
            if current_player.place_robot((cell_x, cell_y), self.board,
                                          self.current_robot_counts[self.current_player]):
                logging.info(
                    f"Player {self.current_player + 1} placed robot at ({index_to_letter(cell_x)}, {cell_y + 1}).")
                self.current_robot_counts[self.current_player] += 1
                self.robots_placed += 1
                if self.robots_placed >= self.total_robots_to_place:
                    logging.info("Placing phase ended. All players have placed their robots.")
                    self.current_player = 0
                    self.placing_phase = False
                    self.update_package_visibility(self.placing_phase)
                    return True
                self.current_player = (self.current_player + 1) % len(self.players)
                time.sleep(0.2)  # Задержка в одну секунду
        return False

    def execute_put_bot(self, player_index, pos):
        """Установка бота для второго режима, его можно не трогать, я его по приколу сделала, потому что
         научник попросил. Я спорить с ним боюсь"""
        row = int(pos[1]) - 1
        col = ord(pos[0].lower()) - ord('a')
        if self.players[player_index].place_robot((col, row), self.board, len(self.players[player_index].robots)):
            logging.info(f"Player {player_index + 1} placed robot at ({pos}).")
            self.ScreenAnimator()
            pygame.time.delay(50)

    def StartTurn(self, player_index, move_steps):
        """Начало хода для второго игрока"""
        move_steps = move_steps.split('-')
        start_pos = self.parse_position(move_steps[0])
        end_pos = self.parse_position(move_steps[-1])

        robot = None
        for r in self.players[player_index].robots:
            if r.pos == start_pos:
                robot = r
                break

        if not robot:
            logging.warning(f"No robot found at start position: {start_pos}")
            return

        for step in range(1, len(move_steps)):
            step_pos = self.parse_position(move_steps[step])
            direction = None
            if robot.pos[0] < step_pos[0]:
                direction = "right"
            elif robot.pos[0] > step_pos[0]:
                direction = "left"
            elif robot.pos[1] < step_pos[1]:
                direction = "down"
            elif robot.pos[1] > step_pos[1]:
                direction = "up"

            if direction and robot.move(direction, self.board):
                self.ScreenAnimator()
                pygame.display.flip()
                pygame.time.delay(30)

            if self.players[player_index].remaining_moves <= 0:
                self.switch_to_next_player()
                break

    def PressedKey(self, event):
        """Нажатие клавиши, обработка чисто нажатий клавиш"""
        if event.key == pygame.K_TAB:
            self.switch_to_next_player()
        elif event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
            robot_num = event.key - pygame.K_1
            if robot_num < len(self.players[self.current_player].robots):
                self.current_robot_index = robot_num
        elif event.key == pygame.K_UP:
            self.players[self.current_player].move_robot(self.current_robot_index, 'up', self.board)
        elif event.key == pygame.K_DOWN:
            self.players[self.current_player].move_robot(self.current_robot_index, 'down', self.board)
        elif event.key == pygame.K_LEFT:
            self.players[self.current_player].move_robot(self.current_robot_index, 'left', self.board)
        elif event.key == pygame.K_RIGHT:
            self.players[self.current_player].move_robot(self.current_robot_index, 'right', self.board)
        if self.players[self.current_player].remaining_moves <= 0:
            self.switch_to_next_player()

    def switch_to_next_player(self):
        """Смена игрока: Переход хода к следующему игроку. Скорее всего какая-то беда здесь тоже может быть,
        но я за 15 часов так и не поняла"""
        self.players[self.current_player].reset_moves()
        self.current_player = (self.current_player + 1) % len(self.players)
        logging.info(f"Switched to player {self.current_player + 1}.")

    def ScreenAnimator(self):
        """Анимация экрана"""
        self.screen.fill((255, 255, 255))

        for i in range(self.board.size):
            for j in range(self.board.size):
                self.board[i][j].display_cell(self.screen)

        for player in self.players:
            player.draw_robots(self.screen)

        score_y_offset = DEFAULT_IMAGE_SIZE[0] // 8
        for i, player in enumerate(self.players):
            position = (self.board.size * DEFAULT_IMAGE_SIZE[0] * 1.25, score_y_offset + i * 40)
            player.draw_score(self.screen, position)
        pygame.display.update()

    def parse_position(self, pos_str):
        column = ord(pos_str[0].lower()) - ord('a')
        row = int(pos_str[1]) - 1
        return column, row

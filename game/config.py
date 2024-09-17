# file_path: AntBotMailStation/game/config.py

class GameConfig:
    def __init__(self, config_path):
        self.config_path = config_path
        self.game_mode = None
        self.version = None
        self.run_count = None
        self.players_info = []
        self.win_score = None
        self.robots_per_player = None
        self.charging_accounting = None
        self.move_limit_per_turn = None
        self._parse_config()

    def _parse_config(self):
        with open(self.config_path, 'r') as file:
            lines = file.readlines()
            self.game_mode = int(lines[0].split('#')[0].strip())    # parse game mode
            self.version = float(lines[1].split('#')[0].strip())    # parse version
            self.move_limit_per_turn = int(lines[2].split('#')[0].strip())      # parse move limit
            self.run_count = int(lines[3].split('#')[0].strip())    # parse run count
            self.players_info = list(map(int, lines[4].split('#')[0].strip().split()))      # parse players info
            self.win_score = int(lines[5].split('#')[0].strip())    # parse win score
            self.robots_per_player = int(lines[6].split('#')[0].strip())    # parse robots per player
            self.charging_accounting = int(lines[7].split('#')[0].strip())      # parse charging accounting

    def get_num_players(self):
        return self.players_info[0]

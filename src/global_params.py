class GlobalParams(object):
    '''Classic Singleton class containing global params'''
    _instance = None
    _chambers = [[0 for i in range(0, 3)] for j in range(0, 3)]
    _player_pos = [0, 0]

    def __new__(cls):
        if not cls._instance:
            cls._instance = super(GlobalParams, cls).__new__(cls)
        return cls._instance

    @property
    def chambers(self):
        return self._chambers

    @property
    def player_pos(self):
        return self._player_pos

    @chambers.setter
    def chambers(self, value):
        self._chambers = value

    @player_pos.setter
    def player_pos(self, value):
        self._player_pos = value

    def chambers_setup(self) -> None:
        for i in range(0, 3):
            for j in range(0, 3):
                if j % 2 == 0 and i % 2 == 0:
                    self._chambers[i][j] = "0"
                elif i == 1 and j == 1:
                    self._chambers[1][1] = "S"
                else:
                    self._chambers[i][j] = "1"

    @staticmethod
    def reset_params() -> None:
        global_params = GlobalParams()
        global_params.chambers.clear()
        temp = [[0 for i in range(0, 3)] for j in range(0, 3)]
        for i in temp:
            global_params.chambers.append(i)
        global_params.chambers_setup()

        global_params.player_pos[0] = 0
        global_params.player_pos[1] = 0

import random
from global_params import GlobalParams

global_params = GlobalParams()
global_params.chambers_setup()
chambers = global_params.chambers
player_pos = global_params.player_pos


class Chambers_builders():
    def __init__(self) -> None:
        pass

    def players_pos_in_list_index(self, x_or_y: str) -> int:
        def chamber_player_index_Y():
            for i, v in enumerate(chambers):
                if "S" in v:
                    center_index_X = i
            return center_index_X - player_pos[1]

        def chamber_player_index_X():
            for i, v in enumerate(chambers):
                if "S" in v:
                    center_index_Y = v.index("S")
            return center_index_Y + player_pos[0]

        if x_or_y == "y":
            return chamber_player_index_Y()
        elif x_or_y == "x":
            return chamber_player_index_X()

    def set_chamber_generator_for_next_chambers_modification(
            self, gen) -> None:
        self.gen = gen

    def generate_new_chambers_in_specific_direction(self, moved: str) -> None:
        if moved == "W":
            temp_chambers = chambers.copy()
            chambers.append("_")
            temp = []
            for i in range(0, len(chambers[0])):
                temp.append(self.specify_chambers_at_Y(i))
            for i in range(1, len(chambers)):
                chambers[i] = temp_chambers[i - 1]
            chambers[0] = temp

        elif moved == "S":
            temp = []
            for i in range(0, len(chambers[0])):
                temp.append(self.specify_chambers_at_Y(i))
            chambers.append(temp)

        elif moved == "D":
            for i, v in enumerate(chambers):
                v.append(self.specify_chambers_at_X(i))

        elif moved == "A":
            for i, v in enumerate(chambers):
                temp = [self.specify_chambers_at_X(i)]
                for j in v:
                    temp.append(j)
                chambers[i] = temp

    def update_entries_inside_chmabers(self, move: str) -> None:
        if move == "w":
            self.update_chambers_at_Y(1)
        elif move == "s":
            self.update_chambers_at_Y(-1)
        elif move == "d":
            self.update_chambers_at_X(-1)
        elif move == "a":
            self.update_chambers_at_X(1)

    def specify_chambers_at_Y(self, index: int) -> str:
        X_pos = self.players_pos_in_list_index("x")

        if index >= X_pos - 1 and index <= X_pos + 1:
            return next(self.gen)
        else:
            return "_"

    def specify_chambers_at_X(self, index: int) -> str:
        Y_pos = self.players_pos_in_list_index("y")

        if index >= Y_pos - 1 and index <= Y_pos + 1:
            return next(self.gen)
        else:
            return "_"

    def update_chambers_at_Y(self, offset: int) -> None:
        Y_pos = self.players_pos_in_list_index("y")
        X_pos = self.players_pos_in_list_index("x")

        for i, row in enumerate(chambers):
            for j, v in enumerate(row):
                if i == Y_pos - offset:
                    if v == "_" and j >= X_pos - 1 and j <= X_pos + 1:
                        if chambers[Y_pos - offset][X_pos] == "0":
                            row[j] = "0"
                        else:
                            row[j] = next(self.gen)

    def update_chambers_at_X(self, offset: int) -> None:
        Y_pos = self.players_pos_in_list_index("y")
        X_pos = self.players_pos_in_list_index("x")

        for i, row in enumerate(chambers):
            for j, v in enumerate(row):
                if j == X_pos - offset:
                    if v == "_" and i >= Y_pos - 1 and i <= Y_pos + 1:
                        if chambers[Y_pos][X_pos - offset] == "0":
                            row[j] = "0"
                        else:
                            row[j] = next(self.gen)


class Chambers_player_movement():
    def __init__(self) -> None:
        pass

    def analyze_player_move(self, move: str) -> None:
        if move == "w" and self.check_if_player_can_move(move):
            player_pos[1] = player_pos[1] + 1

        elif move == "s" and self.check_if_player_can_move(move):
            player_pos[1] = player_pos[1] - 1

        elif move == "d" and self.check_if_player_can_move(move):
            player_pos[0] = player_pos[0] + 1

        elif move == "a" and self.check_if_player_can_move(move):
            player_pos[0] = player_pos[0] - 1

    def check_if_player_can_move(self, move: str) -> bool:
        x = Chambers_builders().players_pos_in_list_index("x")
        y = Chambers_builders().players_pos_in_list_index("y")
        oper_x = 0
        oper_y = 0
        if move == "w":
            oper_y = -1
        elif move == "s":
            oper_y = 1
        elif move == "d":
            oper_x = 1
        elif move == "a":
            oper_x = -1

        if chambers[y + oper_y][x + oper_x] != "0":
            return True
        else:
            print("***I can't move!***")
            return False

    def check_if_player_moved_outside_chmabers(self) -> str:
        x = Chambers_builders().players_pos_in_list_index("x")
        y = Chambers_builders().players_pos_in_list_index("y")
        if y == 0:
            return "W"
        elif y == len(chambers) - 1:
            return "S"
        elif x == len(chambers[0]) - 1:
            return "D"
        elif x == 0:
            return "A"
        else:
            return None


class Chambers_probabilities():
    def __init__(self) -> None:
        self.open_ways = 4
        self.mid_is_0 = False
        self.side_chambers_probability = 25
        self.actual_side_chambers = ['0', '0']

    def chambers_generator(self):
        self.calculate_if_the_center_is_zero()

        yield self.calculate_side_chambers("L")
        yield self.calculate_center_chamber()
        yield self.calculate_side_chambers("R")

    def calculate_if_the_center_is_zero(self):
        odds_MID = random.randint(0, 100)
        self.mid_is_0 = False
        if (odds_MID >= 0 and odds_MID <= 1 * self.open_ways - 3) \
                and self.open_ways > 4:
            self.mid_is_0 = True

    def calculate_side_chambers(self, left_or_right: str) -> str:
        if self.check_side_chambers_possibility() \
                and self.is_zero_at_side_chamber(left_or_right):
            return "1"
        else:
            return "0"

    def calculate_center_chamber(self):
        if self.mid_is_0:
            return "0"
        else:
            return "1"

    def check_side_chambers_possibility(self):
        odds = random.randint(0, 100)

        if (odds >= 0 and odds <= self.side_chambers_probability) \
                and self.mid_is_0 == False:
            return True
        else:
            return False

    def is_zero_at_side_chamber(self, left_or_right):
        if left_or_right == "L":
            index = 0
        elif left_or_right == "R":
            index = 1
        if self.actual_side_chambers[index] == "0":
            return True
        else:
            return False

    def set_actual_side_chambers_generations(self, move: str):
        x = Chambers_builders().players_pos_in_list_index("x")
        y = Chambers_builders().players_pos_in_list_index("y")
        if move == "w":
            self.actual_side_chambers = [
                chambers[y][x - 1],
                chambers[y][x + 1]
            ]
        elif move == "s":
            self.actual_side_chambers = [
                chambers[y][x - 1],
                chambers[y][x + 1]
            ]
        elif move == "d":
            self.actual_side_chambers = [
                chambers[y - 1][x],
                chambers[y + 1][x]
            ]
        elif move == "a":
            self.actual_side_chambers = [
                chambers[y - 1][x],
                chambers[y + 1][x]
            ]

    def open_ways_counter(self) -> None:
        def find_open_ways_in_rows():
            open_ways_in_rows = 0
            for row in chambers:
                for v in row:
                    if v == "1":
                        open_ways_in_rows += 1
                        break
                    elif v == "0":
                        break
                for v in reversed(row):
                    if v == "1":
                        open_ways_in_rows += 1
                        break
                    elif v == "0":
                        break
            return open_ways_in_rows

        def find_open_ways_in_cols():
            open_ways_in_cols = 0
            for x in range(0, len(chambers[0])):
                for y in range(0, len(chambers)):
                    if chambers[y][x] == "1":
                        open_ways_in_cols += 1
                        break
                    elif chambers[y][x] == "0":
                        break
                for y in range(len(chambers) - 1, -1, -1):
                    if chambers[y][x] == "1":
                        open_ways_in_cols += 1
                        break
                    elif chambers[y][x] == "0":
                        break
            return open_ways_in_cols

        self.open_ways = find_open_ways_in_rows() + find_open_ways_in_cols()

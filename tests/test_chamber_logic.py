import pytest
from src.global_params import GlobalParams
from src import chambers_logic as logic

global_params = GlobalParams()


class Test_Chambers_player_movement():
    def setup_method(self):
        logic.global_params.reset_params()
        self.player = logic.Chambers_player_movement()
        self.possible_moves = ['w', 's', 'd', 'a']
        self.y_axis = ['w', 's']
        self.possitive_moves = ['w', 'd']
        self.possitive_moves_in_list = ['s', 'd']

    def test_player_position_after_move(self):
        for i in self.possible_moves:
            if i in self.y_axis:
                axis = 1
            else:
                axis = 0

            if i in self.possitive_moves:
                value = 1
            else:
                value = -1

            self.player.analyze_player_move(i)
            assert logic.player_pos[axis] == value
            logic.global_params.reset_params()

    @pytest.mark.parametrize("move, expected_result", [
        ("w", "W"),
        ("s", "S"),
        ("d", "D"),
        ("a", "A"),
    ])
    def test_check_if_player_moved_outside_chambers(
            self, move, expected_result):
        logic.global_params.reset_params()
        self.player.analyze_player_move(move)
        result = self.player.check_if_player_moved_outside_chmabers()
        assert result == expected_result

    def test_check_if_player_can_move(self):
        for i in self.possible_moves:
            if i in self.possitive_moves_in_list:
                value = 2
            else:
                value = 0

            result = self.player.check_if_player_can_move(i)
            assert result == True

            if i in self.y_axis:
                logic.chambers[value][1] = '0'
            else:
                logic.chambers[1][value] = '0'

            result = self.player.check_if_player_can_move(i)
            assert result == False

    def teardown_method(self):
        del (self.player)


class Test_chamber_logic_builders():
    def setup_method(self):
        logic.global_params.reset_params()
        self.builders = logic.Chambers_builders()
        self.possible_moves = ['w', 's', 'd', 'a']
        self.y_axis = ['w', 's']
        self.possitive_moves = ['w', 'd']
        self.possitive_moves_in_list = ['s', 'd']
        self.possible_chambers_generations = ['0', '1']

    def test_chambers_generation_after_move(self):
        for i in self.possible_moves:
            self.player = logic.Chambers_player_movement()
            self.probabilities = logic.Chambers_probabilities()

            self.player.analyze_player_move(i)
            outside_move = self.player.check_if_player_moved_outside_chmabers()

            self.probabilities.set_actual_side_chambers_generations(i)
            gen = self.probabilities.chambers_generator()
            self.builders.set_chamber_generator_for_next_chambers_modification(
                gen)

            self.builders.generate_new_chambers_in_specific_direction(
                outside_move)

            if i in self.possitive_moves_in_list:
                index = 3
            else:
                index = 0

            if i in self.y_axis:
                for i in range(0, 3):
                    v = logic.chambers[index][i]
                    if i == 1:
                        assert v == '1'
                    else:
                        assert v in self.possible_chambers_generations

            else:
                for i in range(0, 3):
                    v = logic.chambers[i][index]
                    if i == 1:
                        assert v == '1'
                    else:
                        assert v in self.possible_chambers_generations

            logic.global_params.reset_params()

    def test_update_entries_inside_chmabers(self):
        # example scenario
        logic.chambers = [
            ['_', '_', '_', '_', '_', '_', '_', '0', '0', '0', '_'],
            ['_', '_', '_', '_', '_', '_', '_', '0', '1', '0', '0'],
            ['0', '1', '0', '1', '0', '1', '0', '0', '1', '1', '0'],
            ['1', 'S', '1', '1', '1', '1', '1', '1', '1', '0', '0'],
            ['0', '1', '0', '0', '1', '0', '0', '0', '1', '0', '_'],
            ['_', '_', '_', '0', '1', '0', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '0', '1', '0', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '0', '1', '0', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '1', '1', '1', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '0', '1', '0', '_', '_', '_', '_', '_'],
            ['_', '_', '_', '0', '0', '0', '_', '_', '_', '_', '_']
        ]
        for i in self.possible_moves:
            if i == 'w':
                logic.player_pos = [2, 0]
                y = 1
                x = [2, 5]
            elif i == 's':
                logic.player_pos = [7, 0]
                y = 5
                x = [7, 10]
            elif i == 'd':
                logic.player_pos = [3, -5]
                y = [7, 10]
                x = 6
            elif i == 'a':
                logic.player_pos = [3, -5]
                y = [7, 10]
                x = 2
            logic.Chambers_player_movement().analyze_player_move(i)
            logic.Chambers_probabilities().set_actual_side_chambers_generations(i)
            gen = logic.Chambers_probabilities().chambers_generator()
            self.builders.set_chamber_generator_for_next_chambers_modification(
                gen)
            self.builders.update_entries_inside_chmabers(i)
            if i in self.y_axis:
                list_to_check = logic.chambers[y][x[0]:x[1]]
            else:
                list_to_check = []
                for i in range(y[0], y[1]):
                    list_to_check.append(logic.chambers[i][x])

            assert '_' not in list_to_check

            logic.global_params.reset_params()

    def teardown_method(self):
        del (self.builders)


class Test_chamber_probabilities():
    def setup_method(self):
        logic.global_params.reset_params()
        self.probabilities = logic.Chambers_probabilities()

    def test_chambers_generator(self):
        probabilities = logic.Chambers_probabilities()
        gen = probabilities.chambers_generator()
        left_side = next(gen)
        center = next(gen)
        right_side = next(gen)

        assert left_side in ['0', '1']
        assert center in ['0', '1']
        assert right_side in ['0', '1']

    def teardown_method(self):
        del (self.probabilities)

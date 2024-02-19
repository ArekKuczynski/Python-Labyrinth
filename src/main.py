import chambers_logic as logic
from global_params import GlobalParams

global_params = GlobalParams()
chambers = global_params.chambers
global_params.chambers_setup()
player_pos = global_params.player_pos

builders = logic.Chambers_builders()
probabilities = logic.Chambers_probabilities()
player = logic.Chambers_player_movement()


def save_data():
    file1 = open("save.txt", "w")
    first_line = str(player_pos) + " " + \
        str(probabilities.open_ways) + "\n"
    file1.write(first_line)
    for i in chambers:
        for j in i:
            file1.write(j + "\t")
        file1.write("\n")
    file1.close()


def chambers_logic_runner(move):
    player.analyze_player_move(move)
    outside_move = player.check_if_player_moved_outside_chmabers()

    probabilities.set_actual_side_chambers_generations(move)
    gen = probabilities.chambers_generator()
    builders.set_chamber_generator_for_next_chambers_modification(gen)

    if outside_move is None:
        builders.update_entries_inside_chmabers(move)
    else:
        builders.generate_new_chambers_in_specific_direction(outside_move)

    probabilities.open_ways_counter()


def print_current_values():
    print(player_pos, end=" ")
    print("Open ways:", probabilities.open_ways)
    for i in chambers:
        print(i)


if __name__ == "__main__":
    print("*** available moves: w, s, d, a ***")
    while True:
        move = input("move: ")
        if move == "b":
            save_data()
            break
        if move == "x":
            print("*** RESTARTED ***")
            global_params.reset_params()

        chambers_logic_runner(move)
        print_current_values()

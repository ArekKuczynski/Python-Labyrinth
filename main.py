import chambers_logic as logic

builders = logic.Chamber_builders()
probabilities = logic.Chamber_probabilities()
player = logic.Chamber_player_movement()


def save_data():
    file1 = open("save.txt", "w")
    first_line = str(logic.player_pos) + " " + \
        str(probabilities.open_ways) + "\n"
    file1.write(first_line)
    for i in logic.chambers:
        for j in i:
            file1.write(j + "\t")
        file1.write("\n")
    file1.close()


def temp_runner():
    print("*** available moves: w, s, d, a ***")
    while True:
        move = input("move: ")

        if move == "b":
            save_data()
            break

        player.analyze_player_move(move)
        outside_move = player.check_player_move_outside_chmabers()

        probabilities.set_actual_side_chambers_generations(move)
        gen = probabilities.chambers_generator()
        builders.set_chamber_generator_for_next_chambers_modification(gen)

        if outside_move is None:
            builders.update_entries_inside_chmabers(move)
        else:
            builders.generate_new_entries_in_specific_direction(outside_move)
        probabilities.open_ways_counter()

        def print_current_values():
            print(logic.player_pos, end=" ")
            print("Open ways:", probabilities.open_ways)
            for i in logic.chambers:
                print(i)

        print_current_values()


if __name__ == "__main__":
    temp_runner()

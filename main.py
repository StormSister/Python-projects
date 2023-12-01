import util
import engine as engine
import ui

from state import board_history
# -*- coding: utf-8 -*-


def main():
    width, height, obstacles = engine.choose_level()
    player = engine.create_player(width, height)
    board = engine.create_board(height, width, obstacles)
    board_history.append(board)

    util.clear_screen()
    is_running = True

    while is_running:
        
        board = board_history[-1]
        engine.put_player_on_board(board, player)
        ui.display_health_and_points(player)
        ui.display_inventory(player)
        ui.display_board(board, player)
        if player["life"] <= 0:
            print("You lost")
            break
        #button = input("Move the player (W - up, S - down, A - left, D - right, Q - quit): ").upper()
        button = util.key_pressed().upper()
        if button == 'Q':
            print("Goodbye")
            is_running = False
        else:
            engine.move_player(board, player, button)
            engine.move_monsters(board)

        util.clear_screen()


if __name__ == '__main__':
    main()





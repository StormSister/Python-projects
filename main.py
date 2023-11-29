import util
import test
#import ui
import random


def is_loosing(player):
    if player["life"] <= 0:
        return True


def main():

    width, height, obstacles = test.choose_level()
    player = test.create_player(width, height)
    board = test.create_board(height, width, obstacles)

    util.clear_screen()
    is_running = True
    while is_running:
        test.put_player_on_board(board, player)

        test.display_health_and_points(player)  # Wyświetlenie zdrowia i punktów gracza
        test.display_inventory(player)  # Wyświetlenie inwentarza
        test.display_board(board)  # Wyświetlenie planszy

        button = input("Move the player (W - up, S - down, A - left, D - right, Q - quit): ").upper()

        #button = util.key_pressed().upper()
        if is_loosing(player):
            print("You lost")
            is_running = False

        if button == 'Q':
            print("Goodbye")
            is_running = False
        else:
            board = test.move_player(board, player, button)

        util.clear_screen()


if __name__ == '__main__':
    main()

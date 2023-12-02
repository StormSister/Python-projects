# def display_board(board):
#     for row in board:
#         row_str = ''.join(row)
#         print(row_str)



def display_inventory(player):
    print("Player Inventory:")
    if not player["inventory"]:
        print("Inventory is empty.")
    else:
        print("ITEM QUANTITY")
        for item, quantity in player["inventory"].items():
            print(f"{item}: {quantity}")


def display_health_and_points(player):
    print(f"Health: {player['life']}")
    print(f"Points: {player['points']}")
    print(f"Attack: {player['attack']}")


def display_board(board, player):
    visible_range = 3 
    player_row = player["row"]
    player_col = player["col"]

    for i in range(len(board)):
        for j in range(len(board[0])):
            if abs(i - player_row) > visible_range or abs(j - player_col) > visible_range:
                print('🌫️ ', end='')
            else:
                print(board[i][j], end='')
        print()


#battle fog '🌫️ '
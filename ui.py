def display_board(board):
    for row in board:
        row_str = ''.join(row)
        print(row_str)


def display_inventory(player):
    print("Player Inventory:")
    if not player["inventory"]:
        print("Inventory is empty.")
    else:
        for item, quantity in player["inventory"].items():
            print(f"{item}: {quantity}")


def display_health_and_points(player):
    print(f"Health: {player['life']}")
    print(f"Points: {player['points']}")
    print(f"Attack: {player['attack']}")
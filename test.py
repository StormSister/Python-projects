
import random

def choose_level():

    difficulty = {
        "easy": [random.randint(8, 10), random.randint(8, 10), 0.2],
        "medium": [random.randint(11, 15), random.randint(11, 15), 0.3],
        "hard": [random.randint(16, 20), random.randint(16, 20), 0.4],
    }

    user_choice = int(input("Choose level (1 - easy, 2 - medium, 3 - hard):"))
    while user_choice != [1, 2, 3]:
        if user_choice == 1:
            return difficulty["easy"]
        if user_choice == 2:
            return difficulty["medium"]
        if user_choice == 3:
            return difficulty["hard"]


elements = {
    "Grass": {
        "symbol": "🟩",
        "type": "Terrain",
        "passable": True
    },
    "Forest": {
        "symbol": "🌲",
        "type": "Terrain",
        "passable": True,
        "effect": {
            "type": "add_to_inventory",
            "bonus": {
                "Wood": 1
            }
        }
    },
    "Wall": {
        "symbol": "🏔️",
        "type": "Obstacle",
        "passable": False
    },
    "Swamp": {
        "symbol": "🌫️",
        "type": "Terrain",
        "passable": True,
        "effect": {
            "type": "health_reduction",
            "amount": 5
        }
    },
    "Monster": {
        "symbol": "👹",
        "type": "Enemy",
        "life": 50,
        "attack": 15,
        "effect": {
            "type": "fight_with_monster"
        }
    },
    "Door": {
        "symbol": "🌀",
        "type": "Exit",
        "passable": True,
        "effect": {
            "type": "teleport"
        }
    }
}


def create_board(height, width, obstacles):
    total_cells = height * width
    max_elements = total_cells * obstacles

    board = [
        [elements["Grass"]["symbol"] if (0 < i < height - 1 and j > 0 and j < width - 1) else elements["Wall"]["symbol"] for j in range(width)]
        for i in range(height)
    ]

    doors_positions = [
        (0, random.randint(1, width - 2)),
        (height - 1, random.randint(1, width - 2)),
        (random.randint(1, height - 2), 0),
        (random.randint(1, height - 2), width - 1)
    ]

    for row, col in doors_positions:
        board[row][col] = elements["Door"]["symbol"]

    elements_to_place = [element for element in elements if element not in ["Door"]]
    placed_elements = 0

    while placed_elements < max_elements:
        rand_row = random.randint(1, height - 2)
        rand_col = random.randint(1, width - 2)

        if board[rand_row][rand_col] == elements["Grass"]["symbol"]:
            element = random.choice(elements_to_place)
            board[rand_row][rand_col] = elements[element]["symbol"]
            placed_elements += 1

    return board


def display_board(board):
    for row in board:
        row_str = ''.join(row)
        print(row_str)


def create_player(width, height):
    player = {"row": random.randint(1, height - 2),
              "col": random.randint(1, width - 2),
              "symbol": '🧙🏻',
              "life": 100,
              "attack": 20,
              "inventory": {},
              "points": 0}
    return player


def put_player_on_board(board, player):
    row, col = player['row'], player['col']
    board[row][col] = player['symbol']

    return board

def put_player_on_new_board(width, height, player, board):
    new_row = random.randint(1, height - 2)
    new_col = random.randint(1, width - 2)
    player['row'], player['col'] = new_row, new_col
    board[new_row][new_col] = player['symbol']

    return board


def apply_teleport_effect(player):
    width, height, obstacles = choose_level()
    print(width, height, obstacles)
    new_board = create_board(width, height, obstacles)
    player["row"] = random.randint(1, height - 2)
    player["col"] = random.randint(1, width - 2)
    put_player_on_board(new_board, player)
    display_board(new_board)
    return new_board



def apply_player_effect(player, cell_effect):
    if cell_effect:
        if isinstance(cell_effect, dict):
            if cell_effect['type'] == "add_to_inventory":
                apply_inventory_effect(player, cell_effect)

            elif cell_effect['type'] == "health_reduction":
                apply_health_reduction(player, cell_effect)

            elif cell_effect['type'] == "teleport":
                new_board = apply_teleport_effect(player)
                return new_board

            elif cell_effect == "fight_with_monster":

                pass

            else:
                print("Unknown effect")
    else:
        print("No effect on this terrain")


def apply_health_reduction(player, effect):
    global is_running
    if effect['type'] == "health_reduction":
        amount = effect.get('amount')
        if amount:
            player['life'] -= amount
            print(f"You lost {amount} health!")
            if player['life'] <= 0:
                print("Game Over - You lost all your health!")
                is_running = False


def apply_inventory_effect(player, effect):
    if effect['type'] == "add_to_inventory":
        bonus = effect.get('bonus')
        if bonus:
            add_to_inventory(player, bonus)


def add_to_inventory(player, bonus):
    for item, quantity in bonus.items():
        if item in player['inventory']:
            player['inventory'][item] += quantity
        else:
            player['inventory'][item] = quantity
    print("Added bonus to inventory:", bonus)


def move_direction(direction, row, col):
    new_row, new_col = row, col

    if direction == 'W':
        new_row -= 1  # Góra
    elif direction == 'S':
        new_row += 1  # Dół
    elif direction == 'A':
        new_col -= 1  # Lewo
    elif direction == 'D':
        new_col += 1  # Prawo

    return new_row, new_col


def key_for_symbol(board, new_row, new_col):
    current_symbol = board[new_row][new_col]
    #current_cell = None
    for element in elements:
        if elements[element]["symbol"] == current_symbol:
            current_cell = element
            return current_cell


def move_player(board, player, direction):
    row, col = player['row'], player['col']
    #new_row, new_col = row, col
    new_row, new_col = move_direction(direction, row, col)

    if check_position(board, new_row, new_col) and is_passable(board, {'row': new_row, 'col': new_col}):
        current_cell = key_for_symbol(board, new_row, new_col)

        if current_cell and is_passable(board, {'row': new_row, 'col': new_col}):
            player["row"], player["col"] = new_row, new_col
            board[row][col] = elements["Grass"]["symbol"]
            board[player["row"]][player["col"]] = player['symbol']

            if "effect" in elements[current_cell]:
                cell_effect = elements[current_cell].get('effect')
                print(cell_effect)
                if cell_effect == "teleport":
                    board = apply_teleport_effect(player)
                apply_player_effect(player, cell_effect)
                # if cell_effect == "teleport":
                #      board = apply_teleport_effect(player)



    return board


def check_position(board, row, col):
    if 0 <= row < len(board) and 0 <= col < len(board[0]):
        return True
    return False


def is_passable(board, player):
    element_key = None
    row, col = player["row"], player["col"]
    cell = board[row][col]

    for key, value in elements.items():
        if value['symbol'] == cell:
            element_key = key
            break

    if element_key and elements[element_key].get('passable', False):
        return True
    return False


def display_inventory(player):
    print("Player Inventory:")
    if not player["inventory"]:
        print("Inventory is empty.")
    else:
        for item, quantity in player["inventory"].items():
            print(f"{item}: {quantity}")


def display_health_and_points(player):
    print(f"Health: {player['life']}")
    print(f"Points: {player['points']}\n")

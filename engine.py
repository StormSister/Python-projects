
import random
from state import board_history


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
        "symbol": "🗻",
        "type": "Obstacle",
        "passable": False
    },
    "Volcano": {
        "symbol": "🌋",
        "type": "Terrain",
        "passable": True,
        "effect": {
            "type": "health_reduction",
            "amount": -5
        }
    },
    "Monster1": {
        "symbol": "👹",
        "type": "Enemy",
        "passable": True,
        "effect": {
            "life": 50,
            "attack": 15,
            "type": "fight_with_monster",
            "bonus": ["Sword", "Armor", "Health Potion"]
        }
    },
    "Monster2": {
        "symbol": "🐉",
        "type": "Enemy",
        "passable": True,
        "effect": {
            "life": 80,
            "attack": 20,
            "type": "fight_with_monster",
            "bonus": ["Wand", "Shield", "Ham"]
        }
    },

    "Door": {
        "symbol": "🌀",
        "type": "Exit",
        "passable": True,
        "effect": {
            "type": "teleport"
        }
    },
    "Fountain": {
        "symbol": "⛲",
        "type": "Terrain",
        "passable": True,
        "effect": {
            "type": "health_reduction",
            "amount": 15
        }
    },
}


def placing_teleports(height, width, board):
    doors_positions = [
        (0, random.randint(1, width - 2)),
        (height - 1, random.randint(1, width - 2)),
        (random.randint(1, height - 2), 0),
        (random.randint(1, height - 2), width - 1)
    ]

    for row, col in doors_positions:
        board[row][col] = elements["Door"]["symbol"]


def placing_elements(height, width, obstacles, board):
    total_cells = height * width
    max_elements = total_cells * obstacles
    elements_to_place = [element for element in elements if element not in ["Door"]]
    placed_elements = 0

    while placed_elements < max_elements:
        rand_row = random.randint(1, height - 2)
        rand_col = random.randint(1, width - 2)

        if board[rand_row][rand_col] == elements["Grass"]["symbol"]:
            element = random.choice(elements_to_place)
            board[rand_row][rand_col] = elements[element]["symbol"]
            placed_elements += 1


def create_board(height, width, obstacles):

    board = [
        [elements["Grass"]["symbol"] if (0 < i < height - 1 and j > 0 and j < width - 1) else elements["Wall"]["symbol"] for j in range(width)]
        for i in range(height)
    ]
    placing_teleports(height, width, board)
    placing_elements(height, width, obstacles, board)

    return board


def create_player(width, height):
    player = {"row": random.randint(1, height - 2),
              "col": random.randint(1, width - 2),
              "symbol": '🧙‍',
              "life": 100,
              "attack": 20,
              "inventory": {},
              "points": 0}
    return player


def put_player_on_board(board, player):
    row, col = player['row'], player['col']
    board[row][col] = player['symbol']

    return board


def apply_teleport_effect(player):

    width, height, obstacles = choose_level()
    print(width, height, obstacles)
    new_board = create_board(width, height, obstacles)
    board_history.append(new_board)
    player["row"] = random.randint(2, height - 2)
    player["col"] = random.randint(2, width - 2)
    put_player_on_board(new_board, player)
    return board_history


def apply_health_reduction(player, effect):
    global is_running
    if effect['type'] == "health_reduction":
        amount = effect.get('amount')
        if amount:
            player['life'] += amount
            print(f"You gather {amount} health!")
            if player['life'] <= 0:
                print("Game Over - You lost all your health!")


def add_to_inventory(player, bonus):
    for item, quantity in bonus.items():
        if item in player['inventory']:
            player['inventory'][item] += quantity
        else:
            player['inventory'][item] = quantity
    print("Added bonus to inventory:", bonus)


def apply_inventory_effect(player, effect):
    if effect['type'] == "add_to_inventory":
        bonus = effect.get('bonus')
        if bonus:
            add_to_inventory(player, bonus)


def add_random_bonus(player):
    available_bonuses = {
        "Sword": 1,
        "Armor": 1,
        "Health Potion": 1,
        "Gold": 5
    }
    selected_bonus = random.choice(list(available_bonuses.keys()))
    bonus = {selected_bonus: available_bonuses[selected_bonus]}
    add_to_inventory(player, bonus)


def add_points(player, points_to_add):
    player["points"] += points_to_add


def move_monsters(board):
    monster_symbol = elements["Monster1"]["symbol"]

    for row_idx, row in enumerate(board):
        for col_idx, cell in enumerate(row):
            if cell == monster_symbol:
                possible_moves = [
                    (row_idx - 1, col_idx),  
                    (row_idx + 1, col_idx),  
                    (row_idx, col_idx - 1),  
                    (row_idx, col_idx + 1),  
                ]

                valid_moves = [
                    move for move in possible_moves
                    if check_position(board, move[0], move[1]) and (board[move[0]][move[1]] == elements["Grass"]["symbol"])
                ]

                if valid_moves:
                    new_row, new_col = random.choice(valid_moves)
                    board[row_idx][col_idx] = elements["Grass"]["symbol"]
                    board[new_row][new_col] = monster_symbol


def fight_with_monster(player, effect):
    print("You encountered a monster!")
    if effect['type'] == "fight_with_monster":
        monster_life = effect.get('life')
        bonus = effect.get('bonus')

        while player["life"] > 0 and monster_life > 0:

            player_attack = player["attack"]
            monster_life -= player_attack
            print(f"You dealt {player_attack} damage to the monster. Monster's remaining life: {monster_life}")

            if monster_life <= 0:
                print("You defeated the monster!")
                add_points(player, 5)
                break

            monster_attack = effect.get('attack')
            player["life"] -= monster_attack
            print(f"The monster dealt {monster_attack} damage to you. Your remaining life: {player['life']}")

            if player["life"] <= 0:
                print("You were defeated by the monster.")
                break


def apply_player_effect(player, cell_effect):

    if cell_effect:
        if isinstance(cell_effect, dict):
            if cell_effect['type'] == "add_to_inventory":
                apply_inventory_effect(player, cell_effect)

            elif cell_effect['type'] == "health_reduction":
                apply_health_reduction(player, cell_effect)

            elif cell_effect['type'] == "teleport":
                apply_teleport_effect(player)

            elif cell_effect['type'] == "fight_with_monster":
                fight_with_monster(player, cell_effect)
                add_random_bonus(player)
            else:
                print("Unknown effect")
    else:
        print("No effect on this terrain")


def move_direction(direction, row, col):
    new_row, new_col = row, col

    if direction == 'W':
        new_row -= 1
    elif direction == 'S':
        new_row += 1
    elif direction == 'A':
        new_col -= 1
    elif direction == 'D':
        new_col += 1

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
    new_row, new_col = move_direction(direction, row, col)

    if check_position(board, new_row, new_col) and is_passable(board, {'row': new_row, 'col': new_col}):
        current_cell = key_for_symbol(board, new_row, new_col)

        if current_cell and is_passable(board, {'row': new_row, 'col': new_col}):
            player["row"], player["col"] = new_row, new_col
            board[row][col] = elements["Grass"]["symbol"]
            board[player["row"]][player["col"]] = player['symbol']

            if "effect" in elements[current_cell]:
                cell_effect = elements[current_cell].get('effect')
                #print(cell_effect)
                apply_player_effect(player, cell_effect)

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









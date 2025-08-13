from core.models import Game, Board, BOARD_SIZE


# init state
game_state = Game(
    board=Board(black=[], white=[]),
    winner=None
)

def get_game_state():
    return game_state


def reset_game():
    global game_state
    game_state = Game(
        board=Board(black=[], white=[]),
        winner=None
    )

def make_move(player: str, x: int, y: int) -> bool:
    global game_state
    # check whether this position have piece
    if [x, y] in game_state.board.black or [x, y] in game_state.board.white:
        return False
    piece_list = getattr(game_state.board, player)

    if x >= BOARD_SIZE or y >= BOARD_SIZE:
        return False
    
    piece_list.append([x, y])

    win_status = check_win(player=player, x=x, y=y)
    if win_status:
        game_state.winner = player
    return True

def check_win(player: str, x: int, y: int) -> bool:
    global game_state
    piece_list = getattr(game_state.board, player)

    directions = [
        [1, 0],
        [-1, 0],
        [0, 1],
        [0, -1],
        [1, 1],
        [-1, -1],
        [1, -1],
        [-1, 1]
    ]
    for dir in directions:
        length = 1
        c_x = x
        c_y = y
        while [c_x + dir[0], c_y + dir[1]] in piece_list:
            length += 1
            c_x += dir[0]
            c_y += dir[1]

            if length == 5:
                return True
    return False
class Gomoku:
    BOARD_SIZE = 19

    def create_board(self):
        return {
            "black": [],
            "white": []
        }
    
    def is_valid_move(self, board: dict, color: str, x: int, y: int) -> bool:
        if x < 0 or x > self.BOARD_SIZE - 1 or y < 0 or y > self.BOARD_SIZE - 1:
            return False
        
        if color == "black":
            return (x, y) not in board["black"]
        else:
            return (x, y) not in board["white"]

    def move(self, board: dict, color: str, x: int, y: int) -> dict:
        if not self.is_valid_move(board, color, x, y):
            raise ValueError(f"Invalid move: {x}, {y}, {color}")
        
        if color == "black":
            board["black"].append((x, y))
        else:
            board["white"].append((x, y))

        is_win = self.check_win_with_last_move(board, color, x, y)
        return board, is_win
    
    def check_win_with_last_move(self, board: dict, color: str, last_x: int, last_y: int) -> bool:
        directions = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (1, 1),
            (-1, -1),
            (1, -1),
            (-1, 1)
        ]
        pieces = board[color]
        for dx, dy in directions:
            count = 1
            for i in range(1, 5):
                x = last_x + dx * i
                y = last_y + dy * i
                if (x, y) in pieces:
                    count += 1
                else:
                    break
            if count >= 5:
                return True
        return False
        
    
    def check_win(self, board: dict) -> str:
        
        directions = []
        return
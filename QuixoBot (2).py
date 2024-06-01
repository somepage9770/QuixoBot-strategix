import copy

class QuixoBot:
    def __init__(self, symbol):
        self.name = "Strategix"
        self.symbol = symbol
        self.opponent_symbol = -symbol

    def reset(self, symbol):
        self.symbol = symbol
        self.opponent_symbol = -symbol

    def play_turn(self, board):
        best_move = None
        best_value = float('-inf')
        moves = self.generate_moves(board, self.symbol)
        
        for move in moves:
            new_board = self.apply_move(copy.deepcopy(board), move, self.symbol)
            move_value = self.minimax(new_board, 1, float('-inf'), float('inf'), False)
            if move_value > best_value:
                best_value = move_value
                best_move = new_board
        
        return best_move if best_move else board

    def minimax(self, board, depth, alpha, beta, is_maximizing):
        if depth == 0 or self.is_winner(board, self.symbol) or self.is_winner(board, self.opponent_symbol):
            return self.evaluate_board(board, self.symbol, self.opponent_symbol)
        
        if is_maximizing:
            max_eval = float('-inf')
            moves = self.generate_moves(board, self.symbol)
            for move in moves:
                new_board = self.apply_move(copy.deepcopy(board), move, self.symbol)
                eval = self.minimax(new_board, depth - 1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = float('inf')
            moves = self.generate_moves(board, self.opponent_symbol)
            for move in moves:
                new_board = self.apply_move(copy.deepcopy(board), move, self.opponent_symbol)
                eval = self.minimax(new_board, depth - 1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            return min_eval

    def is_winner(self, board, symbol):
        for i in range(5):
            row = [board[i][j] for j in range(5)]
            column = [board[j][i] for j in range(5)]
            if all(cell == symbol for cell in row):
                return True
            if all(cell == symbol for cell in column):
                return True

        diagonal1 = [board[i][i] for i in range(5)]
        if all(cell == symbol for cell in diagonal1):
            return True

        diagonal2 = [board[i][4 - i] for i in range(5)]
        if all(cell == symbol for cell in diagonal2):
            return True

        return False

    def generate_moves(self, board, symbol):
        moves = []
        for row in [0, 4]:  
            for col in range(5):
                if board[row][col] == 0 or board[row][col] == symbol:
                    if row == 0:
                        if col > 0:  
                            moves.append((row, col, 'L'))
                        if col < 4:  
                            moves.append((row, col, 'R'))
                        moves.append((row, col, 'D'))
                    elif row == 4:
                        if col > 0:  
                            moves.append((row, col, 'L'))
                        if col < 4:  
                            moves.append((row, col, 'R'))
                        moves.append((row, col, 'U'))
        for col in [0, 4]:
            for row in range(1, 4):  
                if board[row][col] == 0 or board[row][col] == symbol:
                    if col == 0:
                        if row > 0: 
                            moves.append((row, col, 'U'))
                        if row < 4:  
                            moves.append((row, col, 'D'))
                        moves.append((row, col, 'R'))
                    elif col == 4:
                        if row > 0: 
                            moves.append((row, col, 'U'))
                        if row < 4:  
                            moves.append((row, col, 'D'))
                        moves.append((row, col, 'L'))
        return moves

    def apply_move(self, board, move, symbol):
        row, col, direction = move
        if direction == 'U':
            for i in range(row, 0, -1):
                board[i][col] = board[i - 1][col]
            board[0][col] = symbol
        elif direction == 'D':
            for i in range(row, 4):
                board[i][col] = board[i + 1][col]
            board[4][col] = symbol
        elif direction == 'L':
            for i in range(col, 0, -1):
                board[row][i] = board[row][i - 1]
            board[row][0] = symbol
        elif direction == 'R':
            for i in range(col, 4):
                board[row][i] = board[row][i + 1]
            board[row][4] = symbol
        return board

    def evaluate_board(self, board, bot_symbol, other_symbol):
        score = 0
        for i in range(5):
            row = [board[i][j] for j in range(5)]
            column = [board[j][i] for j in range(5)]
            score += self.heuristic_value(row, bot_symbol)
            score -= self.heuristic_value(row, other_symbol)
            score += self.heuristic_value(column, bot_symbol)
            score -= self.heuristic_value(column, other_symbol)
            
        diagonal1 = [board[i][i] for i in range(5)]
        score += self.heuristic_value(diagonal1, bot_symbol)
        score -= self.heuristic_value(diagonal1, other_symbol)
        diagonal2 = [board[i][4 - i] for i in range(5)]
        score += self.heuristic_value(diagonal2, bot_symbol)
        score -= self.heuristic_value(diagonal2, other_symbol)
        return score

    @staticmethod
    def heuristic_value(line, symbol):
        repetitions = 0
        empty = 0
        max_sequence = 0
        current_sequence = 0
        
        for cell in line:
            if cell == symbol:
                repetitions += 1
                current_sequence += 1
                max_sequence = max(max_sequence, current_sequence)
            elif cell == 0:
                empty += 1
                current_sequence = 0
            else:
                current_sequence = 0
        
        base_points_dict = {
            (5, 0): 2003,
            (4, 1): 50,
            (3, 2): 16,
            (2, 3): 5,
        }

        additional_points_dict = {
            2: 5,
            3: 50,
            4: 2003
        }

        base_points = base_points_dict.get((repetitions, empty), 0)
        additional_points = additional_points_dict.get(max_sequence, 0)
        
        return base_points + additional_points

import random

class MinimaxPlayer:
	def __init__(self, color):
		self.color = color

	def evaluate_board(self, board):
		Inf = 100
		evaluation = [0,   0,   0,   0,   0,   0,   0,   0,   0,
					  0, Inf, -50,  20,  20,  20,  20, -50, Inf,
					  0, -50,-Inf, -25, -25, -25, -25,-Inf, -50,
					  0,  20, -25,  10,   5,   5,  10, -25,  20,
					  0,  20, -25,   5,   1,   1,   5, -25,  20,
					  0,  20, -25,   5,   1,   1,   5, -25,  20,
					  0,  20, -25,  10,   5,   5,  10, -25,  20,
					  0, -50,-Inf, -25, -25, -25, -25,-Inf, -50,
					  0, Inf, -50,  20,  20,  20,  20, -50, Inf]

		opponent = self.color
		if self.color == board.BLACK:
			oponent = board.WHITE
		else:
			oponent = board.BLACK

		board_score = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == self.color:
					board_score += evaluation[i][j]
				if board[i][j] == oponent:
					board_score -= evaluation[i][j]

		return board_score

	def min_play(self, board, level):
		if level == 5:
			return 1

		valid_moves = board.valid_moves(self.color)

		# Player apenas chamado tendo lista com pelo menos um elemento
		best_move = valid_moves[0]
		best_score = 100000

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			move_max, score_max = self.max_play(test_board, level+1)
			if score_max < best_score:
				best_move = move
				best_score = score_max

		return best_move, best_score

	def max_play(self, board, level):
		if level == 5:
			return 1

		valid_moves = board.valid_moves(self.color)

		# Player apenas chamado tendo lista com pelo menos um elemento
		best_move = valid_moves[0]
		best_score = -100000

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			move_min, score_min = self.min_play(test_board, level+1)
			if score_min > best_score:
				best_move = move
				best_score = score_min

		return best_move, best_score

	def play(self, board):
		white_score, black_score = board.score()
		valid_moves = board.valid_moves(self.color)
		
		best_move, best_score = self.max_play(board, 0)
		return best_move

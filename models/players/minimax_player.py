import random

class MinimaxPlayer:
	def __init__(self, color):
		self.color = color

	def evaluate_board(self, board):
		a = -50
		b = 20
		c = -25
		d = 10
		e = 5
		f = 1
		g = 99999999
		evaluation = [[0,   0,   0,   0,   0,   0,   0,   0,   0],
					  [0,   g,   a,   b,   b,   b,   b,   a,   g],
					  [0,   a,   g,   c,   c,   c,   c,   g,   a],
					  [0,   b,   c,   d,   e,   e,   d,   c,   b],
					  [0,   b,   c,   e,   f,   f,   e,   c,   b],
					  [0,   b,   c,   e,   f,   f,   e,   c,   b],
					  [0,   b,   c,   d,   e,   e,   d,   c,   b],
					  [0,   a,   g,   c,   c,   c,   c,   g,   a],
					  [0,   g,   a,   b,   b,   b,   b,   a,   g]]

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
		from models.move import Move
		if level == 3:
			return [Move(0,0), -self.evaluate_board(board)]

		valid_moves = board.valid_moves(self.color)

		if not valid_moves:
			return [Move(0,0), float("inf")]

		best_move = valid_moves[0]
		best_score = float("inf")

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			move_max, score_max = self.max_play(test_board, level+1)
			if score_max < best_score:
				best_move = move
				best_score = score_max

		return [best_move, best_score]

	def max_play(self, board, level):
		from models.move import Move
		if level == 3:
			return [Move(0,0), self.evaluate_board(board)]

		valid_moves = board.valid_moves(self.color)

		if not valid_moves:
			return [Move(0,0), float("-inf")]

		best_move = valid_moves[0]
		best_score = float("-inf")

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			move_min, score_min = self.min_play(test_board, level+1)
			if score_min > best_score:
				best_move = move
				best_score = score_min

		return [best_move, best_score]

	def play(self, board):
		best_move = self.max_play(board, 0)[0]
		return best_move

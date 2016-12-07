class AlphaBetaPlayer:
	def __init__(self, color):
		self.color = color

	def evaluate_board(self, board, player):
		a = -20
		b = 5
		c = -5
		d = 15
		e = 3
		f = 2
		g = 120
		h = 20
		i = -40
		# testar depois colocando os valores direto na matriz
		evaluation = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
					  [0, g, a, h, b, b, h, a, g],
					  [0, a, i, c, c, c, c, i, a],
					  [0, h, c, d, e, e, d, c, h],
					  [0, b, c, e, f, f, e, c, b],
					  [0, b, c, e, f, f, e, c, b],
					  [0, h, c, d, e, e, d, c, h],
					  [0, a, i, c, c, c, c, i, a],
					  [0, g, a, h, b, b, h, a, g]]


		opponent = board._opponent(player)

		board_score = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == player:
					board_score += evaluation[i][j]
				if board[i][j] == opponent:
					board_score -= evaluation[i][j]

		return board_score


	def final_value(self, board, player):
		white_score, black_score = board.score()
		return_value = 0
		if player == board.WHITE:
			return_value = white_score - black_score
		else:
			return_value = black_score - white_score

		if return_value > 0:
			return_value = float('inf')
		elif return_value < 0:
			return_value = float('-inf')

		return return_value

	def alphabeta(self, player, board, alpha, beta, depth):

		if depth == 0:
			return self.evaluate_board(board, player), None

		opponent = board._opponent(player)
		valid_moves = board.valid_moves(player)

		if not valid_moves:
			if not board.valid_moves(opponent):
				return self.final_value(board, player), None
			return -self.alphabeta(opponent, board, -beta, -alpha, depth-1)[0], None

		best_move = valid_moves[0]
		for move in valid_moves:
			if alpha >= beta:
				break
			test_board = board.get_clone()
			test_board.play(move, player)
			val = -self.alphabeta(opponent, test_board, -beta, -alpha, depth-1)[0]
			if val > alpha:
				alpha = val
				best_move = move
		return alpha, best_move

	import random

	def play(self, board):
		
		score = board.score()
		empty_squares = 64 - sum(score)

		if empty_squares == 60:
			return self.random.choice(board.valid_moves(self.color))

		depth = 4
		if board.valid_moves(self.color).__len__() < 6:
			depth = 6
		if empty_squares < 13:
			print "AGORA"
			depth = 20
		move = self.alphabeta(self.color, board, float('-inf'), float('inf'), depth)
		if move[0] == float('inf'):
			print "ate a prox, loser"
		print move[0]
		return move[1]

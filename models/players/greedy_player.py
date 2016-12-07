class GreedyPlayer:
	def __init__(self, color):
		self.color = color

	def play(self, board):
		white_score, black_score = board.score()
		valid_moves = board.valid_moves(self.color)

		# Player apenas chamado tendo lista com pelo menos um elemento
		chosen_move = valid_moves[0]
		maxi = -1

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			test_white_score, test_black_score = test_board.score()
			count = 0

			if self.color == board.WHITE:
				count += (test_white_score - white_score)
			else:
				count += (test_black_score - black_score)

			if count > maxi:
				maxi = count
				chosen_move = move

		return chosen_move

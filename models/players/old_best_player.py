class OldBestPlayer:
	def __init__(self, color):
		self.color = color
		self.abplayer = color
		self.abboard = None

	def is_frontier_piece(self, board, i, j):
		ans = False
		# Olha todos os 8 vizinhos. Casas fora do tabuleiro sao preenchidas com o caractere '?'
		for direction in board.DIRECTIONS:
			ni, nj = i+direction[0], j+direction[1]
			if board[ni][nj] == board.EMPTY:
				ans = True
				break
		return ans

	def frontier(self, board, player):
		opponent = board._opponent(player)
		player_frontier, opponent_frontier = 0, 0
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == player:
					player_frontier += self.is_frontier_piece(board, i, j)
				if board[i][j] == opponent:
					opponent_frontier += self.is_frontier_piece(board, i, j)
		return player_frontier, opponent_frontier

	def get_directions(self, board, corner):
		if corner == [1,1]:
			return board.DOWN, board.RIGHT, board.DOWN_RIGHT
		elif corner == [1,8]:
			return board.DOWN, board.LEFT, board.DOWN_LEFT
		elif corner == [8,1]:
			return board.UP, board.RIGHT, board.UP_RIGHT
		elif corner == [8,8]:
			return board.UP, board.LEFT, board.UP_LEFT

	# Retorna posicao (casa + direction)
	def nova_casa(self, casa, direction):
		return [casa[0] + direction[0], casa[1] + direction[1]]

	# Retorna valor da matriz, indexada pela lista indice[]
	def get(self, matriz, indice):
		return matriz[indice[0]][indice[1]]

	# Atribui matriz[indice] = valor, no qual indice = [x, y]
	def set(self, matriz, indice, valor):
		matriz[indice[0]][indice[1]] = valor

	# Conta quantas pecas estaveis existem em torno de uma quina
	# Ainda com um bug (camadas mais internas podendo ter mais pecas que as externas)
	def count_stable(self, board, player, corner, checked):
		stable_return = [0, 0]

		# Se a quina estiver vazia
		if board[corner[0]][corner[1]] == board.EMPTY:
			return stable_return

		# print "corner:", corner
		
		directions = self.get_directions(board, corner)
		piece = self.get(board, corner)

		# indice do jogador com peca na quina: 0 se for quem esta jogando e 1 se for o oponente
		player = 0 if self.get(board, corner) is player else 1

		# still buggy
		casa_diag = corner
		quantidade_maxima_0 = 10
		quantidade_maxima_1 = 10
		while self.get(board, casa_diag) == piece and min(quantidade_maxima_0, quantidade_maxima_1) > 1:
			quantidade_atual_0 = 1
			quantidade_atual_1 = 1
			# print "casa_diag:", casa_diag
			if self.get(checked, casa_diag) == False:
				stable_return[player] += 1
				self.set(checked, casa_diag, True)

			casa_dir_0 = self.nova_casa(casa_diag, directions[0])
			casa_dir_1 = self.nova_casa(casa_diag, directions[1])

			while self.get(board, casa_dir_0) == piece and quantidade_atual_0 < quantidade_maxima_0 - 2:
				# print "casa_dir_0:", casa_dir_0
				quantidade_atual_0 += 1
				if self.get(checked, casa_dir_0) == False:
					stable_return[player] += 1
					self.set(checked, casa_dir_0, True)
				casa_dir_0 = self.nova_casa(casa_dir_0, directions[0])

			while self.get(board, casa_dir_1) == piece and quantidade_atual_1 < quantidade_maxima_1 - 2:
				# print "casa_dir_1:", casa_dir_1
				quantidade_atual_1 += 1
				if self.get(checked, casa_dir_1) == False:
					stable_return[player] += 1
					self.set(checked, casa_dir_1, True)
				casa_dir_1 = self.nova_casa(casa_dir_1, directions[1])

			quantidade_maxima_0 = quantidade_atual_0
			quantidade_maxima_1 = quantidade_atual_1
			casa_diag = self.nova_casa(casa_diag, directions[2])

		return stable_return

	def stable_pieces(self, board, player):
		player_stable, opponent_stable = 0, 0
		checked = [[False]*9 for _ in xrange(9)]
		corners = [[1,1], [1,8], [8,1], [8,8]]
		for corner in corners:
			player_aux, opponent_aux = self.count_stable(board, player, corner, checked)
			player_stable += player_aux
			opponent_stable += opponent_aux
		return player_stable, opponent_stable


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

		player_frontier, opponent_frontier = self.frontier(board, player)
		board_score += (player_frontier - opponent_frontier) * 11

		player_stable, opponent_stable = self.stable_pieces(board, player)
		board_score += (player_stable - opponent_stable) * 33


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

	def cmp_moves(self, a, b):
		boarda = self.abboard.get_clone()
		boarda.play(a, self.abplayer)
		vala = self.evaluate_board(boarda, self.abplayer)
		boardb = self.abboard.get_clone()
		boardb.play(b, self.abplayer)
		valb = self.evaluate_board(boardb, self.abplayer)
		return valb-vala

	# trocar ordem de player e board na lista de argumentos
	def alphabeta(self, player, board, alpha, beta, depth):

		if depth == 0:
			return self.evaluate_board(board, player), None

		opponent = board._opponent(player)
		valid_moves = board.valid_moves(player)

		if not valid_moves:
			if not board.valid_moves(opponent):
				return self.final_value(board, player), None
			return -self.alphabeta(opponent, board, -beta, -alpha, depth-1)[0], None

		# self.abplayer = player
		# self.abboard = board
		# self.abboard.sort(cmp_moves)

		best_move = valid_moves[0]
		# for i in range((len(valid_moves)+1)/2):
			# move = valid_moves[i]
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

		depth = 3
		if board.valid_moves(self.color).__len__() < 5:
			depth = 6
		if empty_squares < 13:
			# print "AGORA"
			depth = 20
		move = self.alphabeta(self.color, board, float('-inf'), float('inf'), depth)
		if move[0] == float('inf'):
			print "ate a prox, loser"
		print move[0]
		return move[1]


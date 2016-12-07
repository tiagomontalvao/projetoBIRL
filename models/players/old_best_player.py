class BestPlayer:
	def __init__(self, color):
		self.color = color

	def is_frontier_piece(self, board, i, j):
		ans = False
		# Olha todos os 8 vizinhos. Casas fora do tabuleiro sao preenchidas com o caractere '?'
		for direction in board.DIRECTIONS:
			ni, nj = i+direction[0], j+direction[1]
			if board[ni][nj] == board.EMPTY:
				ans = True
				break
		return ans

	def frontier(self, board):
		player, opponent = 0, 0
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == self.color:
					player += self.is_frontier_piece(board, i, j)
				if board[i][j] == board._opponent(self.color):
					opponent += self.is_frontier_piece(board, i, j)
		return player, opponent

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
	def count_stable(self, board, corner, checked):
		stable_return = [0, 0]

		# Se a quina estiver vazia
		if board[corner[0]][corner[1]] == board.EMPTY:
			return stable_return

		# print "corner:", corner
		
		directions = self.get_directions(board, corner)
		piece = self.get(board, corner)

		# indice do jogador com peca na quina: 0 se for quem esta jogando e 1 se for o oponente
		player = 0 if self.get(board, corner) is self.color else 1


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

	def stable_pieces(self, board):
		player, opponent = 0, 0
		checked = [[False]*9 for _ in xrange(9)]
		corners = [[1,1], [1,8], [8,1], [8,8]]
		for corner in corners:
			player_stable, opponent_stable = self.count_stable(board, corner, checked)
			player += player_stable
			opponent += opponent_stable
		return player, opponent

	def play(self, board):
		valid_moves = board.valid_moves(self.color)

		# Testando funcao stable_pieces():
		# player_stable, opponent_stable = self.stable_pieces(board)
		print self.stable_pieces(board)

		# Player apenas chamado tendo lista com pelo menos um elemento
		choosen_move = valid_moves[0]
		maxi = -1

		for move in valid_moves:
			test_board = board.get_clone()
			test_board.play(move, self.color)
			player_frontier, opponent_frontier = self.frontier(board)

			if opponent_frontier - player_frontier > maxi:
				maxi = opponent_frontier - player_frontier
				choosen_move = move

		return choosen_move

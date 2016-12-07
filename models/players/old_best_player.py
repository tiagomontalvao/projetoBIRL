import random

class OldBestPlayer:
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
		return [player, opponent]

	def get_directions(self, board, corner):
		if corner == [1,1]:
			return [board.DOWN, board.RIGHT, board.DOWN_RIGHT, board.UP, board.LEFT]
		elif corner == [1,8]:
			return [board.DOWN, board.LEFT, board.DOWN_LEFT, board.UP, board.RIGHT]
		elif corner == [8,1]:
			return [board.UP, board.RIGHT, board.UP_RIGHT, board.DOWN, board.LEFT]
		elif corner == [8,8]:
			return [board.UP, board.LEFT, board.UP_LEFT, board.DOWN, board.RIGHT]

	# Retorna posicao (casa + direction)
	def nova_casa(self, casa, direction):
		return [casa[0] + direction[0], casa[1] + direction[1]]

	# Retorna valor da matriz, indexada pela lista indice[]
	def valor(self, matriz, indice):
		return matriz[indice[0]][indice[1]]

	# Conta quantas pecas estaveis existem em torno de uma quina
	# Ainda com um bug (camadas mais internas podendo ter mais pecas que as externas)
	def count_stable(self, board, corner, checked):
		stable_return = [0, 0]

		# Se a quina estiver vazia
		if board[corner[0]][corner[1]] == board.EMPTY:
			return stable_return

		# print "corner:", corner
		
		directions = self.get_directions(board, corner)
		piece = board[corner[0]][corner[1]]

		# indice do jogador com peca na quina: 0 se for quem esta jogando e 1 se for o oponente
		player = 0 if self.valor(board, corner) is self.color else 1

		casa_diag = corner
		while self.valor(board, casa_diag) == piece:
			if self.valor(checked, casa_diag) == True:
				break
			# Inicio da correcao do ~bug~
			# if casa_diag != corner:
			# 	a = self.valor(board, self.nova_casa(casa_diag, directions[3])) != piece
			# 	b = self.valor(board, self.nova_casa(casa_diag, directions[4])) != piece
			# 	if a or b:
			# 		break

			checked[casa_diag[0]][casa_diag[1]] = True
			stable_return[player] += 1

			casa_dir_0 = self.nova_casa(casa_diag, directions[0])
			casa_dir_1 = self.nova_casa(casa_diag, directions[1])

			while self.valor(board, casa_dir_0) == piece:
				if self.valor(checked, casa_dir_0) == True:
					break
				checked[casa_dir_0[0]][casa_dir_0[1]] = True
				casa_dir_0 = self.nova_casa(casa_dir_0, directions[0])
				stable_return[player] += 1

			while board[casa_dir_1[0]][casa_dir_1[1]] == piece:
				if self.valor(checked, casa_dir_1) == True:
					break
				checked[casa_dir_1[0]][casa_dir_1[1]] = True
				casa_dir_1 = self.nova_casa(casa_dir_1, directions[1])
				stable_return[player] += 1

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
		return [player, opponent]

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

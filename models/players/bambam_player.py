class BambamPlayer:
	def __init__(self, color):
		self.color = color

	# Retorna 1 se todos ha alguma casa adjacente vazia e 0 caso contrario
	def is_frontier_piece(self, board, i, j):
		ans = 0
		# Olha todos os 8 vizinhos. Casas fora do tabuleiro sao preenchidas com o caractere '?'
		for direction in board.DIRECTIONS:
			ni, nj = i+direction[0], j+direction[1]
			if board[ni][nj] == board.EMPTY:
				ans = 1
		return ans

	# Retorna um par [player_frontier, opponent_frontier] indicando
	# quantas pecas de fronteira cada player possui
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

	# Funcao auxiliar para caminhar a partir de cada corner
	def get_directions(self, board, corner):
		if corner == [1,1]:
			return board.DOWN, board.RIGHT, board.DOWN_RIGHT, board.UP_RIGHT, board.DOWN_LEFT
		elif corner == [1,8]:
			return board.DOWN, board.LEFT, board.DOWN_LEFT, board.UP_LEFT, board.DOWN_RIGHT
		elif corner == [8,1]:
			return board.UP, board.RIGHT, board.UP_RIGHT, board.DOWN_RIGHT, board.UP_LEFT
		elif corner == [8,8]:
			return board.UP, board.LEFT, board.UP_LEFT, board.DOWN_LEFT, board.UP_RIGHT

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
	# Ainda com um pequeno bug
	def count_stable(self, board, player, corner, is_stable):
		stable_return = [0, 0]

		# se a quina estiver vazia
		if board[corner[0]][corner[1]] == board.EMPTY:
			return stable_return

		# pega direcoes
		directions = self.get_directions(board, corner)

		# armazena qual peca esta em corner
		piece = self.get(board, corner)

		# indice do jogador com peca na quina: 0 se for quem esta jogando e 1 se for o oponente
		player = 0 if self.get(board, corner) is player else 1

		# variaveis auxiliares
		casa_diag = corner
		quantidade_maxima_0 = 10
		quantidade_maxima_1 = 10
		# olha cada casa da diagonal da quina
		while self.get(board, casa_diag) == piece and min(quantidade_maxima_0, quantidade_maxima_1) > 1:
			quantidade_atual_0 = 1
			quantidade_atual_1 = 1
			vala = self.get(is_stable, self.nova_casa(casa_diag, directions[3]))
			valb = self.get(is_stable, self.nova_casa(casa_diag, directions[4]))
			if not vala and not valb:
				break
			# se casa nao foi contada antes, conta e marca como visitada
			if self.get(is_stable, casa_diag) == False:
				stable_return[player] += 1
				self.set(is_stable, casa_diag, True)

			# posicoes que serao variadas em cada direcao
			casa_dir_0 = self.nova_casa(casa_diag, directions[0])
			casa_dir_1 = self.nova_casa(casa_diag, directions[1])

			# enquanto a casa for valida, avance na direcao correspondente
			while self.get(board, casa_dir_0) == piece and quantidade_atual_0 < quantidade_maxima_0 - 2:
				quantidade_atual_0 += 1
				# se casa nao foi contada antes, conta e marca como visitada
				if self.get(is_stable, casa_dir_0) == False:
					stable_return[player] += 1
					self.set(is_stable, casa_dir_0, True)
				# avanca na direcao correspondente
				casa_dir_0 = self.nova_casa(casa_dir_0, directions[0])

			# enquanto a casa for valida, avance na direcao correspondente
			while self.get(board, casa_dir_1) == piece and quantidade_atual_1 < quantidade_maxima_1 - 2:
				quantidade_atual_1 += 1
				# se casa nao foi contada antes, conta e marca como visitada
				if self.get(is_stable, casa_dir_1) == False:
					stable_return[player] += 1
					self.set(is_stable, casa_dir_1, True)
				# avanca na direcao correspondente
				casa_dir_1 = self.nova_casa(casa_dir_1, directions[1])

			# atualiza variaveis auxiliares
			quantidade_maxima_0 = quantidade_atual_0
			quantidade_maxima_1 = quantidade_atual_1

			# avanca casa da diagonal
			casa_diag = self.nova_casa(casa_diag, directions[2])

		# segunda passada para cuidar de pecas nao consideradas anteriormente
		casa_diag = corner
		quantidade_maxima_0 = 10
		quantidade_maxima_1 = 10
		# olha cada casa da diagonal da quina
		while self.get(board, casa_diag) == piece and min(quantidade_maxima_0, quantidade_maxima_1) > 1:
			quantidade_atual_0 = 1
			quantidade_atual_1 = 1
			vala = self.get(is_stable, self.nova_casa(casa_diag, directions[3]))
			valb = self.get(is_stable, self.nova_casa(casa_diag, directions[4]))
			if not vala and not valb:
				break
			# se casa nao foi contada antes, conta e marca como visitada
			if self.get(is_stable, casa_diag) == False:
				stable_return[player] += 1
				self.set(is_stable, casa_diag, True)

			# posicoes que serao variadas em cada direcao
			casa_dir_0 = self.nova_casa(casa_diag, directions[0])
			casa_dir_1 = self.nova_casa(casa_diag, directions[1])

			# enquanto a casa for valida, avance na direcao correspondente
			while self.get(board, casa_dir_0) == piece and quantidade_atual_0 < quantidade_maxima_0 - 1:
				if quantidade_atual_0 == quantidade_maxima_0 - 2:
					if not self.get(is_stable, self.nova_casa(casa_dir_0, directions[3])):
						break
				quantidade_atual_0 += 1
				# se casa nao foi contada antes, conta e marca como visitada
				if self.get(is_stable, casa_dir_0) == False:
					stable_return[player] += 1
					self.set(is_stable, casa_dir_0, True)
				# avanca na direcao correspondente
				casa_dir_0 = self.nova_casa(casa_dir_0, directions[0])

			# enquanto a casa for valida, avance na direcao correspondente
			while self.get(board, casa_dir_1) == piece and quantidade_atual_1 < quantidade_maxima_1 - 1:
				if quantidade_atual_1 == quantidade_maxima_1 - 2:
					if not self.get(is_stable, self.nova_casa(casa_dir_1, directions[4])):
						break
				quantidade_atual_1 += 1
				# se casa nao foi contada antes, conta e marca como visitada
				if self.get(is_stable, casa_dir_1) == False:
					stable_return[player] += 1
					self.set(is_stable, casa_dir_1, True)
				# avanca na direcao correspondente
				casa_dir_1 = self.nova_casa(casa_dir_1, directions[1])

			# atualiza variaveis auxiliares
			quantidade_maxima_0 = quantidade_atual_0
			quantidade_maxima_1 = quantidade_atual_1

			# avanca casa da diagonal
			casa_diag = self.nova_casa(casa_diag, directions[2])

		return stable_return

	# Retorna um par [player_stable, opponent_stable] indicando
	# quntas pecas estaveis cada player possui
	def stable_pieces(self, board, player):
		player_stable, opponent_stable = 0, 0
		is_stable = [[True]*10 for _ in xrange(10)]
		for i in range(1,9):
			for j in range(1,9):
				is_stable[i][j] = False
		corners = [[1,1], [1,8], [8,1], [8,8]]
		for corner in corners:
			player_aux, opponent_aux = self.count_stable(board, player, corner, is_stable)
			player_stable += player_aux
			opponent_stable += opponent_aux
		return player_stable, opponent_stable

	# Funcao de avaliacao do tabuleiro
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

		# TROCAR:
		# calcular pecas estaveis antes e dar pesos dinamicamente para a matriz

		# matriz de pesos
		evaluation = [[0, 0, 0, 0, 0, 0, 0, 0, 0],
					  [0, g, a, h, b, b, h, a, g],
					  [0, a, i, c, c, c, c, i, a],
					  [0, h, c, d, e, e, d, c, h],
					  [0, b, c, e, f, f, e, c, b],
					  [0, b, c, e, f, f, e, c, b],
					  [0, h, c, d, e, e, d, c, h],
					  [0, a, i, c, c, c, c, i, a],
					  [0, g, a, h, b, b, h, a, g]]

		# pega oponente de player
		opponent = board._opponent(player)

		# calcula score de acordo com a matriz de pesos
		board_score = 0
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == player:
					board_score += evaluation[i][j]
				if board[i][j] == opponent:
					board_score -= evaluation[i][j]

		# atribui pesos para as pecas de fronteira
		player_frontier, opponent_frontier = self.frontier(board, player)
		board_score += (opponent_frontier - player_frontier) * 11

		# atribui pesos para as pecas estaveis
		player_stable, opponent_stable = self.stable_pieces(board, player)
		board_score += (player_stable - opponent_stable) * 33

		return board_score

	# Funcao chamada quando jogo acabou
	# Retorna inf se player ganhou, -inf se player perdeu ou 0 em caso de empate
	def final_value(self, board, player):
		white_score, black_score = board.score()

		# calcula vantagem do player sobre o oponente
		return_value = 0
		if player == board.WHITE:
			return_value = white_score - black_score
		else:
			return_value = black_score - white_score

		# transforma valor em inf, -inf ou 0
		if return_value > 0:
			return_value = float('inf')
		elif return_value < 0:
			return_value = float('-inf')

		return return_value

	# Minimax com corte alpha-beta
	def alphabeta(self, player, board, alpha, beta, depth):

		# se profundidade limite foi atingida, retorna avaliacao do tabuleiro
		if depth == 0:
			return self.evaluate_board(board, player), None

		# pega oponente e lista de movimentos validos de player 
		opponent = board._opponent(player)
		valid_moves = board.valid_moves(player)

		# se nao tiver movimentos validos...
		if not valid_moves:
			# ... e nem o oponente, entao jogo acabou e eh retornado o valor de final_value
			if not board.valid_moves(opponent):
				return self.final_value(board, player), None
			# ... mas o oponente tem, passa a jogada
			return -self.alphabeta(opponent, board, -beta, -alpha, depth-1)[0], None

		# olha cada movimento
		best_move = valid_moves[0]
		for move in valid_moves:
			# corte alpha-beta
			if alpha >= beta:
				break
			# clona board e faz jogada neste novo tabuleiro
			test_board = board.get_clone()
			test_board.play(move, player)
			# expande a arvore de busca
			val = -self.alphabeta(opponent, test_board, -beta, -alpha, depth-1)[0]
			# atualiza melhor jogada se for o caso
			if val > alpha:
				alpha = val
				best_move = move

		return alpha, best_move

	import random

	def play(self, board):
		
		print self.stable_pieces(board, self.color)

		# calcula quantidade de casas vazias
		score = board.score()
		empty_squares = 64 - sum(score)

		# na primeira jogada faz jogada qualquer
		if empty_squares == 60:
			return self.random.choice(board.valid_moves(self.color))

		# inicializa profundidade padrao de 4 niveis
		depth = 2
		# depth = 4

		# se houver poucos movimentos, aumenta a profundidade
		if board.valid_moves(self.color).__len__() < 6:
			depth = 2
			# depth = 6

		# se houver poucas casas vazias, explora a arvore toda
		if empty_squares < 13:
			# print "AGORA"
			depth = 20

		# faz o movimento
		move = self.alphabeta(self.color, board, float('-inf'), float('inf'), depth)

		# se vitoria estiver garantida, manda mensagens ofensivas hehe
		if move[0] == float('inf'):
			print "ate a prox, loser"

		print move[0]
		
		return move[1]


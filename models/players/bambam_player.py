import timeit

class BambamPlayer:
	def __init__(self, color):
		self.color = color
		self.times = []

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
	def stable_pieces(self, board, player, is_stable):
		player_stable, opponent_stable = 0, 0
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

		is_stable = [[False]*10 for _ in xrange(10)]
		for i in range(10):
			is_stable[i][0] = is_stable[i][9] = True
		for j in range(10):
			is_stable[0][j] = is_stable[9][j] = True

		# calcula score de acordo com a matriz de pesos
		board_score = 0

		# atribui pesos para as pecas estaveis
		player_stable, opponent_stable = self.stable_pieces(board, player, is_stable)
		board_score += (player_stable - opponent_stable) * 33

		# atribui pesos para as pecas de fronteira
		player_frontier, opponent_frontier = self.frontier(board, player)
		board_score += (opponent_frontier - player_frontier) * 11

		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == player:
					if is_stable[i][j]:
						board_score += 151 - int(abs(4.5 - i) + abs(4.5 - j)**2.37)
					else:
						board_score += evaluation[i][j]
				if board[i][j] == opponent:
					if is_stable[i][j]:
						board_score -= 151 - int(abs(4.5 - i) + abs(4.5 - j)**2.37)
					else:
						board_score -= evaluation[i][j]



		return board_score

	# Funcao que faz um movimento em board e retorna lista de pecas viradas
	def make_move(self, board, move, color):
		lista = []
		if (color == board.BLACK) or (color == board.WHITE):
			board.board[move.x][move.y] = color
			lista = self._reverse(board, move, color)
		return lista

	# Funcoes auxiliares para make_move
	def _reverse(self, board, move, color):
		lista = []
		for direction in board.DIRECTIONS:
			lista.extend(self._make_flips(board, move, color, direction))
		return lista

	def _make_flips(self, board, move, color, direction):
		bracket = board._find_bracket(move, color, direction)
		if not bracket:
			return []
		square = [move.x + direction[0], move.y + direction[1]]
		lista = []
		while square != bracket:
			board.board[square[0]][square[1]] = color
			lista.append(square)
			square = [square[0] + direction[0], square[1] + direction[1]]
		return lista

	# Recebe movimento e lista de posicoes flipadas e troca
	def undo_move(self, board, move, flips):
		board.board[move.x][move.y] = board.EMPTY
		for flip in flips:
			flip_color = board._opponent(board.board[flip[0]][flip[1]])
			board.board[flip[0]][flip[1]] = flip_color

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
			# faz o movimento no mesmo tabuleiro
			flips = self.make_move(board, move, player)
			# expande a arvore de busca
			val = -self.alphabeta(opponent, board, -beta, -alpha, depth-1)[0]
			# desfaz o movimento no tabuleiro
			self.undo_move(board, move, flips)
			# atualiza melhor jogada se for o caso
			if val > alpha:
				alpha = val
				best_move = move

		return alpha, best_move

	import random

	def play(self, board):

		is_stable = [[True]*10 for _ in xrange(10)]
		for i in range(1,9):
			for j in range(1,9):
				is_stable[i][j] = False
		print self.stable_pieces(board, self.color, is_stable)

		# calcula quantidade de casas vazias
		score = board.score()
		empty_squares = 64 - sum(score)

		# na primeira jogada faz jogada qualquer
		if empty_squares == 60:
			return self.random.choice(board.valid_moves(self.color))

		# inicializa profundidade padrao de 4 niveis
		depth = 4

		valid_moves = board.valid_moves(self.color)

		if valid_moves.__len__() == 1:
			return valid_moves[0]

		# se houver poucos movimentos, aumenta a profundidade
		if valid_moves.__len__() < 6:
			depth = 6

		# se houver poucas casas vazias, explora a arvore toda
		if empty_squares < 12:
			depth = 20

		# faz o movimento
		start_time = timeit.default_timer()
		move = self.alphabeta(self.color, board, float('-inf'), float('inf'), depth)
		elapsed = timeit.default_timer() - start_time
		self.times.append(elapsed)
		print 'now:', elapsed, 'seconds'
		print 'avg:', sum(self.times)/len(self.times), 'seconds'

		# se vitoria estiver garantida, manda mensagens ofensivas hehe
		if move[0] == float('inf'):
			print "ate a prox, loser"

		print move[0]

		return move[1]
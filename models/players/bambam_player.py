import timeit

class Bambam:
	def __init__(self, color):
		# tempo limite da jogada
		self.time_limit = 30
		# cor do bambam
		self.color = color
		# lista de tempos de cada jogada
		self.times = []
		# transposition table para armazenar jogadas ja calculadas
		self.transposition_table = {}
		# lista de falas do bambam
		self.victory_messages = ['BIRL', 'eh verao o ano todo', 'ajuda o maluco ta doente',
								 'eh ele que a gente quer', 'boraaaa, hora do show p***a',
								 'sai de casa, comi pra c***lho', 'ta saindo da jaula o monstro',
								 'nao vai dar nao', 'que nao vai dar o que']
		# CODIGO PARA TESTE
		self.debug = False

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

		# matriz de pesos com menos de 21 pecas
		evaluation0 = [[0,   0,   0,   0,   0,   0,   0,   0,   0],
					   [0, 150, -20,  33,  20,  20,  33, -20, 150],
					   [0, -20, -50, -10, -10, -10, -10, -50, -20],
					   [0,  33, -10,  20,   3,   3,  20, -10,  33],
					   [0,  20, -10,   3,   2,   2,   3, -10,  20],
					   [0,  20, -10,   3,   2,   2,   3, -10,  20],
					   [0,  33, -10,  20,   3,   3,  20, -10,  33],
					   [0, -20, -50, -10, -10, -10, -10, -50, -20],
					   [0, 150, -20,  33,  20,  20,  33, -20, 150]]

		# matriz de pesos com mais de 20 pecas
		evaluation1 = [[0,   0,   0,   0,   0,   0,   0,   0,   0],
					   [0, 120, -20,  20,   5,   5,  20, -20, 120],
					   [0, -20, -40,  -5,  -5,  -5,  -5, -40, -20],
					   [0,  20,  -5,  15,   3,   3,  15,  -5,  20],
					   [0,   5,  -5,   3,   2,   2,   3,  -5,   5],
					   [0,   5,  -5,   3,   2,   2,   3,  -5,   5],
					   [0,  20,  -5,  15,   3,   3,  15,  -5,  20],
					   [0, -20, -40,  -5,  -5,  -5,  -5, -40, -20],
					   [0, 120, -20,  20,   5,   5,  20, -20, 120]]

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

		# variaveis auxiliares
		player_score, opponent_score = board.score()
		if player == board.BLACK:
			player_score, opponent_score = opponent_score, player_score
		aux = board_score

		# atualiza score de acordo com cada peca e sua respectiva posicao
		for i in range(1, 9):
			for j in range(1, 9):
				if board[i][j] == player:
					if is_stable[i][j]:
						board_score += 151 - (abs(4.5 - i) + abs(4.5 - j))**2.37
					else:
						if player_score + opponent_score <= 20:
							board_score += evaluation0[i][j]
						else:
							board_score += evaluation1[i][j]
				if board[i][j] == opponent:
					if is_stable[i][j]:
						board_score -= 151 - (abs(4.5 - i) + abs(4.5 - j))**2.37
					else:
						if player_score + opponent_score <= 20:
							board_score -= evaluation0[i][j]
						else:
							board_score -= evaluation1[i][j]

		# se player nao tiver pecas, entao perdeu o jogo
		if player_score == 0:
			return float('-inf')
		if opponent_score == 0:
			return float('inf')

		# para debug
		aux = board_score - aux

		# atribui pesos para as pecas de fronteira
		player_frontier, opponent_frontier = self.frontier(board, player)
		frontier_aux = (opponent_frontier - player_frontier) * 11
		if frontier_aux < board_score:
			board_score += frontier_aux

		# CODIGO PARA TESTE
		# valores importantes do tabuleiro
		# self.debug = True
		if self.debug:
			print 'stable:', player_stable, opponent_stable
			print 'frontier:', player_frontier, opponent_frontier
			print 'stable_score:', (player_stable - opponent_stable) * 33
			print 'frontier_score:', frontier_aux
			print 'matrix_weights:', aux
			print 'board_score:', board_score
			self.debug = False

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

	# Recebe movimento e lista de posicoes flipadas e desfaz movimento
	def undo_move(self, board, move, flips):
		board.board[move.x][move.y] = board.EMPTY
		for flip in flips:
			flip_color = board._opponent(board.board[flip[0]][flip[1]])
			board.board[flip[0]][flip[1]] = flip_color

	# Funcao chamada quando jogo acabou
	# Retorna inf se player ganhou, -inf se player perdeu ou 0 em caso de empate
	def final_score(self, board, player):
		white_score, black_score = board.score()

		# calcula vantagem do player sobre o oponente
		return_value = 0
		if player == board.WHITE:
			return_value = white_score - black_score
		else:
			return_value = black_score - white_score

		# transforma valor em inf, -inf ou 0
		if return_value > 0:
			return_value += 1000000000000
		elif return_value < 0:
			return_value -= 1000000000000

		return return_value

	# Negamax com corte alpha-beta
	# Retorna um par [val, best_move], indicando o valor do melhor movimento e o melhor movimento
	def alphabeta(self, board, player, alpha, beta, depth, start_time):

		alphaOrig = alpha

		# tupla que armazena o estado para consulta na transposition table
		state_tuple = tuple(tuple(x) for x in board)

		EXACT, LOWERBOUND, UPPERBOUND = 0, 1, 2

		# consulta a transposition table e retorna o valor se ja foi calculado
		# transposition_table = (value, flag, depth, move)
		if state_tuple in self.transposition_table:
			ttEntry = self.transposition_table[state_tuple]
			if ttEntry[2] >= depth:
				if ttEntry[1] == EXACT:
					return ttEntry[0], ttEntry[3]
				elif ttEntry[1] == LOWERBOUND:
					alpha = max(alpha, ttEntry[0])
				elif ttEntry[1] == UPPERBOUND:
					beta = min(beta, ttEntry[0])
				if alpha >= beta:
					return ttEntry[0], ttEntry[3]

		# se profundidade limite foi atingida, retorna avaliacao do tabuleiro
		if depth == 0:
			return self.evaluate_board(board, player), None

		# pega oponente e lista de movimentos validos de player
		opponent = board._opponent(player)
		valid_moves = board.valid_moves(player)

		# se nao tiver movimentos validos...
		if not valid_moves:
			# ... e nem o oponente, entao jogo acabou e eh retornado o valor de final_score
			if not board.valid_moves(opponent):
				return self.final_score(board, player), None
			# ... mas o oponente tem, passa a jogada
			return -self.alphabeta(board, opponent, -beta, -alpha, depth-1, start_time)[0], None

		# olha cada movimento
		best_score = float('-inf')
		best_move = valid_moves[0]

		for move in valid_moves:
			# so faz jogada se tiver tempo
			if timeit.default_timer() - start_time > self.time_limit:
				return alpha, best_move

			# faz o movimento no mesmo tabuleiro
			flips = self.make_move(board, move, player)
			# expande a arvore de busca
			move_score = -self.alphabeta(board, opponent, -beta, -alpha, depth-1, start_time)[0]
			# desfaz o movimento no tabuleiro
			self.undo_move(board, move, flips)
			# atualiza melhor jogada se for o caso
			if best_score < move_score:
				best_score = move_score
				best_move = move

			alpha = max(alpha, move_score)

			# corte alpha-beta
			if alpha >= beta:
				break

		flag = EXACT
		if best_score <= alphaOrig:
			flag = UPPERBOUND
		elif best_score >= beta:
			flag = LOWERBOUND

		# armazena o valor na transposition table
		self.transposition_table[state_tuple] = (best_score, flag, depth, best_move)

		return best_score, best_move

	import random

	# Funcao principal chamada pelo controller
	# Retorna um move dentro de valid_moves
	def play(self, board):

		# CODIGO PARA TESTE
		# valor do tabuleiro atual
		# self.debug = True
		if self.debug:
			is_stable = [[False]*10 for _ in xrange(10)]
			for i in range(10):
				is_stable[i][0] = is_stable[i][9] = True
			for j in range(10):
				is_stable[0][j] = is_stable[9][j] = True
			self.evaluate_board(board, self.color)
			self.debug = False

		# calcula quantidade de casas vazias
		empty_squares = 64 - sum(board.score())

		# na primeira jogada faz jogada qualquer
		if empty_squares == 60:
			return self.random.choice(board.valid_moves(self.color))

		# inicializa profundidade padrao de 4 niveis
		depth = 5

		valid_moves = board.valid_moves(self.color)

		# se so houver uma jogada valida, nao precisa chamar alphabeta
		if valid_moves.__len__() == 1:
			# self.debug = True
			if self.debug:
				self.times.append(elapsed)
				print 'now:', elapsed, 'seconds'
				print 'avg:', sum(self.times)/len(self.times), 'seconds'
				self.debug = False
			return valid_moves[0]

		# se houver poucos movimentos, aumenta a profundidade
		if valid_moves.__len__() < 6:
			depth = 7

		# se houver poucas casas vazias, explora a arvore toda
		if empty_squares < 12:
			depth = 20

		# inicio da medida de tempo da jogada
		start_time = timeit.default_timer()
		
		# faz o movimento
		move = self.alphabeta(board, self.color, float('-inf'), float('inf'), depth, start_time)

		# final da medida de tempo da jogada
		elapsed = timeit.default_timer() - start_time
		self.times.append(elapsed)

		# CODIGO PARA TESTE
		# medidas de tempo
		# self.debug = True
		if self.debug:
			print 'now:', elapsed, 'seconds'
			# print 'avg:', sum(self.times)/len(self.times), 'seconds'
			self.debug = False

		# se vitoria estiver garantida, manda mensagens ofensivas hehe
		if empty_squares < 12 and move[0] > 1000000000000:
			print self.random.choice(self.victory_messages)

		# CODIGO PARA TESTE
		# valor do melhor movimento
		# self.debug = True
		if self.debug:
			print move[0]
			self.debug = False

		return move[1]
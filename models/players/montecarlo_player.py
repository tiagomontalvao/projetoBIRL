import datetime
from random import choice

class MonteCarloTreeSearchPlayer(object):
	def __init__(self, color):
		self.color = color
		self.states = []
		self.board = None
		self.calculation_time = datetime.timedelta(seconds=6)
		self.max_moves = 100
		self.wins = {}
		self.plays = {}

	def to_tuple(self, mat):
		return tuple(tuple(x) for x in mat)

	def winner(self, board):
		if board.valid_moves(self.color).__len__() > 0:
			return -1
		if board.valid_moves(board._opponent(self.color)).__len__() > 0:
			return -1
		score = board.score()
		if score[0] > score[1]:
			return board.WHITE
		elif score[0] < score[1]:
			return board.BLACK
		else:
			return 0

	def run_simulation(self, player):
		visited_states = set()
		states_copy = self.states[:]
		state = states_copy[-1]

        expand = True
        for t in xrange(self.max_moves):
            legal = self.board.valid_moves(player)

            move = choice(legal)
            state.play(move, player)
            states_copy.append(state)

            # `player` here and below refers to the player
            # who moved into that particular state.
            if expand and (player, state) not in self.plays:
                expand = False
                self.plays[(player, to_tuple(state))] = 0
                self.wins[(player, to_tuple(state))] = 0

            visited_states.add((player, to_tuple(state)))

            player = self.board._opponent(player)
            winner = self.winner(state)
            if winner:
                break

        for player, state in visited_states:
            if (player, state) not in self.plays:
                continue
            self.plays[(player, to_tuple(state))] += 1
            if player == winner:
                self.wins[(player, to_tuple(state))] += 1

	def play(self, board):
		begin = datetime.datetime.utcnow()
		while datetime.datetime.utcnow() - begin < self.calculation_time:
			self.run_simulation(self.color)


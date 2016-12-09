from models.move import Move
class HumanPlayer:
  def __init__(self, color):
    self.color = color

  def play(self, board):
    for idx, move in enumerate(board.valid_moves(self.color)):
      print str(idx) + '. [' + str(move.x) + ', ' + str(move.y) + ']'
    rowInp = int(raw_input("Linha: "))
    colInp = int(raw_input("Coluna: "))
    inp = int(raw_input("Jogada: "))
    while inp < 0 or inp >= board.valid_moves(self.color).__len__():
      print board
      print "Movimento invalido. Insira um valido."
      inp = int(raw_input("Jogada: "))
    return board.valid_moves(self.color)[inp]

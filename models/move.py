class Move:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __str__(self):
    ret =  self.x.__str__()
    ret += " "
    ret += self.y.__str__()
    return ret

  def __getitem__(self, i):
    if i == 0: return x
    if i == 1: return y

  def __eq__(self, other):
    return (self and other and self.x == other.x and self.y == other.y)


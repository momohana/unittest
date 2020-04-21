class HogeError(Exception):
  def __init__(self, code, message):
    self.code = code
    self.message = message
    
  def __str__(self):
    return "[{0}]: {1}".format(self.code, self.message)
  

def fuga():
  raise HogeError(1234, "hoge")

# wgs : weird george stuff
# Mostly recycled

def rf(fileLoc):
  file = open(fileLoc, "r")
  readFile = file.read()
  file.close()
  return readFile

def div(x, y): # avoid ZERO DIVISION ERROR
  if x == 0 or y == 0:
    return 0
  return x/y

def inSquare(x, y, sq1, sq2): # great for buttons or collisions
    if (x > sq1[0] and x < sq2[0]) and (y > sq1[1] and y < sq2[1]):
        return True
    return False

def round(x, y):
  return int(div(x,y))*y

class toggle:
  def __init__(self, togState=None):
    if togState is None:
      togState = False
    self.state = togState

  def tog(self):
    self.state = not self.state

class flipFlop(toggle):
  def __init__(self, funFalse, funTrue, togState=None):
    if togState is None:
      togState = False
    self.state = togState
    self.funs = funTrue, funFalse

  def run(self):
    if self.state:
      self.funs[0]()
    else:
      self.funs[1]()


class diction: # better dictionary
    def __init__(self, dictionary):
        self.key = [x[0] for x in dictionary]
        self.value = [x[1] for x in dictionary]

    def __len__(self):
      return len(self.key)

    def __add__(self, obj2):
      return [(x[0], x[1]) for x in self.key + obj2.key]

    def append(self, key, value):
        self.key.append(key)
        self.value.append(value)

    def get(self, key):
        return self.value[self.key.index(key)]

    def rGet(self, value):
        return self.key[self.value.index(value)]

    def remove(self, kv, key=True):
        if key:
            self.value.remove(self.value[self.key.index(kv)])
            self.key.remove(kv)
        else:
            self.key.remove(self.key[self.value.index(kv)])
            self.value.remove(kv)

    def getValues(self):
        return self.value

    def getKeys(self):
        return self.key

    def setValue(self, key, nv):
        self.value[self.key.index(key)] = nv

    def len(self):
        return len(self.key)

"""I found that this is not the best way to do things, but it is avaliable:


class keys:
    def __init__(self, keyBinds=None):
        if keyBinds is None:
            keyBinds = []
        self.keys = diction([("mouse", False)] + [(x, False) for x in keyBinds])
        self.downs = []

    def update(self):
        # key binds
        self.events = pg.event.get()
        self.gt = 0
        self.downs = []
        for event in self.events:
            if event.type == pg.QUIT:
                return False
            elif event.type == pg.MOUSEBUTTONUP:
                self.keys.setValue("mouse", False)
            elif event.type == pg.MOUSEBUTTONDOWN:
                self.keys.setValue("mouse", True)
                self.downs.append("mouse")
            elif event.type == pg.KEYDOWN:
                if event.key in self.keys.getKeys():
                    self.keys.setValue(event.key, True)
                    self.downs.append(event.key)
            elif event.type == pg.KEYUP:
                if event.key in self.keys.getKeys():
                    self.keys.setValue(event.key, False)
        return True

    def getKey(self, key):
        return self.keys.get(key)

    def getKeys(self):
        out = []
        for x in self.keys.getKeys():
            if self.keys.get(x):
                out.append(x)
        return out

    def getKeyDowns(self):
        return self.downs

    def getMouse(self):
        return self.keys.get("mouse"), pg.mouse.get_pos()

"""

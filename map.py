from chars import animatedSprite
from wgs import div, rf, round
from math import ceil as ru
from math import floor as rd

sd, mfps, cm, ts = None, None, None, None


def init(x, y, z):
    global sd, mfps, ts
    sd, mfps = x, y
    ts = z


class cmo:  # collision map object
    def __init__(self, map):
        global cm, sd, ts

        self.map = "mapDat/cMaps/{}.dat".format(map)
        self.sd = sd
        self.ts = ts
        self.file = rf(self.map)
        self.fl = [[
            x for x in y
        ] for y in self.file.split("\n")
        ]
        cm = self

    def move(self, pos, x=None, y=None):
        pos = [pos[0] - 2, pos[1] - 2]
        if x is None:
            pass
        elif x > 0:
            if not (self.fl[rd(-pos[1])][-rd(pos[0]) - 1] == "-" or self.fl[ru(-pos[1])][-rd(pos[0]) - 1] == "-"):
                pos[0] += x
        elif x < 0:
            if not (self.fl[rd(-pos[1])][rd(-pos[0]) + 1] == "-" or self.fl[ru(-pos[1])][rd(-pos[0]) + 1] == "-"):
                pos[0] += x

        if y is None:
            pass
        elif y < 0:
            if not (self.fl[-ru(pos[1]) + 1][-rd(pos[0])] == "-" or self.fl[-ru(pos[1]) + 1][-ru(pos[0])] == "-"):
                pos[1] += y
        elif y > 0:
            if not (self.fl[-rd(pos[1]) - 1][-rd(pos[0])] == "-" or self.fl[-rd(pos[1]) - 1][-ru(pos[0])] == "-"):
                pos[1] += y
        return [pos[0] + 2, pos[1] + 2]

    def isColliding(self, pos):
        pass


class mo:  # map object
    def __init__(self,
                 map, location=None):  # sd = screen dimensions
        if location is None:
            location = [0, 0]
        global ts
        tileSize = ts
        mapKey = rf("mapDat/maps/" + map + "/data.dat")
        self.location = location
        mapKey = "mapDat/imgs/{}/{}".format(mapKey, "{}")
        self.animations = rf(mapKey.format("ANIM.dat"))
        self.map = rf("mapDat/maps/" + map + "/main.dat").split("\n")
        self.mapList = [[x for x in y] for y in self.map]
        self.dim = (len(self.mapList[0]), len(self.mapList))
        if tileSize == 0:
            self.squareSize = [div(sd[0], self.dim[0]), div(sd[1], self.dim[1])]
        else:
            self.squareSize = tileSize
        self.tileSize = self.squareSize
        self.tL = [  # tile list
            [
                animatedSprite(
                    [x * self.squareSize[0], y * self.squareSize[1]],
                    mapKey.format(self.mapList[y][x] +
                                  self.isAnim(self.mapList[y][x])),
                    (self.squareSize[0] * 1.02, self.squareSize[1] * 1.02),
                    mfps) for x in range(len(self.mapList[y]))
            ] for y in range(len(self.mapList))
        ]

    def getgms(self):
        return len(self.tL[0]) / 5, len(self.tL) / 5


    def isAnim(self, x):
        if x in self.animations:
            return ""
        return ".png"

    """ update with init when done
    def newMap(self, map, sd, mapKey=None):  # sd = screen dimensions
        if mapKey is None:
            mapKey = mk
        self.map = open("imgs/maps/"+map+".dat").read().split("\n")
        self.mapList = [[x for x in y] for y in open("imgs/maps/"+map+".dat").read().split("\n")]
        self.dim = (len(self.mapList), len(self.mapList[0]))
        self.squareSize = [div(sd[0], self.dim[0]), div(sd[1], self.dim[1])]
        self.tL = [ # tile list
            [sprite([x*self.squareSize[0]*0.98, y*self.squareSize[1]*0.98],
                    mapKey[self.map[y][x]],
                    (self.squareSize[0], self.squareSize[1]))
             for x in range(len(self.map[y]))]
            for y in range(len(self.map))] # tile list
"""

    def draw(self, screen, frame):
        location = self.location
        for y in self.tL:
            for x in y:
                x.update(frame)
                x.mDraw(screen, (location[0] * self.tileSize[0],
                                 location[1] * self.tileSize[1]))

    def getts(self):
        return self.tL[0][0].ts

    def ml(self, right=None, down=None):
        if right is None:
            right = 0
        if down is None:
            down = 0
        self.location = cm.move(self.location, -right, -down)

    def getPos(self):
        return self.location

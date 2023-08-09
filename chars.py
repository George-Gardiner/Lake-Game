"""Recycled Code from LaiND (name subject to change) by George, also modified with comments"""

from pygame.image import load as li  # load image
from pygame.transform import scale as si  # scale image
from wgs import rf  # read file
from math import ceil as ru  # round up
from math import floor as rd  # round down
from math import fabs as abs
from wgs import inSquare as iS


class sprite:
    def __init__(self, pos, img, dim):
        self.pos = pos
        self.img = si(li(img), (dim[0], dim[1]))
        self.ts = (dim[0], dim[1])

    def spriteInit(self, pos, img, dim):
        self.pos = pos
        self.img = si(li(img), (dim[0], dim[1]))
        self.ts = (dim[0], dim[1])

    def setImg(self, img, dim):
        self.img = img
        self.img = si(li(img), dim)

    def draw(self, bg):
        bg.blit(self.img, (self.pos[0], self.pos[1]))

    def mDraw(self, bg, additive=None):  # almost the same as above, but could necessary for the SPEEEEEEEEED
        if additive is None:
            additive = 0, 0
        bg.blit(self.img, (self.pos[0] + additive[0], self.pos[1] + additive[1]))


class animation(sprite):  # not tested
    def __init__(self, pos, imgDir, dim, mfps):
        super().__init__(pos, imgDir + "/0.png", dim)
        self.mainFile = rf(imgDir + "/data.dat")
        self.fps = int(self.mainFile.split(",")[0])
        self.fc = int(self.mainFile.split(",")[1])  # frame count (number of frames)
        self.cf = 0
        self.mfps = mfps  # max frames per second
        self.imgDir = imgDir  # image directory
        self.dim = dim
        self.fpf = 20  # frames (of window) per frame (of sprite)

    def animInit(self, pos, imgDir, dim, mfps):
        super().__init__(pos, imgDir + "/0.png", dim)
        self.mainFile = rf(imgDir + "/data.dat")
        self.fps = int(self.mainFile.split(",")[0])
        self.fc = int(self.mainFile.split(",")[1])  # frame count (number of frames)
        self.cf = 0
        self.mfps = mfps  # max frames per second
        self.imgDir = imgDir
        self.dim = dim
        self.fpf = mfps / self.fps  # frames (of window) per frame (of sprite)

    def update(self, frame):
        # seconds = frame/self.mfps # should be the number of seconds since the start of the code
        pf = self.cf  # previos frame
        if frame % self.fpf == 0:  # seconds%(self.fps**-1) == 0:
            self.cf = (self.cf + 1) % self.fc
        # print(seconds)

        if pf != self.cf:
            super().setImg("{}/{}.png".format(self.imgDir, str(self.cf)), self.dim)


class animatedSprite(animation, sprite):
    def __init__(self, pos, img, dim, mfps):
        if ".png" in img:
            super().spriteInit(pos, img, dim)
        else:
            super().animInit(pos, img, dim, mfps)
        self.animated = not ".png" in img

    def update(self, frame):
        if self.animated:
            super().update(frame)


class collectable(animatedSprite):
    def __init__(self, pos, img, ts, mfps, fun, fipn=None, size=None):
        self.exists = True
        if size is None:
            size = ts
        self.rPos = pos
        pos = [pos[x] * ts[x] for x in range(2)]
        super().__init__(pos, img, size, mfps)
        self.fun = fun
        self.ts = ts

    def isColliding(self, pl):
        return self.col

    def draw(self, bg, pl, mp, f):
        if self.exists:
            pl = [abs(pl[0]), abs(pl[1])]
            super().mDraw(bg, (2 * self.ts[0] + self.ts[0] * mp[0], 2 * self.ts[1] + self.ts[1] * mp[1]))
            if ((ru(pl[0]), ru(pl[1])) == self.rPos) or ((ru(pl[0]), rd(pl[1])) == self.rPos) or (
                    (rd(pl[0]), ru(pl[1])) == self.rPos) or ((rd(pl[0]), rd(pl[1])) == self.rPos):
                print(7)
                self.col = True
                if not self.fun():
                    self.exists = False
            else:
                self.col = False


class interactable(collectable):
    pass



# unfinished:________________________________________________________________________________________________________________________
class btn(sprite):
    def __init__(self, startPos, endPos, img):
        super().__init__(startPos, img, (endPos[0] - startPos[0], endPos[1] - startPos[1]))
        self.collision, self.scp, self.ecp = [startPos,
                                              endPos], startPos, endPos  # start collision position, end collision position

    def isPressed(self, mousePos):
        if iS(mousePos[0], mousePos[1], self.scp, self.ecp):
            return True
        return False

# ___________________________________________________________________________________________________________________________________


class char(sprite):
    def __init__(self, mhp, pos, imgF, ts):
        super().__init__((pos[0] * ts[0], pos[1] * ts[1]), "Chars/{}/{}Idle.gif".format(imgF, imgF), ts)
        self.mhp = mhp  # max hit points
        self.chp = mhp  # current hit points
        self.imgFile = "Chars/{}/{}".format(imgF, imgF)
        self.ts = ts  # tile size

    def td(self, damage):  # take damage
        self.chp -= damage

    def move(self, pos, dir=None):
        if dir is None:
            if pos[0] < 0:
                self.setImg(self.imgFile + "Left.gif", self.ts)
            elif pos[0] > 0:
                self.setImg(self.imgFile + "Right.gif", self.ts)

        else:
            self.setImg(self.imgFile + dir, self.ts)


class player(char):
    def __init__(self, ts, sp=None):
        if sp is None:
            sp = 0, 0
        self.pos = sp  # tile location, not pixel location

"""The Lake Game
Copywrite, Copywrite, yada yada yada"""

import pygame as pg
from time import time as t
import math as pain
import winsound
from chars import *
from map import mo, cmo
import map as mp
from colors import lightGrey
from journal import journal

# vars
running = True
sd = 500, 500 # screen dimensions (x, y) || 80, 80 or multiple of is best
lf = t()  # last frame
fc = 0  # frame count
maps = []  # map1: main, map2: collision...
ts = (sd[0] / 5, sd[1] / 5)  # tile size
currentMap = 0, 0  # x, y (ts(tile size), not pxs(pixel size))
mfps = 24  # max fps
fps = mfps  # current frame rate
keys = {
    "mouse": False,
    pg.K_w: False,
    pg.K_a: False,
    pg.K_s: False,
    pg.K_d: False,
    pg.K_e: False,
    pg.K_q: False,
    pg.K_TAB: False
}
downKeys = []
book = journal(sd)
book.addPage("find the missing pages (total of 5)")
player = animation((sd[0] / 2 - sd[0] / 10, sd[1] / 2 - sd[0] / 10), "pDat/MC/IMG/IDLE", (sd[0] / 5, sd[1] / 5), mfps)

# setup pygame
pg.init()

bg = pg.display.set_mode(sd)

pgc = pg.time.Clock()


# main functions (these are in the program for the global variables)
def generalMainLoop():
    global running, downKeys, fc, fps

    downKeys = []

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.MOUSEBUTTONDOWN:
            keys["mouse"] = True
        elif event.type == pg.MOUSEBUTTONUP:
            keys["mouse"] = False
        elif event.type == pg.KEYDOWN:
            downKeys.append(event.key)
            if event.key in keys:
                keys[event.key] = True
        elif event.type == pg.KEYUP:
            if event.key in keys:
                keys[event.key] = False

    pg.display.update()

    pgc.tick(mfps)

    fc += 1


def chooseSave():
    global running

    while running:
        generalMainLoop()


def menu():
    global running

    while running:
        generalMainLoop()


def mainGameKeyBinds():
    for map in maps:
        if keys[pg.K_TAB]:
            if pg.K_e in downKeys:
                book.fp(True)
            if pg.K_q in downKeys:
                book.fp(False)
            book.draw(bg)
        else:
            if keys[pg.K_s]:
                map.ml(down=0.0625)
            if keys[pg.K_w]:
                map.ml(down=-0.0625)
            if keys[pg.K_d]:
                map.ml(right=0.0625)
            if keys[pg.K_a]:
                map.ml(right=-0.0625)


def mainGame():  # put char movement here
    global running

    while running:
        generalMainLoop()

        bg.fill(lightGrey)
        for map in maps:
            map.draw(bg, fc)

        for item in Rs:
            item.update(fc)
            item.draw(bg, maps[0].location, maps[0].location, fc)

        player.update(fc)
        player.draw(bg)
        maps[1].draw(bg, fc)

        mainGameKeyBinds()


#                create map
mp.init(sd, mfps, ts)
maps.append(mo("1-0", [-2, 0]))
maps.append(mo("1-1", [-2, 0]))
maps.append(mo("1-2", [-2, 0]))
gms = maps[0].getgms()
cm = cmo("1")



#                more vars and objects
#         collectables
def collect1():
    book.addPage("1:3")
    return False

def collect2():
    book.addPage("2:1")
    return False

def collect3():
    book.addPage("3:2")
    return False

def collect4():
    book.addPage("4:2")
    return False

def collect5():
    book.addPage("5:1")
    return False


Rs = [collectable((1, 6), "bookDat/paper.png", ts, mfps, collect1),
      collectable((7, 4), "bookDat/paper.png", ts, mfps, collect2),
      collectable((8, 13), "bookDat/paper.png", ts, mfps, collect3),
      collectable((15, 1), "bookDat/paper.png", ts, mfps, collect4),
      collectable((14, 8), "bookDat/paper.png", ts, mfps, collect5)]

mainGame()

pg.quit()

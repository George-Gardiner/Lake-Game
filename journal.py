from chars import sprite
from pygame import font as f

f.init()
font = f.Font('freesansbold.ttf', 32)
var = 0


class journal(sprite):
    def __init__(self, sd):
        self.pages = []
        self.currentPage = 0  # which pair, not which individual
        self.sd = sd
        super().__init__((0, 0), "bookDat/page.png", sd)

    def addPage(self, text):
        self.pages.append(page(text, self.sd))
        self.pages.append(page("buffer", self.sd))

    def draw(self, bg):
        super().draw(bg)
        self.pages[self.currentPage].draw(bg)

    def fp(self, pos):  # flipPage
        global var
        var += 1
        print(var)
        if pos:  # positive
            print(pos, "::", var)
            self.currentPage += 1
            if self.currentPage > len(self.pages) - 1:
                print("UpperLimitTriggered")
                self.currentPage = len(self.pages) - 2
        else:
            self.currentPage -= 1
            if self.currentPage < 0:
                print("LowerLimitTriggered")
                self.currentPage = 0
        print(self.currentPage, ":: Page")
        print(len(self.pages), ":: LEN")


class page():
    def __init__(self, text, sd):
        self.text = font.render(text, True, (0, 0, 0))
        self.textRect = self.text.get_rect()
        self.textRect.center = sd[0] / 2, sd[1] / 2

    def draw(self, sd):
        sd.blit(self.text, self.textRect)

from chars import sprite
from pygame import font as f

f.init()
font = f.Font('freesansbold.ttf', 32)


class journal(sprite):
    def __init__(self, sd):
        self.pages = []
        self.currentPage = 0  # which pair, not which individual
        self.sd = sd
        super().__init__((0, 0), "bookDat/page.png", sd)

    def addPage(self, text):
        self.pages.append(page(text, self.sd))
        self.pages.append(page("buffer", self.sd))
        self.pages.append(page("buffer", self.sd))

    def draw(self, bg):
        super().draw(bg)
        self.pages[self.currentPage].draw(bg)

    def fp(self, pos):  # flipPage
        if pos:  # positive
            self.currentPage += 1
            if self.currentPage > len(self.pages) - 1:
                self.currentPage = len(self.pages) - 3
        else:
            self.currentPage -= 1
            if self.currentPage < 0:
                self.currentPage = 0
        print(self.currentPage, "/", len(self.pages))


class page():
    def __init__(self, text, sd):
        self.text = []
        for x in text.split("\n"):
            self.text.append(font.render(x, True, (0, 0, 0)))

    def draw(self, sd):
        y = 0
        for x in range(len(self.text)):
            sd.blit(self.text[x], (0, y))
            y += 20

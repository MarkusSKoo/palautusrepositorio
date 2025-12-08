class Sovelluslogiikka:
    def __init__(self, arvo=0):
        self._arvo = arvo
        self._edellinen = [self._arvo]

    def miinus(self, operandi):
        self._edellinen.append(self._arvo)
        self._arvo = self._arvo - operandi

    def plus(self, operandi):
        self._edellinen.append(self._arvo)
        self._arvo = self._arvo + operandi

    def nollaa(self):
        self._edellinen.append(self._arvo)
        self._arvo = 0

    def aseta_arvo(self, arvo):
        self._edellinen.append(self._arvo)
        self._arvo = arvo

    def arvo(self):
        return self._arvo

    def kumoa(self):
        if len(self._edellinen) > 0:
            self._arvo = self._edellinen[-1]
            self._edellinen.pop()

from tkinter import constants

class Summa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._logiikka = sovelluslogiikka
        self._lue = lue_syote

    def suorita(self):
        try:
            arvo = int(self._lue())
        except:
            arvo = 0
        self._logiikka.plus(arvo)


class Erotus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._logiikka = sovelluslogiikka
        self._lue = lue_syote

    def suorita(self):
        try:
            arvo = int(self._lue())
        except:
            arvo = 0
        self._logiikka.miinus(arvo)


class Nollaus:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._logiikka = sovelluslogiikka

    def suorita(self):
        self._logiikka.nollaa()

class Kumoa:
    def __init__(self, sovelluslogiikka, lue_syote):
        self._logiikka = sovelluslogiikka

    def suorita(self):
        self._logiikka.kumoa()

from tuomari import Tuomari
from tekoaly_parannettu import TekoalyParannettu
from kivi_paperi_sakset import KiviPaperiSakset


class KPSParempiTekoaly(KiviPaperiSakset):
    def __init__(self):
        super().__init__()
        self.parempi_ai = TekoalyParannettu(10)

    def _toisen_siirto(self, ensimmaisen_siirto):
        self.parempi_ai.aseta_siirto(ensimmaisen_siirto)
        return self.parempi_ai.anna_siirto()

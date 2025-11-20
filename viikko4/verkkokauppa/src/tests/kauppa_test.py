import unittest
from unittest.mock import Mock, ANY
from kauppa import Kauppa
from viitegeneraattori import Viitegeneraattori
from varasto import Varasto
from tuote import Tuote

class TestKauppa(unittest.TestCase):
    def setUp(self):
        self.pankki_mock = Mock()
        self.viitegeneraattori_mock = Mock()
        # palautetaan aina arvo 42
        self.viitegeneraattori_mock.uusi.return_value = 42

    def test_maksettaessa_ostos_pankin_metodia_tilisiirto_kutsutaan(self):
        varasto_mock = Mock()
        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called()
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_ostos_kaytetaan_oikeita_parametreja(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuote, jonka id on 1
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_2_eri_ostosta_kaytetaan_oikeita_parametreja(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 20

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 10)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuotteet, joiden id on 1 ja 2
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 15)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_2_samaa_ostosta_kaytetaan_oikeita_parametreja(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuotteet, joiden id on 1 ja 2
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 10)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_maksettaessa_puuttuva_ja_loytyva_tuote_kaytetaan_oikeita_parametreja(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id ==2:
                return None

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuotteet, joiden id on 1 ja 2
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

    def test_aloita_asiointi_nollaa_edellisen_ostoskorin_tiedot(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 0

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id ==2:
                return None

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuotteet, joiden id on 1 ja 2
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)
        # toistaiseksi ei välitetä kutsuun liittyvistä argumenteista

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.tilimaksu("pekka", "12345")
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

    def test_maksettaessa_uusi_ostos_pyydetaan_uusi_viite(self):
        pankki_mock = Mock()
        viitegeneraattori_mock = Mock()
        # palautetaan aina arvo 42
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, pankki_mock, viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuote, jonka id on 1
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 1)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 2)

        kauppa.aloita_asiointi()
        kauppa.lisaa_koriin(1)
        kauppa.tilimaksu("pekka", "12345")

        self.assertEqual(viitegeneraattori_mock.uusi.call_count, 3)

    def test_poista_tuote_korista(self):
        varasto_mock = Mock()

        # tehdään toteutus saldo-metodille
        def varasto_saldo(tuote_id):
            if tuote_id == 1:
                return 10
            if tuote_id == 2:
                return 10

        # tehdään toteutus hae_tuote-metodille
        def varasto_hae_tuote(tuote_id):
            if tuote_id == 1:
                return Tuote(1, "maito", 5)
            if tuote_id == 2:
                return Tuote(2, "leipä", 10)

        # otetaan toteutukset käyttöön
        varasto_mock.saldo.side_effect = varasto_saldo
        varasto_mock.hae_tuote.side_effect = varasto_hae_tuote

        # alustetaan kauppa
        kauppa = Kauppa(varasto_mock, self.pankki_mock, self.viitegeneraattori_mock)

        # tehdään ostokset
        kauppa.aloita_asiointi()
        # lisätään ostoskoriin tuotteet, joiden id on 1 ja 2
        kauppa.lisaa_koriin(1)
        kauppa.lisaa_koriin(2)
        kauppa.poista_korista(2)
        kauppa.tilimaksu("pekka", "12345")

        # varmistetaan, että metodia tilisiirto on kutsuttu
        self.pankki_mock.tilisiirto.assert_called_with("pekka", 42, "12345", "33333-44455", 5)

#creating second commit to first tag

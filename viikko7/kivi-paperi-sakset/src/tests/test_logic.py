from tuomari import Tuomari
from tekoaly import Tekoaly


def test_tuomari_counts_scores_and_ties():
    tuomari = Tuomari()

    tuomari.kirjaa_siirto("k", "s")  # player wins
    tuomari.kirjaa_siirto("p", "s")  # player loses
    tuomari.kirjaa_siirto("k", "k")  # tie

    assert tuomari.ekan_pisteet == 1
    assert tuomari.tokan_pisteet == 1
    assert tuomari.tasapelit == 1
    assert "Tasapelit: 1" in str(tuomari)


def test_tekoaly_cycles_through_moves():
    ai = Tekoaly()
    sequence = [ai.anna_siirto() for _ in range(6)]
    assert sequence == ["p", "s", "k", "p", "s", "k"]

from datetime import date, timedelta

from domain.calculadora_multa import CalculadoraMulta


LIMITE = date(2026, 11, 25)


def test_calcular_devueltoAntesDelLimite_noHayMulta():
    calculadora = CalculadoraMulta()

    multa = calculadora.calcular(LIMITE, LIMITE - timedelta(days=1), False)

    assert multa == 0


def test_calcular_devueltoUnDiaTarde_cobra2000():
    calculadora = CalculadoraMulta()

    multa = calculadora.calcular(LIMITE, LIMITE + timedelta(days=1), False)

    assert multa == 2000


def test_calcular_devueltoVeintiseisDiasTarde_aplicaMultaMaxima():
    calculadora = CalculadoraMulta()

    multa = calculadora.calcular(LIMITE, LIMITE + timedelta(days=26), False)

    assert multa == 50000

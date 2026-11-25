from datetime import date, timedelta

from domain.calculadora_multa import CalculadoraMulta


FECHA_LIMITE = date(2026, 11, 25)
UN_DIA = timedelta(days=1)
MULTA_SIN_RETRASO = 0
VALOR_DIARIO_RETRASO = 2_000
MULTA_MAXIMA = 50_000
DIVISOR_DESCUENTO_MONITOR = 2
DIAS_RETRASO_QUE_SUPERAN_EL_TOPE = MULTA_MAXIMA // VALOR_DIARIO_RETRASO + 1
MITAD_DE_LA_MULTA_MAXIMA = MULTA_MAXIMA // DIVISOR_DESCUENTO_MONITOR


def test_calcular_devueltoAntesDelLimite_noHayMulta():
    calculadora = CalculadoraMulta()
    fecha_devolucion = FECHA_LIMITE - UN_DIA

    multa_calculada = calculadora.calcular(FECHA_LIMITE, fecha_devolucion, False)

    assert multa_calculada == MULTA_SIN_RETRASO


def test_calcular_devueltoUnDiaTarde_cobra2000():
    calculadora = CalculadoraMulta()
    fecha_devolucion = FECHA_LIMITE + UN_DIA

    multa_calculada = calculadora.calcular(FECHA_LIMITE, fecha_devolucion, False)

    assert multa_calculada == VALOR_DIARIO_RETRASO


def test_calcular_devueltoVeintiseisDiasTarde_aplicaMultaMaxima():
    calculadora = CalculadoraMulta()
    fecha_devolucion = FECHA_LIMITE + timedelta(
        days=DIAS_RETRASO_QUE_SUPERAN_EL_TOPE
    )

    multa_calculada = calculadora.calcular(FECHA_LIMITE, fecha_devolucion, False)

    assert multa_calculada == MULTA_MAXIMA


def test_calcular_monitorDevuelveVeintiseisDiasTarde_pagaMitadDelTope():
    calculadora = CalculadoraMulta()
    fecha_devolucion = FECHA_LIMITE + timedelta(
        days=DIAS_RETRASO_QUE_SUPERAN_EL_TOPE
    )

    multa_calculada = calculadora.calcular(FECHA_LIMITE, fecha_devolucion, True)

    assert multa_calculada == MITAD_DE_LA_MULTA_MAXIMA

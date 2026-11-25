from unittest.mock import create_autospec

import pytest

from data.disponibilidad_http import DisponibilidadEquiposHttp
from domain.contratos import Notificador
from domain.errores import EquipoNoDisponible
from domain.solicitar_prestamo import SolicitarPrestamo


class PrestamoRepositoryEnMemoria:
    """Fake: funciona de verdad, pero guarda en una lista en vez de una BD."""

    def __init__(self):
        self.prestamos = []
        self._contador = 0

    def siguiente_id(self):
        self._contador += 1
        return self._contador

    def guardar(self, prestamo):
        self.prestamos.append(prestamo)


@pytest.fixture
def repositorio():
    return PrestamoRepositoryEnMemoria()


@pytest.fixture
def notificador():
    return create_autospec(Notificador, instance=True)


def test_solicitarPrestamo_equipoDisponibleEnApi_quedaGuardadoEnElFake(
    httpserver, repositorio, notificador
):
    # Arrange: adaptador HTTP REAL contra el servidor de prueba, fake y mock
    httpserver.expect_request("/api/v1/equipos/12").respond_with_json(
        {"id": 12, "nombre": "Portatil", "estado": "disponible"}
    )
    adaptador = DisponibilidadEquiposHttp(url_base=httpserver.url_for(""))
    caso_de_uso = SolicitarPrestamo(adaptador, repositorio, notificador)
    # Act
    prestamo = caso_de_uso.ejecutar("1023", 12)
    # Assert
    assert repositorio.prestamos == [prestamo]
    assert prestamo.equipo_id == 12
    notificador.notificar.assert_called_once_with("1023", "Solicitud 1 registrada")


def test_solicitarPrestamo_equipoPrestadoEnApi_noGuardaNada(httpserver, repositorio, notificador):
    # Arrange
    httpserver.expect_request("/api/v1/equipos/12").respond_with_json(
        {"id": 12, "nombre": "Portatil", "estado": "prestado"}
    )
    adaptador = DisponibilidadEquiposHttp(url_base=httpserver.url_for(""))
    caso_de_uso = SolicitarPrestamo(adaptador, repositorio, notificador)
    # Act
    with pytest.raises(EquipoNoDisponible):
        caso_de_uso.ejecutar("1023", 12)
    # Assert
    assert repositorio.prestamos == []
    notificador.notificar.assert_not_called()

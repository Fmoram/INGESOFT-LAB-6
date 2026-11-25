from unittest.mock import create_autospec

import pytest

from domain.contratos import DisponibilidadEquipos, Notificador, PrestamoRepository
from domain.errores import EquipoNoDisponible
from domain.prestamo import EstadoPrestamo
from domain.solicitar_prestamo import SolicitarPrestamo


@pytest.fixture
def disponibilidad():
    return create_autospec(DisponibilidadEquipos, instance=True)


@pytest.fixture
def repositorio():
    return create_autospec(PrestamoRepository, instance=True)


@pytest.fixture
def notificador():
    return create_autospec(Notificador, instance=True)


@pytest.fixture
def caso_de_uso(disponibilidad, repositorio, notificador):
    # Arrange común
    return SolicitarPrestamo(disponibilidad, repositorio, notificador)


def test_ejecutar_equipoDisponible_guardaYNotifica(
    caso_de_uso, disponibilidad, repositorio, notificador
):
    # Arrange
    disponibilidad.esta_disponible.return_value = True
    repositorio.siguiente_id.return_value = 50
    # Act
    prestamo = caso_de_uso.ejecutar("1023", 12)
    # Assert
    assert prestamo.estado == EstadoPrestamo.PENDIENTE
    repositorio.guardar.assert_called_once_with(prestamo)
    notificador.notificar.assert_called_once_with("1023", "Solicitud 50 registrada")


def test_ejecutar_equipoNoDisponible_noGuardaNiNotifica(
    caso_de_uso, disponibilidad, repositorio, notificador
):
    # Arrange
    disponibilidad.esta_disponible.return_value = False
    # Act
    with pytest.raises(EquipoNoDisponible) as error:
        caso_de_uso.ejecutar("1023", 12)
    # Assert
    assert str(error.value) == "Equipo 12 no disponible"
    repositorio.guardar.assert_not_called()
    notificador.notificar.assert_not_called()


def test_ejecutar_falloAlGuardar_noNotifica(
    caso_de_uso, disponibilidad, repositorio, notificador
):
    # Arrange
    disponibilidad.esta_disponible.return_value = True
    repositorio.siguiente_id.return_value = 50
    repositorio.guardar.side_effect = RuntimeError("BD caída")
    # Act
    with pytest.raises(RuntimeError) as error:
        caso_de_uso.ejecutar("1023", 12)
    # Assert
    assert str(error.value) == "BD caída"
    notificador.notificar.assert_not_called()

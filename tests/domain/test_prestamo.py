from datetime import date

import pytest

from domain.prestamo import EstadoPrestamo, Prestamo

HOY = date(2026, 11, 18)


@pytest.fixture
def prestamo():
    # Arrange común
    return Prestamo(id=1, estudiante_id="1023", equipo_id=12)


def test_aprobar_prestamoPendiente_quedaAprobadoConLimiteEnSieteDias(prestamo):
    # Act
    prestamo.aprobar(HOY)
    # Assert
    assert prestamo.estado == EstadoPrestamo.APROBADO
    assert prestamo.fecha_limite == date(2026, 11, 25)


def test_renovar_porSegundaVez_lanzaError(prestamo):
    # Arrange
    prestamo.aprobar(HOY)
    prestamo.renovar()
    # Act
    with pytest.raises(ValueError) as error:
        prestamo.renovar()
    # Assert
    assert str(error.value) == "El préstamo ya fue renovado"


def test_renovar_unaVezPrestamoAprobado_extiendeLimiteSieteDias(prestamo):
    # Arrange
    prestamo.aprobar(HOY)
    # Act
    prestamo.renovar()
    # Assert
    assert prestamo.fecha_limite == date(2026, 12, 2)
    assert prestamo.renovaciones == 1


def test_aprobar_prestamoYaAprobado_lanzaError(prestamo):
    # Arrange
    prestamo.aprobar(HOY)
    # Act
    with pytest.raises(ValueError) as error:
        prestamo.aprobar(HOY)
    # Assert
    assert str(error.value) == "Solo se aprueba un préstamo pendiente"


def test_renovar_prestamoPendiente_lanzaError(prestamo):
    # Act
    with pytest.raises(ValueError) as error:
        prestamo.renovar()
    # Assert
    assert str(error.value) == "Solo se renueva un préstamo aprobado"


def test_devolver_prestamoAprobado_quedaDevuelto(prestamo):
    # Arrange
    prestamo.aprobar(HOY)
    # Act
    prestamo.devolver()
    # Assert
    assert prestamo.estado == EstadoPrestamo.DEVUELTO


def test_devolver_prestamoYaDevuelto_lanzaError(prestamo):
    # Arrange
    prestamo.aprobar(HOY)
    prestamo.devolver()
    # Act
    with pytest.raises(ValueError) as error:
        prestamo.devolver()
    # Assert
    assert str(error.value) == "Solo se devuelve un préstamo aprobado"
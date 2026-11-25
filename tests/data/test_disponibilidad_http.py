import pytest

from data.disponibilidad_http import DisponibilidadEquiposHttp
from domain.errores import ServicioNoDisponible


@pytest.fixture
def adaptador(httpserver):
    # Arrange común: el adaptador real apunta al servidor local de pytest-httpserver
    return DisponibilidadEquiposHttp(url_base=httpserver.url_for(""))


def test_estaDisponible_equipoDisponible_devuelveVerdaderoYLlamaLaRutaCorrecta(
    adaptador, httpserver
):
    # Arrange
    httpserver.expect_request("/api/v1/equipos/12").respond_with_json(
        {"id": 12, "nombre": "Portatil", "estado": "disponible"}
    )
    # Act
    resultado = adaptador.esta_disponible(12)
    # Assert
    assert resultado is True
    peticion, _ = httpserver.log[-1]
    assert peticion.method == "GET"
    assert peticion.path == "/api/v1/equipos/12"


def test_estaDisponible_equipoPrestado_devuelveFalso(adaptador, httpserver):
    # Arrange
    httpserver.expect_request("/api/v1/equipos/12").respond_with_json(
        {"id": 12, "nombre": "Portatil", "estado": "prestado"}
    )
    # Act
    resultado = adaptador.esta_disponible(12)
    # Assert
    assert resultado is False


def test_estaDisponible_equipoNoExiste404_devuelveFalso(adaptador, httpserver):
    # Arrange
    httpserver.expect_request("/api/v1/equipos/12").respond_with_data("", status=404)
    # Act
    resultado = adaptador.esta_disponible(12)
    # Assert
    assert resultado is False


def test_estaDisponible_servidorFalla500_lanzaServicioNoDisponible(adaptador, httpserver):
    # Arrange
    httpserver.expect_request("/api/v1/equipos/12").respond_with_data("error", status=500)
    # Act
    with pytest.raises(ServicioNoDisponible) as error:
        adaptador.esta_disponible(12)
    # Assert
    assert str(error.value) == "HTTP 500"


def test_estaDisponible_sinConexion_lanzaServicioNoDisponible():
    # Arrange: puerto 1 sin servidor => error de red real
    adaptador = DisponibilidadEquiposHttp(url_base="http://localhost:1", timeout=1)
    # Act / Assert
    with pytest.raises(ServicioNoDisponible):
        adaptador.esta_disponible(12)

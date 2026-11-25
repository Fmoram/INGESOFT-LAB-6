import requests

from domain.errores import ServicioNoDisponible


class DisponibilidadEquiposHttp:
    """Cumple el contrato DisponibilidadEquipos consultando la API de equipos."""

    def __init__(self, url_base: str, timeout: float = 5.0):
        self._url_base = url_base.rstrip("/")
        self._timeout = timeout

    def esta_disponible(self, equipo_id: int) -> bool:
        url = f"{self._url_base}/api/v1/equipos/{equipo_id}"
        try:
            respuesta = requests.get(url, timeout=self._timeout)
        except requests.RequestException as error:
            raise ServicioNoDisponible(str(error)) from error

        if respuesta.status_code == 404:
            return False
        if respuesta.status_code != 200:
            raise ServicioNoDisponible(f"HTTP {respuesta.status_code}")
        return respuesta.json()["estado"] == "disponible"

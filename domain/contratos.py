from typing import Protocol

from domain.prestamo import Prestamo


class DisponibilidadEquipos(Protocol):
    def esta_disponible(self, equipo_id: int) -> bool: ...


class PrestamoRepository(Protocol):
    def siguiente_id(self) -> int: ...

    def guardar(self, prestamo: Prestamo) -> None: ...


class Notificador(Protocol):
    def notificar(self, estudiante_id: str, mensaje: str) -> None: ...

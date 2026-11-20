from datetime import timedelta
from enum import Enum


class EstadoPrestamo(Enum):
    PENDIENTE = "PENDIENTE"
    APROBADO = "APROBADO"
    DEVUELTO = "DEVUELTO"


class Prestamo:
    def __init__(self, id, estudiante_id, equipo_id):
        self.id = id
        self.estudiante_id = estudiante_id
        self.equipo_id = equipo_id
        self.estado = EstadoPrestamo.PENDIENTE
        self.fecha_limite = None
        self.renovaciones = 0

    def aprobar(self, hoy):
        if self.estado != EstadoPrestamo.PENDIENTE:
            raise ValueError("Solo se aprueba un préstamo pendiente")
        self.estado = EstadoPrestamo.APROBADO
        self.fecha_limite = hoy + timedelta(days=7)

    def renovar(self):
        if self.estado != EstadoPrestamo.APROBADO:
            raise ValueError("Solo se renueva un préstamo aprobado")
        if self.renovaciones >= 1:
            raise ValueError("El préstamo ya fue renovado")
        self.fecha_limite = self.fecha_limite + timedelta(days=7)
        self.renovaciones += 1

    def devolver(self):
        if self.estado != EstadoPrestamo.APROBADO:
            raise ValueError("Solo se devuelve un préstamo aprobado")
        self.estado = EstadoPrestamo.DEVUELTO
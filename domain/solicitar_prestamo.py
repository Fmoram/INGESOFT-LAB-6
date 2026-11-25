from domain.contratos import DisponibilidadEquipos, Notificador, PrestamoRepository
from domain.errores import EquipoNoDisponible
from domain.prestamo import Prestamo


class SolicitarPrestamo:
    def __init__(
        self,
        disponibilidad: DisponibilidadEquipos,
        repositorio: PrestamoRepository,
        notificador: Notificador,
    ):
        self._disponibilidad = disponibilidad
        self._repositorio = repositorio
        self._notificador = notificador

    def ejecutar(self, estudiante_id: str, equipo_id: int) -> Prestamo:
        if not self._disponibilidad.esta_disponible(equipo_id):
            raise EquipoNoDisponible(equipo_id)
        prestamo = Prestamo(
            id=self._repositorio.siguiente_id(),
            estudiante_id=estudiante_id,
            equipo_id=equipo_id,
        )
        self._repositorio.guardar(prestamo)
        self._notificador.notificar(estudiante_id, f"Solicitud {prestamo.id} registrada")
        return prestamo

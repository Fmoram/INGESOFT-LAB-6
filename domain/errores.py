class EquipoNoDisponible(Exception):
    def __init__(self, equipo_id):
        super().__init__(f"Equipo {equipo_id} no disponible")


class ServicioNoDisponible(Exception):
    """El servicio externo de equipos no respondió como se esperaba."""

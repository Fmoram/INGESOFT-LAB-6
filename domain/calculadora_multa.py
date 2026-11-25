MULTA_SIN_RETRASO = 0
VALOR_DIARIO_RETRASO = 2_000
MULTA_MAXIMA = 50_000
DIVISOR_DESCUENTO_MONITOR = 2


class CalculadoraMulta:
    def calcular(self, fecha_limite, fecha_devolucion, es_monitor):
        dias_retraso = (fecha_devolucion - fecha_limite).days
        multa_sin_descuento = min(
            MULTA_MAXIMA,
            max(MULTA_SIN_RETRASO, dias_retraso * VALOR_DIARIO_RETRASO),
        )
        if es_monitor:
            return multa_sin_descuento // DIVISOR_DESCUENTO_MONITOR
        return multa_sin_descuento

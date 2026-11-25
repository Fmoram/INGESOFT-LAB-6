class CalculadoraMulta:
    def calcular(self, fecha_limite, fecha_devolucion, es_monitor):
        dias_retraso = (fecha_devolucion - fecha_limite).days
        multa = min(50000, max(0, dias_retraso * 2000))
        if es_monitor:
            return multa // 2
        return multa

class CalculadoraMulta:
    def calcular(self, fecha_limite, fecha_devolucion, es_monitor):
        dias_retraso = (fecha_devolucion - fecha_limite).days
        return max(0, dias_retraso * 2000)
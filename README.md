# Prestamos-G4

Laboratorio 6: Testing. Ingeniería de Software II, 2026-II.

## Stack

| Pieza | Herramienta |
|---|---|
| Framework de pruebas | pytest |
| Dobles (mocks) | unittest.mock |
| Cliente HTTP y JSON | requests |
| Servidor HTTP de prueba | pytest-httpserver |
| Cobertura | pytest-cov |

## Cómo ejecutar

Instalar dependencias:

    pip install -r requirements.txt

Correr las pruebas:

    pytest -v

Correr con cobertura (genera reporte HTML en htmlcov/):

    pytest --cov=domain --cov=data --cov-report=term-missing --cov-report=html
# Sistema de Priorización de Solicitudes de Equipamiento

Proyecto académico en Python que aplica programación funcional, lógica y multiparadigma.

## Requisitos
- Python 3.11 o superior.
- Dependencias indicadas en `requirements.txt`.

## Ejecutar en Windows (PowerShell)
Desde la carpeta del proyecto, ejecutar:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

El programa permite seleccionar un equipo del catálogo, consultar su stock inicial automáticamente y registrar, evaluar y guardar solicitudes. **Registrar una solicitud no descuenta stock**, porque el sistema no realiza despachos. Los ejemplos están en `datos/solicitudes.json`.

## Archivos principales
- `main.py`: menú principal.
- `modulos/funcional.py`: cálculos y filtros.
- `modulos/logico.py`: hechos y reglas con miniKanren.
- `modulos/multiparadigma.py`: gestión de solicitudes.
- `datos/solicitudes.json`: solicitudes de ejemplo.

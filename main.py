"""Sistema de priorización de solicitudes de equipamiento.

Uso:
    python main.py               # menú interactivo
"""
import argparse
from pathlib import Path
from modulos.multiparadigma import GestorSolicitudes

DATOS = Path(__file__).resolve().parent / "datos" / "solicitudes.json"

# Catálogo de equipos con stock inicial de referencia.
# Registrar una solicitud NO modifica estas cantidades.
CATALOGO = {
    "Sensor de inclinación": 3,
    "Datalogger": 0,
    "Cable de comunicación": 20,
    "Conectores": 2,
}


def mostrar_solicitudes(gestor):
    print("\nSOLICITUDES REGISTRADAS")
    print("-" * 69)
    print(f"{'ID':<6} {'Equipo':<24} {'Cant.':>5} {'Stock':>5} {'Urgencia':<8}")
    for s in gestor.consultar():
        print(f"{s['id']:<6} {s['equipo'][:24]:<24} {s['cantidad']:>5} {s['stock']:>5} {s['urgencia']:<8}")


def mostrar_evaluacion(gestor):
    print("\nRESULTADOS DE EVALUACIÓN")
    print("-" * 90)
    print(f"{'ID':<6} {'Equipo':<24} {'Urg.':<7} {'Faltan':>6}  {'Atención':<24} {'Coincide':<8}")
    for s in gestor.evaluar():
        coincide = "Sí" if s["coincide_con_funcional"] else "NO"
        print(f"{s['id']:<6} {s['equipo'][:24]:<24} {s['urgencia']:<7} {s['faltante']:>6}  {s['atencion']:<24} {coincide:<8}")


def mostrar_resumen(gestor):
    r = gestor.obtener_resumen()
    print("\nRESUMEN")
    print(f"Total de solicitudes: {r['total_solicitudes']}")
    print(f"Solicitudes urgentes: {r['urgentes']} ({', '.join(r['urgentes_ids']) or 'ninguna'})")
    print(f"Unidades solicitadas: {r['total_unidades_solicitadas']}")
    print(f"Unidades faltantes: {r['total_unidades_faltantes']}")
    print(f"Urgencias: alta={r['por_urgencia']['alta']}, media={r['por_urgencia']['media']}, baja={r['por_urgencia']['baja']}")


def ingresar_entero(mensaje, minimo):
    while True:
        try:
            numero = int(input(mensaje))
            if numero >= minimo:
                return numero
        except ValueError:
            pass
        print(f"Ingrese un número entero mayor o igual a {minimo}.")


def seleccionar_equipo():
    """Muestra el catálogo y devuelve el equipo y su stock inicial."""
    equipos = list(CATALOGO.items())
    print("\nEQUIPOS DISPONIBLES")
    for numero, (nombre, stock) in enumerate(equipos, start=1):
        print(f"{numero}. {nombre} | Stock: {stock}")

    while True:
        opcion = ingresar_entero("Seleccione un equipo (número): ", 1)
        if opcion <= len(equipos):
            equipo, stock = equipos[opcion - 1]
            print(f"Equipo seleccionado: {equipo}")
            print(f"Stock disponible (referencia): {stock}")
            return equipo, stock
        print("Seleccione un número de la lista.")


def menu(gestor, archivo):
    while True:
        print("\n=== GESTIÓN DE SOLICITUDES ===")
        print("1. Registrar solicitud")
        print("2. Consultar solicitudes")
        print("3. Evaluar solicitudes (lógica + funcional)")
        print("4. Mostrar resumen")
        print("5. Guardar información")
        print("6. Salir")
        opcion = input("Seleccione una opción: ").strip()
        if opcion == "1":
            equipo, stock = seleccionar_equipo()
            cantidad = ingresar_entero("Cantidad requerida: ", 1)
            urgencia = input("Urgencia (alta/media/baja): ").strip().lower()
            try:
                s = gestor.registrar(equipo, cantidad, urgencia, stock)
                print(f"Solicitud {s['id']} registrada correctamente.")
                print("El stock inicial no cambia: solo se registró y evaluará la solicitud.")
            except ValueError as error:
                print(f"No se registró: {error}")
        elif opcion == "2":
            mostrar_solicitudes(gestor)
        elif opcion == "3":
            mostrar_evaluacion(gestor)
        elif opcion == "4":
            mostrar_resumen(gestor)
        elif opcion == "5":
            gestor.guardar(archivo)
            print(f"Información guardada en: {archivo}")
        elif opcion == "6":
            print("Fin del programa. (Recuerde guardar si realizó cambios.)")
            return
        else:
            print("Opción no válida.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--demo", action="store_true", help="Muestra resultados de ejemplo sin modificar datos")
    parser.add_argument("--datos", type=Path, default=DATOS, help="Ruta del archivo JSON")
    args = parser.parse_args()
    try:
        gestor = GestorSolicitudes.cargar(args.datos)
    except FileNotFoundError:
        gestor = GestorSolicitudes()
    except (ValueError, OSError) as error:
        parser.error(f"No se pudieron cargar los datos: {error}")
    if args.demo:
        print("SISTEMA DE PRIORIZACIÓN DE SOLICITUDES - DEMOSTRACIÓN")
        mostrar_solicitudes(gestor)
        mostrar_evaluacion(gestor)
        mostrar_resumen(gestor)
    else:
        menu(gestor, args.datos)


if __name__ == "__main__":
    main()

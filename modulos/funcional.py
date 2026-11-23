"""Paradigma funcional: transformaciones puras, filtros y ordenamientos."""
from collections import Counter

PRIORIDAD = {"alta": 0, "media": 1, "baja": 2}


def cantidad_faltante(solicitud):
    """Calcula faltante sin alterar la solicitud original."""
    return max(solicitud["cantidad"] - solicitud["stock"], 0)


def disponibilidad(solicitud):
    """Determina si se puede atender la cantidad solicitada con el stock."""
    return "suficiente" if cantidad_faltante(solicitud) == 0 else "insuficiente"


def filtrar_urgentes(solicitudes):
    """Retorna una lista NUEVA de solicitudes de urgencia alta."""
    return list(filter(lambda s: s["urgencia"] == "alta", solicitudes))


def ordenar_por_prioridad(solicitudes):
    """Devuelve una lista ordenada sin mutar el orden de origen."""
    return sorted(solicitudes, key=lambda s: (PRIORIDAD[s["urgencia"]], s["id"]))


def calcular_faltantes(solicitudes):
    """Produce una nueva lista de pares (id, faltante)."""
    return list(map(lambda s: (s["id"], cantidad_faltante(s)), solicitudes))


def clasificar_funcional(solicitud):
    """Clasificación de referencia por combinación de atributos."""
    reglas = {
        ("alta", "suficiente"): "Despacho prioritario",
        ("alta", "insuficiente"): "Compra urgente",
        ("media", "suficiente"): "Despacho regular",
        ("baja", "suficiente"): "Despacho regular",
        ("media", "insuficiente"): "Compra programada",
        ("baja", "insuficiente"): "Compra programada",
    }
    return reglas[(solicitud["urgencia"], disponibilidad(solicitud))]


def resumen(solicitudes):
    """Resumen de cantidades y urgencias, sin alterar la entrada."""
    conteos = Counter(s["urgencia"] for s in solicitudes)
    return {
        "total_solicitudes": len(solicitudes),
        "urgentes": len(filtrar_urgentes(solicitudes)),
        "total_unidades_solicitadas": sum(s["cantidad"] for s in solicitudes),
        "total_unidades_faltantes": sum(cantidad_faltante(s) for s in solicitudes),
        "por_urgencia": {u: conteos.get(u, 0) for u in ("alta", "media", "baja")},
    }

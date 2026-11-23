"""Paradigma lógico: hechos y reglas relacionales con miniKanren.

Los hechos son del tipo urgencia(solicitud, nivel) y stock(solicitud, estado).
Las reglas lógicas consisten en conjunciones/disyunciones (goals) y se
resuelven por unificación y búsqueda, NO por if/else de la clasificación.
"""
from kanren import Relation, facts, lall, lany, run, var
from .funcional import disponibilidad as obtener_disponibilidad


def _reglas(urgencia, disponibilidad):
    """Reglas declarativas; s puede ser una variable lógica libre."""

    def despacho_prioritario(s):
        return lall(urgencia(s, "alta"), disponibilidad(s, "suficiente"))

    def compra_urgente(s):
        return lall(urgencia(s, "alta"), disponibilidad(s, "insuficiente"))

    def despacho_regular(s):
        return lall(
            lany(urgencia(s, "media"), urgencia(s, "baja")),
            disponibilidad(s, "suficiente"),
        )

    def compra_programada(s):
        return lall(
            lany(urgencia(s, "media"), urgencia(s, "baja")),
            disponibilidad(s, "insuficiente"),
        )

    return {
        "Despacho prioritario": despacho_prioritario,
        "Compra urgente": compra_urgente,
        "Despacho regular": despacho_regular,
        "Compra programada": compra_programada,
    }


def consultar_por_atencion(solicitudes, tipo_atencion):
    """Consulta lógica: ¿qué ID de solicitud cumple la regla de atención?"""
    urgencia = Relation()
    disponibilidad = Relation()
    facts(urgencia, *((s["id"], s["urgencia"]) for s in solicitudes))
    facts(disponibilidad, *((s["id"], obtener_disponibilidad(s)) for s in solicitudes))

    reglas = _reglas(urgencia, disponibilidad)
    if tipo_atencion not in reglas:
        raise ValueError(f"Tipo de atención no reconocido: {tipo_atencion}")

    identificador = var()
    encontrados = run(0, identificador, reglas[tipo_atencion](identificador))
    # El orden que devuelve miniKanren no es parte de la clasificación lógica.
    return sorted(encontrados)


def clasificar_solicitudes(solicitudes):
    """Clasifica cada ID consultando las reglas lógicas sobre la base de hechos."""
    clasificacion = {}
    for tipo in (
        "Despacho prioritario",
        "Compra urgente",
        "Despacho regular",
        "Compra programada",
    ):
        for identificador in consultar_por_atencion(solicitudes, tipo):
            if identificador in clasificacion:
                raise ValueError(f"Reglas solapadas para {identificador}")
            clasificacion[identificador] = tipo

    ids = {s["id"] for s in solicitudes}
    if set(clasificacion) != ids:
        raise ValueError("Hay solicitudes sin clasificación lógica")
    return clasificacion

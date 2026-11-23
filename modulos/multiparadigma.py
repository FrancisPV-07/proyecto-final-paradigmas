"""Paradigma multiparadigma: clase gestora, operaciones imperativas y funciones."""
import json
from pathlib import Path
from .funcional import (
    cantidad_faltante, clasificar_funcional, filtrar_urgentes,
    ordenar_por_prioridad, resumen,
)
from .logico import clasificar_solicitudes

URGENCIAS = {"alta", "media", "baja"}


def validar_solicitud(s):
    """Evita cantidades inválidas, IDs repetibles y urgencias no admitidas."""
    campos = {"id", "equipo", "cantidad", "urgencia", "stock"}
    if not isinstance(s, dict) or set(s) != campos:
        raise ValueError("La solicitud debe tener id, equipo, cantidad, urgencia y stock")
    if not isinstance(s["id"], str) or not s["id"].strip():
        raise ValueError("El ID debe ser un texto no vacío")
    if not isinstance(s["equipo"], str) or not s["equipo"].strip():
        raise ValueError("El equipo debe tener un nombre")
    for campo in ("cantidad", "stock"):
        if type(s[campo]) is not int:  # bool también es int en Python; lo evitamos.
            raise ValueError(f"{campo} debe ser un número entero")
    if s["cantidad"] < 1 or s["stock"] < 0:
        raise ValueError("La cantidad debe ser positiva y el stock no negativo")
    if s["urgencia"] not in URGENCIAS:
        raise ValueError("La urgencia debe ser alta, media o baja")


class GestorSolicitudes:
    """Reúne programación orientada a objetos, imperativa y funcional."""

    def __init__(self, solicitudes=None):
        self.solicitudes = []
        for s in solicitudes or []:
            self._agregar_validada(s)

    def _agregar_validada(self, solicitud):
        validar_solicitud(solicitud)
        if any(s["id"] == solicitud["id"] for s in self.solicitudes):
            raise ValueError(f"ID duplicado: {solicitud['id']}")
        self.solicitudes.append(dict(solicitud))

    def registrar(self, equipo, cantidad, urgencia, stock):
        usados = {s["id"] for s in self.solicitudes}
        numero = 1
        while f"S{numero:03d}" in usados:
            numero += 1
        nueva = {
            "id": f"S{numero:03d}",
            "equipo": equipo.strip() if isinstance(equipo, str) else equipo,
            "cantidad": cantidad,
            "urgencia": urgencia.strip().lower() if isinstance(urgencia, str) else urgencia,
            "stock": stock,
        }
        self._agregar_validada(nueva)
        return dict(nueva)

    def consultar(self):
        return [dict(s) for s in ordenar_por_prioridad(self.solicitudes)]

    def evaluar(self):
        logicas = clasificar_solicitudes(self.solicitudes)
        evaluadas = []
        for s in self.consultar():
            atencion = logicas[s["id"]]
            referencia = clasificar_funcional(s)
            evaluadas.append({
                **s,
                "faltante": cantidad_faltante(s),
                "atencion": atencion,
                "coincide_con_funcional": atencion == referencia,
            })
        return evaluadas

    def obtener_resumen(self):
        datos = resumen(self.solicitudes)
        datos["urgentes_ids"] = [s["id"] for s in filtrar_urgentes(self.solicitudes)]
        return datos

    def guardar(self, ruta):
        ruta = Path(ruta)
        ruta.parent.mkdir(parents=True, exist_ok=True)
        ruta.write_text(json.dumps(self.solicitudes, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    @classmethod
    def cargar(cls, ruta):
        datos = json.loads(Path(ruta).read_text(encoding="utf-8"))
        if not isinstance(datos, list):
            raise ValueError("El archivo JSON debe contener una lista")
        return cls(datos)

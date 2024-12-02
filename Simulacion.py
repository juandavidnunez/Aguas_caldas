import networkx as nx
import random
import json
import logging
from collections import deque


class Simulacion:
    def __init__(self):
        self.ciudad = nx.Graph()  # Grafo que representa la ciudad
        self.barrios = {}
        self.casasp = {}  # Diccionario de casas por barrio
        self.tanques = {}  # Diccionario de tanques por barrio
        self.consumo_total = 0
        self.dias_simulados = 0
        logging.basicConfig(level=logging.INFO)

    def agregar_barrio(self, barrio):
        if barrio.id_barrio not in self.barrios:
            self.barrios[barrio.id_barrio] = barrio
            self.ciudad.add_node(barrio.id_barrio, tipo="barrio", nombre=barrio.nombre)
            logging.info(f"Barrio {barrio.nombre} agregado al grafo de la ciudad.")
        else:
            logging.warning(f"El barrio {barrio.nombre} ya existe en la ciudad.")

    def conectar_barrios(self, barrio1, barrio2, distancia):
        if barrio1.id_barrio in self.barrios and barrio2.id_barrio in self.barrios:
            self.ciudad.add_edge(barrio1.id_barrio, barrio2.id_barrio, distancia=distancia)
            logging.info(
                f"Conexión establecida entre {barrio1.nombre} y {barrio2.nombre} con una distancia de {distancia} km.")
        else:
            logging.warning("Uno o ambos barrios no existen en la ciudad.")

    def agregar_casa(self, casa, barrio):
        if barrio.id_barrio in self.barrios:
            self.casasp.setdefault(barrio.id_barrio, []).append(casa)
            self.ciudad.add_node(casa.id, tipo="casa", nombre=casa.nombre, barrio=barrio.id_barrio)
            self.ciudad.add_edge(barrio.id_barrio, casa.id, tipo="conexión casa")
            barrio.agregar_casa(casa)
            logging.info(f"Casa {casa.nombre} agregada al barrio {barrio.nombre}.")
        else:
            logging.warning(f"El barrio {barrio.nombre} no existe. No se puede agregar la casa.")

    def agregar_tanque(self, tanque, barrio):
        if barrio.id_barrio in self.barrios:
            self.tanques.setdefault(barrio.id_barrio, []).append(tanque)
            self.ciudad.add_node(tanque.id, tipo="tanque", nombre=tanque.nombre, barrio=barrio.id_barrio,
                                 capacidad=tanque.capacidad)
            self.ciudad.add_edge(barrio.id_barrio, tanque.id, tipo="conexión tanque")
            barrio.agregar_tanque(tanque)
            logging.info(f"Tanque {tanque.nombre} agregado al barrio {barrio.nombre}.")
        else:
            logging.warning(f"El barrio {barrio.nombre} no existe. No se puede agregar el tanque.")

    def simular_consumo(self, dias):
        total_consumo = 0
        self.dias_simulados += dias
        logging.info(f"Iniciando simulación de consumo de agua para {dias} días.")

        for barrio in self.barrios.values():
            for casa in barrio.casas:
                consumo = casa.simular_consumo(dias)
                total_consumo += consumo
                self.consumo_total += consumo
            for tanque in barrio.tanques:
                if tanque.estado != "activo":
                    logging.warning(f"El tanque {tanque.nombre} está inactivo, no puede abastecer.")
                else:
                    agua_disponible = tanque.nivel_agua - total_consumo
                    if agua_disponible < 0:
                        logging.warning(
                            f"El tanque {tanque.nombre} no tiene suficiente agua para satisfacer la demanda.")
                    else:
                        tanque.nivel_agua -= total_consumo
                        logging.info(f"El tanque {tanque.nombre} ha distribuido agua para {total_consumo} litros.")

        logging.info(f"Simulación completada. Total consumo en {dias} días: {total_consumo} litros.")

    def simular_fallos(self):
        logging.info("Simulando fallos en tanques y casas.")
        for barrio in self.barrios.values():
            for tanque in barrio.tanques:
                if random.random() < 0.1:  # 10% de probabilidad de fallo
                    tanque.estado = "inactivo"
                    logging.warning(f"El tanque {tanque.nombre} en el barrio {barrio.nombre} ha fallado.")
            for casa in barrio.casas:
                if random.random() < 0.05:  # 5% de probabilidad de fallo
                    casa.estado = "sin_servicio"
                    logging.warning(f"La casa {casa.nombre} en el barrio {barrio.nombre} ha fallado y no tiene agua.")

    def simular_direccion_agua(self):
        logging.info("Simulando distribución de agua en la ciudad.")
        for barrio in self.barrios.values():
            for casa in barrio.casas:
                if casa.estado == "sin_servicio":
                    logging.warning(f"La casa {casa.nombre} no está recibiendo agua debido a un fallo.")
                else:
                    # Simular que la casa recibe agua de los tanques más cercanos
                    tanques_cercanos = self.obtener_tanques_cercanos(barrio)
                    for tanque in tanques_cercanos:
                        if tanque.estado == "activo":
                            logging.info(
                                f"La casa {casa.nombre} en el barrio {barrio.nombre} recibe agua del tanque {tanque.nombre}.")
                            break

    def obtener_tanques_cercanos(self, barrio):
        # Obtener tanques cercanos dentro del grafo (esto podría mejorar usando una heurística de distancia)
        vecinos = list(self.ciudad.neighbors(barrio.id_barrio))
        tanques_cercanos = []
        for vecino in vecinos:
            if self.ciudad.nodes[vecino]["tipo"] == "tanque":
                tanque = next(t for t in barrio.tanques if t.id == vecino)
                tanques_cercanos.append(tanque)
        return tanques_cercanos

    def mostrar_red(self):
        logging.info("Mostrando la red de la ciudad:")
        for barrio in self.barrios.values():
            logging.info(
                f"Barrio {barrio.nombre} tiene casas: {[casa.nombre for casa in barrio.casas]} y tanques: {[tanque.nombre for tanque in barrio.tanques]}.")

    def simular_mantenimiento(self):
        for barrio in self.barrios.values():
            for tanque in barrio.tanques:
                if random.random() < 0.1:  # 10% probabilidad de que un tanque necesite mantenimiento
                    tanque.estado = "en_mantenimiento"
                    logging.info(f"El tanque {tanque.nombre} en el barrio {barrio.nombre} está en mantenimiento.")

    def ejecutar_simulacion(self, dias):
        self.simular_consumo(dias)
        self.simular_fallos()
        self.simular_direccion_agua()
        self.simular_mantenimiento()

    def obtener_consumo_total(self):
        return self.consumo_total

    def obtener_dias_simulados(self):
        return self.dias_simulados

    def generar_informacion_resumen(self):
        resumen = {
            "dias_simulados": self.dias_simulados,
            "consumo_total": self.consumo_total,
            "barrios": {barrio.nombre: barrio.generar_informacion_resumen() for barrio in self.barrios.values()}
        }
        return resumen

    def exportar_a_json(self):
        return json.dumps(self.generar_informacion_resumen(), indent=4)


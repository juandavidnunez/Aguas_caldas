import os
import json
import tkinter as tk
from tkinter import Canvas, Button, Frame, messagebox
import networkx as nx
from collections import defaultdict

class CityWaterSimulation:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Simulación de Sistema de Acueducto")
        self.root.geometry("1200x800")

        # Dividir la ventana principal en áreas
        self.canvas = Canvas(self.root, bg="#f0f0f0", width=900, height=800)
        self.canvas.pack(side="left", fill="both", expand=False)

        self.control_frame = Frame(self.root, bg="#404040", width=300)
        self.control_frame.pack(side="right", fill="y")

        # Colores y fuentes
        self.colors = {
            "house_with_water": "#32a852",
            "house_without_water": "#ff0000",
            "tank": "#3298a8",
            "blocked_edge": "#ff5e5e",
            "functional_edge": "#5e9cff",
        }
        self.font = ("Arial", 10)

        # Botones de control
        self.create_styled_button("Bloquear Arista", self.block_random_edge)
        self.create_styled_button("Recalcular Flujo", self.recalculate_flow)
        self.create_styled_button("Actualizar", self.update_data)
        self.create_styled_button("Mostrar Alertas", self.show_alerts)
        self.create_styled_button("Salir", self.root.quit)

        # Cargar datos iniciales
        self.houses = self.load_data("data/casas/casas.json")
        self.districts = self.load_data("data/barrios/barrios.json")
        self.tanks = self.load_data("data/tanques/tanques.json")

        # Inicializar el grafo
        self.city_graph = nx.DiGraph()
        self.alerts = []

        # Construcción del grafo y dibujo inicial
        self.build_city_graph()
        self.recalculate_flow()

    def create_styled_button(self, text, command):
        """Crea un botón estilizado en el panel de control."""
        Button(
            self.control_frame,
            text=text,
            command=command,
            bg="#505050",
            fg="white",
            font=self.font,
            activebackground="#707070",
        ).pack(pady=10, padx=20, fill="x")

    @staticmethod
    def load_data(filepath):
        """Carga datos desde un archivo JSON."""
        if not os.path.exists(filepath):
            return []
        with open(filepath, "r") as file:
            return json.load(file)

    def build_city_graph(self):
        """Construir el grafo de la ciudad a partir de datos."""
        self.city_graph.clear()

        for district in self.districts:
            district_name = district["nombre"]
            houses_in_district = [house["id"] for house in self.houses if house["barrio_id"] == district["id"]]

            for house in houses_in_district:
                self.city_graph.add_node(house, type="house", district=district_name, has_water=False)

            for i in range(len(houses_in_district) - 1):
                self.city_graph.add_edge(
                    houses_in_district[i], houses_in_district[i + 1], status="functional"
                )

            if "tanque_id" in district:
                tank_id = district["tanque_id"]
                if any(tank["id"] == tank_id for tank in self.tanks):
                    self.city_graph.add_edge(tank_id, houses_in_district[0], status="functional")

        for tank in self.tanks:
            self.city_graph.add_node(
                tank["id"], type="tank", capacity=tank["capacidad"], pressure=tank["presion"]
            )

    def draw_graph(self):
        """Dibuja el grafo en el canvas."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Separar barrios y tanques
        district_positions = {}
        tank_positions = {}

        x_offset = 100
        y_offset = 100
        x_step = 300
        y_step = 200

        current_x = x_offset
        current_y = y_offset

        # Posicionar barrios
        for district in self.districts:
            district_name = district["nombre"]
            houses_in_district = [house["id"] for house in self.houses if house["barrio_id"] == district["id"]]

            for i, house in enumerate(houses_in_district):
                district_positions[house] = (current_x, current_y + i * 50)

            current_x += x_step

        # Posicionar tanques
        current_x = width - x_step
        current_y = y_offset

        for tank in self.tanks:
            tank_positions[tank["id"]] = (current_x, current_y)
            current_y += y_step

        # Combinar posiciones
        pos = {**district_positions, **tank_positions}

        for node, data in self.city_graph.nodes(data=True):
            x, y = pos[node]
            color = (
                self.colors["house_with_water"]
                if data.get("has_water")
                else self.colors["house_without_water"]
                if data["type"] == "house"
                else self.colors["tank"]
            )
            label = data["district"] if "district" in data else "Tanque"

            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, outline="black")
            self.canvas.create_text(x, y - 15, text=f"{node}\n{label}", font=self.font)

        for u, v, edge_data in self.city_graph.edges(data=True):
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            color = (
                self.colors["functional_edge"]
                if edge_data["status"] == "functional"
                else self.colors["blocked_edge"]
            )

            self.canvas.create_line(x1, y1, x2, y2, fill=color, width=2)

    def recalculate_flow(self):
        """Recalcula el suministro de agua en el sistema."""
        # Reiniciar estado del agua
        for node in self.city_graph.nodes:
            if self.city_graph.nodes[node]["type"] == "house":
                self.city_graph.nodes[node]["has_water"] = False

        for tank in [n for n, d in self.city_graph.nodes(data=True) if d["type"] == "tank"]:
            pressure = self.city_graph.nodes[tank]["pressure"]
            queue = [tank]

            while queue and pressure > 0:
                current = queue.pop(0)

                for neighbor in self.city_graph.successors(current):
                    if self.city_graph.nodes[neighbor]["type"] == "house" and not self.city_graph.nodes[neighbor][
                        "has_water"
                    ]:
                        self.city_graph.nodes[neighbor]["has_water"] = True
                        pressure -= 1

                    if pressure > 0:
                        queue.append(neighbor)

        self.draw_graph()

    def block_random_edge(self):
        """Bloquea una arista funcional al azar."""
        functional_edges = [e for e in self.city_graph.edges(data=True) if e[2]["status"] == "functional"]

        if functional_edges:
            u, v, data = functional_edges[0]  # Selecciona la primera arista funcional
            self.city_graph.edges[u, v]["status"] = "blocked"
            self.alerts.append(f"Se bloqueó la arista {u} -> {v}.")
            self.recalculate_flow()

    def update_data(self):
        """Actualiza los datos del sistema cargando nuevos barrios o tanques."""
        self.houses = self.load_data("data/casas/casas.json")
        self.districts = self.load_data("data/barrios/barrios.json")
        self.tanks = self.load_data("data/tanques/tanques.json")

        self.build_city_graph()
        self.recalculate_flow()

    def show_alerts(self):
        """Muestra las alertas generadas."""
        if not self.alerts:
            messagebox.showinfo("Alertas", "No hay alertas en este momento.")
        else:
            messagebox.showinfo("Alertas", "\n".join(self.alerts))
            self.alerts = []

# Configuración inicial
root = tk.Tk()
simulation = CityWaterSimulation(root)
root.mainloop()

import os
import json
import tkinter as tk
from tkinter import Canvas, Button, Frame, messagebox
import networkx as nx
from collections import defaultdict

class ImprovedCityWaterSimulation:
    def __init__(self, root):
        # Configuración de la ventana principal
        self.root = root
        self.root.title("Simulación Mejorada de Sistema de Acueducto")
        self.root.geometry("1200x800")

        # Marcos principales para diseño
        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.main_frame, bg="#f0f0f0")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.control_frame = Frame(self.main_frame, bg="#404040")
        self.control_frame.pack(side="right", fill="y")

        # Colores y fuentes
        self.colors = {
            "house": "#32a852",
            "tank": "#3298a8",
            "blocked_edge": "#ff5e5e",
            "functional_edge": "#5e9cff",
        }
        self.font = ("Arial", 10)  # Definir la fuente antes de usarla

        # Botones de control estilizados
        self.create_styled_button("Bloquear Arista", self.block_random_edge)
        self.create_styled_button("Recalcular Flujo", self.recalculate_flow)
        self.create_styled_button("Mostrar Alertas", self.show_alerts)
        self.create_styled_button("Salir", self.root.quit)

        # Cargar datos
        self.houses = self.load_data("data/casas/casas.json")
        self.districts = self.load_data("data/barrios/barrios.json")
        self.tanks = self.load_data("data/tanques/tanques.json")

        # Configuración inicial del grafo
        self.city_graph = nx.Graph()
        self.house_nodes = set()
        self.tank_nodes = set()
        self.blocked_edges = set()
        self.alerts = []

        # Construir el grafo de la ciudad
        self.build_city_graph()
        self.draw_graph()

        # Redibujar el grafo al redimensionar la ventana
        self.root.bind("<Configure>", lambda event: self.draw_graph())

    def create_styled_button(self, text, command):
        """Crea un botón estilizado."""
        Button(
            self.control_frame,
            text=text,
            command=command,
            bg="#505050",
            fg="white",
            font=self.font,
            activebackground="#707070"
        ).pack(pady=10, padx=20, fill="x")

    @staticmethod
    def load_data(filepath):
        """Carga datos desde un archivo JSON."""
        if not os.path.exists(filepath):
            return []
        with open(filepath, 'r') as file:
            return json.load(file)

    def build_city_graph(self):
        """Construir el grafo de la ciudad con casas, tanques y barrios."""
        for house in self.houses:
            house_id = house["id"]
            district_id = house["barrio_id"]
            self.city_graph.add_node(house_id, type="house", district=district_id)
            self.house_nodes.add(house_id)

        for tank in self.tanks:
            tank_id = tank["id"]
            self.city_graph.add_node(tank_id, type="tank", capacity=int(tank["capacidad"]),
                                     pressure=int(tank["presion"]))
            self.tank_nodes.add(tank_id)

        for district in self.districts:
            district_id = district["id"]
            houses_in_district = [h["id"] for h in self.houses if h["barrio_id"] == district_id]
            self.city_graph.add_nodes_from(houses_in_district, type='house', district=district_id)

            # Conectar casas como árbol balanceado
            self.build_balanced_tree(houses_in_district)

            # Conectar tanque al nodo más cercano del barrio
            if "tanque_id" in district and district["tanque_id"] in self.tank_nodes:
                tank_id = district["tanque_id"]
                nearest_house = self.get_nearest_house(houses_in_district, tank_id)
                if nearest_house:
                    self.city_graph.add_edge(nearest_house, tank_id, status="functional")

    def build_balanced_tree(self, houses):
        """Construye un árbol balanceado a partir de una lista de casas."""
        if not houses:
            return

        for i in range(1, len(houses)):
            parent = houses[(i - 1) // 2]
            child = houses[i]
            self.city_graph.add_edge(parent, child, status="functional")

    def get_nearest_house(self, houses, tank_id):
        """Encuentra la casa más cercana a un tanque."""
        return min(houses, key=lambda h: abs(h - tank_id)) if houses else None

    def draw_graph(self):
        """Dibuja el grafo en el canvas."""
        self.canvas.delete("all")
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        pos = nx.spring_layout(self.city_graph, center=(width / 2, height / 2), scale=min(width, height) / 2.5)

        for node, data in self.city_graph.nodes(data=True):
            x, y = pos[node]
            color = self.colors["tank"] if data["type"] == "tank" else self.colors["house"]
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, tags=f"node_{node}")
            self.canvas.create_text(x, y - 15, text=str(node), font=self.font, tags=f"label_{node}")

        for u, v, edge_data in self.city_graph.edges(data=True):
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            color = self.colors["functional_edge"] if edge_data["status"] == "functional" else self.colors["blocked_edge"]
            self.canvas.create_line(x1, y1, x2, y2, fill=color, tags=f"edge_{u}-{v}")

    def block_random_edge(self):
        """Bloquea una arista funcional al azar."""
        edges = [e for e in self.city_graph.edges if self.city_graph.edges[e]["status"] == "functional"]
        if edges:
            edge_to_block = edges[0]
            self.city_graph.edges[edge_to_block]["status"] = "blocked"
            self.blocked_edges.add(edge_to_block)
            self.alerts.append(f"Se bloqueó la arista {edge_to_block}.")
            self.draw_graph()

    def recalculate_flow(self):
        """Recalcula el suministro de agua y actualiza los colores."""
        disconnected = []
        for house in self.house_nodes:
            if not self.check_water_supply(house):
                disconnected.append(house)
        if disconnected:
            self.alerts.append(f"Casas desconectadas: {', '.join(map(str, disconnected))}.")
        self.draw_graph()

    def check_water_supply(self, house_id):
        """Verifica si una casa tiene suministro de agua."""
        for tank in self.tank_nodes:
            try:
                path = nx.shortest_path(self.city_graph, source=tank, target=house_id)
                if all(self.city_graph.edges[edge]["status"] == "functional" for edge in zip(path, path[1:])):
                    return True
            except nx.NetworkXNoPath:
                continue
        return False

    def show_alerts(self):
        """Muestra las alertas acumuladas."""
        if not self.alerts:
            messagebox.showinfo("Alertas", "No hay alertas en este momento.")
        else:
            messagebox.showinfo("Alertas", "\n".join(self.alerts))
            self.alerts = []

# Configuración inicial
root = tk.Tk()
simulation = ImprovedCityWaterSimulation(root)
root.mainloop()

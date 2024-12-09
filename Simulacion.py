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

        # Marcos para diseño
        self.main_frame = Frame(root)
        self.main_frame.pack(fill="both", expand=True)

        self.canvas = Canvas(self.main_frame, bg="white")
        self.canvas.pack(side="left", expand=True, fill="both")

        self.button_frame = Frame(self.main_frame)
        self.button_frame.pack(side="right", fill="y")

        # Botones de control
        Button(self.button_frame, text="Bloquear Arista", command=self.block_random_edge).pack(pady=5)
        Button(self.button_frame, text="Recalcular Suministro", command=self.recalculate_flow).pack(pady=5)
        Button(self.button_frame, text="Salir", command=self.root.quit).pack(pady=5)

        # Cargar datos
        self.houses = self.load_data("data/casas/casas.json")
        self.districts = self.load_data("data/barrios/barrios.json")
        self.tanks = self.load_data("data/tanques/tanques.json")

        # Configuración inicial del grafo
        self.city_graph = nx.Graph()
        self.house_nodes = set()
        self.tank_nodes = set()
        self.blocked_edges = set()
        self.capacity_usage = defaultdict(int)

        # Crear grafo de la ciudad
        self.build_city_graph()
        self.draw_graph()

        # Evento para redimensionar
        self.root.bind("<Configure>", lambda event: self.draw_graph())

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

        mid = len(houses) // 2
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

        # Calcular posiciones del grafo
        pos = nx.spring_layout(self.city_graph, center=(width / 2, height / 2), scale=min(width, height) / 2.5)

        for node, data in self.city_graph.nodes(data=True):
            x, y = pos[node]
            color = "blue" if data["type"] == "tank" else "green"
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill=color, tags=f"node_{node}")
            self.canvas.create_text(x, y - 15, text=str(node), font=("Arial", 8), tags=f"label_{node}")

        for u, v, edge_data in self.city_graph.edges(data=True):
            x1, y1 = pos[u]
            x2, y2 = pos[v]
            color = "blue" if edge_data["status"] == "functional" else "red"
            self.canvas.create_line(x1, y1, x2, y2, fill=color, tags=f"edge_{u}-{v}")

    def block_random_edge(self):
        """Bloquea una arista funcional al azar."""
        edges = [e for e in self.city_graph.edges if self.city_graph.edges[e]["status"] == "functional"]
        if edges:
            edge_to_block = edges[0]
            self.city_graph.edges[edge_to_block]["status"] = "blocked"
            self.blocked_edges.add(edge_to_block)
            self.draw_graph()

    def recalculate_flow(self):
        """Recalcula el suministro de agua y actualiza los colores."""
        for house in self.house_nodes:
            if not self.check_water_supply(house):
                self.canvas.itemconfig(f"node_{house}", fill="red")
            else:
                self.canvas.itemconfig(f"node_{house}", fill="green")

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


# Configuración inicial
root = tk.Tk()
simulation = CityWaterSimulation(root)
root.mainloop()

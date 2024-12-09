import json
import logging
import os
import tkinter as tk
from tkinter import messagebox, ttk
import matplotlib.pyplot as plt

import networkx as nx
import ttkbootstrap as tb

from Simulacion import Simulation
from barrios import Barrio
from casas import Casa
from tanques import Tanque


class BotinApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Aguas-Caldas")
        self.geometry("1000x600")

        self.nombre_barrio_var = tk.StringVar()
        self.numero_casas_var = tk.StringVar()
        self.capacidad_tanque_var = tk.StringVar()
        self.tipo_tanque_var = tk.StringVar()

        # Aquí se pueden inicializar más variables necesarias para la clase
        self.option_display = tk.Frame()  # Placeholder, debe ser el contenedor en el que se dibujan los componentes
        self.barrios = []
        self.tanques = []
        self.casas = []

        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="white")
        menu_bar = tk.Frame(self, bg="#004080", height=60, relief='raised', bd=2)
        menu_bar.pack(side="top", fill="x")
        title_label = tk.Label(menu_bar, text="Aguas-Caldas", font=("Helvetica", 20, "bold"),
                               bg="#004080", fg="white")
        title_label.pack(side="left", padx=10, pady=5)

        options = ["CREATE", "UPDATE", "SIMULATE"]
        self.buttons = []
        for option in options:
            button = tb.Button(menu_bar, text=option, bootstyle="primary-outline", width=15,
                               command=lambda opt=option: self.show_option(opt))
            button.pack(side="left", padx=5, pady=10)
            self.buttons.append(button)

        self.option_display = tk.LabelFrame(self, text="Welcome", font=("Helvetica", 20), fg="black", bg="white",
                                            relief="groove", bd=3)
        self.option_display.pack(pady=20, padx=10, fill="both", expand=True)

    def show_option(self, option):
        self.option_display.config(text=option)
        for widget in self.option_display.winfo_children():
            widget.destroy()

        if option == "SIMULATE":
            self.show_simulation()
        elif option == "CREATE":
            self.show_create()
        elif option == "UPDATE":
            self.show_update()

    def show_create(self):
        self.option_display.config(text="Crear Barrio, Tanque y Casas")
        for widget in self.option_display.winfo_children():
            widget.destroy()

        create_frame = tk.Frame(self.option_display, bg="white")
        create_frame.pack(pady=10, fill="both", expand=True)

        # Dividir la interfaz en dos partes: una para crear barrios y otra para tanques
        barrio_frame = tk.LabelFrame(create_frame, text="Crear Barrio", font=("Helvetica", 14), fg="black", bg="white",
                                     relief="groove", bd=2)
        barrio_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

        tanque_frame = tk.LabelFrame(create_frame, text="Crear Tanque", font=("Helvetica", 14), fg="black", bg="white",
                                     relief="groove", bd=2)
        tanque_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

        # ------------------------------------------- SECCIÓN DE CREAR BARRIO -------------------------------------------

        # Nombre Barrio
        tk.Label(barrio_frame, text="Nombre Barrio:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.nombre_barrio_var = tk.StringVar()
        tk.Entry(barrio_frame, textvariable=self.nombre_barrio_var, font=("Helvetica", 12)).grid(row=0, column=1,
                                                                                                 padx=5, pady=5)

        # Número de casas
        tk.Label(barrio_frame, text="Número de casas:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.numero_casas_var = tk.StringVar()
        tk.Entry(barrio_frame, textvariable=self.numero_casas_var, font=("Helvetica", 12)).grid(row=1, column=1, padx=5,
                                                                                                pady=5)

        # Botón para crear barrio
        create_barrio_button = tk.Button(barrio_frame, text="Crear Barrio", font=("Helvetica", 12),
                                         command=self.crear_barrio)
        create_barrio_button.grid(row=2, column=0, columnspan=2, pady=10)

        # ------------------------------------------- SECCIÓN DE CREAR TANQUE -------------------------------------------

        # Capacidad Tanque
        tk.Label(tanque_frame, text="Capacidad Tanque (litros):", font=("Helvetica", 12)).grid(row=0, column=0, padx=5,
                                                                                               pady=5)
        self.capacidad_tanque_var = tk.StringVar()
        tk.Entry(tanque_frame, textvariable=self.capacidad_tanque_var, font=("Helvetica", 12)).grid(row=0, column=1,
                                                                                                    padx=5, pady=5)

        # Tipo Tanque
        tk.Label(tanque_frame, text="Tipo de Tanque:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5, pady=5)
        self.tipo_tanque_var = tk.StringVar()
        tk.Entry(tanque_frame, textvariable=self.tipo_tanque_var, font=("Helvetica", 12)).grid(row=1, column=1, padx=5,
                                                                                               pady=5)

        # Botón para crear tanque
        create_tanque_button = tk.Button(tanque_frame, text="Crear Tanque", font=("Helvetica", 12),
                                         command=self.crear_tanque)
        create_tanque_button.grid(row=2, column=0, columnspan=2, pady=10)

    def crear_barrio(self):
        nombre_barrio = self.nombre_barrio_var.get().strip()
        numero_casas = self.numero_casas_var.get().strip()

        if not nombre_barrio or not numero_casas.isdigit():
            messagebox.showerror("Error", "Por favor, complete correctamente los campos del barrio.")
            return

        barrio_id = self.generar_id("barrios")

        nuevo_barrio = Barrio(barrio_id, nombre_barrio, "")
        Barrio.guardar_barrio(nuevo_barrio)
        Casa.crear_casas(int(numero_casas), barrio_id)

        messagebox.showinfo("Éxito", f"Barrio '{nombre_barrio}' creado con éxito junto con {numero_casas} casas.")

    def crear_tanque(self):
        capacidad_tanque = self.capacidad_tanque_var.get().strip()
        tipo_tanque = self.tipo_tanque_var.get().strip()

        if not capacidad_tanque.isdigit() or not tipo_tanque:
            messagebox.showerror("Error", "Por favor, complete correctamente los campos del tanque.")
            return

        tanque_id = self.generar_id("tanques")

        nuevo_tanque = Tanque(tanque_id, capacidad_tanque, 0)  # Asignamos presión como 0 por defecto
        Tanque.guardar_tanque(nuevo_tanque)

        messagebox.showinfo("Éxito", f"Tanque '{tipo_tanque}' creado con éxito.")

    def generar_id(self, tipo):
        """
        Genera un ID único para cada entidad (casas, tanques),
        garantizando que no se solapen.
        """
        directory = "data"
        if not os.path.exists(directory):
            os.makedirs(directory)

        last_id = 0
        for file_name in ["casas/casas.json", "tanques/tanques.json"]:
            file_path = os.path.join(directory, file_name)
            if os.path.exists(file_path):
                with open(file_path, 'r') as file:
                    try:
                        data = json.load(file)
                        if data:
                            ids = [item["id"] for item in data]
                            last_id = max(last_id, max(ids))
                    except json.JSONDecodeError:
                        continue

        return last_id + 1

    def guardar_datos_json(self, directory, id, data):
        """
        Guarda los datos en un archivo JSON dentro del directorio especificado.
        """
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, f"{directory.split('/')[-1]}_{id}.json")
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    def show_update(self):
        self.option_display.config(text="Actualizar / Eliminar Barrio, Tanque y Casas")
        for widget in self.option_display.winfo_children():
            widget.destroy()

        update_frame = tk.Frame(self.option_display, bg="white")
        update_frame.pack(pady=10, fill="both", expand=True)

        barrio_frame = tk.LabelFrame(update_frame, text="Actualizar Barrio", font=("Helvetica", 14), fg="black",
                                     bg="white",
                                     relief="groove", bd=2)
        barrio_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

        # ID del Barrio
        tk.Label(barrio_frame, text="ID Barrio:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.id_barrio_var_upd = tk.StringVar()
        tk.Entry(barrio_frame, textvariable=self.id_barrio_var_upd, font=("Helvetica", 12)).grid(row=0, column=1,
                                                                                                 padx=5, pady=5)

        # Obtener casas del barrio
        tk.Button(barrio_frame, text="Obtener Casas", font=("Helvetica", 12), command=self.obtener_casas_barrio).grid(
            row=1, column=0, columnspan=2, pady=10)

        # Nuevo nombre del barrio
        tk.Label(barrio_frame, text="Nuevo Nombre Barrio:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5,
                                                                                         pady=5)
        self.nombre_barrio_var_upd = tk.StringVar()
        tk.Entry(barrio_frame, textvariable=self.nombre_barrio_var_upd, font=("Helvetica", 12)).grid(row=2, column=1,
                                                                                                     padx=5, pady=5)

        # Nueva ubicación del barrio
        tk.Label(barrio_frame, text="Nueva Ubicación Barrio:", font=("Helvetica", 12)).grid(row=3, column=0, padx=5,
                                                                                            pady=5)
        self.ubicacion_barrio_var_upd = tk.StringVar()
        tk.Entry(barrio_frame, textvariable=self.ubicacion_barrio_var_upd, font=("Helvetica", 12)).grid(row=3, column=1,
                                                                                                        padx=5, pady=5)

        # Casas del barrio - desplegable
        tk.Label(barrio_frame, text="Casas del Barrio:", font=("Helvetica", 12)).grid(row=4, column=0, padx=5, pady=5)
        self.casas_barrio_var_upd = tk.StringVar()
        self.casas_dropdown = ttk.Combobox(barrio_frame, textvariable=self.casas_barrio_var_upd, font=("Helvetica", 12))
        self.casas_dropdown.grid(row=4, column=1, padx=5, pady=5)

        # Botón para añadir casas
        tk.Button(barrio_frame, text="Añadir Casa", font=("Helvetica", 12), command=self.anadir_casa).grid(row=5,
                                                                                                           column=0,
                                                                                                           columnspan=2,
                                                                                                           pady=10)

        # Botones actualizar y eliminar barrio
        tk.Button(barrio_frame, text="Actualizar Barrio", font=("Helvetica", 12), command=self.actualizar_barrio).grid(
            row=6, column=0, pady=10)
        tk.Button(barrio_frame, text="Eliminar Casa", font=("Helvetica", 12), command=self.eliminar_casa).grid(row=6,
                                                                                                               column=1,
                                                                                                               pady=10)
        tk.Button(barrio_frame, text="Eliminar Barrio", font=("Helvetica", 12), command=self.eliminar_barrio).grid(
            row=7, column=0, columnspan=2, pady=10)

        tanque_frame = tk.LabelFrame(update_frame, text="Actualizar Tanque", font=("Helvetica", 14), fg="black",
                                     bg="white",
                                     relief="groove", bd=2)
        tanque_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew", ipadx=10, ipady=10)

        # ID del Tanque
        tk.Label(tanque_frame, text="ID Tanque:", font=("Helvetica", 12)).grid(row=0, column=0, padx=5, pady=5)
        self.id_tanque_var_upd = tk.StringVar()
        tk.Entry(tanque_frame, textvariable=self.id_tanque_var_upd, font=("Helvetica", 12)).grid(row=0, column=1,
                                                                                                 padx=5, pady=5)

        # Nueva capacidad del tanque
        tk.Label(tanque_frame, text="Nueva Capacidad Tanque:", font=("Helvetica", 12)).grid(row=1, column=0, padx=5,
                                                                                            pady=5)
        self.capacidad_tanque_var_upd = tk.StringVar()
        tk.Entry(tanque_frame, textvariable=self.capacidad_tanque_var_upd, font=("Helvetica", 12)).grid(row=1, column=1,
                                                                                                        padx=5, pady=5)

        # Nuevo tipo del tanque
        tk.Label(tanque_frame, text="Nuevo Tipo de Tanque:", font=("Helvetica", 12)).grid(row=2, column=0, padx=5,
                                                                                          pady=5)
        self.tipo_tanque_var_upd = tk.StringVar()
        tk.Entry(tanque_frame, textvariable=self.tipo_tanque_var_upd, font=("Helvetica", 12)).grid(row=2, column=1,
                                                                                                   padx=5, pady=5)

        # Botones actualizar y eliminar tanque
        tk.Button(tanque_frame, text="Actualizar Tanque", font=("Helvetica", 12), command=self.actualizar_tanque).grid(
            row=3, column=0, pady=10)
        tk.Button(tanque_frame, text="Eliminar Tanque", font=("Helvetica", 12), command=self.eliminar_tanque).grid(
            row=3, column=1, pady=10)

    def actualizar_barrio(self):
        id_barrio = self.id_barrio_var_upd.get().strip()
        nombre_barrio = self.nombre_barrio_var_upd.get().strip()
        ubicacion_barrio = self.ubicacion_barrio_var_upd.get().strip()
        tanque_id = self.tanque_id_var_upd.get().strip()

        try:
            with open("data/barrios/barrios.json", "r") as file:
                barrios = json.load(file)

            barrio_encontrado = False
            for barrio in barrios:
                if barrio["id"] == int(id_barrio):
                    barrio_encontrado = True
                    if nombre_barrio:
                        barrio["nombre"] = nombre_barrio
                    if ubicacion_barrio:
                        barrio["ubicacion"] = ubicacion_barrio
                    if tanque_id.isdigit():
                        barrio["tanque_id"] = int(tanque_id)
                    with open("data/barrios/barrios.json", "w") as file:
                        json.dump(barrios, file, indent=4)
                    messagebox.showinfo("Éxito", f"Barrio con ID {id_barrio} actualizado.")
                    break

            if not barrio_encontrado:
                messagebox.showerror("Error", f"Barrio con ID {id_barrio} no encontrado.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de barrios no encontrado.")

    def eliminar_barrio(self):
        id_barrio = self.id_barrio_var_upd.get().strip()

        try:
            with open("data/barrios/barrios.json", "r") as file:
                barrios = json.load(file)

            barrios = [barrio for barrio in barrios if barrio["id"] != int(id_barrio)]

            with open("data/barrios/barrios.json", "w") as file:
                json.dump(barrios, file, indent=4)

            # Eliminar casas asociadas
            with open("data/casas/casas.json", "r") as file:
                casas = json.load(file)

            casas = [casa for casa in casas if casa["barrio_id"] != int(id_barrio)]

            with open("data/casas/casas.json", "w") as file:
                json.dump(casas, file, indent=4)

            messagebox.showinfo("Éxito", f"Barrio con ID {id_barrio} y sus casas asociadas han sido eliminados.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de barrios o casas no encontrado.")

    def actualizar_tanque(self):
        id_tanque = self.id_tanque_var_upd.get().strip()
        capacidad_tanque = self.capacidad_tanque_var_upd.get().strip()
        tipo_tanque = self.tipo_tanque_var_upd.get().strip()

        try:
            with open("data/tanques/tanques.json", "r") as file:
                tanques = json.load(file)

            tanque_encontrado = False
            for tanque in tanques:
                if tanque["id"] == int(id_tanque):
                    tanque_encontrado = True
                    if capacidad_tanque:
                        tanque["capacidad"] = int(capacidad_tanque)
                    if tipo_tanque:
                        tanque["tipo"] = tipo_tanque

                    # Abrir el archivo en modo escritura para actualizar los cambios
                    with open("data/tanques/tanques.json", "w") as file:
                        json.dump(tanques, file, indent=4)

                    messagebox.showinfo("Éxito", f"Tanque con ID {id_tanque} actualizado.")
                    break

            if not tanque_encontrado:
                messagebox.showerror("Error", f"Tanque con ID {id_tanque} no encontrado.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de tanques no encontrado.")

    def eliminar_tanque(self):
        id_tanque = self.id_tanque_var_upd.get().strip()

        try:
            with open("data/tanques/tanques.json", "r") as file:
                tanques = json.load(file)

            tanques = [tanque for tanque in tanques if tanque["id"] != int(id_tanque)]

            with open("data/tanques/tanques.json", "w") as file:
                json.dump(tanques, file, indent=4)
            messagebox.showinfo("Éxito", f"Tanque con ID {id_tanque} eliminado.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de tanques no encontrado.")

    def eliminar_casa(self):
        id_barrio = self.id_barrio_var_upd.get().strip()
        casa_id = self.casas_barrio_var_upd.get().strip()

        try:
            with open("data/casas/casas.json", "r") as file:
                casas = json.load(file)

            casas = [casa for casa in casas if casa["id"] != int(casa_id) or casa["barrio_id"] != int(id_barrio)]

            with open("data/casas/casas.json", "w") as file:
                json.dump(casas, file, indent=4)
            messagebox.showinfo("Éxito", f"Casa con ID {casa_id} eliminada del barrio {id_barrio}.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de casas no encontrado.")

    def obtener_casas_barrio(self):
        id_barrio = self.id_barrio_var_upd.get().strip()

        try:
            with open("data/casas/casas.json", "r") as file:
                casas = json.load(file)

            casas_del_barrio = [casa for casa in casas if casa["barrio_id"] == int(id_barrio)]
            casas_ids = [casa["id"] for casa in casas_del_barrio]

            if casas_ids:
                self.casas_dropdown['values'] = casas_ids
                messagebox.showinfo("Éxito", f"Casas del barrio {id_barrio} obtenidas.")
            else:
                messagebox.showinfo("Sin Casas", f"No se encontraron casas para el barrio con ID {id_barrio}.")
        except FileNotFoundError:
            messagebox.showerror("Error", f"Archivo de casas no encontrado.")

    def anadir_casa(self):
        id_barrio = self.id_barrio_var_upd.get().strip()

        if not id_barrio.isdigit():
            messagebox.showerror("Error", "Por favor, ingrese un ID de barrio válido.")
            return

        try:
            with open("data/casas/casas.json", "r") as file:
                casas = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            casas = []

        try:
            with open("data/tanques/tanques.json", "r") as file:
                tanques = json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            tanques = []

        # Obtener el último ID y asegurarse de que el nuevo ID no esté en uso
        last_id_casas = max([casa["id"] for casa in casas], default=0)
        last_id_tanques = max([tanque["id"] for tanque in tanques], default=0)
        new_id = max(last_id_casas, last_id_tanques) + 1

        ids_en_uso = {casa["id"] for casa in casas}.union({tanque["id"] for tanque in tanques})
        if new_id in ids_en_uso:
            messagebox.showerror("Error", f"ID {new_id} ya está en uso, por favor intente nuevamente.")
            return

        new_casa = {"id": new_id, "nombre": new_id, "barrio_id": int(id_barrio)}
        casas.append(new_casa)

        with open("data/casas/casas.json", "w") as file:
            json.dump(casas, file, indent=4)

        messagebox.showinfo("Éxito", f"Casa con ID {new_id} añadida al barrio {id_barrio}.")



    def show_simulation(self):
       pass

if __name__ == "__main__":
    app = BotinApp()
    app.mainloop()

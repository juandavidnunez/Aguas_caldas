import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
import random
import subprocess

class BotinApp(tb.Window):
    def __init__(self):
        super().__init__(themename="superhero")
        self.title("Aguas-Caldas")
        self.geometry("800x500")

        if not os.path.exists("data"):
            os.makedirs("data")
        self.data = self.load_data()
        self.next_id = self.get_next_id()

        self.current_option = tk.StringVar()
        self.current_option.set("welcome")

        self.equipos = {}

        # Intento de cargar la imagen de fondo con manejo de excepciones
        try:
            self.background_image = tk.PhotoImage(file="imag/conF.png")
        except tk.TclError:
            self.background_image = None  # Si no existe la imagen, no la cargamos

        # Intento de cargar el icono de la ventana usando PIL
        try:
            # Cargar la imagen usando PIL para admitir formatos como .jpg o .bmp
            logo_image_pil = Image.open("imag/conF.png")  # Cambia la ruta si es necesario
            logo_image_pil = logo_image_pil.resize((32, 32), Image.ANTIALIAS)  # Ajusta el tamaño del icono
            self.logo_image = ImageTk.PhotoImage(logo_image_pil)  # Convertir a un formato que tkinter pueda usar
            self.iconphoto(True, self.logo_image)  # Establecer como icono de ventana
        except Exception as e:
            print(f"Error al cargar el icono: {e}")

        self.create_widgets()

    def create_widgets(self):
        self.configure(bg="white")
        menu_bar = tk.Frame(self, bg="#004080", height=60, relief='raised', bd=2)
        menu_bar.pack(side="top", fill="x")

        title_label = tk.Label(menu_bar, text="Aguas-Caldas", font=("Helvetica", 20, "bold"), bg="#004080", fg="white")
        title_label.pack(side="left", padx=10, pady=5)

        options = ["SEARCH", "TREE", "INVENTORY"]
        self.buttons = []
        for i, option in enumerate(options):
            button = tb.Button(menu_bar, text=option, bootstyle="primary-outline", width=15, command=lambda opt=option: self.show_option(opt))
            button.pack(side="left", padx=5, pady=10)
            self.buttons.append(button)

        self.option_display = tk.LabelFrame(self, text="Welcome", font=("Helvetica", 20), fg="black", bg="white", relief="groove", bd=3)
        self.option_display.pack(pady=20, padx=10, fill="both", expand=True)

        # Si se cargó la imagen de fondo, mostrarla
        if self.background_image:
            self.background_label = tk.Label(self.option_display, image=self.background_image, bg="white")
            self.background_label.image = self.background_image
            self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

    def show_option(self, option):
        self.current_option.set(option)
        self.option_display.config(text=option)
        for widget in self.option_display.winfo_children():
            widget.destroy()

        # Si se cargó la imagen de fondo, mostrarla
        if self.background_image:
            self.background_label = tk.Label(self.option_display, image=self.background_image, bg="white")
            self.background_label.image = self.background_image
            self.background_label.place(relx=0, rely=0, relwidth=1, relheight=1)

        if option == "SEARCH":
            self.show_SEARCH()
        elif option == "TREE":
            self.show_TREE()
        elif option == "INVENTORY":
            self.show_CREATE()


    import tkinter as tk

    def show_SEARCH(self):
        # Limpiar la pantalla actual
        for widget in self.option_display.winfo_children():
            widget.destroy()

        # Crear un frame para la barra de búsqueda
        search_frame = tk.Frame(self.option_display, bg="white")
        search_frame.pack(fill="x", padx=10, pady=10)

        # Primera fila: búsqueda por ID
        id_frame = tk.Frame(search_frame, bg="white")
        id_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(id_frame, text="Buscar por ID", bg="white", font=("Helvetica", 12)).pack(side="left", padx=5, pady=5)
        self.id_search_var = tk.StringVar()
        tk.Entry(id_frame, textvariable=self.id_search_var, font=("Helvetica", 12)).pack(side="left", padx=5, pady=5)
        tk.Button(id_frame, text="Buscar", font=("Helvetica", 12), command=self.buscar).pack(side="left", padx=5,
                                                                                             pady=5)

        # Segunda fila: búsqueda por nombre
        name_frame = tk.Frame(search_frame, bg="white")
        name_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(name_frame, text="Buscar por Nombre", bg="white", font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                pady=5)
        self.nombre_search_var = tk.StringVar()
        tk.Entry(name_frame, textvariable=self.nombre_search_var, font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                               pady=5)
        tk.Button(name_frame, text="Buscar", font=("Helvetica", 12), command=self.buscar).pack(side="left", padx=5,
                                                                                               pady=5)

        # Tercera fila: búsqueda por rango de precios (mínimo y máximo)
        price_range_frame = tk.Frame(search_frame, bg="white")
        price_range_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(price_range_frame, text="Precio Mínimo", bg="white", font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                   pady=5)
        self.precio_min_var = tk.StringVar()
        tk.Entry(price_range_frame, textvariable=self.precio_min_var, font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                   pady=5)

        tk.Label(price_range_frame, text="Precio Máximo", bg="white", font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                   pady=5)


        self.precio_max_var = tk.StringVar()
        tk.Entry(price_range_frame, textvariable=self.precio_max_var, font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                   pady=5)
        tk.Button(price_range_frame, text="Buscar", font=("Helvetica", 12), command=self.buscar).pack(side="left", padx=5,
                                                                                                   pady=5)

        # Cuarta fila: búsqueda por precio exacto
        price_exact_frame = tk.Frame(search_frame, bg="white")
        price_exact_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(price_exact_frame, text="Buscar por Precio Exacto", bg="white", font=("Helvetica", 12)).pack(
            side="left", padx=5, pady=5)
        self.precio_search_var = tk.StringVar()
        tk.Entry(price_exact_frame, textvariable=self.precio_search_var, font=("Helvetica", 12)).pack(side="left",
                                                                                                      padx=5, pady=5)
        tk.Button(price_exact_frame, text="Buscar", font=("Helvetica", 12), command=self.buscar).pack(side="left",
                                                                                                      padx=5, pady=5)

        # Quinta fila: búsqueda por género
        genre_frame = tk.Frame(search_frame, bg="white")
        genre_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(genre_frame, text="Buscar por Género", bg="white", font=("Helvetica", 12)).pack(side="left", padx=5,
                                                                                                 pady=5)
        self.genero_search_var = tk.StringVar()
        genero_options = ["", "Femenino", "Masculino", "Infantil Femenino", "Infantil Masculino"]
        ttk.Combobox(genre_frame, textvariable=self.genero_search_var, values=genero_options,
                     font=("Helvetica", 12)).pack(side="left", padx=5, pady=5)

        # Sexta fila: búsqueda por tipo de prenda
        type_frame = tk.Frame(search_frame, bg="white")
        type_frame.pack(fill="x", padx=5, pady=5)

        tk.Label(type_frame, text="Buscar por Tipo de Prenda", bg="white", font=("Helvetica", 12)).pack(side="left",
                                                                                                        padx=5, pady=5)
        self.tipo_search_var = tk.StringVar()
        tipo_options = ["", "Interior", "Buso", "Pantalón", "Saco"]
        ttk.Combobox(type_frame, textvariable=self.tipo_search_var, values=tipo_options, font=("Helvetica", 12)).pack(
            side="left", padx=5, pady=5)

        # Botón de búsqueda
        tk.Button(search_frame, text="Buscar", font=("Helvetica", 12), command=self.buscar).pack(side="left", padx=5,
                                                                                                 pady=5)

        # Frame para mostrar los resultados
        self.resultados_frame = tk.Frame(self.option_display, bg="white")
        self.resultados_frame.pack(fill="both", expand=True, padx=10, pady=10)

    def buscar(self):
        """Función para buscar un producto por ID, nombre, rango de precios, precio exacto, género o tipo de prenda."""
        id_filtro = self.id_search_var.get().strip()
        nombre_filtro = self.nombre_search_var.get().strip().lower()
        precio_min_filtro = self.precio_min_var.get().strip()
        precio_max_filtro = self.precio_max_var.get().strip()
        precio_filtro = self.precio_search_var.get().strip()
        genero_filtro = self.genero_search_var.get()
        tipo_filtro = self.tipo_search_var.get()

        # Cargar los datos del archivo JSON
        inventario = self.load_data()

        # Limpiar los resultados anteriores
        for widget in self.resultados_frame.winfo_children():
            widget.destroy()

        # Inicializar lista de resultados con todos los productos
        resultados = list(inventario.values())

        # Filtrar productos por ID (ID numérico)
        if id_filtro:
            try:
                id_filtro = int(id_filtro)  # Convertimos el filtro de ID a entero
                resultados = [prenda for prenda in resultados if prenda['id'] == id_filtro]
            except ValueError:
                tk.Label(self.resultados_frame, text="El ID debe ser un número.", bg="white",
                         font=("Helvetica", 12)).pack(pady=20)
                return

        # Filtrar productos por nombre
        if nombre_filtro:
            resultados = [prenda for prenda in resultados if nombre_filtro in prenda['nombre'].lower()]

        # Filtrar productos por rango de precios
        if precio_min_filtro or precio_max_filtro:
            try:
                precio_min_filtro = float(precio_min_filtro)
                precio_max_filtro = float(precio_max_filtro)
                resultados = [prenda for prenda in resultados if
                              precio_min_filtro <= prenda['precio'] <= precio_max_filtro]

            except ValueError:
                tk.Label(self.resultados_frame, text="Los precios deben ser números válidos.", bg="white",
                         font=("Helvetica", 12)).pack(pady=20)
                return

        # Filtrar productos por precio exacto
        if precio_filtro:
            try:
                precio_filtro = float(precio_filtro)
                resultados = [prenda for prenda in resultados if prenda['precio'] == precio_filtro]
            except ValueError:
                tk.Label(self.resultados_frame, text="El precio debe ser un número válido.", bg="white",
                         font=("Helvetica", 12)).pack(pady=20)
                return

        # Filtrar productos por género
        if genero_filtro:
            resultados = [prenda for prenda in resultados if genero_filtro in prenda['categoria']]

        # Filtrar productos por tipo de prenda
        if tipo_filtro:
            resultados = [prenda for prenda in resultados if tipo_filtro in prenda['categoria']]

        # Mostrar los resultados
        if resultados:
            for prenda in resultados:
                resultado_texto = f"ID: {prenda['id']} - {prenda['nombre']} - {prenda['categoria']}  - Precio: ${prenda['precio']}- {prenda['estado']}"
                tk.Label(self.resultados_frame, text=resultado_texto, bg="white", font=("Helvetica", 12)).pack(pady=5)
        else:
            tk.Label(self.resultados_frame, text="No se encontraron prendas con las características buscadas.",
                     bg="white", font=("Helvetica", 12)).pack(pady=20)

    def show_TREE(self):
        def run_city_script():
            subprocess.run(["python", "TREE.py"], check=True)

        button = tk.Button(self.option_display, text="Show tree Information", command=run_city_script, font=("Helvetica", 12))
        button.pack(pady=20)

    def load_data(self):
        """Carga los datos desde un archivo JSON o crea un diccionario vacío."""
        try:
            with open("data/inventario_data.json", "r") as file:
                return json.load(file)
        except FileNotFoundError:
            return {}

    def save_data(self):
        """Guarda los datos en un archivo JSON."""
        with open("data/inventario_data.json", "w") as file:
            json.dump(self.data, file, indent=4)

    def get_next_id(self):
        """Determina el próximo ID disponible para una nueva prenda."""
        if self.data:
            return max(int(key) for key in self.data.keys()) + 1
        return 1

    def show_CREATE(self):
        """Función base que crea la interfaz gráfica y ejecuta las secciones correspondientes."""
        # Limpiar los widgets anteriores
        for widget in self.option_display.winfo_children():
            widget.destroy()

        main_frame = tk.Frame(self.option_display, bg="white")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        prendas_frame = tk.LabelFrame(main_frame, text="Datos de la Prenda", font=("Helvetica", 12), bg="white")
        prendas_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        inventario_frame = tk.LabelFrame(main_frame, text="Inventario", font=("Helvetica", 12), bg="white")
        inventario_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

        main_frame.grid_columnconfigure(0, weight=1)
        main_frame.grid_columnconfigure(1, weight=1)
        main_frame.grid_rowconfigure(0, weight=1)

        self.create_prendas_section(prendas_frame)
        self.create_inventario_section(inventario_frame)

    def create_prendas_section(self, frame):
        """Sección donde se ingresan los datos de la prenda."""
        tk.Label(frame, text="Género", font=("Helvetica", 12), bg="white").grid(row=0, column=0, padx=5, pady=5, sticky='e')
        self.genero_var = tk.StringVar()
        genero_options = ["Femenino", "Masculino", "Infantil Femenino", "Infantil Masculino"]
        genero_menu = ttk.Combobox(frame, textvariable=self.genero_var, values=genero_options, font=("Helvetica", 12))
        genero_menu.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Tipo de Prenda", font=("Helvetica", 12), bg="white").grid(row=1, column=0, padx=5, pady=5, sticky='e')
        self.tipo_var = tk.StringVar()
        tipo_options = ["Interior", "Buso", "Pantalón", "Saco"]
        tipo_menu = ttk.Combobox(frame, textvariable=self.tipo_var, values=tipo_options, font=("Helvetica", 12))
        tipo_menu.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Nombre de la Prenda", font=("Helvetica", 12), bg="white").grid(row=2, column=0, padx=5, pady=5, sticky='e')
        self.nombre_var = tk.StringVar()
        nombre_entry = tk.Entry(frame, textvariable=self.nombre_var, font=("Helvetica", 12))
        nombre_entry.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(frame, text="Unidades", font=("Helvetica", 12), bg="white").grid(row=3, column=0, padx=5, pady=5, sticky='e')
        self.unidades_var = tk.IntVar()
        unidades_entry = tk.Entry(frame, textvariable=self.unidades_var, font=("Helvetica", 12))
        unidades_entry.grid(row=3, column=1, padx=5, pady=5)

        tk.Label(frame, text="Precio ($)", font=("Helvetica", 12), bg="white").grid(row=4, column=0, padx=5, pady=5, sticky='e')
        self.precio_var = tk.DoubleVar()
        precio_entry = tk.Entry(frame, textvariable=self.precio_var, font=("Helvetica", 12))
        precio_entry.grid(row=4, column=1, padx=5, pady=5)

        guardar_button = tk.Button(frame, text="Guardar Prenda", command=self.guardar_prenda, font=("Helvetica", 12))
        guardar_button.grid(row=5, columnspan=2, pady=10)

    def guardar_prenda(self):
        """Función para guardar una prenda en el inventario."""

        if not self.genero_var.get() or not self.tipo_var.get() or not self.nombre_var.get() or not self.precio_var.get():
            messagebox.showwarning("Advertencia", "Todos los campos deben ser llenados.")
            return

        prenda = {
            "id": self.next_id,
            "nombre": self.nombre_var.get(),
            "unidades": self.unidades_var.get(),
            "precio": self.precio_var.get(),
            "categoria": f"{self.genero_var.get()} {self.tipo_var.get()}",
            "estado": False if self.unidades_var.get() == 0 else True
        }

        self.data[str(self.next_id)] = prenda
        self.save_data()
        self.next_id += 1
        self.update_inventario_listbox()
        messagebox.showinfo("Éxito", "Prenda guardada correctamente")

    def create_inventario_section(self, frame):
        """Sección para mostrar el inventario de prendas."""
        self.inventario_listbox = tk.Listbox(frame, font=("Helvetica", 12))
        self.inventario_listbox.grid(row=0, column=0, columnspan=2, padx=50, pady=50, sticky='nsew')
        self.update_inventario_listbox()

        editar_button = tk.Button(frame, text="Editar Prenda", command=self.editar_prenda, font=("Helvetica", 12))
        editar_button.grid(row=1, column=0, columnspan=30, pady=30)

    def update_inventario_listbox(self):
        """Actualiza la lista del inventario visualmente."""
        self.inventario_listbox.delete(0, tk.END)
        for id_prenda, prenda in self.data.items():
            self.inventario_listbox.insert(tk.END,
                                           f"{prenda['id']}: {prenda['nombre']} - {prenda['categoria']} - Unidades: {prenda['unidades']} - Precio: ${prenda['precio']}")

    def editar_prenda(self):
        """Función para editar una prenda seleccionada."""
        try:
            selected_index = self.inventario_listbox.curselection()[0]
            selected_id = list(self.data.keys())[selected_index]
            prenda = self.data[selected_id]
            self.editar_prenda_window(prenda)
        except IndexError:
            messagebox.showwarning("Advertencia", "Debe seleccionar una prenda para editar.")

    def editar_prenda_window(self, prenda):
        """Ventana para editar una prenda."""
        edit_window = tk.Toplevel(self)
        edit_window.title(f"Editar Prenda ID {prenda['id']}")

        tk.Label(edit_window, text="Nombre de la Prenda", font=("Helvetica", 12)).grid(row=0, column=0, padx=10, pady=10, sticky='e')
        nombre_var = tk.StringVar(value=prenda["nombre"])
        nombre_entry = tk.Entry(edit_window, textvariable=nombre_var, font=("Helvetica", 12))
        nombre_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Unidades", font=("Helvetica", 12)).grid(row=1, column=0, padx=50, pady=50, sticky='e')
        unidades_var = tk.IntVar(value=prenda["unidades"])
        unidades_entry = tk.Entry(edit_window, textvariable=unidades_var, font=("Helvetica", 12))
        unidades_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(edit_window, text="Precio ($)", font=("Helvetica", 12)).grid(row=2, column=0, padx=50, pady=50, sticky='e')
        precio_var = tk.DoubleVar(value=prenda["precio"])
        precio_entry = tk.Entry(edit_window, textvariable=precio_var, font=("Helvetica", 12))
        precio_entry.grid(row=2, column=1, padx=50, pady=50)

        guardar_button = tk.Button(edit_window, text="Guardar Cambios", font=("Helvetica", 12),
                                   command=lambda: self.guardar_cambios_prenda(prenda["id"], nombre_var.get(),
                                                                               unidades_var.get(), precio_var.get(),
                                                                               edit_window))
        guardar_button.grid(row=30, columnspan=30, pady=30)

    def guardar_cambios_prenda(self, id_prenda, nuevo_nombre, nuevas_unidades, nuevo_precio, window):
        """Guarda los cambios realizados en la prenda editada."""
        # Asegúrate de que id_prenda está en self.data
        if str(id_prenda) in self.data:
            # Actualiza los valores
            self.data[str(id_prenda)]["nombre"] = nuevo_nombre
            self.data[str(id_prenda)]["unidades"] = nuevas_unidades
            self.data[str(id_prenda)]["precio"] = nuevo_precio

            # Actualiza el estado basado en las unidades
            self.data[str(id_prenda)]["estado"] = False if nuevas_unidades == 0 else True

            # Guarda los datos y actualiza la lista
            self.save_data()
            self.update_inventario_listbox()

            # Cierra la ventana y muestra el mensaje de éxito
            window.destroy()
            messagebox.showinfo("Éxito", "Prenda actualizada correctamente")
        else:
            # Manejo del error si id_prenda no existe
            messagebox.showerror("Error", "La prenda con ese ID no existe.")


if __name__ == "__main__":
    app = BotinApp()
    app.mainloop()

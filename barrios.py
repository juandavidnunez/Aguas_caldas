import json
import os
from casas import Casa


class Barrio:
    def __init__(self, id, nombre, ubicacion):
        self.id = id
        self.nombre = nombre
        self.ubicacion = ubicacion

    def to_dict(self):
        """
        Convierte la instancia del barrio en un diccionario.
        """
        return {
            "id": self.id,
            "nombre": self.nombre,
            "ubicacion": self.ubicacion
        }

    @staticmethod
    def generar_id():
        """
        Genera un nuevo ID para un barrio basado en el archivo JSON existente.
        """
        directory = os.path.join("data", "barrios")
        os.makedirs(directory, exist_ok=True)  # Aseguramos la creación de la carpeta

        file_path = os.path.join(directory, "barrios.json")
        last_id = 0

        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                    last_id = max(barrio["id"] for barrio in data)
                except (json.JSONDecodeError, ValueError):
                    pass  # Si el archivo está vacío o tiene formato incorrecto

        return last_id + 1

    @staticmethod
    def guardar_barrio(barrio):
        """
        Guarda la información del barrio en un archivo JSON.
        """
        directory = os.path.join("data", "barrios")
        os.makedirs(directory, exist_ok=True)  # Aseguramos la creación de la carpeta

        file_path = os.path.join(directory, "barrios.json")

        # Leer datos existentes, si los hay
        data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []

        # Agregar el nuevo barrio
        data.append(barrio.to_dict())

        # Guardar los datos actualizados
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)

    @staticmethod
    def crear_barrio(nombre, ubicacion, numero_casas):
        """
        Crea un barrio y sus casas asociadas.
        :param nombre: Nombre del barrio.
        :param ubicacion: Ubicación del barrio.
        :param numero_casas: Número de casas a crear en el barrio.
        """
        # Generar un nuevo ID para el barrio
        barrio_id = Barrio.generar_id()

        # Crear la instancia del nuevo barrio
        nuevo_barrio = Barrio(barrio_id, nombre, ubicacion)

        # Guardar el barrio en el archivo JSON correspondiente
        Barrio.guardar_barrio(nuevo_barrio)

        # Crear las casas asociadas al barrio
        Casa.crear_casas(numero_casas, barrio_id)

        print(f"Barrio '{nombre}' creado con ID {barrio_id} y {numero_casas} casas asociadas.")

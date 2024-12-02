import json
import os


class Tanque:
    def __init__(self, id_tanque, capacidad, presion):
        self.id_tanque = id_tanque
        self.capacidad = capacidad
        self.presion = presion

    def to_dict(self):
        return {"id": self.id_tanque, "capacidad": self.capacidad, "presion": self.presion}

    @staticmethod
    def guardar_tanque(tanque):
        directory = os.path.join("data", "tanques")
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_path = os.path.join(directory, "tanques.json")

        # Inicializar la lista de tanques
        tanques = []
        if os.path.exists(file_path):  # Si el archivo existe, cargar su contenido
            with open(file_path, 'r') as file:
                try:
                    tanques = json.load(file)
                except json.JSONDecodeError:
                    tanques = []  # Si el archivo está corrupto, inicializar lista vacía

        # Añadir el nuevo tanque a la lista
        tanques.append(tanque.to_dict())

        # Guardar todos los tanques en el archivo JSON
        with open(file_path, 'w') as file:
            json.dump(tanques, file, indent=4)

import json
import os


class Casa:
    @staticmethod
    def crear_casas(numero_casas, barrio_id):
        directory = os.path.join("data", "casas")  # Ahora usamos subcarpeta específica
        os.makedirs(directory, exist_ok=True)  # Crear toda la estructura de carpetas si no existe

        file_path = os.path.join(directory, "casas.json")

        # Inicializar la lista de casas
        casas = []
        if os.path.exists(file_path):  # Si el archivo existe, cargar su contenido
            with open(file_path, 'r') as f:
                try:
                    casas = json.load(f)
                except json.JSONDecodeError:
                    casas = []  # Si el archivo está corrupto, inicializar lista vacía

        # Obtener el último ID de casa
        last_id = casas[-1]["id"] if casas else 0

        # Crear las nuevas casas
        for i in range(1, numero_casas + 1):
            casas.append({
                "id": last_id + i,  # ID numérico único
                "nombre": last_id + i,  # Nombre igual al ID
                "barrio_id": barrio_id  # Relación con el ID del barrio
            })

        # Guardar todas las casas en el archivo JSON
        with open(file_path, 'w') as f:
            json.dump(casas, f, indent=4)

        print(f"{numero_casas} casas creadas y guardadas en '{file_path}' para el barrio con ID {barrio_id}.")

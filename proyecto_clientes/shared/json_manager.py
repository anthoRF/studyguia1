# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
import json
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
import os


# CLASE GestorJSON: define cómo serán los objetos de este tipo.
# Crear una clase no crea todavía un estudiante ni un cliente concreto.
class GestorJSON:
    """Lee y guarda una lista de diccionarios en un archivo JSON."""

    # CONSTRUCTOR: se ejecuta al crear un objeto con el nombre de su clase.
    # self representa al objeto que se está preparando. self.nombre guarda
    # el nombre dentro de ese objeto; nombre es el argumento recibido.
    # Los parámetros con None son opcionales. None significa que no se
    # entregó un valor, y permite crear colecciones nuevas para cada objeto.
    def __init__(self, ruta):
        # Guarda la ruta del archivo para usarla al leer y escribir.
        self.ruta = ruta
        # Extrae la carpeta de la ruta para poder crearla si hace falta.
        carpeta = os.path.dirname(ruta)
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if carpeta and not os.path.exists(carpeta):
            # Llama a os.makedirs para realizar su tarea con los argumentos indicados.
            os.makedirs(carpeta)

    # Lee el archivo y obtiene una lista de diccionarios.
    # Si no existe el archivo, devuelve [] porque todavía no hay registros.
    # En Estudiantes, un JSON dañado o una raíz que no sea lista produce
    # un error: así no se confunde un archivo dañado con un sistema vacío.
    # El ejemplo de Clientes conserva la lectura original de la guía,
    # que devuelve [] también si el archivo está dañado.
    def leer(self):
        # Devuelve SIEMPRE una lista: vacía si el archivo no existe o está dañado
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if not os.path.exists(self.ruta):
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return []
        # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
        # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
        try:
            # Abre el archivo para este bloque y lo cierra automáticamente al terminar.
            # "r" lee; "w" escribe reemplazando el contenido; utf-8 conserva las tildes.
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
                datos = json.load(archivo)
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return datos if isinstance(datos, list) else []
        # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
        except (json.JSONDecodeError, OSError):
            # Capturamos errores concretos, nunca un "except:" pelado
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return []

    # Recibe la lista de fichas y trata de guardarla en el archivo.
    # Devuelve True si lo logra y False si ocurre un error previsto.
    # En Estudiantes convierte primero los datos en texto JSON. De ese
    # modo un error de conversión no abre ni vacía el archivo existente.
    # allow_nan=False impide guardar NaN o infinito como valores JSON.
    # Esta opción complementa la validación de notas del controlador.
    def guardar(self, datos):
        # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
        # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
        try:
            # Abre el archivo para este bloque y lo cierra automáticamente al terminar.
            # "r" lee; "w" escribe reemplazando el contenido; utf-8 conserva las tildes.
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                # Llama a json.dump para realizar su tarea con los argumentos indicados.
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return True
        # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
        except (TypeError, OSError):
            # TypeError aparece si intentas guardar un set: JSON no lo conoce
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return False

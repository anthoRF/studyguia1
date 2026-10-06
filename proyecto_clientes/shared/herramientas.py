# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
import os

# DICCIONARIO: cada color tiene su etiqueta y su código de consola
# Diccionario que relaciona el nombre de cada color con su código de consola.
COLORES = {
    "ROJO": "\033[91m",
    "VERDE": "\033[92m",
    "AZUL": "\033[94m",
    "AMARILLO": "\033[93m",
    "CYAN": "\033[96m",
    "BLANCO": "\033[97m",
    "RESET": "\033[0m",
}

# TUPLA: respuestas afirmativas aceptadas. Es fija, por eso no es lista.
# Tupla fija de respuestas afirmativas para confirmar una eliminación.
RESPUESTAS_SI = ("si", "sí", "s", "yes", "y")


# Pide al sistema operativo que limpie la consola.
# Usa clear en sistemas POSIX y cls en Windows, como en la guía.
def limpiar_pantalla():
    # Llama a os.system para realizar su tarea con los argumentos indicados.
    os.system("clear" if os.name == "posix" else "cls")


# Busca el código del color en COLORES y muestra el texto con ese color.
# Al final agrega RESET para que el siguiente mensaje no herede el color.
def imprimir_color(texto, color):
    # Código de color; get() usa blanco si el nombre solicitado no existe.
    codigo = COLORES.get(color, COLORES["BLANCO"])   # .get evita el error si el color no existe
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"{codigo}{texto}{COLORES['RESET']}")


# Limpia la consola y muestra un título entre líneas de signos igual.
# Es presentación: por eso puede usar print() y limpiar_pantalla().
def imprimir_titulo(texto):
    # Llama a limpiar_pantalla para realizar su tarea con los argumentos indicados.
    limpiar_pantalla()
    # Llama a imprimir_color para realizar su tarea con los argumentos indicados.
    imprimir_color("=" * 60, "AZUL")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"  {texto}".center(60))
    # Llama a imprimir_color para realizar su tarea con los argumentos indicados.
    imprimir_color("=" * 60, "AZUL")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print()


# Muestra un mensaje de éxito en verde. No decide si la operación fue válida.
def imprimir_exito(mensaje):
    # Llama a imprimir_color para realizar su tarea con los argumentos indicados.
    imprimir_color(f"✓ {mensaje}", "VERDE")


# Muestra un mensaje de error en rojo. Recibe el texto ya preparado.
def imprimir_error(mensaje):
    # Llama a imprimir_color para realizar su tarea con los argumentos indicados.
    imprimir_color(f"✗ {mensaje}", "ROJO")


# Muestra un mensaje informativo en color cyan. Es una herramienta de presentación.
def imprimir_info(mensaje):
    # Llama a imprimir_color para realizar su tarea con los argumentos indicados.
    imprimir_color(f"ℹ {mensaje}", "CYAN")


# Pide una respuesta y la compara con la tupla fija RESPUESTAS_SI.
# Devuelve True para una respuesta afirmativa y False para las demás.
# La Vista usa esa respuesta antes de llamar a eliminar_estudiante().
def confirmar(pregunta):
    # Devuelve True si el usuario respondió algo de la tupla RESPUESTAS_SI
    # Texto escrito en la confirmación, sin espacios extremos y en minúsculas.
    respuesta = input(f"{pregunta} (si/no): ").strip().lower()
    # Devuelve True o False según el resultado de la comparación.
    return respuesta in RESPUESTAS_SI


# Validación mínima del docente: un solo @, usuario no vacío y
# un dominio que contenga un punto y no termine con punto.
# No comprueba si existe la dirección ni si puede recibir mensajes.
# El controlador de Estudiantes también rechaza espacios comunes.
def es_email_valido(texto):
    # Validación mínima: un @, algo antes, algo después y un punto al final
    # Prepara el texto que se guardará o se mostrará en esta etapa.
    texto = texto.strip()
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if texto.count("@") != 1:
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return False
    # Desempaqueta varios valores: cada variable recibe su elemento correspondiente.
    usuario, dominio = texto.split("@")
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")

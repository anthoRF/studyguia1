# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from models import CAMPOS_CLIENTE
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from views import (
    crear_cliente, obtener_todos, obtener_por_id, buscar_clientes,
    actualizar_cliente, eliminar_cliente, estadisticas
)


# Espera que pulses Enter para que puedas leer el resultado antes de volver al menú.
def pausa():
    # Espera una entrada del usuario; input() devuelve texto.
    input("\nPresione Enter para continuar...")


# Recibe objetos y muestra una fila por registro.
# Los formatos como :<25 reservan un ancho mínimo y alinean a la izquierda.
# Un texto más largo puede superar esa anchura; no se corta el dato.
# En Estudiantes, el modelo entrega el promedio; aquí solo se muestra.
def mostrar_tabla(clientes):
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CIUDAD':<15}{'TELÉFONO':<12}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("-" * 85)
    # Recorre la colección de uno en uno. cliente recibe el elemento de cada vuelta.
    for cliente in clientes:
        # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
        print(f"{cliente.id:<5}{cliente.obtener_nombre_completo():<25}"
              f"{cliente.email:<28}{cliente.ciudad:<15}{cliente.telefono:<12}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("-" * 85)
    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info(f"Total: {len(clientes)} cliente(s)")


# ---------- C · CREAR ----------
# VISTA de Crear: pide los campos, arma un diccionario, llama al
# controlador y presenta la respuesta. No genera IDs ni valida carnets.
def opcion_crear():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("CREAR NUEVO CLIENTE")
    # Recorro la TUPLA de campos: si mañana agrego un campo al Modelo,
    # este formulario se actualiza solo.
    # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
    datos = {}
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_CLIENTE:
        # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
        datos[campo] = input(f"{campo.capitalize()}: ")

    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = crear_cliente(datos)          # desempaqueto la TUPLA que devuelve
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if exito:
        # Llama a imprimir_exito para realizar su tarea con los argumentos indicados.
        imprimir_exito(mensaje)
    else:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(mensaje)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- R · LEER TODOS ----------
# Solicita la lista al controlador. Si está vacía muestra un aviso;
# si contiene objetos, los pasa a la función que imprime la tabla.
def opcion_ver_todos():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("LISTA DE CLIENTES")
    # Asigna a clientes el resultado de la expresión de la derecha.
    clientes = obtener_todos()
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not clientes:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Todavía no hay clientes. Use la opción 1 para crear el primero.")
    else:
        # Llama a mostrar_tabla para realizar su tarea con los argumentos indicados.
        mostrar_tabla(clientes)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- S · BUSCAR ----------
# Pide el término de búsqueda y solicita las coincidencias al controlador.
# La Vista muestra el resultado, pero no hace la comparación de campos.
def opcion_buscar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("BUSCAR CLIENTE")
    # Guarda el texto que se buscará dentro de los campos de cada registro.
    termino = input("Nombre, email, teléfono o ciudad: ")
    # Lista donde se acumulan los objetos que coinciden con la búsqueda.
    encontrados = buscar_clientes(termino)

    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not encontrados:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info(f"Ningún cliente coincide con '{termino}'.")
    else:
        # Llama a mostrar_tabla para realizar su tarea con los argumentos indicados.
        mostrar_tabla(encontrados)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- R · LEER UNO ----------
# Pide el ID y solicita el objeto. Si no existe, muestra el error.
# Si existe, presenta sus datos sin leer directamente el archivo JSON.
def opcion_ver_por_id():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("VER CLIENTE POR ID")
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Asigna a id_cliente el resultado de la expresión de la derecha.
        id_cliente = int(input("Id del cliente: "))
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except ValueError:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error("El id debe ser un número entero")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return pausa()

    # Asigna a cliente el resultado de la expresión de la derecha.
    cliente = obtener_por_id(id_cliente)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not cliente:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un cliente con id {id_cliente}")
    else:
        # Recorro el DICCIONARIO del cliente: clave y valor a la vez
        # Recorre los pares clave y valor del diccionario y los recibe en (clave, valor).
        for clave, valor in cliente.a_diccionario().items():
            # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
            print(f"  {clave.capitalize():<12}: {valor}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- U · ACTUALIZAR ----------
# Pide el ID, muestra los valores actuales y recoge los nuevos.
# Un campo vacío significa conservar su valor. cambios solo contiene
# lo que escribiste. El controlador comprueba si esos cambios son válidos.
def opcion_actualizar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("ACTUALIZAR CLIENTE")
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Asigna a id_cliente el resultado de la expresión de la derecha.
        id_cliente = int(input("Id del cliente: "))
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except ValueError:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error("El id debe ser un número entero")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return pausa()

    # Asigna a cliente el resultado de la expresión de la derecha.
    cliente = obtener_por_id(id_cliente)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not cliente:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return pausa()

    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info(f"Editando a {cliente.obtener_nombre_completo()}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("Deje en blanco el campo que no quiera cambiar.\n")

    # Armo un DICCIONARIO solo con lo que el usuario escribió
    # Diccionario con los campos que el usuario desea modificar.
    cambios = {}
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_CLIENTE:
        # Valor del campo antes de editarlo.
        actual = getattr(cliente, campo)
        # Texto introducido para un campo; vacío significa conservar el valor anterior.
        nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if nuevo:
            # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
            cambios[campo] = nuevo

    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = actualizar_cliente(id_cliente, cambios)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if exito:
        # Llama a imprimir_exito para realizar su tarea con los argumentos indicados.
        imprimir_exito(mensaje)
    else:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(mensaje)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- D · ELIMINAR ----------
# Pide el ID, muestra a quién se eliminará y solicita confirmación.
# Solo llama a la eliminación cuando confirmar() devuelve True.
# Cancelar no cambia el archivo de datos.
def opcion_eliminar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("ELIMINAR CLIENTE")
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Asigna a id_cliente el resultado de la expresión de la derecha.
        id_cliente = int(input("Id del cliente: "))
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except ValueError:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error("El id debe ser un número entero")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return pausa()

    # Asigna a cliente el resultado de la expresión de la derecha.
    cliente = obtener_por_id(id_cliente)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not cliente:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un cliente con id {id_cliente}")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return pausa()

    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info(f"Se eliminará: {cliente}")
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if confirmar("¿Confirma la eliminación?"):
        # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
        # recibe el mensaje o los datos devueltos por la operación.
        exito, mensaje = eliminar_cliente(id_cliente)
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if exito:
            # Llama a imprimir_exito para realizar su tarea con los argumentos indicados.
            imprimir_exito(mensaje)
        else:
            # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
            imprimir_error(mensaje)
    else:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Operación cancelada")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# ---------- EXTRA · ESTADÍSTICAS ----------
# Solicita el resumen del controlador de Clientes y presenta sus valores.
# Los grupos y conjuntos del informe se preparan en views.py.
def opcion_estadisticas():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("ESTADÍSTICAS")
    # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
    datos = estadisticas()
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"  Clientes registrados : {datos['total']}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"  Ciudades distintas   : {len(datos['ciudades'])} -> {', '.join(datos['ciudades'])}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"  Dominios de email    : {', '.join(datos['dominios'])}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"  Sin teléfono         : {len(datos['sin_telefono'])}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Muestra la despedida y devuelve el texto "salir".
# El ciclo principal reconoce ese resultado y termina con break.
def salir():
    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info("¡Hasta luego! 👋")
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
# Diccionario del menú: cada tecla guarda una tupla de texto y función.
OPCIONES = {
    "1": ("Crear cliente", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Estadísticas", opcion_estadisticas),
    "0": ("Salir", salir),
}


# Recorre el diccionario OPCIONES, que guarda tecla -> (texto, función).
# Muestra las teclas y los textos. Las funciones se guardan sin paréntesis
# para que no se ejecuten mientras se construye el menú.
def mostrar_menu():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("SISTEMA DE GESTIÓN DE CLIENTES")
    # Recorre los pares clave y valor del diccionario y los recibe en (tecla, (texto, _funcion)).
    for tecla, (texto, _funcion) in OPCIONES.items():
        # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
        print(f"  {tecla}. {texto}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print()


# Es el ciclo principal de la Vista. Repite el menú con while True.
# Lee la tecla, comprueba que esté en OPCIONES y obtiene su función.
# funcion() ejecuta la opción elegida; si devuelve "salir", usa break.
# En Estudiantes también presenta errores de lectura del JSON sin
# inventar que el archivo está vacío ni escribir encima de él.
def main():
    # Repite el bloque. while True continúa hasta que se ejecuta break.
    while True:
        # Llama a mostrar_menu para realizar su tarea con los argumentos indicados.
        mostrar_menu()
        # Guarda la opción escrita por el usuario como texto, por ejemplo "1" o "10".
        tecla = input("Seleccione una opción: ").strip()

        # Comprueba que el valor todavía no pertenece a la colección o no es una opción válida.
        if tecla not in OPCIONES:          # búsqueda instantánea por clave
            # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
            imprimir_error("Opción no válida")
            # Espera Enter para que puedas leer la pantalla antes de continuar.
            pausa()
            # Salta lo que queda de esta vuelta y vuelve al comienzo del ciclo.
            continue

        # Desempaqueta la tupla del menú en texto y función.
        # Guardar una función es distinto de ejecutarla: se ejecuta con ().
        _texto, funcion = OPCIONES[tecla]
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if funcion() == "salir":
            # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
            break


# Ejecuta el programa cuando este archivo se inicia directamente.
# Si otro archivo lo importa, esta condición no inicia el menú.
if __name__ == "__main__":
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Llama a main para realizar su tarea con los argumentos indicados.
        main()
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except KeyboardInterrupt:
        # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
        print("\nPrograma interrumpido por el usuario.")

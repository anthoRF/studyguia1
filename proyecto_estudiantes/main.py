# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from models import CAMPOS_ESTUDIANTE
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.herramientas import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar
)
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from views import (
    crear_estudiante, obtener_todos, obtener_por_id, buscar_estudiantes,
    actualizar_estudiante, eliminar_estudiante, agregar_nota,
    obtener_promedio, materias_ofertadas, estudiantes_en_comun
)


# Espera que pulses Enter para que puedas leer el resultado antes de volver al menú.
def pausa():
    # Espera una entrada del usuario; input() devuelve texto.
    input("\nPresione Enter para continuar...")


# Recibe la tupla ya desempaquetada como exito y mensaje.
# Solo elige cómo mostrarla: verde si fue éxito y rojo si fue error.
# Evita repetir ese mismo if/else en cada opción del menú.
def mostrar_resultado(exito, mensaje):
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if exito:
        # Llama a imprimir_exito para realizar su tarea con los argumentos indicados.
        imprimir_exito(mensaje)
    else:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(mensaje)


# Pide el ID por consola y convierte el texto a entero con int().
# Si escribes letras, captura ValueError, muestra el mensaje y devuelve
# None. Si es un entero, el controlador comprobará si ese ID existe.
def pedir_id(pregunta="Id del estudiante: "):
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return int(input(pregunta))
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except ValueError:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error("El id debe ser un número entero")
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return None


# Recibe objetos y muestra una fila por registro.
# Los formatos como :<25 reservan un ancho mínimo y alinean a la izquierda.
# Un texto más largo puede superar esa anchura; no se corta el dato.
# En Estudiantes, el modelo entrega el promedio; aquí solo se muestra.
def mostrar_tabla(estudiantes):
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print(f"{'ID':<5}{'NOMBRE':<25}{'EMAIL':<28}{'CARNET':<15}{'PROMEDIO':<10}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("-" * 83)
    # Recorre la colección de uno en uno. estudiante recibe el elemento de cada vuelta.
    for estudiante in estudiantes:
        # Recibe el resultado calculado por el modelo; la Vista solo lo presenta.
        promedio = estudiante.obtener_promedio()
        # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
        print(f"{estudiante.id:<5}{estudiante.obtener_nombre_completo():<25}"
              f"{estudiante.email:<28}{estudiante.carnet:<15}{promedio:<10.2f}")
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("-" * 83)
    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")


# VISTA de Crear: pide los campos, arma un diccionario, llama al
# controlador y presenta la respuesta. No genera IDs ni valida carnets.
def opcion_crear():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("CREAR NUEVO ESTUDIANTE")
    # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
    datos = {}
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_ESTUDIANTE:
        # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
        datos[campo] = input(f"{campo.capitalize()}: ")
    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = crear_estudiante(datos)
    # Llama a mostrar_resultado para realizar su tarea con los argumentos indicados.
    mostrar_resultado(exito, mensaje)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Solicita la lista al controlador. Si está vacía muestra un aviso;
# si contiene objetos, los pasa a la función que imprime la tabla.
def opcion_ver_todos():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("LISTA DE ESTUDIANTES")
    # Lista de objetos Estudiante para devolver o presentar.
    estudiantes = obtener_todos()
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not estudiantes:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Todavía no hay estudiantes. Use la opción 1.")
    else:
        # Llama a mostrar_tabla para realizar su tarea con los argumentos indicados.
        mostrar_tabla(estudiantes)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide el término de búsqueda y solicita las coincidencias al controlador.
# La Vista muestra el resultado, pero no hace la comparación de campos.
def opcion_buscar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("BUSCAR ESTUDIANTE")
    # Guarda el texto que se buscará dentro de los campos de cada registro.
    termino = input("Nombre, apellido, email o carnet: ")
    # Lista donde se acumulan los objetos que coinciden con la búsqueda.
    encontrados = buscar_estudiantes(termino)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not encontrados:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("No hay estudiantes que coincidan con la búsqueda.")
    else:
        # Llama a mostrar_tabla para realizar su tarea con los argumentos indicados.
        mostrar_tabla(encontrados)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide el ID y solicita el objeto. Si no existe, muestra el error.
# Si existe, presenta sus datos sin leer directamente el archivo JSON.
def opcion_ver_por_id():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("VER ESTUDIANTE POR ID")
    # Asigna a id_estudiante el resultado de la expresión de la derecha.
    id_estudiante = pedir_id()
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_estudiante is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = obtener_por_id(id_estudiante)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante is None:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
    else:
        # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
        datos = estudiante.a_diccionario()
        # Recorre los pares clave y valor del diccionario y los recibe en (clave, valor).
        for clave, valor in datos.items():
            # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
            print(f"  {clave.capitalize()}: {valor}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide el ID, muestra los valores actuales y recoge los nuevos.
# Un campo vacío significa conservar su valor. cambios solo contiene
# lo que escribiste. El controlador comprueba si esos cambios son válidos.
def opcion_actualizar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("ACTUALIZAR ESTUDIANTE")
    # Asigna a id_estudiante el resultado de la expresión de la derecha.
    id_estudiante = pedir_id()
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_estudiante is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = obtener_por_id(id_estudiante)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante is None:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
    print("Deje en blanco el campo que no quiera cambiar.\n")
    # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
    datos = estudiante.a_diccionario()
    # Diccionario con los campos que el usuario desea modificar.
    cambios = {}
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_ESTUDIANTE:
        # Texto introducido para un campo; vacío significa conservar el valor anterior.
        nuevo = input(f"{campo.capitalize()} [{datos[campo]}]: ").strip()
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if nuevo:
            # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
            cambios[campo] = nuevo
    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = actualizar_estudiante(id_estudiante, cambios)
    # Llama a mostrar_resultado para realizar su tarea con los argumentos indicados.
    mostrar_resultado(exito, mensaje)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide el ID, muestra a quién se eliminará y solicita confirmación.
# Solo llama a la eliminación cuando confirmar() devuelve True.
# Cancelar no cambia el archivo de datos.
def opcion_eliminar():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("ELIMINAR ESTUDIANTE")
    # Asigna a id_estudiante el resultado de la expresión de la derecha.
    id_estudiante = pedir_id()
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_estudiante is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = obtener_por_id(id_estudiante)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante is None:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(f"No existe un estudiante con id {id_estudiante}")
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info(f"Se eliminará: {estudiante.obtener_nombre_completo()}")
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if confirmar("¿Confirma la eliminación?"):
        # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
        # recibe el mensaje o los datos devueltos por la operación.
        exito, mensaje = eliminar_estudiante(id_estudiante)
        # Llama a mostrar_resultado para realizar su tarea con los argumentos indicados.
        mostrar_resultado(exito, mensaje)
    else:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Operación cancelada")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide ID, materia y nota. Envía la nota como texto al controlador.
# Allí se comprueba que sea numérica y que esté entre 0 y 20.
def opcion_agregar_nota():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("AGREGAR NOTA")
    # Asigna a id_estudiante el resultado de la expresión de la derecha.
    id_estudiante = pedir_id()
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_estudiante is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Guarda el nombre de la materia; normalizar_materia aplica strip() y lower().
    materia = input("Materia: ")
    # Convierte el texto a número decimal. Después aún debe comprobarse su rango.
    nota = input("Nota entre 0 y 20 (ejemplo decimal: 18.5): ")
    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = agregar_nota(id_estudiante, materia, nota)
    # Llama a mostrar_resultado para realizar su tarea con los argumentos indicados.
    mostrar_resultado(exito, mensaje)
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Solicita al controlador el promedio del ID pedido y presenta el mensaje.
# Si existe el estudiante, también muestra sus listas de notas por materia.
# No contiene la suma ni la división del promedio.
def opcion_ver_promedio():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("VER PROMEDIO")
    # Asigna a id_estudiante el resultado de la expresión de la derecha.
    id_estudiante = pedir_id()
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_estudiante is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = obtener_promedio(id_estudiante)
    # Llama a mostrar_resultado para realizar su tarea con los argumentos indicados.
    mostrar_resultado(exito, mensaje)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if exito:
        # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
        estudiante = obtener_por_id(id_estudiante)
        # Recorre los pares clave y valor del diccionario y los recibe en (materia, notas).
        for materia, notas in estudiante.notas.items():
            # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
            print(f"  {materia}: {notas}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Pide dos IDs y recibe (exito, resultado) del controlador.
# Distingue un error de IDs, un conjunto vacío y un conjunto con materias.
# La intersección ya se hizo en el modelo, no se calcula en la Vista.
def opcion_materias_en_comun():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("MATERIAS EN COMÚN")
    # Asigna a id_a el resultado de la expresión de la derecha.
    id_a = pedir_id("Id del primer estudiante: ")
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_a is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Asigna a id_b el resultado de la expresión de la derecha.
    id_b = pedir_id("Id del segundo estudiante: ")
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if id_b is None:
        # Espera Enter para que puedas leer la pantalla antes de continuar.
        pausa()
        # Termina esta función y vuelve a quien la llamó; sin valor explícito devuelve None.
        return
    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, resultado = estudiantes_en_comun(id_a, id_b)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not exito:
        # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
        imprimir_error(resultado)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    elif not resultado:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Los estudiantes no tienen materias en común.")
    else:
        # Recorre la colección de uno en uno. materia recibe el elemento de cada vuelta.
        for materia in sorted(resultado):
            # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
            print(f"  - {materia}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Solicita el conjunto con todas las materias inscritas y lo presenta.
# sorted() ordena su presentación, pero no reemplaza el set del controlador.
def opcion_materias_ofertadas():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("MATERIAS OFERTADAS")
    # Conjunto de materias; no admite nombres duplicados.
    materias = materias_ofertadas()
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not materias:
        # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
        imprimir_info("Todavía no hay materias inscritas.")
    else:
        # Recorre la colección de uno en uno. materia recibe el elemento de cada vuelta.
        for materia in sorted(materias):
            # Muestra este resultado en la consola. Las f-strings insertan valores entre llaves.
            print(f"  - {materia}")
    # Espera Enter para que puedas leer la pantalla antes de continuar.
    pausa()


# Muestra la despedida y devuelve el texto "salir".
# El ciclo principal reconoce ese resultado y termina con break.
def salir():
    # Llama a imprimir_info para realizar su tarea con los argumentos indicados.
    imprimir_info("¡Hasta luego!")
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return "salir"


# DICCIONARIO de opciones: tecla -> (texto del menú, función)
# Diccionario del menú: cada tecla guarda una tupla de texto y función.
OPCIONES = {
    "1": ("Crear estudiante", opcion_crear),
    "2": ("Ver todos", opcion_ver_todos),
    "3": ("Buscar", opcion_buscar),
    "4": ("Ver por id", opcion_ver_por_id),
    "5": ("Actualizar", opcion_actualizar),
    "6": ("Eliminar", opcion_eliminar),
    "7": ("Agregar nota", opcion_agregar_nota),
    "8": ("Ver promedio", opcion_ver_promedio),
    "9": ("Materias en común", opcion_materias_en_comun),
    "10": ("Materias ofertadas", opcion_materias_ofertadas),
    "0": ("Salir", salir),
}


# Recorre el diccionario OPCIONES, que guarda tecla -> (texto, función).
# Muestra las teclas y los textos. Las funciones se guardan sin paréntesis
# para que no se ejecuten mientras se construye el menú.
def mostrar_menu():
    # Llama a imprimir_titulo para realizar su tarea con los argumentos indicados.
    imprimir_titulo("SISTEMA DE GESTIÓN DE ESTUDIANTES")
    # Recorre los pares clave y valor del diccionario y los recibe en (tecla, (texto, funcion)).
    for tecla, (texto, funcion) in OPCIONES.items():
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
        if tecla not in OPCIONES:
            # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
            imprimir_error("Opción no válida")
            # Espera Enter para que puedas leer la pantalla antes de continuar.
            pausa()
            # Salta lo que queda de esta vuelta y vuelve al comienzo del ciclo.
            continue
        # Desempaqueta la tupla del menú en texto y función.
        # Guardar una función es distinto de ejecutarla: se ejecuta con ().
        texto, funcion = OPCIONES[tecla]
        # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
        # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
        try:
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if funcion() == "salir":
                # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
                break
        # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
        except (ValueError, OSError) as error:
            # Llama a imprimir_error para realizar su tarea con los argumentos indicados.
            imprimir_error(f"No se pudo completar la operación: {error}")
            # Espera Enter para que puedas leer la pantalla antes de continuar.
            pausa()


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

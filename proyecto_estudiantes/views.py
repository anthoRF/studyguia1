# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from models import Estudiante, CAMPOS_ESTUDIANTE
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.json_manager import GestorJSON
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.herramientas import es_email_valido, normalizar_materia


# Crea el gestor que trabajará con el JSON de este proyecto.
gestor = GestorJSON("data/estudiantes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
# Tupla con los campos que no pueden quedar vacíos.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email", "carnet")
# Tupla con los campos que revisará la búsqueda por texto.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "carnet")


# Construye un set con los carnets guardados para detectar duplicados.
# Normaliza espacios y mayúsculas antes de comparar.
# excepto_id permite excluir a quien estamos editando: conservar
# el carnet propio no debe contarse como un duplicado.
def carnets_registrados(excepto_id=None):
    # Empieza con un set vacío; después agrega los carnets encontrados.
    carnets = set()
    # Recorre la colección de uno en uno. registro recibe el elemento de cada vuelta.
    for registro in gestor.leer():
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if registro["id"] != excepto_id:
            # add() agrega al conjunto; si el elemento ya existe, no lo duplica.
            carnets.add(registro["carnet"].strip().lower())
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return carnets


# Busca el mayor ID entre los registros existentes y devuelve mayor + 1.
# En Estudiantes empezamos en 0 y lo actualizamos con un for y un if.
# Sin registros, devuelve 1. Si hay IDs 1, 3 y 8, devuelve 9.
# No es len(registros) + 1: borrar un registro intermedio podría causar
# un ID repetido si solo contáramos cuántos registros quedan.
# Sigue la regla de la guía: puede reutilizar el mayor ID si se borró.
def siguiente_id():
    # Guarda el mayor ID encontrado hasta este punto del recorrido.
    mayor = 0
    # Recorre la colección de uno en uno. registro recibe el elemento de cada vuelta.
    for registro in gestor.leer():
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if registro["id"] > mayor:
            # Guarda el mayor ID encontrado hasta este punto del recorrido.
            mayor = registro["id"]
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return mayor + 1


# Reúne las reglas de los datos personales para no repetirlas
# al crear y actualizar: campos obligatorios, email y carnet único.
# Devuelve (False, mensaje) al encontrar un problema, o (True, mensaje)
# si todos los datos son válidos. No imprime ni pide información.
def validar_datos(datos, excepto_id=None):
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_OBLIGATORIOS:
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if datos[campo] == "":
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, f"El campo {campo} es obligatorio"
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not es_email_valido(datos["email"]):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "El email no tiene un formato válido"
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if " " in datos["email"]:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "El email no debe contener espacios"
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if datos["carnet"].lower() in carnets_registrados(excepto_id):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "Ese carnet ya está registrado"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, "Datos válidos"


# Recibe un diccionario con nombre, apellido, email y carnet.
# Limpia espacios, valida, genera el ID y construye el objeto.
# Después agrega su ficha a la lista y pide al gestor que la guarde.
# Devuelve una tupla (exito, mensaje). Solo informa éxito si se guardó.
def crear_estudiante(datos):
    # Diccionario con los datos de entrada normalizados para validar.
    valores = {}
    # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
    for campo in CAMPOS_ESTUDIANTE:
        # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
        valores[campo] = str(datos.get(campo, "")).strip()

    # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
    # recibe el mensaje o los datos devueltos por la operación.
    exito, mensaje = validar_datos(valores)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not exito:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, mensaje

    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = Estudiante(
        siguiente_id(), valores["nombre"], valores["apellido"],
        valores["email"], valores["carnet"],
    )

    # 6) Agrego a la LISTA y guardo
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # append() agrega este elemento al final de la lista; conserva los anteriores.
    registros.append(estudiante.a_diccionario())
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not gestor.guardar(registros):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "No se pudo escribir el archivo"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, f"Estudiante creado con id {estudiante.id}"


# Lee la lista de fichas del JSON y convierte cada ficha en un objeto.
# Devuelve una lista de objetos, no imprime una tabla.
# En Estudiantes usamos una lista vacía, un for y append().
def obtener_todos():
    # Lista de objetos Estudiante para devolver o presentar.
    estudiantes = []
    # Recorre la colección de uno en uno. registro recibe el elemento de cada vuelta.
    for registro in gestor.leer():
        # append() agrega este elemento al final de la lista; conserva los anteriores.
        estudiantes.append(Estudiante.desde_diccionario(registro))
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return estudiantes


# Recibe un ID y recorre los objetos buscando uno que tenga ese ID.
# Devuelve el objeto al encontrarlo. Si termina sin coincidencias,
# devuelve None; eso permite distinguir un ID inexistente.
def obtener_por_id(id_estudiante):
    # Recorre la colección de uno en uno. estudiante recibe el elemento de cada vuelta.
    for estudiante in obtener_todos():
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if estudiante.id == id_estudiante:
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return estudiante
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return None


# Recibe un texto y busca coincidencias parciales en los campos
# de CAMPOS_BUSCABLES. La búsqueda no distingue mayúsculas.
# Cada estudiante se agrega una sola vez: break termina el recorrido
# de sus campos cuando alguno coincide, y sigue con el siguiente.
def buscar_estudiantes(termino):
    # Guarda el texto que se buscará dentro de los campos de cada registro.
    termino = termino.strip().lower()
    # Lista donde se acumulan los objetos que coinciden con la búsqueda.
    encontrados = []
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if termino == "":
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return encontrados
    # Recorre la colección de uno en uno. estudiante recibe el elemento de cada vuelta.
    for estudiante in obtener_todos():
        # Guarda los datos obtenidos en esta etapa; observa si vienen del objeto o del JSON.
        datos = estudiante.a_diccionario()
        # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
        for campo in CAMPOS_BUSCABLES:
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if termino in datos[campo].lower():
                # append() agrega este elemento al final de la lista; conserva los anteriores.
                encontrados.append(estudiante)
                # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
                break
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return encontrados


# Recibe el ID y un diccionario solo con los campos que quieres cambiar.
# Busca la posición, copia la ficha y aplica los cambios a esa copia.
# Valida antes de guardar. No permite modificar ID, notas o materias
# mediante esta operación de datos personales.
# Reconstruir el objeto conserva las notas y normaliza las materias.
def actualizar_estudiante(id_estudiante, cambios):
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # enumerate() entrega dos valores por vuelta: posición y registro.
    # La posición sirve para reemplazar la ficha dentro de la lista.
    for posicion, registro in enumerate(registros):
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if registro["id"] == id_estudiante:
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if not cambios:
                # Devuelve una tupla con varios resultados y termina esta función.
                # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                return False, "No se indicó ningún cambio"
            # Copia de la ficha original: se cambian sus datos personales sin perder notas.
            nuevos_datos = registro.copy()
            # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
            for campo in cambios:
                # Comprueba que el valor todavía no pertenece a la colección o no es una opción válida.
                if campo not in CAMPOS_ESTUDIANTE:
                    # Devuelve una tupla con varios resultados y termina esta función.
                    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                    return False, f"El campo {campo} no se puede modificar"
                # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
                nuevos_datos[campo] = str(cambios[campo]).strip()

            # Desempaqueta una tupla: exito recibe True o False; el segundo nombre
            # recibe el mensaje o los datos devueltos por la operación.
            exito, mensaje = validar_datos(nuevos_datos, id_estudiante)
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if not exito:
                # Devuelve una tupla con varios resultados y termina esta función.
                # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                return False, mensaje

            # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
            estudiante = Estudiante.desde_diccionario(nuevos_datos)
            # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
            registros[posicion] = estudiante.a_diccionario()
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if not gestor.guardar(registros):
                # Devuelve una tupla con varios resultados y termina esta función.
                # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                return False, "No se pudo guardar la actualización"
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return True, f"Estudiante {id_estudiante} actualizado"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return False, f"No existe un estudiante con id {id_estudiante}"


# Construye una lista nueva con los registros que deben permanecer.
# encontrado empieza en False y cambia a True cuando aparece el ID.
# No borramos de la lista mientras la recorremos: podría saltar datos.
# Devuelve error si no existe el ID o si no se pudo guardar.
def eliminar_estudiante(id_estudiante):
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # Lista nueva para los registros que permanecerán tras la eliminación.
    quedan = []
    # Bandera: indica si ya apareció el registro con el ID buscado.
    encontrado = False
    # Recorre la colección de uno en uno. registro recibe el elemento de cada vuelta.
    for registro in registros:
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if registro["id"] == id_estudiante:
            # Bandera: indica si ya apareció el registro con el ID buscado.
            encontrado = True
        else:
            # append() agrega este elemento al final de la lista; conserva los anteriores.
            quedan.append(registro)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not encontrado:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"No existe un estudiante con id {id_estudiante}"
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not gestor.guardar(quedan):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "No se pudo guardar la eliminación"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, f"Estudiante {id_estudiante} eliminado"


# En el CONTROLADOR recibe ID, materia y nota, valida los datos,
# localiza al estudiante y coordina el guardado de su ficha.
# En el MODELO recibe materia y nota ya válida: inscribe la materia
# y agrega la nota a su lista. Son dos funciones de capas distintas.
# Agregar conserva las notas anteriores: no reemplaza su lista.
def agregar_nota(id_estudiante, materia, nota):
    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = obtener_por_id(id_estudiante)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante is None:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"No existe un estudiante con id {id_estudiante}"
    # Guarda el nombre de la materia; normalizar_materia aplica strip() y lower().
    materia = normalizar_materia(materia)
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if materia == "":
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "La materia es obligatoria"
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # Convierte el texto a número decimal. Después aún debe comprobarse su rango.
        nota = float(str(nota).strip())
    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except ValueError:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "La nota debe ser un número entre 0 y 20"
    # Exige una nota dentro de 0 a 20, incluidos los extremos.
    # not invierte la comprobación: si no está dentro, devuelve error.
    # También rechaza NaN, porque NaN no satisface este intervalo.
    if not (0 <= nota <= 20):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "La nota debe estar entre 0 y 20"

    # Llama a estudiante.agregar_nota para realizar su tarea con los argumentos indicados.
    estudiante.agregar_nota(materia, nota)
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # enumerate() entrega dos valores por vuelta: posición y registro.
    # La posición sirve para reemplazar la ficha dentro de la lista.
    for posicion, registro in enumerate(registros):
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if registro["id"] == id_estudiante:
            # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
            registros[posicion] = estudiante.a_diccionario()
            # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
            break
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not gestor.guardar(registros):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "No se pudo guardar la nota"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, f"Nota {nota:g} agregada en {materia}"


# En el MODELO calcula el promedio de todas las notas individuales.
# En Estudiantes usamos total como acumulador y cantidad como contador.
# Ejemplo: 18, 20 y 16 -> total 54, cantidad 3 -> promedio 18.
# Si no hay notas, devuelve 0 para evitar dividir entre cero.
# La función del CONTROLADOR con este nombre recibe un ID y devuelve
# una tupla con éxito o error y el mensaje que mostrará la Vista.
def obtener_promedio(id_estudiante):
    # Guarda el objeto Estudiante que se crea, se consulta o se reconstruye.
    estudiante = obtener_por_id(id_estudiante)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante is None:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"No existe un estudiante con id {id_estudiante}"
    # Recibe el resultado calculado por el modelo; la Vista solo lo presenta.
    promedio = estudiante.obtener_promedio()
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, f"Promedio de {estudiante.obtener_nombre_completo()}: {promedio:.2f}"


# Reúne las materias inscritas de todos los estudiantes en un solo set.
# Un nombre repetido se agrega una sola vez. No crea un catálogo externo.
# Si no hay materias inscritas, devuelve un conjunto vacío.
def materias_ofertadas():
    # Conjunto de materias; no admite nombres duplicados.
    materias = set()
    # Recorre la colección de uno en uno. estudiante recibe el elemento de cada vuelta.
    for estudiante in obtener_todos():
        # Recorre la colección de uno en uno. materia recibe el elemento de cada vuelta.
        for materia in estudiante.materias:
            # add() agrega al conjunto; si el elemento ya existe, no lo duplica.
            materias.add(materia)
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return materias


# Recibe los IDs de dos estudiantes. Aunque el nombre diga estudiantes,
# lo que devuelve son las MATERIAS que esos estudiantes comparten.
# Si algún ID no existe, devuelve (False, mensaje). Si ambos existen,
# devuelve (True, conjunto), incluso si ese conjunto está vacío.
def estudiantes_en_comun(id_a, id_b):
    # Obtiene el primer estudiante usando su ID.
    estudiante_a = obtener_por_id(id_a)
    # Obtiene el segundo estudiante usando su ID.
    estudiante_b = obtener_por_id(id_b)
    # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
    if estudiante_a is None or estudiante_b is None:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, "Uno o ambos estudiantes no existen"
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, estudiante_a.materias_en_comun(estudiante_b)

# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from models import Cliente, CAMPOS_CLIENTE
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.json_manager import GestorJSON
# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.herramientas import es_email_valido

# Crea el gestor que trabajará con el JSON de este proyecto.
gestor = GestorJSON("data/clientes.json")

# TUPLAS de configuración: fijas, nadie las modifica en tiempo de ejecución
# Tupla con los campos que no pueden quedar vacíos.
CAMPOS_OBLIGATORIOS = ("nombre", "apellido", "email")
# Tupla con los campos que revisará la búsqueda por texto.
CAMPOS_BUSCABLES = ("nombre", "apellido", "email", "telefono", "ciudad")


# ===================== AYUDAS INTERNAS =====================

# Ejemplo del docente: construye un set con los emails registrados.
# La comparación usa minúsculas para detectar ANA@x.com y ana@x.com.
# excepto_id excluye al cliente que está siendo actualizado.
def emails_registrados(excepto_id=None):
    """CONJUNTO con los emails ya usados. Sirve para detectar duplicados al instante."""
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return {
        registro["email"].lower()
        for registro in gestor.leer()
        if registro["id"] != excepto_id
    }


# Busca el mayor ID entre los registros existentes y devuelve mayor + 1.
# En Estudiantes empezamos en 0 y lo actualizamos con un for y un if.
# Sin registros, devuelve 1. Si hay IDs 1, 3 y 8, devuelve 9.
# No es len(registros) + 1: borrar un registro intermedio podría causar
# un ID repetido si solo contáramos cuántos registros quedan.
# Sigue la regla de la guía: puede reutilizar el mayor ID si se borró.
def siguiente_id():
    # Asigna a ids el resultado de la expresión de la derecha.
    ids = [registro["id"] for registro in gestor.leer()]
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return max(ids) + 1 if ids else 1


# ===================== C · CREATE =====================

# Este es el ejemplo original del docente para crear un cliente.
# Normaliza los campos, revisa obligatorios, formato y email duplicado.
# Cliente(siguiente_id(), **valores) reparte las claves del diccionario
# como argumentos con nombre. Es un recurso que aparece en la guía.
# En el proyecto nuevo de Estudiantes los argumentos están explícitos.
def crear_cliente(datos):
    """datos: diccionario con las claves de CAMPOS_CLIENTE. Devuelve (exito, mensaje)."""
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # 1) Normalizo: un diccionario con todos los campos, sin espacios sobrantes
        # Diccionario con los datos de entrada normalizados para validar.
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_CLIENTE}

        # 2) Reviso obligatorios recorriendo la TUPLA
        # Asigna a faltantes el resultado de la expresión de la derecha.
        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if faltantes:
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        # 3) Formato del email
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if not es_email_valido(valores["email"]):
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        # 4) Duplicado: búsqueda instantánea dentro del CONJUNTO
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if valores["email"].lower() in emails_registrados():
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, "Ese email ya está registrado"

        # 5) Creo el objeto del Modelo. ** convierte el diccionario en argumentos
        # Asigna a cliente el resultado de la expresión de la derecha.
        cliente = Cliente(siguiente_id(), **valores)

        # 6) Agrego a la LISTA y guardo
        # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
        registros = gestor.leer()
        # append() agrega este elemento al final de la lista; conserva los anteriores.
        registros.append(cliente.a_diccionario())
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if not gestor.guardar(registros):
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, "No se pudo escribir el archivo"

        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return True, f"Cliente {cliente.obtener_nombre_completo()} creado con id {cliente.id}"

    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except Exception as error:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

# Lee la lista de fichas del JSON y convierte cada ficha en un objeto.
# Devuelve una lista de objetos, no imprime una tabla.
# En Estudiantes usamos una lista vacía, un for y append().
def obtener_todos():
    """LISTA de objetos Cliente."""
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return [Cliente.desde_diccionario(registro) for registro in gestor.leer()]


# Recibe un ID y recorre los objetos buscando uno que tenga ese ID.
# Devuelve el objeto al encontrarlo. Si termina sin coincidencias,
# devuelve None; eso permite distinguir un ID inexistente.
def obtener_por_id(id_cliente):
    # Recorre la colección de uno en uno. cliente recibe el elemento de cada vuelta.
    for cliente in obtener_todos():
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if cliente.id == id_cliente:
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return cliente
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return None


# ===================== S · SEARCH =====================

# Recorre los registros y sus campos para buscar coincidencias parciales.
# Devuelve la lista de coincidencias; puede ser una lista vacía.
# El break evita repetir un cliente cuando coinciden varios campos.
def buscar_clientes(termino):
    """Búsqueda lineal: revisa registro por registro los campos de CAMPOS_BUSCABLES."""
    # Guarda el texto que se buscará dentro de los campos de cada registro.
    termino = termino.strip().lower()
    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if not termino:
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return []

    # Lista donde se acumulan los objetos que coinciden con la búsqueda.
    encontrados = []
    # Recorre la colección de uno en uno. registro recibe el elemento de cada vuelta.
    for registro in gestor.leer():
        # Recorre la colección de uno en uno. campo recibe el elemento de cada vuelta.
        for campo in CAMPOS_BUSCABLES:                 # recorro la TUPLA de campos
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if termino in str(registro.get(campo, "")).lower():
                # append() agrega este elemento al final de la lista; conserva los anteriores.
                encontrados.append(Cliente.desde_diccionario(registro))
                # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
                break                                   # ya coincidió: paso al siguiente cliente
    # Devuelve el resultado a quien llamó esta función y termina su ejecución.
    return encontrados


# ===================== U · UPDATE =====================

# Ejemplo original: recibe el ID y un diccionario de cambios.
# Comprueba claves, valida el email y encuentra la posición del cliente.
# update(cambios) reemplaza solo los campos presentes en ese diccionario.
# El ejemplo anuncia éxito sin comprobar el resultado de guardar();
# lo conservamos como está. Estudiantes sí comprueba ese resultado.
def actualizar_cliente(id_cliente, cambios):
    """cambios: diccionario solo con los campos que se quieren modificar."""
    # Intenta ejecutar este bloque. Si aparece uno de los errores nombrados
    # en except, ejecuta su bloque de manejo en lugar de continuar normalmente.
    try:
        # DIFERENCIA DE CONJUNTOS: ¿mandaron algún campo que no existe?
        # Asigna a desconocidos el resultado de la expresión de la derecha.
        desconocidos = set(cambios) - set(CAMPOS_CLIENTE)
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if desconocidos:
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if not cambios:
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, "No se indicó ningún cambio"

        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if "email" in cambios:
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if not es_email_valido(cambios["email"]):
                # Devuelve una tupla con varios resultados y termina esta función.
                # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                return False, "El email no tiene un formato válido"
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if cambios["email"].lower() in emails_registrados(excepto_id=id_cliente):
                # Devuelve una tupla con varios resultados y termina esta función.
                # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
                return False, "Ese email ya lo usa otro cliente"

        # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
        registros = gestor.leer()
        # Índice de la ficha dentro de la lista; no es el ID del registro.
        posicion = None
        # enumerate() entrega dos valores por vuelta: posición y registro.
        # La posición sirve para reemplazar la ficha dentro de la lista.
        for indice, registro in enumerate(registros):   # enumerate me da índice y valor
            # Condición: si la expresión es verdadera se ejecuta este bloque.
            # Si hay else o elif, esos bloques cubren las alternativas.
            if registro["id"] == id_cliente:
                # Índice de la ficha dentro de la lista; no es el ID del registro.
                posicion = indice
                # Termina el ciclo más cercano. En la búsqueda evita agregar dos veces el mismo objeto.
                break

        # Comprueba si falta un resultado. None no es lo mismo que cero ni que una lista vacía.
        if posicion is None:
            # Devuelve una tupla con varios resultados y termina esta función.
            # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
            return False, f"No existe un cliente con id {id_cliente}"

        # Llama a registros[posicion].update para realizar su tarea con los argumentos indicados.
        registros[posicion].update(cambios)             # actualizo el diccionario en su lugar
        # Llama a gestor.guardar para realizar su tarea con los argumentos indicados.
        gestor.guardar(registros)
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return True, f"Cliente {id_cliente} actualizado ({len(cambios)} campo/s)"

    # Maneja únicamente los errores indicados aquí y prepara la respuesta correspondiente.
    except Exception as error:
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

# Ejemplo original: filtra los registros para dejar fuera el ID pedido.
# Si la cantidad no cambió, ese ID no existía. Luego guarda la lista.
# Este ejemplo tampoco comprueba el resultado de guardar();
# Estudiantes sí lo comprueba antes de anunciar una eliminación exitosa.
def eliminar_cliente(id_cliente):
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # Construyo una LISTA NUEVA sin ese registro: nunca borro mientras recorro
    # Lista nueva para los registros que permanecerán tras la eliminación.
    quedan = [registro for registro in registros if registro["id"] != id_cliente]

    # Condición: si la expresión es verdadera se ejecuta este bloque.
    # Si hay else o elif, esos bloques cubren las alternativas.
    if len(quedan) == len(registros):
        # Devuelve una tupla con varios resultados y termina esta función.
        # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
        return False, f"No existe un cliente con id {id_cliente}"

    # Llama a gestor.guardar para realizar su tarea con los argumentos indicados.
    gestor.guardar(quedan)
    # Devuelve una tupla con varios resultados y termina esta función.
    # Normalmente el primero indica éxito; el segundo es el mensaje o los datos.
    return True, f"Cliente {id_cliente} eliminado"


# ===================== EXTRA: estadísticas con conjuntos =====================

# Ejemplo de Clientes: prepara un diccionario de resultados para la Vista.
# Usa conjuntos para ciudades y dominios únicos y una lista para quienes
# no tienen teléfono. Aquí se preparan datos, no se imprime el informe.
def estadisticas():
    """Devuelve un DICCIONARIO de resumen. Práctica pura de colecciones."""
    # Lista de fichas leída mediante el gestor. Cada ficha es un diccionario.
    registros = gestor.leer()
    # Asigna a ciudades el resultado de la expresión de la derecha.
    ciudades = {r.get("ciudad", "").title() for r in registros if r.get("ciudad")}
    # Asigna a dominios el resultado de la expresión de la derecha.
    dominios = {r["email"].split("@")[1].lower() for r in registros if "@" in r["email"]}
    # Asigna a sin_telefono el resultado de la expresión de la derecha.
    sin_telefono = [r["nombre"] for r in registros if not r.get("telefono")]

    # Devuelve el diccionario completo con los datos del objeto.
    return {
        "total": len(registros),
        "ciudades": sorted(ciudades),
        "dominios": sorted(dominios),
        "sin_telefono": sin_telefono,
    }

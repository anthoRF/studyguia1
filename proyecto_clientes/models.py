# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
import json

# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
# Tupla fija de campos del ejemplo; recorrerla evita repetir cada nombre.
CAMPOS_CLIENTE = ("nombre", "apellido", "email", "telefono", "ciudad", "direccion")


# CLASE Cliente: define cómo serán los objetos de este tipo.
# Crear una clase no crea todavía un estudiante ni un cliente concreto.
class Cliente:
    """MODELO: representa a un cliente."""

    # CONSTRUCTOR: se ejecuta al crear un objeto con el nombre de su clase.
    # self representa al objeto que se está preparando. self.nombre guarda
    # el nombre dentro de ese objeto; nombre es el argumento recibido.
    # Los parámetros con None son opcionales. None significa que no se
    # entregó un valor, y permite crear colecciones nuevas para cada objeto.
    def __init__(self, id_cliente, nombre, apellido, email, telefono, ciudad, direccion):
        # Guarda en este objeto el identificador recibido por el constructor.
        self.id = id_cliente          # no usamos 'id' como parámetro: es una función de Python
        # Guarda el nombre como atributo del objeto: se consulta con objeto.nombre.
        self.nombre = nombre
        # Guarda el apellido como atributo del objeto.
        self.apellido = apellido
        # Guarda el email como texto dentro del objeto.
        self.email = email
        # Guarda el teléfono como texto para conservar sus ceros iniciales.
        self.telefono = telefono
        # Guarda la ciudad del cliente dentro de su objeto.
        self.ciudad = ciudad
        # Guarda la dirección del cliente dentro de su objeto.
        self.direccion = direccion

    # Une el nombre y el apellido del objeto y devuelve un texto.
    # No imprime: quien llama al método decide qué hacer con ese texto.
    def obtener_nombre_completo(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return f"{self.nombre} {self.apellido}"

    # Convierte el objeto en una ficha con claves y valores.
    # Por ejemplo, la clave nombre guarda el valor de self.nombre.
    # El gestor JSON recibe estas fichas, no objetos Estudiante o Cliente.
    # En Estudiantes, sorted(self.materias) devuelve una lista ordenada,
    # porque un set no se puede guardar directamente en JSON.
    def a_diccionario(self):
        # Objeto -> diccionario (listo para JSON)
        # Devuelve el diccionario completo con los datos del objeto.
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "telefono": self.telefono,
            "ciudad": self.ciudad,
            "direccion": self.direccion,
        }

    # Reconstruye un objeto a partir de una ficha leída del JSON.
    # @classmethod indica que se llama sobre la clase: por ejemplo,
    # Estudiante.desde_diccionario(registro). cls representa esa clase.
    # return cls(...) llama al constructor y devuelve el objeto nuevo.
    # get(clave, valor) usa el valor alternativo si esa clave no existe.
    @classmethod
    def desde_diccionario(cls, datos):
        # Diccionario -> objeto. Es un método de la CLASE, no de un objeto:
        # se usa así -> Cliente.desde_diccionario({...})
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return cls(
            datos["id"],
            datos["nombre"],
            datos["apellido"],
            datos["email"],
            datos["telefono"],
            datos.get("ciudad", ""),      # .get por si el archivo es de una versión vieja
            datos.get("direccion", ""),
        )

    # Convierte la ficha del objeto en un texto JSON.
    # dumps() devuelve texto; por sí sola no crea un archivo en el disco.
    def a_json(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return json.dumps(self.a_diccionario(), ensure_ascii=False)

    # Define el texto que representa al objeto al usar str(objeto)
    # o al mostrarlo con print(). Devuelve un texto, no lo imprime aquí.
    def __str__(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return f"[{self.id}] {self.obtener_nombre_completo()} - {self.email}"


# CLASE Estudiante: define cómo serán los objetos de este tipo.
# Crear una clase no crea todavía un estudiante ni un cliente concreto.
class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    # CONSTRUCTOR: se ejecuta al crear un objeto con el nombre de su clase.
    # self representa al objeto que se está preparando. self.nombre guarda
    # el nombre dentro de ese objeto; nombre es el argumento recibido.
    # Los parámetros con None son opcionales. None significa que no se
    # entregó un valor, y permite crear colecciones nuevas para cada objeto.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet, notas=None, materias=None):
        # Guarda en este objeto el identificador recibido por el constructor.
        self.id = id_estudiante
        # Guarda el nombre como atributo del objeto: se consulta con objeto.nombre.
        self.nombre = nombre
        # Guarda el apellido como atributo del objeto.
        self.apellido = apellido
        # Guarda el email como texto dentro del objeto.
        self.email = email
        # Guarda el carnet del estudiante; es un dato distinto del ID numérico.
        self.carnet = carnet                      # ej: EST2026001
        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        # Prepara el diccionario de listas de notas que pertenece a este estudiante.
        self.notas = notas if notas else {}
        # CONJUNTO: materias en las que está inscrito, sin repetidos
        # Prepara el conjunto de materias inscritas de este estudiante.
        self.materias = set(materias) if materias else set()

    # Une el nombre y el apellido del objeto y devuelve un texto.
    # No imprime: quien llama al método decide qué hacer con ese texto.
    def obtener_nombre_completo(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return f"{self.nombre} {self.apellido}"

    # Registra una materia en el conjunto de este estudiante.
    # add() mantiene un único elemento aunque inscribas la misma materia
    # varias veces. En el sistema nuevo también normalizamos su nombre.
    def inscribir_materia(self, materia):
        # add() no duplica: si ya estaba inscrito, no pasa nada
        # add() agrega al conjunto; si el elemento ya existe, no lo duplica.
        self.materias.add(materia)

    # En el CONTROLADOR recibe ID, materia y nota, valida los datos,
    # localiza al estudiante y coordina el guardado de su ficha.
    # En el MODELO recibe materia y nota ya válida: inscribe la materia
    # y agrega la nota a su lista. Son dos funciones de capas distintas.
    # Agregar conserva las notas anteriores: no reemplaza su lista.
    def agregar_nota(self, materia, nota):
        # Llama a self.inscribir_materia para realizar su tarea con los argumentos indicados.
        self.inscribir_materia(materia)
        # setdefault crea la lista vacía la primera vez que aparece la materia
        # append() agrega este elemento al final de la lista; conserva los anteriores.
        self.notas.setdefault(materia, []).append(nota)

    # PROMEDIO DEL MODELO ORIGINAL DEL DOCENTE: prepara la lista todas.
    # values() obtiene cada lista de notas y extend() agrega sus elementos.
    # sum(todas) calcula la suma y len(todas) cuenta las notas.
    # Divide la suma por la cantidad y redondea con round(..., 2).
    # Si todas está vacía, devuelve 0 antes de dividir.
    # En el proyecto separado de Estudiantes reemplazamos esta suma
    # y conteo por dos variables actualizadas dentro de ciclos.
    def obtener_promedio(self):
        # Asigna a todas el resultado de la expresión de la derecha.
        todas = []
        # Recorre los valores del diccionario; aquí cada valor es una lista de notas.
        for lista_notas in self.notas.values():
            # Llama a todas.extend para realizar su tarea con los argumentos indicados.
            todas.extend(lista_notas)
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if not todas:
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return 0
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return round(sum(todas) / len(todas), 2)

    # Recibe otro objeto Estudiante. self es el primero y el argumento
    # es el segundo. & es la intersección: conserva las materias presentes
    # en ambos conjuntos. Si ninguna coincide, el resultado es set().
    def materias_en_comun(self, otro_estudiante):
        # INTERSECCIÓN de conjuntos: qué materias comparten dos estudiantes
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return self.materias & otro_estudiante.materias

    # Convierte el objeto en una ficha con claves y valores.
    # Por ejemplo, la clave nombre guarda el valor de self.nombre.
    # El gestor JSON recibe estas fichas, no objetos Estudiante o Cliente.
    # En Estudiantes, sorted(self.materias) devuelve una lista ordenada,
    # porque un set no se puede guardar directamente en JSON.
    def a_diccionario(self):
        # Devuelve el diccionario completo con los datos del objeto.
        return {
            "id": self.id,
            "nombre": self.nombre,
            "apellido": self.apellido,
            "email": self.email,
            "carnet": self.carnet,
            "notas": self.notas,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "materias": sorted(self.materias),
        }

    # Reconstruye un objeto a partir de una ficha leída del JSON.
    # @classmethod indica que se llama sobre la clase: por ejemplo,
    # Estudiante.desde_diccionario(registro). cls representa esa clase.
    # return cls(...) llama al constructor y devuelve el objeto nuevo.
    # get(clave, valor) usa el valor alternativo si esa clave no existe.
    @classmethod
    def desde_diccionario(cls, datos):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return cls(
            datos["id"], datos["nombre"], datos["apellido"], datos["email"],
            datos["carnet"],
            notas=datos.get("notas", {}),
            # y al leer lo volvemos a convertir en set
            materias=set(datos.get("materias", [])),
        )

    # Define el texto que representa al objeto al usar str(objeto)
    # o al mostrarlo con print(). Devuelve un texto, no lo imprime aquí.
    def __str__(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return f"[{self.carnet}] {self.obtener_nombre_completo()} - Promedio: {self.obtener_promedio()}"

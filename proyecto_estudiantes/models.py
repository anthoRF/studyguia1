# VERSIÓN PARA ESTUDIAR: comentarios explicativos; el código ejecutable
# es el mismo que el de la versión para entregar.
# Lee primero la explicación de cada función y después sigue sus pasos.
# Las líneas que empiezan con # no son instrucciones de Python.

# Importa herramientas o nombres definidos en otro módulo.
# Importar permite usarlos aquí sin escribir otra vez su implementación.
from shared.herramientas import normalizar_materia


# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
# Tupla fija de campos personales; la Vista y el Controlador la comparten.
CAMPOS_ESTUDIANTE = ("nombre", "apellido", "email", "carnet")


# CLASE Estudiante: define cómo serán los objetos de este tipo.
# Crear una clase no crea todavía un estudiante ni un cliente concreto.
class Estudiante:
    """MODELO: representa a un estudiante. Usa las cuatro colecciones."""

    # CONSTRUCTOR: se ejecuta al crear un objeto con el nombre de su clase.
    # self representa al objeto que se está preparando. self.nombre guarda
    # el nombre dentro de ese objeto; nombre es el argumento recibido.
    # Los parámetros con None son opcionales. None significa que no se
    # entregó un valor, y permite crear colecciones nuevas para cada objeto.
    def __init__(self, id_estudiante, nombre, apellido, email, carnet,
                 notas=None, materias=None):
        # Guarda en este objeto el identificador recibido por el constructor.
        self.id = id_estudiante
        # Guarda el nombre como atributo del objeto: se consulta con objeto.nombre.
        self.nombre = nombre
        # Guarda el apellido como atributo del objeto.
        self.apellido = apellido
        # Guarda el email como texto dentro del objeto.
        self.email = email
        # Guarda el carnet del estudiante; es un dato distinto del ID numérico.
        self.carnet = carnet

        # DICCIONARIO DE LISTAS: {"Matemática": [18, 19], "Inglés": [17]}
        # Prepara el diccionario de listas de notas que pertenece a este estudiante.
        self.notas = {}
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if notas is not None:
            # Recorre los pares clave y valor del diccionario y los recibe en (materia, lista_notas).
            for materia, lista_notas in notas.items():
                # Guarda el nombre de la materia; normalizar_materia aplica strip() y lower().
                materia = normalizar_materia(materia)
                # Comprueba que el valor todavía no pertenece a la colección o no es una opción válida.
                if materia not in self.notas:
                    # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
                    self.notas[materia] = []
                # Recorre la colección de uno en uno. nota recibe el elemento de cada vuelta.
                for nota in lista_notas:
                    # append() agrega este elemento al final de la lista; conserva los anteriores.
                    self.notas[materia].append(nota)

        # CONJUNTO: materias en las que está inscrito, sin repetidos
        # Prepara el conjunto de materias inscritas de este estudiante.
        self.materias = set()
        # Condición: si la expresión es verdadera se ejecuta este bloque.
        # Si hay else o elif, esos bloques cubren las alternativas.
        if materias is not None:
            # Recorre la colección de uno en uno. materia recibe el elemento de cada vuelta.
            for materia in materias:
                # add() agrega al conjunto; si el elemento ya existe, no lo duplica.
                self.materias.add(normalizar_materia(materia))
        # Recorre la colección de uno en uno. materia recibe el elemento de cada vuelta.
        for materia in self.notas:
            # add() agrega al conjunto; si el elemento ya existe, no lo duplica.
            self.materias.add(materia)

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
        self.materias.add(normalizar_materia(materia))

    # En el CONTROLADOR recibe ID, materia y nota, valida los datos,
    # localiza al estudiante y coordina el guardado de su ficha.
    # En el MODELO recibe materia y nota ya válida: inscribe la materia
    # y agrega la nota a su lista. Son dos funciones de capas distintas.
    # Agregar conserva las notas anteriores: no reemplaza su lista.
    def agregar_nota(self, materia, nota):
        # Guarda el nombre de la materia; normalizar_materia aplica strip() y lower().
        materia = normalizar_materia(materia)
        # Llama a self.inscribir_materia para realizar su tarea con los argumentos indicados.
        self.inscribir_materia(materia)
        # Comprueba que el valor todavía no pertenece a la colección o no es una opción válida.
        if materia not in self.notas:
            # Escribe en una posición o clave de la colección; puede agregar o reemplazar su valor.
            self.notas[materia] = []
        # append() agrega este elemento al final de la lista; conserva los anteriores.
        self.notas[materia].append(nota)

    # En el MODELO calcula el promedio de todas las notas individuales.
    # En Estudiantes usamos total como acumulador y cantidad como contador.
    # Ejemplo: 18, 20 y 16 -> total 54, cantidad 3 -> promedio 18.
    # Si no hay notas, devuelve 0 para evitar dividir entre cero.
    # La función del CONTROLADOR con este nombre recibe un ID y devuelve
    # una tupla con éxito o error y el mensaje que mostrará la Vista.
    def obtener_promedio(self):
        # Acumulador: guarda la suma de las notas procesadas hasta ahora.
        total = 0
        # Contador: guarda cuántas notas individuales se han procesado.
        cantidad = 0
        # Recorre los valores del diccionario; aquí cada valor es una lista de notas.
        for lista_notas in self.notas.values():
            # Recorre la colección de uno en uno. nota recibe el elemento de cada vuelta.
            for nota in lista_notas:
                # Acumulador: guarda la suma de las notas procesadas hasta ahora.
                total = total + nota
                # Contador: guarda cuántas notas individuales se han procesado.
                cantidad = cantidad + 1
        # Caso sin notas: devuelve 0 antes de intentar la división.
        if cantidad == 0:
            # Devuelve el resultado a quien llamó esta función y termina su ejecución.
            return 0
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return round(total / cantidad, 2)

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
            datos["carnet"], datos.get("notas", {}), datos.get("materias", []),
        )

    # Define el texto que representa al objeto al usar str(objeto)
    # o al mostrarlo con print(). Devuelve un texto, no lo imprime aquí.
    def __str__(self):
        # Devuelve el resultado a quien llamó esta función y termina su ejecución.
        return (f"[{self.carnet}] {self.obtener_nombre_completo()} "
                f"- Promedio: {self.obtener_promedio()}")

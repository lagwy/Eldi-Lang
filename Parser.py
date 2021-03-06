# -*- coding: utf-8 -*-
import ply.yacc as yacc
import Scanner            # Importar el analizador léxico
from Cubo import *        # Importar los identificadores numéricos asignados
tokens = Scanner.tokens   # Lista de tokens
import sys                # Librería para poder finalizar el programa
import json               # Librería para poder visualizar los diccionarios y listas como JSON

# Precedencia de los operadores
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS', 'NOTEQUAL'),
    ('left', 'GREATERTHAN', 'GREATEREQUAL', 'LESSTHAN', 'LESSEQUAL'),
    ('left', 'SUM', 'LESS'),
    ('left', 'TIMES', 'DIVISION'),
)

# Creación de los diccionarios de tipos con sus contadores
# Variables globales
globales_int = {}
globales_int_cont = 0
globales_float = {}
globales_float_cont = 200
globales_char = {}
globales_char_cont = 400
globales_string = {}
globales_string_cont = 600
globales_boolean = {}
globales_boolean_cont = 800

# Variables locales
locales_int = {}
locales_int_cont = 1000
locales_float = {}
locales_float_cont = 1200
locales_char = {}
locales_char_cont = 1400
locales_string = {}
locales_string_cont = 1600
locales_boolean = {}
locales_boolean_cont = 1800

"""
# Variables temporales
temporales_int = {}
temporales_int_cont = 2000
temporales_float = {}
temporales_float_cont = 2200
temporales_char = {}
temporales_char_cont = 2400
temporales_string = {}
temporales_string_cont = 2600
temporales_boolean = {}
temporales_boolean_cont = 2800"""
listTemporales = []
contTemp = 2000

# Variables constantes
constantes_int = []
constantes_int_cont = 3000
constantes_float = []
constantes_float_cont = 3200
constantes_char = []
constantes_char_cont = 3400
constantes_string = []
constantes_string_cont = 3600
constantes_boolean = []
constantes_boolean_cont = 3800

lista_cuadruplos = []           # Lista de cuádruplos
diccionario_metodos = {}        # Diccionario de métodos
parametros = {}                 # Diccionario de parámetros para cada método
temporalActual = 1              # Número del temporal actual
tipo_exp = None                 # Contiene si la expresión es llamada u operación
cont_args = 1                   # Contador para identificar el número de argumento en una llamada
solo_una_expresion = None       # Revisa si la expresión es una asignación directa o una operación
params_metodo = None            # Método al que pertenece este parámetro
tipo_metodo = None              # Tipo de dato del método
vars_metodo = None              # Variables que pertenecen a la declaración del método
metodoActual = None             # Identificador del método sobre el que se está trabajando
inicioCuadruplo = None          # Número de cuádruplo en el cual inicia la ejecución del método
metodo_llamada = None           # Método al que se está realizando una llamada
ciclo_exp = None                # Expresión del ciclo
condicion_exp = None            # Expresión del condicional
saltos_ciclos = []              # Pila de saltos de los ciclo
saltos_condicion = []           # Pila de saltos en las condiciones
tiene_return = False            # Controlador para saber si la función tiene un estatuto de retorno
tipo_ultima_expresion = None    # Tipo de la última expresión
saltos_return = []              # Pila de cuádruplos donde hay un return, para al final mandarlos al endproc
cuadruplo_main = None           # Número de cuádruplo donde está el endproc del main

###########################################################################
#   checkMetodos
#   Revisa si un identificador existe en el diccionario de métodos
###########################################################################
def checkMetodos(id):
    if id in diccionario_metodos:
        return True
    return False

###########################################################################
#   checkParametros
#   Revisa si el identificador existe en la lista de parámetros
###########################################################################
def checkParametros(id):
    if id in parametros:
        # Si existe el parámetro
        return True
    # El identificador no se ha utilizado
    return False

###########################################################################
#   resetVariablesLocales
#   Regresar los diccionarios de variables locales a como estaban en un comienzo
#   con el fin de reutilizar las direcciones
###########################################################################
def resetVariablesLocales():
    global locales_int_cont, locales_char_cont, locales_float_cont
    global locales_string_cont, locales_boolean_cont
    locales_int_cont = 1000
    locales_float_cont = 1200
    locales_char_cont = 1400
    locales_string_cont = 1600
    locales_boolean_cont = 1800
    locales_int.clear()
    locales_char.clear()
    locales_float.clear()
    locales_string.clear()
    locales_boolean.clear()

###########################################################################
#   checkDataType
#   Regresa el tipo de dato del valor recibido, es de acuerdo a la definición
#   de nuestro lenguaje
###########################################################################
def checkDataType(var):
    # Revisar si es un booleano
    if var == "true" or var == "false":
        return "boolean";
    else:
        # Revisar si es un tipo numérico
        datatype = type(var)
        if datatype == int:
            return "int"
        elif datatype == float:
            return "float"
        elif datatype == bool:
            return "boolean"
        else:
            # Las opciones restantes son char, string o variable
            if var <> None:
                # Revisar si es un char
                if len(var) == 3 and var[0] == '\'':
                    return "char"
                # Revisar si es un string
                elif var[0] == '"':
                    return "string"
                else:
                    # Regresar el nombre de la variable
                    return var
            else:
                return var

###########################################################################
#   getNumericalType
#   Regresa el código numérico del último tipo a analizar
###########################################################################
def getNumericalType(type):
    datatype = checkDataType(type)
    if datatype == "int":
        return INT
    elif datatype == "char":
        return CHAR
    elif datatype == "boolean":
        return BOOLEAN
    elif datatype == "float":
        return FLOAT
    elif datatype == "string":
        return STRING
    else:
        return type

###########################################################################
#   checkVariableGlobal
#   Revisar si un identificador ya existe en las variables globales declaradas
###########################################################################
def checkVariableGlobal(id):
    if id in globales_int:
        return True
    elif id in globales_float:
        return True
    elif id in globales_char:
        return True
    elif id in globales_string:
        return True
    elif id in globales_boolean:
        return True
    return False

###########################################################################
#   varGlobalDictionary
#   Revisar en que diccionario existe un identificador, dado que ya se conoce
#   que existe en las variables globales
###########################################################################
def varGlobalDictionary(id):
    if id in globales_int:
        return INT
    elif id in globales_float:
        return FLOAT
    elif id in globales_char:
        return CHAR
    elif id in globales_string:
        return STRING
    elif id in globales_boolean:
        return BOOLEAN

###########################################################################
#   addVariableGlobal
#   Añadir un identificador a los diccionarios globales de acuerdo a su tipo
###########################################################################
def addVariableGlobal(identificador, tipo):
    # Revisar si la variable ya había sido declarada con anterioridad
    if checkVariableGlobal(identificador) or checkMetodos(identificador):
        print "El identificador <<" + identificador + ">> ya había sido declarado como variable global"
        sys.exit()
    else:
        # Utilizar las variables globales que contienen los contadores
        global globales_int, globales_float, globales_char, globales_string, globales_boolean
        global globales_int_cont, globales_float_cont, globales_char_cont
        global globales_string_cont, globales_boolean_cont
        # Si no había sido declarada, añadirla a su diccionario de variables
        if tipo == INT:
            variable = {}
            # Asignar un valor temporal a la variable global
            # variable['valor'] = None
            variable['direccionMemoria'] = globales_int_cont
            globales_int[ identificador ] = variable.copy()
            globales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Asignar un valor temporal a la variable global
            # variable['valor'] = None
            variable['direccionMemoria'] = globales_float_cont
            globales_float[ identificador ] = variable.copy()
            globales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Asignar un valor temporal a la variable global
            # variable['valor'] = None
            variable['direccionMemoria'] = globales_char_cont
            globales_char[ identificador ] = variable.copy()
            globales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Asignar un valor temporal a la variable global
            # variable['valor'] = None
            variable['direccionMemoria'] = globales_string_cont
            globales_string[ identificador ] = variable.copy()
            globales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Asignar un valor temporal a la variable global
            # variable['valor'] = None
            variable['direccionMemoria'] = globales_boolean_cont
            globales_boolean[ identificador ] = variable.copy()
            globales_boolean_cont +=1

###########################################################################
#   addVariableLocal
#   Añadir una variable local al diccionario dependiendo de su tipo, y a una
#   una lista de parámetros que será asignada al método
###########################################################################
def addVariableLocal(id, tipo, posicion, largo):
    # Revisar si el nombre de la variable existe en los parámetros o en los método
    if checkParametros(id) or checkMetodos(id):
        print "El identificador <<" + id + ">> ya está en uso."
        sys.exit()
    else:
        # Especificar al programa que serán modificados los contadores
        global locales_int_cont, locales_float_cont, locales_char_cont
        global locales_string_cont, locales_boolean_cont
        # Añadir a las variables locales
        if tipo == INT:
            variable = {}
            # Asignar el valor de la variable como nulo
            # variable['valor'] = None
            variable['direccionMemoria'] = locales_int_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            variable['tam'] = largo
            parametros[ id ] = variable
            locales_int[ id ] = variable
            locales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Asignar el valor de la variable como nulo
            # variable['valor'] = None
            variable['direccionMemoria'] = locales_float_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            variable['tam'] = largo
            parametros[ id ] = variable
            locales_float[ id ] = variable
            locales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Asignar el valor de la variable como nulo
            # variable['valor'] = None
            variable['direccionMemoria'] = locales_char_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            variable['tam'] = largo
            parametros[ id ] = variable
            locales_char[ id ] = variable
            locales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Asignar el valor de la variable como nulo
            # variable['valor'] = None
            variable['direccionMemoria'] = locales_string_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            variable['tam'] = largo
            parametros[ id ] = variable
            locales_string[ id ] = variable
            locales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Asignar el valor de la variable como nulo
            # variable['valor'] = None
            variable['direccionMemoria'] = locales_boolean_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            variable['tam'] = largo
            parametros[ id ] = variable
            locales_boolean[ id ] = variable
            locales_boolean_cont += 1

###########################################################################
#   addGlobalVars
#   Añadir una variable global a la lista
###########################################################################
def addGlobalVars(lista):
    # Revisar que existan variables globales
    if lista != None:
        for declaracion in lista:
            # Ciclo para leer los identificadores, estos se encuentran
            # a partir del segundo elemento (casilla 1)
            for i in range(1, len(declaracion)):
                # Añadir variable global
                addVariableGlobal(declaracion[i], declaracion[0])

###########################################################################
#   p_programa
#   Regla para la especificación del programa
###########################################################################
def p_programa(p):
    '''programa : goto_main add_globales metodos'''
    # Como este código se ejecuta hasta el final del método, se muestra que
    # el procedimiento ha finalizado
    # Generación del método intermedio
    quad = []
    quad.append("END")
    quad.append(None)
    quad.append(None)
    quad.append(None)
    # Añadir el cuádruplo recién generado a la lista de cuádruplos totales
    lista_cuadruplos.append(quad)
    # Añadir al endproc del main, el salto hasta el END que indica el final de la ejecución
    lista_cuadruplos[cuadruplo_main-1][1] = len(lista_cuadruplos)

###########################################################################
#   p_goto_main
#   Regla que sirve para aclarar que el primer método de la función debe
#    contener su nombre
###########################################################################
def p_goto_main(p):
    '''goto_main :'''
    # Apuntar hacia el siguiente cuádruplo después de la ejecución del primero
    quad = []
    quad.append("GOTO")
    quad.append(None)
    quad.append(None)
    quad.append("MAIN")
    # Añadir el cuádruplo recién generado a la lista de todos los cuádruplos
    lista_cuadruplos.append(quad)

###########################################################################
#   p_add_globales
#   Añadir una lista de variables globales
###########################################################################
def p_add_globales(p):
    '''add_globales : variables_list'''
    # Retornar al método de programa, la cantidad con las variabless
    p[0] = p[1]
    addGlobalVars(p[1])

###########################################################################
#   p_variables_list
#   Revisar cuales son las variables recibidas
###########################################################################
def p_variables_list(p):
    '''variables_list : variables_list variables
        | empty'''
    # Revisar que no esté vacío
    if len(p) == 3:
        variables = []
        if p[1] == None:
            variables.append(p[2])
        else:
            p[1].append(p[2])
            variables = p[1]
        # Utilizar la lista de variables como una especia de retorno
        p[0] = variables

###########################################################################
#   p_variables
#   Añadir una variable local al diccionario dependiendo de su tipo, y a una
###########################################################################
def p_variables(p):
    '''variables : VAR tipo ID lista_variables SEMICOLON
        | VAR tipo ID LEFTSB INT_CTE RIGHTSB lista_variables SEMICOLON'''
    # Recibir las variables cuando hay una lista, parte sin arreglos
    if len(p) == 6:
        if p[4] != None:
            vars = []
            vars.append(p[2])
            vars.append(p[3])
            vars = vars + p[4]
            p[0] = vars
        else:
            vars = []
            vars.append(p[2])
            vars.append(p[3])
            p[0] = vars
    else:
        if p[7] != None:
            vars = []
            vars.append(p[2])
            vars.append(p[3])
            vars.append(p[5])
            vars = vars + p[7]
            p[0] = vars
        else:
            vars = []
            vars.append(p[2])
            vars.append(p[3])
            vars.append(p[5])
            p[0] = vars

###########################################################################
#   p_lista_variables
#   Método que revisa si existe más de una variable declarada en la lista
###########################################################################
def p_lista_variables(p):
    '''lista_variables : COMMA ID lista_variables
        | COMMA ID LEFTSB INT_CTE RIGHTSB lista_variables
        | empty'''
    # Revisar que sea un identificador
    if len(p) == 4:
        vars = []
        vars.append( p[2] )
        if p[3] != None:
            p[0] = vars + p[3]
        else:
            p[0] = vars
    elif len(p) > 4:
        vars = []
        vars.append( p[2] )
        vars.append(p[4])
        if p[6] != None:
            p[0] = vars + p[6]
        else:
            p[0] = vars

###########################################################################
#   p_metodos
#   Función que revisa si existen métodos
###########################################################################
def p_metodos(p):
    '''metodos : metodos metodo
        | empty'''
    # Revisar que se cumpla la primer regla, la cual implica que hay métodos
    if len(p) == 3:
        # Revisar si hay métodos previos ya observados
        aux = []
        aux.append(p[2])
        if p[1] <> None:
            p[0] = p[1] + aux
        else:
            p[0] = aux

tipo_retorno = None
###########################################################################
#   p_metodo
#   Regla que obtiene toda la estructura de un método declarado
###########################################################################
def p_metodo(p):
    '''metodo : inicio_method METHOD tipo_metodo metodo1 LEFTP save_params RIGHTP LEFTB method_vars add_method bloque RIGHTB end_method'''
    global metodoActual, contTemp, params_metodo, tipo_metodo, vars_metodo, inicioCuadruplo, tiene_return, tipo_retorno
    if tipo_metodo <> "void":
        if not(tiene_return):
            print metodoActual + ": No existe un valor de retorno."
            sys.exit()
    # Como ya se ha obtenido toda la información sobre el método,
    # resetea todas las variables utilizadas para futuras declaraciones
    param_len = 0               # Regresar el contador de parámetros
    resetVariablesLocales()     # Limpiar todos los diccionarios de variables locales
    parametros.clear()          # Limpiar el diccionario de parámetros
    #contTemp = 2000             # Reiniciar el contador de temporales
    # Limpiar las variables del método
    tiene_return = False
    metodoActual = None
    params_metodo = None
    tipo_metodo = None
    vars_metodo = None
    inicioCuadruplo = None
    tipo_retorno = None

###########################################################################
#   p_inicio_method
#   Regla que obtiene el cuádruplo en el que comienza el método
###########################################################################
def p_inicio_method(p):
    '''inicio_method : '''
    global inicioCuadruplo
    # Se suma uno porque se considera antes de cualquier expresión en el método
    inicioCuadruplo = len(lista_cuadruplos) + 1

###########################################################################
#   p_end_method
#   Escribir el último cuádruplo del método
###########################################################################
def p_end_method(p):
    '''end_method : '''
    # Revisar si se ha utilizado el return si el método tiene algún tipo
    # Generación del cuádruplo de fin del método

    # Apuntar todos los return al endproc, se guarda en la casilla 1 del cuádruplo
    while len(saltos_return) <> 0:
        salto = saltos_return.pop()
        # print lista_cuadruplos[salto-1][3]
        lista_cuadruplos[salto-1][1] = len(lista_cuadruplos) + 1
        # lista_cuadruplos[saltos_return.pop()][3] = len(lista_cuadruplos)

    # Revisar si el método actual es el main
    if metodoActual == "main":
        global cuadruplo_main
        cuadruplo_main =  len(lista_cuadruplos) + 1


    quad = []
    quad.append('ENDPROC')
    quad.append(None)
    quad.append(None)
    quad.append(metodoActual)
    # Añadir el cuádruplo a la lista
    lista_cuadruplos.append(quad)

###########################################################################
#   p_metodo1
#   Obtener el identificador del método
###########################################################################
def p_metodo1(p):
    '''metodo1 : MAIN
        | ID'''
    # Actualizar la variable global metodoActual, para que todas las demás funciones
    # consideren en que contexto se encuentran
    global metodoActual
    metodoActual = p[1]
    # Si el identificador de la función es main, entonces se actualiza el primer
    # cuádruplo para realizar el salto en máquina virtual
    if metodoActual == "main":
        lista_cuadruplos[0][3] = len(lista_cuadruplos) + 1
    # Regresar el identificador a la regla de declaración de método
    p[0] = p[1]

###########################################################################
#   p_save_params
#   Revisar los parámetros que recibe un método, esta función sirve como
#   intermediaria para poder guardarlos antes de que termine la regla principal
#   del método
###########################################################################
def p_save_params(p):
    '''save_params : params'''
    global params_metodo
    # Revisar que la función contenga parámetros
    if p[1] <> None:
        params_metodo = p[1]
    p[0] = p[1]

###########################################################################
#   p_tipo_metodo
#   Obtener que tipo de dato retorna la función en declaración
###########################################################################
def p_tipo_metodo(p):
    '''tipo_metodo : VOID
        | tipo'''
    # Guardar el tipo en una variable global para poder añadirla al diccionario
    global tipo_metodo
    tipo_metodo = p[1]
    p[0] = p[1]

###########################################################################
#   p_add_method
#   Añadir la información del método a un diccionario para poder mantener
#   un control sobre todos los que se han declarado
###########################################################################
def p_add_method(p):
    '''add_method : '''
    # Revisar que existan parámetros en el método
    if params_metodo != None:
        # Posición en la que se recibirá el parámetro
        posicion = 1
        # Para cada uno de los parámetros, añadirlo como si fuera una variable local
        for parametro in params_metodo:
            # A partir del segundo elemento (casilla 1, pues el primero tiene el id)
            addVariableLocal(parametro[1], parametro[0], posicion, 0)
            posicion += 1
        # Escribir la cantidad de parámetros que fueron añadidos
        param_len =  len(params_metodo)
    else:
        # No contiene parámetros
        param_len = 0
    # Revisar si el método tiene declaración de variables locales
    if vars_metodo != None:
        # Para cada una de las listas de variables que fueron declaradas
        for variable in vars_metodo:
            # Añadir la variable a la lista de variables locales, se realiza la
            # a partir de la posición 1 porque la posición 0 contiene el tipo
            for i in range(1, len(variable)):
                # print(variable[i])
                if isinstance(variable[i], str):
                    largo = 0
                    if len(variable) > i + 1 and isinstance(variable[i + 1], int):
                        largo = variable[i + 1]
                    addVariableLocal(variable[i], variable[0], 0, largo)
    # Revisar si el identificador del método ya había sido utilizado como nombre
    # de otro método o como variable global
    if ( checkMetodos(metodoActual) or checkVariableGlobal(metodoActual) ):
        print "El identificador " + metodoActual + " ya está en uso."
        sys.exit()
    else:
        # Creación de un diccionario para mantener los datos del método, y
        # posteriormente añadirlo a la lista
        full_method = {}
        met = {}
        # Guardar el tipo de dato que retorna el método
        met['tipo'] = tipo_metodo
        # Guardar el diccionario de variables locales
        # Parámetros contiene también las declaradas
        met['vars'] = parametros.copy()
        # Guardar la cantidad de parámetros que recibe el método
        met['param_len'] = param_len
        # Guardar el número de cuádruplo en el que comienzan las operaciones
        met['cuadruplo_inicio'] = inicioCuadruplo - 1
        # Guardar el metodo en la lista de diccionarios
        diccionario_metodos[metodoActual] = met.copy()
        # Regresar la declaración del método a la regla inicial
        p[0] = full_method.copy()

###########################################################################
#   p_method_vars
#   Obtener las declaraciones de métodos que se realizaron para variables locales
###########################################################################
def p_method_vars(p):
    '''method_vars : variables_list'''
    # Guardarlo para el método que guarda las variables
    global vars_metodo
    vars_metodo = p[1]
    p[0] = p[1]

###########################################################################
#   p_params
#   Parámetros que recibe el método que se está declarando
###########################################################################
def p_params(p):
    '''params : params parametro
        | params COMMA parametro
        | empty'''
    # Revisar la longitud de la regla para al final contener una lista que contenga
    # todos los parámetros
    if len(p) == 3:
        if p[1] <> None:
            p[0] = p[1]
        else:
            p[0] = []
        p[0].append( p[2] )
    elif len(p) == 4:
        if p[1] <> None:
            p[0] = p[1]
        else:
            p[0] = []
        p[0].append( p[3] )

###########################################################################
#   p_parametro
#   Obtener el tipo e identificador de cada parámetro
###########################################################################
def p_parametro(p):
    '''parametro : tipo ID'''
    # Regresarlos como una lista en el cual primero se tiene el tipo, y
    # después el identificador
    p[0] = []
    p[0].append(p[1])
    p[0].append(p[2])

###########################################################################
#   p_bloque
#   Lista de estatutos que puede utilizar el método
###########################################################################
def p_bloque(p):
    '''bloque : bloque estatuto
        | empty'''

###########################################################################
#   p_estatuto
#   Tipos de estatutos que pueden utilizar los métodos
###########################################################################
def p_estatuto(p):
    '''estatuto : condicion
        | ciclo
        | return
        | lectura
        | escritura
        | llamada SEMICOLON
        | asignacion
        '''

###########################################################################
#   p_return
#   Regla para cuando el estatuto es retorno
###########################################################################
def p_return(p):
    '''return : RETURN return1 SEMICOLON'''
    # Su principal acción es llamar a la regla return1 que guarda el cuádruplo
    # La función si tiene valor de retorno
    global tiene_return
    tiene_return = True

###########################################################################
#   p_return1
#   Generación del cuádruplo para el estatuto de retorno
###########################################################################
def p_return1(p):
    '''return1 : exp'''
    # Revisar el tipo de expresión, puede ser una expresión como tal o una llamada
    global tipo_exp, tipo_retorno, saltos_return
    # Añadir el número de este cuádruplo a la pila de retornos
    saltos_return.append(len(lista_cuadruplos) + 1)
    # Generación del cuádruplo de return
    quad = []
    quad.append("RETURN")
    quad.append(None)
    quad.append(None)
    # Revisar que sea una expresión
    if tipo_exp == 1:
        # Revisar si la expresión es una asignación directa
        if solo_una_expresion:
            # print p[1]
            # quad.append(p[1])
            datatype = checkDataType(p[1])
            # Utilizar una variable para obtener el identificador numérico
            # Revisar los rangos de las variables
            num_datatype = None
            if p[1] in range(3000, 3200):
                num_datatype = INT
            elif p[1] in range(3200, 3400):
                num_datatype = FLOAT
            elif p[1] in range(3400, 3600):
                num_datatype = CHAR
            elif p[1] in range(3600, 3800):
                num_datatype = STRING
            elif p[1] in range(3800, 4000):
                num_datatype = BOOLEAN
            else:
                # Revisar en el diccionario de métodos que tipo corresponde a esta variable
                if p[1] in diccionario_metodos[metodoActual]['vars']:
                    num_datatype = diccionario_metodos[metodoActual]['vars'][p[1]]['type']
                    # print diccionario_metodos[metodoActual]['vars'][p[1]]
                    quad.append(diccionario_metodos[metodoActual]['vars'][p[1]]['direccionMemoria'])
                else:
                    # Revisar en el diccionario de variables globales
                    revisa_global = varGlobalDictionary(p[1])
                    if revisa_global in range(INT, BOOLEAN+1):
                        num_datatype = revisa_global
                    else:
                        print p[1] + "No se encuentra en las variables globales y locales"
            if len(quad) == 3:
                quad.append(p[1])
            tipo_retorno = num_datatype
        else:
            # Si la expresión es la última operación realizada, asignar
            # el último temporal que se realizó
            tipo_retorno = tipo_ultima_expresion
            quad.append(contTemp-1)
    else:
        # Si es una llamada, anexar el nombre
        quad.append("llamada")
    # Revisar si el método tiene un tipo, debe tener un return
    if tipo_retorno <> None:
        if tipo_retorno <> tipo_metodo:
            print metodoActual + ": El tipo de retorno no coincide con el tipo del método"
            sys.exit()
        else:
            # Tipo de retorno correcto
            pass
    else:
        if tiene_return:
            print metodoActual + ": Esta función no debería tener retorno."
            sys.exit()
    # Añadir el cuádruplo a la lista
    lista_cuadruplos.append(quad)

###########################################################################
#   p_lectura
#   Generación del cuádruplo de cuando es una lectura
###########################################################################
def p_lectura(p):
    '''lectura : ID ASSIGN READ LEFTP RIGHTP SEMICOLON'''
    # Notificar al programa que se puede hacer modificaciones a esas variables globales
    global globales_int, globales_float, globales_char, globales_string, globales_boolean
    # Dirección a la cual se guardará el valor leído
    direccionLectura = None
    # Revisar que exista el identificador como variable local en el método
    if p[1] in diccionario_metodos[metodoActual]['vars']:
        # Obtener la dirección de esa variable para poder guardarla
        direccionLectura = diccionario_metodos[metodoActual]['vars'][p[1]]['direccionMemoria']
        # Actualiar el valor de esa variable
        # diccionario_metodos[metodoActual]['vars'][p[1]]['valor'] = direccionLectura
    else:
        # Si no se encuentra, revisar si existe en las variables globales
        if checkVariableGlobal(p[1]):
            # Se encuentra en las variables globales, entonces revisar a que tipo pertenece
            tipo_global = varGlobalDictionary(p[1])
            # Revisar de que tipo es, cuando lo encuentre, buscar la variable en el diccionario
            # al que pertenece y obtener la dirección, después actualizar el valor
            if tipo_global == INT:
                direccionMemoria = globales_int[p[1]]["direccionMemoria"]
                # globales_int[p[1]]["valor"] = p[3]
            elif tipo_global == FLOAT:
                direccionMemoria = globales_float[p[1]]["direccionMemoria"]
                # globales_float[p[1]]["valor"] = p[3]
            elif tipo_global == CHAR:
                direccionMemoria = globales_char[p[1]]["direccionMemoria"]
                # globales_char[p[1]]["valor"] = p[3]
            elif tipo_global == STRING:
                direccionMemoria = globales_string[p[1]]["direccionMemoria"]
                # globales_string[p[1]]["valor"] = p[3]
            elif tipo_global == BOOLEAN:
                direccionMemoria = globales_boolean[p[1]]["direccionMemoria"]
                # globales_boolean[p[1]]["valor"] = p[3]
            direccionLectura = direccionMemoria
        else:
            # El identificador no se encuentra en las variables locales y globales
            print "Lectura: La variable <<" + p[1] + ">> no está declarada"
            sys.exit()
    # Generación del cuádruplo de lectura
    quad = []
    # Guardar el primer elemento como el nombre de la operación en mayúsculas
    quad.append(p[3].upper())
    # Utilizar x como el valor temporal leído
    x = 4
    quad.append(x)
    quad.append(None)
    quad.append(direccionLectura)
    # Añadir el cuádruplo a la lista
    lista_cuadruplos.append(quad)

###########################################################################
#   p_escritura
#   Generación del cuádruplo para imprimir en pantalla
###########################################################################
def p_escritura(p):
    '''escritura : PRINT LEFTP exp RIGHTP SEMICOLON'''
    # Generación del cuádruplo de escritura
    quad = []
    quad.append(p[1].upper())
    quad.append(None)
    quad.append(None)
    # Expresión que se desea imprimir, cambiar por la dirección
    direc = diccionario_metodos.get(metodoActual).get("vars").get(p[3])
    if(direc is None):
        direc = p[3]
    else:
        direc = direc.get('direccionMemoria')
    quad.append(direc)
    # Añadir a la lista de cuádruplos
    lista_cuadruplos.append(quad)

###########################################################################
#   p_llamada
#   Generación del cuádruplo para realizar una llamada
###########################################################################
def p_llamada(p):
    '''llamada : llamada1 LEFTP args RIGHTP'''
    global cont_args
    # Revisar si la llamada tiene argumentos
    if p[3] <> None:
        # Obtener la cantidad de parámetros
        call_len = len(p[3])
        # Cantidad de parámetros que espera el método
        cant = diccionario_metodos[p[1]]['param_len']
    else:
        # Como no tiene argumentos, establecerlo como 0
        call_len = 0
        # Cantidad de parámetros que espera el método
        cant = diccionario_metodos[p[1]]['param_len']
    # Comparar si los argumentos coincide con la cantidad de parámetros que espera el método
    if call_len == cant:
        # Generación del cuádruplo de GOSUB
        quad_gosub = []
        quad_gosub.append("GOSUB")
        # Cuádruplo del método al que se hará la llamada
        quad_gosub.append(diccionario_metodos[p[1]]['cuadruplo_inicio'])
        quad_gosub.append(None)
        quad_gosub.append(None)
        # Añadir a la lista de cuádruplos
        lista_cuadruplos.append(quad_gosub)
    else:
        # Si la cantidad no coincide mostrar un mensaje para notificar
        print "La cantidad de parámetros en la llamada <<" + p[1] + ">> no es compatible."
        print "Cantidad de parámetros esperados: " + str(cant)
        sys.exit()
    # Reiniciar las variables que fueron utilizadas para realizar la llamada
    metodo_llamada = None
    cont_args = 1

###########################################################################
#   p_llamada1
#   Obtener el identificador del método al cual se hará la llamada
###########################################################################
def p_llamada1(p):
    '''llamada1 : ID'''
    global metodo_llamada
    # Revisar que exista en la lista de método
    if not( checkMetodos(p[1]) ):
        print "El método <<" + p[1] + ">> no está definido."
        sys.exit()
    # Si esta, generar el cuádruplo para separar la memoria
    metodo_llamada = p[1]       # Reservar el nombre del método al que se hará la llamada
    quad_era = []
    quad_era.append("ERA")
    quad_era.append(p[1])       # Este elemento contiene el nombre del método
    quad_era.append(None)
    quad_era.append(None)
    # Añadir a la lista de métodos
    lista_cuadruplos.append(quad_era)
    # Retornar el identificador a la regla principal
    p[0] = p[1]

###########################################################################
#   revisaTipoParametro
#   Revisar que el tipo del parámetro coincida con lo esperado en el método
###########################################################################
def revisaTipoParametro(tipo, metodo):
    # Para cada una de las variables en la posición del método
    for var in diccionario_metodos[metodo]['vars']:
        # Buscar la posición del parámetro actual
        if diccionario_metodos[metodo]['vars'][var]['posicion'] == cont_args:
            # Obtener el tipo que existe en el diccionario
            tipo_parametro = diccionario_metodos[metodo]['vars'][var]['type']
            # Compararlo con el que se está enviando
            if tipo_parametro == tipo:
                pass
            else:
                print "Llamada a " + metodo + ": El parámetro #" + str(cont_args) + " tiene tipo incorrecto."
                print "El tipo esperado es " + str(tipo_parametro) + ", recibido " + str(tipo)
                sys.exit()

###########################################################################
#   p_args
#   Argumentos que serán enviados para realizar la llamada
###########################################################################
def p_args(p):
    '''args : exp
        | args COMMA exp
        | empty'''
    global cont_args
    # Revisar la longitud de la regla
    if len(p) == 4:
        # Revisar si existen más argumentos
        if p[1] <> None:
            p[0] = p[1]
        else:
            p[0] = []
        # Generación del cuádruplo PARAM
        quad_arg = []
        quad_arg.append("PARAM")
        # Revisar el tipo del parámetro
        if p[3] <> None:
            datatype = checkDataType(p[3])
            # Utilizar una variable para obtener el identificador numérico
            num_datatype = None
            if datatype == "int":
                num_datatype = INT
            elif datatype == "float":
                num_datatype = FLOAT
            elif datatype == "char":
                num_datatype = CHAR
            elif datatype == "string":
                num_datatype = STRING
            elif datatype == "boolean":
                num_datatype = BOOLEAN
            else:
                # Revisar en el diccionario de métodos que tipo corresponde a esta variable
                num_datatype = diccionario_metodos[metodoActual]['vars'][p[3]]['type']
            # Revisar que los tipos enviados y recibido coincidan
            revisaTipoParametro(num_datatype, metodo_llamada)
        else:
            # Obtener el tipo de método llamado
            tipo_llamada = diccionario_metodos[metodo_llamada]['tipo']
            # Si el tipo de método al que se llama es void, no tiene sentido la llamada
            if tipo_llamada == 'void':
                print "Argumento: No es posible utilizar el método <<" + metodo_llamada + ">> como argumento porque es de tipo void"
                sys.exit()
            else:
                # Revisar el tipo de dato de la llamada a realizar
                revisaTipoParametro( tipo_llamada, metodo_llamada )
        # Añadir la expresión como parámetro
        quad_arg.append(p[3])
        quad_arg.append(None)
        # Nombre del parámetro que se está enviando
        quad_arg.append("param" + str(cont_args))
        # Añadir el cuádruplo a la lista
        lista_cuadruplos.append(quad_arg)
        cont_args += 1                  # Incrementar el contador de argumento
        p[0].append(p[3])
    elif len(p) == 2:
        # En el caso de que sólo se contenga un argumento, revisar si es una expresión
        # o una llamada
        if p[1] <> None:
            p[0] = []
            p[0].append(p[1])
            quad_arg = []
            quad_arg.append("PARAM")
            # Revisar el tipo de parámetro
            if p[1] <> None:
                datatype = checkDataType(p[1])
                num_datatype = None
                if datatype == "int":
                    num_datatype = INT
                elif datatype == "float":
                    num_datatype = FLOAT
                elif datatype == "char":
                    num_datatype = CHAR
                elif datatype == "string":
                    num_datatype = STRING
                elif datatype == "boolean":
                    num_datatype = BOOLEAN
                else:
                    # Revisar el diccionario para obtener el tipo de dato del método
                    num_datatype =  diccionario_metodos[metodoActual]['vars'][p[1]]['type']
                # Revisar que los tipos de datos enviado y recibido coincidan
                revisaTipoParametro( num_datatype, metodo_llamada )
            else:
                # Obtener el tipo de método llamado
                tipo_llamada = diccionario_metodos[metodo_llamada]['tipo']
                # Revisar que no sea void
                if tipo_llamada == 'void':
                    print "Argumento: No es posible utilizar el método <<" + metodo_llamada + ">> como argumento porque es de tipo void"
                    sys.exit()
                else:
                    # Revisar que los tipos coincidan
                    revisaTipoParametro( tipo_llamada, metodo_llamada )
            # Corregir para cuando es negativo el valor
            if(diccionario_metodos[metodoActual]['vars'].has_key(p[1])):
                direc = diccionario_metodos[metodoActual]['vars'].get(p[1]).get("direccionMemoria")
            else:
                direc = p[1]
            quad_arg.append(direc)       # Guardar la expresión
            quad_arg.append(None)
            # Nombre del parámetro que se está enviando
            quad_arg.append("param" + str(cont_args))
            # Añadir el cuádruplo a la lista
            lista_cuadruplos.append(quad_arg)
            # Incrementar el contador de argumentos
            cont_args += 1


posicion_arreglo = None
id_arreglo = None
direccionArreglo = None
tempResAsign = None
expEsArr = None
###########################################################################
#   p_asignacion
#   Regla de estatuto de asignación
###########################################################################
def p_asignacion(p):
    '''asignacion : ID ASSIGN exp SEMICOLON
        | asignacion_id LEFTSB asignacion1 asignacion_inter asignacion2 RIGHTSB ASSIGN exp SEMICOLON'''
    # Diccionarios globales que pueden modificarse durante la asignación
    global diccionario_metodos, solo_una_expresion, posicion_arreglo, id_arreglo, direccionArreglo, expEsArr
    global globales_int, globales_float, globales_char, globales_string, globales_boolean, tempResAsign
    # Variable de dirección de memoria en la cual se guardará el valor
    direccionAsignacion = None
    # Revisar que la variable exista en el diccionario de método
    if p[1] in diccionario_metodos[metodoActual]['vars']:
        # Obtener la dirección a la cual se asignará
        direccionAsignacion = diccionario_metodos[metodoActual]['vars'][p[1]]['direccionMemoria']
        # Asignar el valor a esa variable
        # diccionario_metodos[metodoActual]['vars'][p[1]]['valor'] = p[3]
    else:
        # Revisar si es una variable global en la que se asignará
        if checkVariableGlobal(p[1]):
            # Obtener el tipo de la variable global
            tipo_global = varGlobalDictionary(p[1])
            # Obtener la dirección en la que se guardará y guardar la expresión
            if tipo_global == INT:
                direccionAsignacion = globales_int[p[1]]["direccionMemoria"]
                # globales_int[p[1]]["valor"] = p[3]
            elif tipo_global == FLOAT:
                direccionAsignacion = globales_float[p[1]]["direccionMemoria"]
                # globales_float[p[1]]["valor"] = p[3]
            elif tipo_global == CHAR:
                direccionAsignacion = globales_char[p[1]]["direccionMemoria"]
                # globales_char[p[1]]["valor"] = p[3]
            elif tipo_global == STRING:
                direccionAsignacion = globales_string[p[1]]["direccionMemoria"]
                # globales_string[p[1]]["valor"] = p[3]
            elif tipo_global == BOOLEAN:
                direccionAsignacion = globales_boolean[p[1]]["direccionMemoria"]
                # globales_boolean[p[1]]["valor"] = p[3]
            direccionAsignacion = direccionAsignacion
        else:
            # La variable no se encuentra como local o global
            print "Asignación: La variable <<" + p[1] + ">> no está declarada"
            sys.exit()
    # Asignación a una variable no dimensionada
    if len(p) == 5:
        quad = []
        quad.append(p[2])
        # Revisar si una expresión es directa o son operaciones
        if solo_una_expresion == True:
            # Obtener el tipo de la expresión a guardar
            tipo1 = getNumericalType(p[3])
            # Rango del 0 al 4 que representan los tipos de datos
            rangoTipos = range(0, 5)
            # Si en tipo1 y tipo2 no hay un número del 1 al 4, entonces es una variable
            if not( tipo1 in rangoTipos):
                # Revisar que tipo1 sea una variable global
                if tipo1 in diccionario_metodos[metodoActual]['vars']:
                    # Obtener el valor y modificar su valor
                    #valor = diccionario_metodos[metodoActual]['vars'][tipo1]['valor']
                    # diccionario_metodos[metodoActual]['vars'][p[1]]['valor'] = valor
                    # Añadir el valor al cuádruplo
                    # print tipo1
                    quad.append(diccionario_metodos[metodoActual]['vars'][tipo1]['direccionMemoria'])
                else:
                    # Revisar si se encuentra en las variables globales
                    if checkVariableGlobal(tipo1):
                        # Revisar a que diccionario corresponde
                        '''
                        if tipo_global == INT:
                            quad.append(globales_int[tipo1]['valor'])
                        elif tipo_global == FLOAT:
                            quad.append(globales_float[tipo1]['valor'])
                        elif tipo_global == CHAR:
                            quad.append( globales_char[tipo1]['valor'])
                        elif tipo_global == STRING:
                            quad.append( globales_string[tipo1]['valor'])
                        elif tipo_global == BOOLEAN:
                            quad.append(globales_boolean[tipo1]['valor'])'''
                        quad.append(6)
                    else:
                        # Revisar si el valor a asignar corresponde a una llamada
                        if tipo_exp == 0:
                            quad.append(metodo_llamada)
                        else:
                            print "Asignación: La variable <<" + str(tipo1) + ">> no se encuentra."
                            sys.exit()
            else:
                # Si es de tipo común, guardarlo
                quad.append(p[3])
        # Si no fue sólo una expresión
        else:
            # Revisar si fue una llamada
            if tipo_exp == 0:
                quad.append("llamada")
            else:
                # Si fue una operación, asignar el último temporal
                quad.append(contTemp-1)
        quad.append(None)
        # Dirección a la cual se asignará
        quad.append(direccionAsignacion)
        # Añadir el cuádruplo a la lista
        lista_cuadruplos.append(quad)
    else:
        # Generación del cuádruplo para asignación de arreglo
        quad = []
        quad.append(p[7])
        if solo_una_expresion:
            if expEsArr <> None:
                quad.append(expEsArr)
            else:
                quad.append(p[8])
            quad.append(None)
            quad.append(contTemp-1)
        else:
            quad.append(contTemp-1)
            quad.append(None)
            # Operacion
            quad.append(tempResAsign)
        lista_cuadruplos.append(quad)
        # print "Asignacion a variable dimensionada"
    # Establecer las variables como antes de la asignación
    solo_una_expresion = None
    posicion_arreglo = None
    id_arreglo = None
    direccionArreglo = None
    tempResAsign = None
    expEsArr = None

def p_asignacion_id(p):
    '''asignacion_id : ID'''
    global id_arreglo
    id_arreglo = p[1]
    p[0] = p[1]


def p_asignacion1(p):
    '''asignacion1 : '''
    # Generar cuádruplo para revisar que el identificador es de un arreglo
    global contTemp, lista_cuadruplos, direccionArreglo
    quad = []
    quad.append("VAL")
    dirArreglo = 0
    # Obtener el identificador del arreglo
    if id_arreglo in diccionario_metodos[metodoActual]['vars']:
        dirArreglo = diccionario_metodos[metodoActual]['vars'][id_arreglo]['direccionMemoria']
    else:
        # Revisar en las globales
        if id_arreglo in globales_int:
            dirArreglo = globales_int[id_arreglo]['direccionMemoria']
        elif id_arreglo in globales_float:
            dirArreglo = globales_float[id_arreglo]['direccionMemoria']
        elif id_arreglo in globales_char:
            dirArreglo = globales_char[id_arreglo]['direccionMemoria']
        elif id_arreglo in globales_string:
            dirArreglo = globales_string[id_arreglo]['direccionMemoria']
        elif id_arreglo in globales_boolean:
            dirArreglo = globales_boolean[id_arreglo]['direccionMemoria']
        else:
            print str(id_arreglo) + ": no está declarada en las variables dimensionadas"
            sys.exit()
    quad.append(dirArreglo)
    direccionArreglo = dirArreglo
    quad.append(None)
    quad.append(contTemp)
    contTemp += 1
    lista_cuadruplos.append(quad)

def p_asignacion_inter(p):
    '''asignacion_inter : exp'''
    # Igualar los valores
    global posicion_arreglo
    posicion_arreglo = p[1]
    p[0] = p[1]

def p_asignacion2(p):
    '''asignacion2 : '''
    global contTemp, lista_cuadruplos, tempResAsign
    quad = []
    quad.append("VER")
    quad.append(direccionArreglo)
    quad.append(posicion_arreglo)
    quad.append(contTemp)
    contTemp += 1
    lista_cuadruplos.append(quad)

    quad = []
    quad.append("RES")
    quad.append(direccionArreglo)
    quad.append(contTemp-1)
    quad.append(contTemp)
    tempResAsign = contTemp
    contTemp += 1
    lista_cuadruplos.append(quad)


###########################################################################
#   p_ciclo
#   Función de la regla para cuando es un ciclo
###########################################################################
def p_ciclo(p):
    '''ciclo : WHILE salto_ciclo LEFTP exp ciclo1 RIGHTP LEFTB bloque ciclo2 RIGHTB'''
    # Revisar que la condición sea una expresión
    if p[3] <> None:
        global ciclo_exp
        ciclo_exp = p[3]

###########################################################################
#   p_salto_ciclo
#   Guardar donde el cuádruplo donde comienza la expresión
###########################################################################
def p_salto_ciclo(p):
    '''salto_ciclo : '''
    global saltos_ciclos
    saltos_ciclos.append( len(lista_cuadruplos))

###########################################################################
#   p_ciclo1
#   Generación del cuádruplo inicial del ciclo
###########################################################################
def p_ciclo1(p):
    'ciclo1 :'
    # Generación del cuádruplo inicial
    quad = []
    quad.append("GOTOFc")
    if ciclo_exp == None:
        quad.append(contTemp-1)
    else:
        quad.append(ciclo_exp)
    quad.append(None)
    # Realizar el salto al cuádruplo
    quad.append('x')
    # Añadir el cuádruplo a la lista
    lista_cuadruplos.append(quad)
    global saltos_ciclos
    saltos_ciclos.append( len(lista_cuadruplos) - 1)

cantidad_expresiones = 0
###########################################################################
#   p_ciclo2
#   Repetir las instrucciones del ciclo
###########################################################################
def p_ciclo2(p):
    'ciclo2 :'
    global lista_cuadruplos
    # Generación del cuádruplo del goto para volver a validar
    quad_goto = []
    quad_goto.append("GOTO")
    quad_goto.append(None)
    quad_goto.append(None)
    # Cuádruplo al que se hará el salto
    salto = saltos_ciclos.pop()
    salto_goto = saltos_ciclos.pop()
    quad_goto.append( salto_goto + 1 )
    lista_cuadruplos.append(quad_goto)
    # Cambiar el GOTOF
    # Aquí existe un cambio dependiendo de si tiene o no más de una expresión
    lista_cuadruplos[salto][3] = len(lista_cuadruplos) + 1

###########################################################################
#   p_condicion
#   Regla para las condicionales
###########################################################################
def p_condicion(p):
    '''condicion : IF LEFTP condicion1 RIGHTP condicion2 LEFTB bloque RIGHTB condicion3 condicion4
        | IF LEFTP condicion1 RIGHTP condicion2 LEFTB bloque RIGHTB condicion3 ELSE LEFTB bloque condicion4 RIGHTB'''

###########################################################################
#   p_condicion1
#   Obtener la expresión de la condición
###########################################################################
def p_condicion1(p):
    '''condicion1 : exp'''
    # Asignar el tipo de expresión que se hace
    global condicion_exp
    condicion_exp = p[1]

###########################################################################
#   p_condicion2
#   Generación del cuádruplo de GOTO en falso
###########################################################################
def p_condicion2(p):
    '''condicion2 : '''
    global condicion_exp
    quad = []
    quad.append("GOTOFi")
    # Revisar si hay sólo una expresión
    if solo_una_expresion:
        # Añadir la expresión si sólo es una
        datatype = type(condicion_exp)
        if datatype <> int:
            # Revisar la dirección de la variable en las variables locales
            if condicion_exp in diccionario_metodos[metodoActual]['vars']:
                quad.append( diccionario_metodos[metodoActual]['vars'][condicion_exp]['direccionMemoria'] )
            else:
                # Revisar en las variables globales (solo en boolean porque no puede pertenecer a otro tipo)
                if condicion_exp in globales_boolean:
                    quad.append(globales_boolean[condicion_exp]['direccionMemoria'])
                else:
                    print "No se encuentra el identificador " + condicion_exp
                    sys.exit()
        else:
            quad.append(condicion_exp)
        condicion_exp = None
    else:
        # Añadir el temporal
        quad.append(contTemp-1)
    quad.append(None)
    # Cuádruplo al que se saltará
    quad.append('x')
    # Añadir el cuádruplo a la lista
    lista_cuadruplos.append(quad)
    # Obtener el número de cuádruplo en el que se encuentra el GOTOF
    saltos_condicion.append( len(lista_cuadruplos) )
    # print "condicion2 " + str( len(lista_cuadruplos))

###########################################################################
#   p_condicion3
#   Generación del cuádruplo de GOTO cuando se termina de hacer la parte verdadera
###########################################################################
def p_condicion3(p):
    '''condicion3 : '''
    global lista_cuadruplos
    quad = []
    quad.append("GOTO")
    quad.append(None)
    quad.append(None)
    # Ir al final del else, en caso se existir
    quad.append("finalElse")
    lista_cuadruplos.append(quad)
    # Obtener el número de cuádruplo en el que se guarda el GOTO
    salto = saltos_condicion.pop()
    # Hacer el salto a la siguiente dirección después del GOTO
    lista_cuadruplos[salto-1][3] = len(lista_cuadruplos) + 1
    # Insertar en la pila el actual
    saltos_condicion.append(len(lista_cuadruplos))

###########################################################################
#   p_condicion4
#   Modificar el GOTO después de realizar la condición cuando es verdadera
###########################################################################
def p_condicion4(p):
    '''condicion4 : '''
    global lista_cuadruplos
    salto = saltos_condicion.pop()
    lista_cuadruplos[salto-1][3] = len(lista_cuadruplos) + 1


###########################################################################
#   p_exp
#   Revisar el tipo de expresión que se hace, si es llamada u operación
###########################################################################
def p_exp(p):
    '''exp : llamada exp1
        | expresion exp2'''
    global cantidad_expresiones
    cantidad_expresiones += 1
    # Si p[1] es None, entonces es una llamada
    if p[1] <> None:
        p[0] = p[1]

###########################################################################
#   p_exp1
#   Regresar que el tipo de expresión es una llamada
###########################################################################
def p_exp1(p):
    '''exp1 : '''
    global tipo_exp
    tipo_exp = 0

###########################################################################
#   p_exp2
#   Regresar que el tipo de expresión es una operación
###########################################################################
def p_exp2(p):
    '''exp2 : '''
    global tipo_exp
    tipo_exp = 1


direccion = None
###########################################################################
#   p_expresion
#   Operaciones que se pueden realizar
###########################################################################
def p_expresion(p):
    '''expresion : expresion TIMES expresion
        | expresion DIVISION expresion
        | expresion SUM expresion
        | expresion LESS expresion
        | expresion EQUALS expresion
        | expresion NOTEQUAL expresion
        | expresion GREATEREQUAL expresion
        | expresion GREATERTHAN expresion
        | expresion LESSTHAN expresion
        | expresion LESSEQUAL expresion
        | expresion AND expresion
        | expresion OR expresion'''
    global contTemp, solo_una_expresion, tipo_ultima_expresion
    # La expresión ya no es un sólo término
    solo_una_expresion = False
    # Obtener el tipo del primer término
    tipo1 = getNumericalType(p[1])
    # Obtener el tipo del segundo término
    tipo2 = getNumericalType(p[3])
    # Variable para controlar los rangos a los que pertenecen los tipos de datos
    rangoTipos = range(0, 5)
    # Si en tipo1 y tipo2 no hay un número del 1 al 4, entonces es una variable
    # Buscar el tipo1 en las variables locales y después en las globales
    if not( tipo1 in rangoTipos):
        # print "tipo1 " +  str(tipo1)
        # Revisar en las variables locales
        if p[1] in diccionario_metodos[metodoActual]['vars']:
            if diccionario_metodos[metodoActual]['vars'][p[1]]['tam'] == 0:
                p[1] = diccionario_metodos[metodoActual]['vars'][p[1]]['direccionMemoria']
                tipo1 = getNumericalType(p[1])
            else:
                # print "es un arreglo"
                p[1] = diccionario_metodos[metodoActual]['vars'][p[1]]['direccionMemoria']
                tipo1 = getNumericalType(p[1])
        else:
            # Revisar en las variables globales
            if checkVariableGlobal(p[1]):
                tipo_global = varGlobalDictionary(tipo1)
                '''
                if tipo_global == INT:
                    p[1] = globales_int[p[1]]['valor']
                elif tipo_global == FLOAT:
                    p[1] = globales_float[p[1]]['valor']
                elif tipo_global == CHAR:
                    p[1] = globales_char[p[1]]['valor']
                elif tipo_global == STRING:
                    p[1] = globales_string[p[1]]['valor']
                elif tipo_global == BOOLEAN:
                    p[1] = globales_boolean[p[1]]['valor']'''
                tipo1 = tipo_global
            else:
                # La variable no existe en las locales y globales
                print metodoActual + ": La variable <<" + str(tipo1) + ">> no se encuentra."
                sys.exit()
    # Realizar el mismo procedimiento para el tipo del segundo término
    if not( tipo2 in rangoTipos):
        # print "tipo1 " +  str(tipo1)
        if p[3] in diccionario_metodos[metodoActual]['vars']:
            if diccionario_metodos[metodoActual]['vars'][p[3]]['tam'] == 0:
                p[3] = diccionario_metodos[metodoActual]['vars'][p[3]]['direccionMemoria']
                tipo2 = getNumericalType(p[3])
            else:
                # print "es un arreglo"
                p[3] = diccionario_metodos[metodoActual]['vars'][p[3]]['direccionMemoria']
                tipo2 = getNumericalType(p[3])
        else:
            if checkVariableGlobal(tipo2):
                tipo_global = varGlobalDictionary(tipo2)
                '''if tipo_global == INT:
                    p[3] = globales_int[tipo2]['valor']
                elif tipo_global == FLOAT:
                    p[3] = globales_float[tipo2]['valor']
                elif tipo_global == CHAR:
                    p[3] = globales_char[tipo2]['valor']
                elif tipo_global == STRING:
                    p[3] = globales_string[tipo2]['valor']
                elif tipo_global == BOOLEAN:
                    p[3] = globales_boolean[tipo2]['valor']'''
                tipo2 = tipo_global
            else:
                # La variable no se encuentra en el método y en las globales
                print metodoActual + ": La variable <<" + str(tipo1) + ">> no se encuentra."
                sys.exit()

    if p[3] in range(3800, 4000):
        tipo2 = 4
    # print tipo1, tipo2
    # Obtener el tipo de dato resultante
    tipoResultante = resultante( tipo1 , tipo2 , getNumTypeOperation(p[2]))
    tipo_ultima_expresion = tipoResultante
    # Revisar que la operación sea posible de realizar
    if resultante( tipo1 , tipo2 , getNumTypeOperation(p[2])) == ERROR:
        print "No es posible realizar la operación " + p[2] + " a los operadores " + str(p[1]) + ", " + str(p[3])
        sys.exit()
    else:
        # Generar el cuádruplo de la expresión
        quad_exp = []
        quad_exp.append(p[2])           # Operación que se realizará
        # Revisar si se toma como expresión el último temporal

        if p[1] > 4000:
            quad_exp.append(contTemp-1)     # Primer término
        else:
            quad_exp.append(p[1])           # Primer término
        # Revisar si se toma como expresión el último temporal
        if p[3] > 4000:
            quad_exp.append(contTemp-1)     # Segundo término
        else:
            quad_exp.append(p[3])           # Segundo término
        quad_exp.append(contTemp)       # Guardarlo en un temporal
        contTemp = contTemp + 1         # Aumentar el contador de temporales
        # Añadir el cuádruplo a la lista
        lista_cuadruplos.append(quad_exp)
    # Revisar cual es la operación que se hará
'''
    if p[2] == '*':
        p[0] = p[1] * p[3]
    elif p[2] == '/':
        p[0] = p[1] / p[3]
    elif p[2] == '+':
        p[0] = p[1] + p[3]
    elif p[2] == '-':
        p[0] = p[1] - p[3]
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == '!=':
        p[0] = p[1] <> p[3]
    elif p[2] == '>=':
        p[0] = p[1] >= p[3]
    elif p[2] == '>':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '&&':
        #  Convertir los términos a booleanos
        if tipo1 == 4 and tipo2 == 4:
            # Convertirlos a booleanos
            if p[1] == "true":
                p[1] = True
            else:
                p[1] = False
            if p[3] == "true":
                p[3] = True
            else:
                p[3] = False
            p[0] = p[1] and p[3]
        else:
            print "No es posible realizar la operación " + p[2] + " a los operadores " + str(p[1]) + ", " + str(p[3])
            sys.exit()
    elif p[2] == '||':
        # Convertir los términos a booleano
        if tipo1 == 4 and tipo2 == 4:
            # Convertirlos a booleanos
            if p[1] == "true":
                p[1] = True
            else:
                p[1] = False
            if p[3] == "true":
                p[3] = True
            else:
                p[3] = False
            p[0] = p[1] and p[3]
        else:
            # SI no es posible realizar la operación
            print "No es posible realizar la operación " + p[2] + " a los operadores " + str(p[1]) + ", " + str(p[3])
            sys.exit()'''
    # Añadir al diccionario de temporales
    #addVariableTemporal( tipoResultante, p[0] )

###########################################################################
#   p_expresion2
#   Término que puede utilizarse para las expresiones
###########################################################################
def p_expresion2(p):
    '''expresion : constante conf
        | ID
        | ID LEFTSB exp RIGHTSB
        | LEFTP expresion RIGHTP'''
    global solo_una_expresion, constantes_int, constantes_int_cont
    global constantes_float, constantes_float_cont, constantes_char, constantes_char_cont
    global constantes_string, constantes_string_cont, constantes_boolean, constantes_boolean_cont
    # Revisar si la longitud de la regla es de 2
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    if len(p) == 3:
        datatype = checkDataType(p[1])
        num_datatype = None
        if datatype == "int":
            constantes_int.append(p[1])
            p[0] = constantes_int_cont
            constantes_int_cont += 1
            num_datatype = INT
        elif datatype == "float":
            constantes_float.append(p[1])
            p[0] = constantes_float_cont
            constantes_float_cont += 1
            num_datatype = FLOAT
        elif datatype == "char":
            constantes_char.append(p[1])
            p[0] = constantes_char_cont
            constantes_char_cont += 1
            num_datatype = CHAR
        elif datatype == "string":
            constantes_string.append(p[1])
            p[0] = constantes_string_cont
            constantes_string_cont += 1
            num_datatype = STRING
        elif datatype == "boolean":
            constantes_boolean.append(p[1])
            p[0] = constantes_boolean_cont
            constantes_boolean_cont += 1
            num_datatype = BOOLEAN
        # print num_datatype
    if len(p) == 5:
        # Generar los cuadruplos para verificar
        global contTemp, lista_cuadruplos
        quad = []
        quad.append("VAL")
        id_arreglo = p[1]
        dirArreglo = 0
        # Obtener el identificador del arreglo
        if id_arreglo in diccionario_metodos[metodoActual]['vars']:
            dirArreglo = diccionario_metodos[metodoActual]['vars'][id_arreglo]['direccionMemoria']
        else:
            # Revisar en las globales
            if id_arreglo in globales_int:
                dirArreglo = globales_int[id_arreglo]['direccionMemoria']
            elif id_arreglo in globales_float:
                dirArreglo = globales_float[id_arreglo]['direccionMemoria']
            elif id_arreglo in globales_char:
                dirArreglo = globales_char[id_arreglo]['direccionMemoria']
            elif id_arreglo in globales_string:
                dirArreglo = globales_string[id_arreglo]['direccionMemoria']
            elif id_arreglo in globales_boolean:
                dirArreglo = globales_boolean[id_arreglo]['direccionMemoria']
            else:
                print "No está declarada en las variables dimensionadas"
                sys.exit()
        quad.append(dirArreglo)
        quad.append(None)
        quad.append(contTemp)
        contTemp += 1
        lista_cuadruplos.append(quad)

        quad = []
        quad.append("VER")
        quad.append(dirArreglo)
        quad.append(p[3])
        quad.append(contTemp)
        global expEsArr
        expEsArr = contTemp - 2
        # print contTemp
        contTemp += 1
        lista_cuadruplos.append(quad)

        quad = []
        quad.append("RES")
        quad.append(dirArreglo)
        quad.append(contTemp-1)
        quad.append(contTemp)
        contTemp += 1
        lista_cuadruplos.append(quad)
        p[0] = contTemp-1


    # Hasta el momento, la expresión es sólo una
    solo_una_expresion = True

def p_conf(p):
    '''conf : '''
    p[0] = True

###########################################################################
#   p_tipo
#   Regla para los tipos de datos
###########################################################################
def p_tipo(p):
    '''tipo : INT
        | CHAR
        | BOOLEAN
        | FLOAT
        | STRING'''
    # Convertir el tipo de dato a número
    datatype = p[1]
    if datatype == "int":
        p[0] =  INT
    elif datatype == "char":
        p[0] = CHAR
    elif datatype == "boolean":
        p[0] = BOOLEAN
    elif datatype == "float":
        p[0] = FLOAT
    elif datatype == "string":
        p[0] = STRING
    else:
        p[0] = ERROR

###########################################################################
#   p_constante
#   Obtener constantes
###########################################################################
def p_constante(p):
    '''constante : FLOAT_CTE
        | INT_CTE
        | CHAR_CTE
        | STRING_CTE
        | TRUE
        | FALSE'''
    p[0] = p[1]

###########################################################################
#   p_empty
#   Regla para simular vacío
###########################################################################
def p_empty(p):
    'empty :'
    pass

###########################################################################
#   p_error
#   Si existe un error de gramática en la expresión
###########################################################################
def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
        sys.exit()
    else:
        print("Syntax error at EOF")

# Cargar el analizador sintáctico
yacc.yacc()

def getCuadruplos():
    # Leer el programa de un archivo
    data = open('Programas/Fibonnaci_Recursivo.eldi','r').read()
    t = yacc.parse(data)
    # Validar que el método main se encuentra en el diccionario métodos
    if not( checkMetodos("main") ):
        print "No se ha encontrado el método main"
        sys.exit()
    # print lista_cuadruplos
    return lista_cuadruplos

# Mostrar la lista de cuádruplos
contador = 1
for cuadruplo in getCuadruplos():
    print contador, " ", cuadruplo
    contador += 1
#print json.dumps(diccionario_metodos)

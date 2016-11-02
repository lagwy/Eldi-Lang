# -*- coding: utf-8 -*-
###########################################################################
#   Scanner.py
#   Análisis sintáctico para el lenguaje Eldi
#
#   @author Luis Angel Martinez
#   @author Daniel Garcia Mena
#   @date 12/10/2016
###########################################################################
import ply.yacc as yacc
import Scanner            # Importar el analizador léxico
from Cubo import *        # Importar los identificadores numéricos asignados
tokens = Scanner.tokens   # Lista de tokens
import sys

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
temporales_boolean_cont = 2800

# Variables constantes
constantes_int = {}
constantes_int_cont = 3000
constantes_float = {}
constantes_float_cont = 3200
constantes_char = {}
constantes_char_cont = 3400
constantes_string = {}
constantes_string_cont = 3600
constantes_boolean = {}
constantes_boolean_cont = 3800

# Diccionario de métodos
diccionario_metodos = {}

# Declaración de variables globales
state = 0
actualType = None
methodType = None
paramType = None
scope = None
parametros = {} # Diccionario de parámetros para cada método
cont_param = 0 # Contador de la cantidad de parámetros

###########################################################################
#   getNumericalType
#   Regresa el código numérico del último tipo a analizar
###########################################################################
def getNumericalType(type):
    if type == "int":
        return INT
    elif type == "char":
        return CHAR
    elif type == "boolean":
        return BOOLEAN
    elif type == "float":
        return FLOAT
    elif type == "string":
        return STRING
    else:
        return ERROR

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
#   checkParametros
#   Función para revisar si un identificador fue empleado anteriormente
#   para la lista de parámetros de ese método
###########################################################################
def checkParametros(id):
    if id in parametros:
        # Si existe el parámetro
        return True
    # El identificador no se ha utilizado
    return False

###########################################################################
#   addVariableLocal
#   Añadir una variable local al diccionario dependiendo de su tipo, y a una
#   una lista de parámetros que será asignada al método
###########################################################################
def addVariableLocal(id, tipo):
    if checkParametros(id):
        print "El identificador <<" + id + ">> ya es utilzado como parámetro en este método."
        sys.exit()
    else:
        global locales_int_cont, locales_float_cont, locales_char_cont
        global locales_string_cont, locales_boolean_cont
        # Añadir a las variables locales
        if tipo == INT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_int_cont
            variable['posicion'] = cont_param
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_int[ id ] = variable
            locales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_float_cont
            variable['posicion'] = cont_param
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_float[ id ] = variable
            locales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_char_cont
            variable['posicion'] = cont_param
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_char[ id ] = variable
            locales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_string_cont
            variable['posicion'] = cont_param
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_string[ id ] = variable
            locales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_boolean_cont
            variable['posicion'] = cont_param
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_boolean[ id ] = variable
            locales_boolean_cont += 1


###########################################################################
#   addVariableGlobal
#   Añadir una variable global al diccionario dependiendo de su tipo
###########################################################################
def addVariableGlobal(identificador, tipo):
    # Revisar si la variable ya había sido declarada con anterioridad
    if checkVariableGlobal(identificador):
        print "El identificador <<" + identificador + ">> ya había sido declarado."
        sys.exit()
    else:
        # Utilizar las variables globales que contienen los contadores
        global globales_int_cont, globales_float_cont, globales_char_cont
        global globales_string_cont, globales_boolean_cont
        # Si no había sido declarada, añadirla a su diccionario de variables
        if tipo == INT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_int_cont
            globales_int[ identificador ] = variable
            globales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_float_cont
            globales_float[ identificador ] = variable
            globales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_char_cont
            globales_char[ identificador ] = variable
            globales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_string_cont
            globales_string[ identificador ] = variable
            globales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_boolean_cont
            globales_boolean[ identificador ] = variable
            globales_boolean_cont +=1

def p_programa(p):
    '''programa : variables_list metodos'''

def p_variables_list(p):
    '''variables_list : variables_list variables
        | empty'''

def p_variables(p):
    '''variables : VAR tipo ID lista_variables SEMICOLON
        | VAR tipo ID LEFTSB INT_CTE RIGHTSB lista_variables SEMICOLON'''
    if  state == 0:
        # Agregar los identificadores a la lista
        addVariableGlobal(p[3], actualType)

def p_lista_variables(p):
    '''lista_variables : COMMA ID lista_variables
        | COMMA ID LEFTSB INT_CTE RIGHTSB lista_variables
        | empty'''
    if state == 0:
        if len(p) > 0:
            if len(p) != 2:
                # Agregar más identificadores del mismo tipo a los arreglos
                addVariableGlobal(p[2],actualType)

def p_metodos(p):
    '''metodos : metodos metodo
        | empty'''
    global state
    """ Mostrar las variables globales
    if state == 0:
        print globales_int
        print len(globales_int)
        print globales_float
        print len(globales_float)
        print globales_char
        print len(globales_char)
        print globales_string
        print len(globales_string)
        print globales_boolean
        print len(globales_boolean)
    """
    state = 1


def p_metodo(p):
    '''metodo : METHOD VOID MAIN LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD VOID ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD tipo ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB'''
    global state, actualType, methodType, parametros
    global locales_int_cont, locales_char_cont, locales_float_cont
    global locales_string_cont, locales_boolean_cont, cont_param
    var_metodo = {}
    if state == 1:
        if p[2] == None:
            # Quiere decir que el método tiene un tipo
            print str(methodType) + " " + p[3]
            var_metodo['tipoRetorno'] = methodType
            # Regresar el tipo de método a vacío por si existen más funciones
            methodType = None
            # Cambiar el estado a lectura de parámetros
            state = 2
        else:
            # La función es void
            print p[2] + " " + p[3]
            var_metodo['tipoRetorno'] = 5
            state = 2
    print parametros
    # Creación del método para guardarlo
    var_metodo['cantidadParametros'] = len(parametros)
    var_metodo['lineaComienzo'] = None # Temporalmente none
    var_metodo['parametrosMetodo'] = parametros.copy()
    var_metodo['size'] = None
    # Utilizar como llave el nombre de la función y guardar el método
    diccionario_metodos[ p[3] ] = var_metodo

    # Resetear las variables utilizadas para guardar los parámetros
    locales_int_cont = 1000
    locales_float_cont = 1200
    locales_char_cont = 1400
    locales_string_cont = 1600
    locales_boolean_cont = 1800
    cont_param = 0 # Resetear el contador de parámetros
    parametros.clear()
    # Imprimir el diccionario de métodos
    print "Diccionario de metodos"
    print diccionario_metodos
    print "Termina diccionario de metodos"


def p_params(p):
    '''params : params parametro
        | params COMMA parametro
        | empty'''

def p_parametro(p):
    '''parametro : tipo ID'''
    global parametros, cont_param
    # print str(paramType) + " " + p[2]
    addVariableLocal(p[2], paramType )
    cont_param += 1

def p_bloque(p):
    '''bloque : bloque estatuto
        | empty'''

def p_estatuto(p):
    '''estatuto : return
        | lectura
        | escritura
        | llamada SEMICOLON
        | asignacion
        | ciclo
        | condicion'''

def p_return(p):
    '''return : RETURN exp SEMICOLON'''

def p_lectura(p):
    '''lectura : ID ASSIGN READ LEFTP RIGHTP SEMICOLON'''

def p_escritura(p):
    '''escritura : PRINT LEFTP exp RIGHTP SEMICOLON'''

def p_llamada(p):
    '''llamada : ID LEFTP llamada_list RIGHTP'''

def p_llamada_list(p):
    '''llamada_list : llamada_list args
        | empty'''

def p_args(p):
    '''args : exp mas_args'''

def p_mas_args(p):
    '''mas_args : COMMA exp
        | empty'''

def p_asignacion(p):
    '''asignacion : ID ASSIGN exp SEMICOLON
        | ID LEFTSB exp RIGHTSB ASSIGN exp SEMICOLON'''

def p_ciclo(p):
    '''ciclo : WHILE LEFTP exp RIGHTP LEFTB bloque RIGHTB'''

def p_condicion(p):
    '''condicion : IF LEFTP exp RIGHTP LEFTB bloque RIGHTB
        | IF LEFTP exp RIGHTP LEFTB bloque RIGHTB ELSE LEFTB bloque RIGHTB'''

def p_exp(p):
    '''exp : llamada
        | expresion'''

def p_expresion(p):
    '''expresion : expresion1
        | expresion1 TIMES expresion
        | expresion1 DIVISION expresion'''

def p_expresion1(p):
    '''expresion1 : expresion2
        | expresion2 SUM expresion1
        | expresion2 LESS expresion1'''

def p_expresion2(p):
    '''expresion2 : expresion3
        | expresion3 EQUALS expresion2
        | expresion3 NOTEQUAL expresion2
        | expresion3 GREATEREQUAL expresion2
        | expresion3 GREATERTHAN expresion2
        | expresion3 LESSTHAN expresion2
        | expresion3 LESSEQUAL expresion2'''

def p_expresion3(p):
    '''expresion3 : expresion4
        | expresion4 AND expresion3
        | expresion4 OR expresion3'''

def p_expresion4(p):
    '''expresion4 : constante
        | ID
        | LEFTP expresion RIGHTP'''

def p_tipo(p):
    '''tipo : INT
        | CHAR
        | BOOLEAN
        | FLOAT
        | STRING'''
    global actualType, methodType, paramType
    if state == 0:
        actualType = getNumericalType(p[1])
    elif state == 1:
        # Si es diferente de vacío guardarlo
        if methodType == None:
            methodType = getNumericalType(p[1])
        else:
            paramType = getNumericalType(p[1])

def p_constante(p):
    '''constante : INT_CTE
        | FLOAT_CTE
        | CHAR_CTE
        | STRING_CTE
        | TRUE
        | FALSE'''

#VACIO
def p_empty(p):
    'empty :'
    pass

def p_error(p):
    if p:
        print("Syntax error at '%s'" % p.value)
        sys.exit()
    else:
        print("Syntax error at EOF")

yacc.yacc()

# Read program file
data = open('Program2.eldi','r').read()
t = yacc.parse(data)

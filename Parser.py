# -*- coding: utf-8 -*-
import ply.yacc as yacc
import Scanner            # Importar el analizador léxico
from Cubo import *        # Importar los identificadores numéricos asignados
tokens = Scanner.tokens   # Lista de tokens
import sys
import json

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
# Diccionario de parámetros para cada método
parametros = {}
metodoActual = None

# Debe revisar si existe en metodos, variables globales
def checkMetodos(id):
    if id in diccionario_metodos:
        return True
    return False

# Debe revisar si existe en los parametros, y en los metodos
def checkParametros(id):
    if id in parametros:
        # Si existe el parámetro
        return True
    # El identificador no se ha utilizado
    return False

'''
###########################################################################
#   isfloat
#   Revisa si el parámetro recibido es un número flotante
###########################################################################
def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True
        '''

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

'''
###########################################################################
#   isint
#   Revisa si el parámetro recibido es un número entero
###########################################################################
def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b


###########################################################################
#   castVariable
#   Convierte la variable de string a numérica
###########################################################################
def castVariable(num):
    if isint(num):
        result = int(num)
    elif isfloat(num):
        result = float(num)
    else:
        result = None
    return result
    '''

def checkDataType(var):
    if var == "true" or var == "false":
        # print "bool"
        return "boolean";
    else:
        datatype = type(var)
        if datatype == int:
            return "int"
        elif datatype == float:
            return "float"
        # elif datatype == str:
        #    print var

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

def addVariableGlobal(identificador, tipo):
    # Revisar si la variable ya había sido declarada con anterioridad
    if checkVariableGlobal(identificador) or checkMetodos(identificador):
        print "El identificador <<" + identificador + ">> ya había sido declarado como variable global"
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

###########################################################################
#   addVariableLocal
#   Añadir una variable local al diccionario dependiendo de su tipo, y a una
#   una lista de parámetros que será asignada al método
###########################################################################
def addVariableLocal(id, tipo, posicion):
    if checkParametros(id) or checkMetodos(id):
        print "El identificador <<" + id + ">> ya es está en uso."
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
            variable['posicion'] = posicion
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_int[ id ] = variable
            locales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_float_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_float[ id ] = variable
            locales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_char_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_char[ id ] = variable
            locales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_string_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_string[ id ] = variable
            locales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = locales_boolean_cont
            variable['posicion'] = posicion
            variable['type'] = tipo
            parametros[ id ] = variable
            locales_boolean[ id ] = variable
            locales_boolean_cont += 1

def addGlobalVars(lista):
    for declaracion in lista:
        # Ciclo para leer los identificadores, estos se encuentran
        # a partir del segundo elemento (casilla 1)
        for i in range(1, len(declaracion)):
            # Añadir variable global
            addVariableGlobal(declaracion[i], declaracion[0])


def p_programa(p):
    '''programa : variables_list metodos'''
    # En este lugar ya se tienen las variables que son globales
    # Añadir las variables globales
    addGlobalVars(p[1])
    ''' Imprimir las variables globales
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
    '''
    # print json.dumps(p[1])
    #if p[2] <> None:
    #   print json.dumps( p[2] )

def p_variables_list(p):
    '''variables_list : variables_list variables
        | empty'''
    if len(p) == 3:
        variables = []
        if p[1] == None:
            variables.append(p[2])
        else:
            p[1].append(p[2])
            variables = p[1]
        p[0] = variables

def p_variables(p):
    '''variables : VAR tipo ID lista_variables SEMICOLON
        | VAR tipo ID LEFTSB INT_CTE RIGHTSB lista_variables SEMICOLON'''
    # Recibir las variables cuando hay una lista
    if len(p) == 6:
        if p[4] <> None:
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
    # print p[0]


def p_lista_variables(p):
    '''lista_variables : COMMA ID lista_variables
        | COMMA ID LEFTSB INT_CTE RIGHTSB lista_variables
        | empty'''
    if len(p) == 4:
        vars = []
        vars.append( p[2] )
        if p[3] <> None:
            p[0] = vars + p[3]
        else:
            p[0] = vars
    # elif len(p) == 6:
    #    vars = []

def p_metodos(p):
    '''metodos : metodos metodo
        | empty'''
    if len(p) == 3:
        aux = []
        aux.append(p[2])
        if p[1] <> None:
            p[0] = p[1] + aux
        else:
            p[0] = aux


def p_metodo(p):
    '''metodo : METHOD VOID MAIN LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD VOID ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD tipo ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB'''
    # if p[8] <> None:
    #    print p[8]
    # print str(p[2]) + " " + p[3]
    global metodoActual
    metodoActual = p[3]
    param_len = 0
    if p[5] <> None:
        # print "Parametros:"
        posicion = 1
        for parametro in p[5]:
            # Ciclo para leer los parámetros
            # a partir del segundo elemento (casilla 1, pues el primero tiene el id)
            # print "Tipo " + str(parametro[0]) + ", Id " + parametro[1]
            addVariableLocal(parametro[1], parametro[0], posicion)
            posicion += 1
        # print p[5]
        param_len =  len(p[5])
    else:
        # No contiene parámetros
        param_len = 0
    # Imprimir la cantidad de parámetros
    #print param_len
    if p[8] <> None:
        # print "Variables:"
        for variable in p[8]:
            addVariableLocal(variable[1], variable[0], 0)
        # print p[8]
    # print "Variables locales:"
    # print parametros
    if ( checkMetodos(p[3]) or checkVariableGlobal(p[3]) ):
        print "El identificador " + p[3] + " ya está en uso."
        sys.exit()
    else:
        full_method = {}
        met = {}
        met['tipo'] = p[2]
        met['vars'] = parametros.copy()
        met['param_len'] = param_len
        # diccionario_metodos[ p[3] ] = met
        full_method[ p[3] ] = met.copy()
        # Guardar el metodo en un diccionario
        diccionario_metodos[p[3]] = full_method.copy()
        p[0] = full_method.copy()
    resetVariablesLocales()
    parametros.clear()

def p_params(p):
    '''params : params parametro
        | params COMMA parametro
        | empty'''
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


def p_parametro(p):
    '''parametro : tipo ID'''
    p[0] = []
    p[0].append(p[1])
    p[0].append(p[2])
    # print p[0]

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
    '''llamada : ID LEFTP args RIGHTP'''
    if checkMetodos(p[1]):
        # Realizar el procedimiento cuando el método si existe
        # Verificar los parámetros
        x = 1
    else:
        # Ver los métodos declarados antes
        # print json.dumps(diccionario_metodos)
        print "El método <<" + p[1] + ">> no está definido."
        sys.exit()
    if p[3] <> None:
        # Cantidad de argumentos que tiene la llamada
        # print p[3]
        # Para obtener la cantidad de parámetros que posee el método
        call_len = len(p[3])
        cant = diccionario_metodos[p[1]][p[1]]['param_len']
    else:
        call_len = 0
        cant = diccionario_metodos[p[1]][p[1]]['param_len']
    if call_len == cant:
        # Sólo para no imprimir en pantalla
        if 1 == 2:
            print "Mismo tam"
            # Revisar tipos
    else:
        print "La cantidad de parámetros en la llamada <<" + p[1] + ">> no es compatible."
        print "Cantidad de parámetros esperados: " + str(cant)
        sys.exit()

def p_args(p):
    '''args : exp
        | args COMMA exp
        | empty'''
    if len(p) == 4:
        if p[1] <> None:
            p[0] = p[1]
        else:
            p[0] = []
        p[0].append(p[3])
    elif len(p) == 2:
        if p[1] <> None:
            p[0] = []
            p[0].append(p[1])

def p_asignacion(p):
    '''asignacion : ID ASSIGN exp SEMICOLON
        | ID LEFTSB exp RIGHTSB ASSIGN exp SEMICOLON'''
    # if len(p) == 5:
    #    print p[3]
    #print p[1]
    #if len(p) == 5:
    #    print p[3]
    #print ""

def p_ciclo(p):
    '''ciclo : WHILE LEFTP exp RIGHTP LEFTB bloque RIGHTB'''

def p_condicion(p):
    '''condicion : IF LEFTP exp RIGHTP LEFTB bloque RIGHTB
        | IF LEFTP exp RIGHTP LEFTB bloque RIGHTB ELSE LEFTB bloque RIGHTB'''

def p_exp(p):
    '''exp : llamada
        | expresion'''
    if p[1] <> None:
        p[0] = p[1]

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
    # Revisar la operación que se está haciendo y los parametros
    print p[2] + " " + str(p[1]) + " " + str(p[3])
    print resultante( getNumericalType(p[1]) , getNumericalType(p[3]) , getNumTypeOperation(p[2]));

    # Revisar que operación corresponde
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
    elif p[2] == 'NOTEQUAL':
        p[0] = p[1] <> p[3]
    elif p[2] == 'GREATEREQUAL':
        p[0] = p[1] >= p[3]
    elif p[2] == 'GREATERTHAN':
        p[0] = p[1] > p[3]
    elif p[2] == '<':
        p[0] = p[1] < p[3]
    elif p[2] == '<=':
        p[0] = p[1] <= p[3]
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]
    # Imprimir la operación que se esta realizando
    # print str(p[1]) + p[2] + str(p[3])
    # print p[0]

def p_expresion2(p):
    '''expresion : constante
        | ID
        | LEFTP expresion RIGHTP'''
    # Revisar si la longitud de la regla es de 2
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]

def p_tipo(p):
    '''tipo : INT
        | CHAR
        | BOOLEAN
        | FLOAT
        | STRING'''
    p[0] = getNumericalType(p[1])

def p_constante(p):
    '''constante : FLOAT_CTE
        | INT_CTE
        | CHAR_CTE
        | STRING_CTE
        | TRUE
        | FALSE'''
    p[0] = p[1]

# Elemento vacío
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

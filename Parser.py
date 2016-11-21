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
listTemporales = []
contTemp = 2000

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
temporalActual = 1
tipo_exp = None
cont_args = 1
solo_una_expresion = None

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

def resetVariablesTemporales():
    global temporales_int_cont, temporales_char_cont, temporales_float_cont
    global temporales_string_cont, temporales_boolean_cont
    temporales_int_cont = 2000
    temporales_float_cont = 2200
    temporales_char_cont = 2400
    temporales_string_cont = 2600
    temporales_boolean_cont = 2800
    temporales_int.clear()
    temporales_char.clear()
    temporales_float.clear()
    temporales_string.clear()
    temporales_boolean.clear()
    temporalActual = 1

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
        elif datatype == bool:
            return "boolean"
        else:
            # El tipo debería ser char o string
            # print var + " " + str(len(var))
            print var
            if len(var) == 3 and var[0] == '\'':
                return "char"
            elif var[0] == '"':
                return "string"
            else:
                return ERROR
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

def addVariableTemporal(tipo, valor):
    global temporales_int, temporales_float, temporales_char, temporales_string, temporalActual
    global temporales_boolean, temporales_int_cont, temporales_char_cont, temporales_float_cont, temporales_string_cont, temporales_boolean_cont
    # print temporalActual
    if tipo == INT:
        variable = {}
        # Valores temporales para estos campos
        variable['valor'] = valor
        variable['direccionMemoria'] = temporales_int_cont
        # print variable
        temporales_int[ temporalActual ] = variable
        temporales_int_cont += 1
    elif tipo == FLOAT:
        variable = {}
        # Valores temporales para estos campos
        variable['valor'] = valor
        variable['direccionMemoria'] = temporales_float_cont
        # print variable
        temporales_float[ temporalActual ] = variable
        temporales_float_cont += 1
    elif tipo == CHAR:
        variable = {}
        # Valores temporales para estos campos
        variable['valor'] = valor
        variable['direccionMemoria'] = temporales_char_cont
        print variable
        temporales_char[ temporalActual ] = variable
        temporales_char_cont += 1
    elif tipo == STRING:
        variable = {}
        # Valores temporales para estos campos
        variable['valor'] = valor
        variable['direccionMemoria'] = temporales_string_cont
        # print variable
        temporales_string[ temporalActual ] = variable
        temporales_string_cont += 1
    elif tipo == BOOLEAN:
        variable = {}
        # Valores temporales para estos campos
        variable['valor'] = valor
        variable['direccionMemoria'] = temporales_boolean_cont
        # print variable
        temporales_boolean[ temporalActual ] = variable
        temporales_boolean_cont +=1
    temporalActual += 1
    """
    print temporales_int
    print len(temporales_int)
    print temporales_float
    print len(temporales_float)
    print temporales_char
    print len(temporales_char)
    print temporales_string
    print len(temporales_string)
    print temporales_boolean
    print len(temporales_boolean)
    print """

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
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_int_cont
            globales_int[ identificador ] = variable.copy()
            globales_int_cont += 1
        elif tipo == FLOAT:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_float_cont
            globales_float[ identificador ] = variable.copy()
            globales_float_cont += 1
        elif tipo == CHAR:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_char_cont
            globales_char[ identificador ] = variable.copy()
            globales_char_cont += 1
        elif tipo == STRING:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_string_cont
            globales_string[ identificador ] = variable.copy()
            globales_string_cont += 1
        elif tipo == BOOLEAN:
            variable = {}
            # Valores temporales para estos campos
            variable['valor'] = None
            variable['direccionMemoria'] = globales_boolean_cont
            globales_boolean[ identificador ] = variable.copy()
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
    '''programa : add_globales metodos'''
    # En este lugar ya se tienen las variables que son globales
    # Añadir las variables globales
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
    #   print json.dumps( diccionario_metodos )

def p_add_globales(p):
    '''add_globales : variables_list'''
    p[0] = p[1]
    addGlobalVars(p[1])

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

params_metodo = None
tipo_metodo = None
vars_metodo = None
metodoActual = None
def p_metodo(p):
    '''metodo : METHOD tipo_metodo metodo1 LEFTP save_params RIGHTP LEFTB method_vars add_method bloque RIGHTB'''
    # if p[8] <> None:
    #    print p[8]
    # print str(p[2]) + " " + p[3]
    param_len = 0
    global metodoActual, contTemp, params_metodo, tipo_metodo, vars_metodo
    resetVariablesLocales()
    parametros.clear()
    # Reiniciar el contador de temporales
    contTemp = 2000
    # print metodoActual
    # Limpiar las variables del método
    metodoActual = None
    params_metodo = None
    tipo_metodo = None
    vars_metodo = None

def p_metodo1(p):
    '''metodo1 : MAIN
        | ID'''
    global metodoActual
    metodoActual = p[1]
    p[0] = p[1]

def p_save_params(p):
    '''save_params : params'''
    global params_metodo
    if p[1] <> None:
        params_metodo = p[1]
    p[0] = p[1]

def p_tipo_metodo(p):
    '''tipo_metodo : VOID
        | tipo'''
    global tipo_metodo
    tipo_metodo = p[1]
    p[0] = p[1]

def p_add_method(p):
    '''add_method : '''
    """
    print "Adding method"
    print metodoActual
    print params_metodo
    print tipo_metodo
    print vars_metodo """
    # p[5] son params
    # print metodoActual
    # print params_metodo
    if params_metodo <> None:
        # print "Parametros:"
        posicion = 1
        for parametro in params_metodo:
            # Ciclo para leer los parámetros
            # a partir del segundo elemento (casilla 1, pues el primero tiene el id)
            # print "Tipo " + str(parametro[0]) + ", Id " + parametro[1]
            addVariableLocal(parametro[1], parametro[0], posicion)
            posicion += 1
        # print p[5]
        param_len =  len(params_metodo)
    else:
        # No contiene parámetros
        param_len = 0
    # Imprimir la cantidad de parámetros
    #print param_len
    # p[8] son vars
    if vars_metodo <> None:
        # print "Variables:"
        for variable in vars_metodo:
            addVariableLocal(variable[1], variable[0], 0)
        # print p[8]
    # print "Variables locales:"
    # print parametros
    # p[3] es nombre del método
    # p[2] es el tipo
    if ( checkMetodos(metodoActual) or checkVariableGlobal(metodoActual) ):
        print "El identificador " + metodoActual + " ya está en uso."
        sys.exit()
    else:
        full_method = {}
        met = {}
        met['tipo'] = tipo_metodo
        met['vars'] = parametros.copy()
        met['param_len'] = param_len
        # diccionario_metodos[ p[3] ] = met
        full_method[ metodoActual ] = met.copy()
        # Guardar el metodo en un diccionario
        diccionario_metodos[metodoActual] = full_method.copy()
        p[0] = full_method.copy()

def p_method_vars(p):
    '''method_vars : variables_list'''
    global vars_metodo
    vars_metodo = p[1]
    p[0] = p[1]

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
    '''estatuto : condicion
        | ciclo
        | return
        | lectura
        | escritura
        | llamada SEMICOLON
        | asignacion
        '''
    # print p[1]

def p_return(p):
    '''return : RETURN return1 SEMICOLON'''

def p_return1(p):
    '''return1 : exp'''
    global tipo_exp
    # Generación del cuádruplo de return
    quad = []
    quad.append("RETURN")
    quad.append(None)
    quad.append(None)
    if tipo_exp == 1:
        if solo_una_expresion:
            quad.append(p[1])
        else:
            quad.append(contTemp-1)
    else:
        quad.append("llamada")
    print quad
    return_exp = None

def p_lectura(p):
    '''lectura : ID ASSIGN READ LEFTP RIGHTP SEMICOLON'''
    # Generación del cuádruplo de lectura
    quad = []
    quad.append(p[3].upper())
    # x = input("Value for %s: " % p[1])
    x = 4
    quad.append(x)
    quad.append(None)
    quad.append(p[1])
    print quad

def p_escritura(p):
    '''escritura : PRINT LEFTP exp RIGHTP SEMICOLON'''
    # Generación del cuádruplo de escritura
    quad = []
    quad.append(p[1].upper())
    quad.append(None)
    quad.append(None)
    quad.append(p[3])
    print quad

def p_llamada(p):
    '''llamada : llamada1 LEFTP args RIGHTP'''
    if checkMetodos(p[1]):
        # Realizar el procedimiento cuando el método si existe
        # Verificar los parámetros
        # algo random
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
        #if 1 == 2:
        # print "Mismo tam"
        # Revisar tipos

        if p[3] <> None:
            # print p[3]
            global cont_args
            cont_args = 1
            """
            for arg in p[3]:
                # print arg

                quad_arg = []
                quad_arg.append("PARAM")
                quad_arg.append(arg)
                quad_arg.append(None)
                quad_arg.append("param" + str(cont))"""
                # print quad_arg
                # cont += 1
    else:
        print "La cantidad de parámetros en la llamada <<" + p[1] + ">> no es compatible."
        print "Cantidad de parámetros esperados: " + str(cant)
        sys.exit()

def p_llamada1(p):
    '''llamada1 : ID'''
    p[0] = p[1]
    quad_era = []
    quad_era.append("ERA")
    quad_era.append(p[1])
    quad_era.append(None)
    quad_era.append(None)
    print quad_era

def p_args(p):
    '''args : exp
        | args COMMA exp
        | empty'''
    global cont_args
    if len(p) == 4:
        if p[1] <> None:
            p[0] = p[1]
        else:
            p[0] = []
        quad_arg = []
        quad_arg.append("PARAM")
        quad_arg.append(p[3])
        quad_arg.append(None)
        quad_arg.append("param" + str(cont_args))
        print quad_arg
        cont_args += 1
        p[0].append(p[3])
    elif len(p) == 2:
        if p[1] <> None:
            p[0] = []
            p[0].append(p[1])
            quad_arg = []
            quad_arg.append("PARAM")
            quad_arg.append(p[1])
            quad_arg.append(None)
            quad_arg.append("param" + str(cont_args))
            print quad_arg
            cont_args += 1

def p_asignacion(p):
    '''asignacion : ID ASSIGN exp SEMICOLON
        | ID LEFTSB exp RIGHTSB ASSIGN exp SEMICOLON'''
    # print p[1]
    # Debe de tener doble el nombre del método
    # print json.dumps( diccionario_metodos[metodoActual][metodoActual] )
    direccionAsignacion = None
    if p[1] in diccionario_metodos[metodoActual][metodoActual]['vars']:
        print diccionario_metodos[metodoActual][metodoActual]['vars'][p[1]]['direccionMemoria']
        direccionAsignacion = diccionario_metodos[metodoActual][metodoActual]['vars'][p[1]]['direccionMemoria']
        # print p[1] + " Si esta xd"
    else:
        if checkVariableGlobal(p[1]):
            direccionAsignacion = "global"
            print p[1] + " sta en global"
        else:
            print "La variable <<" + p[1] + ">> no está declarada"
            sys.exit()
    # print diccionario_metodos[metodoActual][metodoActual]['vars'][p[1]]
    # Validar que la variable exista en el método
    # exp contiene la lista de cuadruplos que se hicieron en expression
    global solo_una_expresion
    # Generación de cuádruplo
    if len(p) == 5:
        # Revisar que la variable exista en el método
        # print diccionario_metodos[metodoActual]

        # Generación del cuádruplo de la asignación
        quad = []
        quad.append(p[2])
        if solo_una_expresion == True:
            quad.append(p[3])
        else:
            if tipo_exp == 0:
                quad.append("llamada")
            else:
                quad.append(contTemp-1)
        quad.append(None)
        quad.append(direccionAsignacion)
        print quad
    solo_una_expresion = None

ciclo_exp = None
def p_ciclo(p):
    '''ciclo : WHILE ciclo1 LEFTP exp RIGHTP LEFTB bloque ciclo2 RIGHTB'''
    if p[3] <> None:
        global ciclo_exp
        ciclo_exp = p[3]

# Elemento vacío
def p_ciclo1(p):
    'ciclo1 :'
    # Generación del cuádruplo inicial
    quad = []
    quad.append("GOTOFc")
    quad.append(ciclo_exp)
    quad.append(None)
    quad.append('x')
    print quad
    # print "ciclo1"

# Elemento vacío
def p_ciclo2(p):
    'ciclo2 :'
    # Generación del cuádruplo del goto para volver a Validar
    quad_goto = []
    quad_goto.append("GOTO")
    quad_goto.append(None)
    quad_goto.append(None)
    quad_goto.append('y')
    print quad_goto

def p_condicion(p):
    '''condicion : IF LEFTP condicion1 RIGHTP condicion2 LEFTB bloque RIGHTB
        | IF LEFTP condicion1 RIGHTP condicion2 LEFTB bloque RIGHTB condicion3 ELSE LEFTB bloque RIGHTB'''
    # if p[3] <> None:

condicion_exp = None
def p_condicion1(p):
    '''condicion1 : exp'''
    # print p[1]
    global condicion_exp
    condicion_exp = p[1]

def p_condicion2(p):
    '''condicion2 : '''
    quad = []
    quad.append("GOTOFi")
    # Revisar si hay sólo una expresión
    if solo_una_expresion:
        global condicion_exp
        quad.append(condicion_exp)
        condicion_exp = None
    else:
        quad.append(contTemp-1)
    quad.append(None)
    quad.append('x')
    print quad

def p_condicion3(p):
    '''condicion3 : '''
    quad = []
    quad.append("GOTO")
    quad.append(None)
    quad.append(None)
    quad.append("finalElse")
    print quad

def p_exp(p):
    '''exp : llamada exp1
        | expresion exp2'''
    if p[1] <> None:
        p[0] = p[1]

def p_exp1(p):
    '''exp1 : '''
    global tipo_exp
    # Llamada
    tipo_exp = 0

def p_exp2(p):
    '''exp2 : '''
    global tipo_exp
    # expresion
    tipo_exp = 1

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
    # print p[2] + " " + str(p[1]) + " " + str(p[3])
    # Imprimir el tipo del resultante
    global contTemp, solo_una_expresion
    solo_una_expresion = False
    tipo1 = getNumericalType(p[1])
    tipo2 = getNumericalType(p[3])
    tipoResultante = resultante( tipo1 , tipo2 , getNumTypeOperation(p[2]))
    if resultante( getNumericalType(p[1]) , getNumericalType(p[3]) , getNumTypeOperation(p[2])) == ERROR:
        print "No es posible realizar la operación " + p[2] + " a los operadores " + str(p[1]) + ", " + str(p[3])
        sys.exit()
    else:
        quad_exp = []
        quad_exp.append(p[2])
        quad_exp.append(p[1])
        quad_exp.append(p[3])
        #quad_exp.append("var")
        quad_exp.append(contTemp)
        contTemp = contTemp + 1
        print quad_exp

    # getNumericalType(p[1])
    # getNumericalType(p[3])
    # print diccionario_metodos
    # print "\n\n"
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
    addVariableTemporal( tipoResultante, p[0] )

def p_expresion2(p):
    '''expresion : constante
        | ID
        | LEFTP expresion RIGHTP'''
    # Revisar si la longitud de la regla es de 2
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = p[2]
    global solo_una_expresion
    solo_una_expresion = True

def p_tipo(p):
    '''tipo : INT
        | CHAR
        | BOOLEAN
        | FLOAT
        | STRING'''
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

# Leer el program
data = open('Program2.eldi','r').read()
t = yacc.parse(data)
# Validar que el método main se encuentra en el diccionario métodos
# print diccionario_metodos
if checkMetodos("main"):
    if 1 == 2:
        print "Si esta"
else:
    print "No se ha encontrado el método main"
    sys.exit()

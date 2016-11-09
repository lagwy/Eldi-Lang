# -*- coding: utf-8 -*-
import ply.yacc as yacc
import Scanner            # Importar el analizador léxico
from Cubo import *        # Importar los identificadores numéricos asignados
tokens = Scanner.tokens   # Lista de tokens
import sys

# Precedencia de los operadores
precedence = (
    ('right', 'ASSIGN'),
    ('left', 'AND', 'OR'),
    ('left', 'EQUALS', 'NOTEQUAL'),
    ('left', 'GREATERTHAN', 'GREATEREQUAL', 'LESSTHAN', 'LESSEQUAL'),
    ('left', 'SUM', 'LESS'),
    ('left', 'TIMES', 'DIVISION'),
)



def isfloat(x):
    try:
        a = float(x)
    except ValueError:
        return False
    else:
        return True

def isint(x):
    try:
        a = float(x)
        b = int(a)
    except ValueError:
        return False
    else:
        return a == b

def castVariable(num):
    if isint(num):
        result = int(num)
    elif isfloat(num):
        result = float(num)
    else:
        result = None
    return result

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

def p_programa(p):
    '''programa : variables_list metodos'''

def p_variables_list(p):
    '''variables_list : variables_list variables
        | empty'''

def p_variables(p):
    '''variables : VAR tipo ID lista_variables SEMICOLON
        | VAR tipo ID LEFTSB INT_CTE RIGHTSB lista_variables SEMICOLON'''

def p_lista_variables(p):
    '''lista_variables : COMMA ID lista_variables
        | COMMA ID LEFTSB INT_CTE RIGHTSB lista_variables
        | empty'''

def p_metodos(p):
    '''metodos : metodos metodo
        | empty'''

def p_metodo(p):
    '''metodo : METHOD VOID MAIN LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD VOID ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD tipo ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB'''

def p_params(p):
    '''params : params parametro
        | params COMMA parametro
        | empty'''

def p_parametro(p):
    '''parametro : tipo ID'''

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
    if len(p) == 5:
        print p[3]

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
    # Revisar que operación corresponde
    if p[2] == '*':
        p[0] = castVariable(p[1]) * castVariable(p[3])
    elif p[2] == '/':
        p[0] = castVariable(p[1]) / castVariable(p[3])
    elif p[2] == '+':
        p[0] = castVariable(p[1]) + castVariable(p[3])
    elif p[2] == '-':
        p[0] = castVariable(p[1]) - castVariable(p[3])
    elif p[2] == '==':
        p[0] = p[1] == p[3]
    elif p[2] == 'NOTEQUAL':
        p[0] = castVariable(p[1]) <> castVariable(p[3])
    elif p[2] == 'GREATEREQUAL':
        p[0] = castVariable(p[1]) >= castVariable(p[3])
    elif p[2] == 'GREATERTHAN':
        p[0] = castVariable(p[1]) > castVariable(p[3])
    elif p[2] == '<':
        p[0] = castVariable(p[1]) < castVariable(p[3])
    elif p[2] == '<=':
        p[0] = castVariable(p[1]) <= castVariable(p[3])
    elif p[2] == '&&':
        p[0] = p[1] and p[3]
    elif p[2] == '||':
        p[0] = p[1] or p[3]

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
    '''constante : INT_CTE
        | FLOAT_CTE
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

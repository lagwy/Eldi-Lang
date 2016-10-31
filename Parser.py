# -*- coding: utf-8 -*-
###########################################################################
#   Scanner.py
#   Análisis léxico para el lenguaje Eldi
#
#   @author Luis Angel Martinez
#   @author Daniel Garcia Mena
#   @date 12/10/2016
###########################################################################
import ply.yacc as yacc
import Scanner            # Import lexer information
tokens = Scanner.tokens   # Need token list

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

state = 0

def p_programa(p):
    '''programa : variables_list metodos'''

def p_variables_list(p):
    '''variables_list : variables_list variables
        | empty'''

def p_variables(p):
    '''variables : VAR tipo ID lista_variables SEMICOLON
        | VAR tipo ID LEFTSB INT_CTE RIGHTSB lista_variables SEMICOLON'''
    if  state == 0:
        print p[3]

def p_lista_variables(p):
    '''lista_variables : COMMA ID lista_variables
        | COMMA ID LEFTSB INT_CTE RIGHTSB lista_variables
        | empty'''

def p_metodos(p):
    '''metodos : metodos metodo
        | empty'''
    global state
    state = 1

def p_metodo(p):
    '''metodo : METHOD VOID MAIN LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD VOID ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB
        | METHOD tipo ID LEFTP params RIGHTP LEFTB variables_list bloque RIGHTB'''

def p_params(p):
    '''params : params parametro
        | empty'''

def p_parametro(p):
    '''parametro : tipo ID mas_parametros'''

def p_mas_parametros(p):
    '''mas_parametros : COMMA tipo ID
        | empty'''

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
    if state == 0:
        print p[1]

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
    else:
        print("Syntax error at EOF")

yacc.yacc()

# Read program file
data = open('Program2.eldi','r').read()
t = yacc.parse(data)

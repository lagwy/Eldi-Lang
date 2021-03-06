# -*- coding: utf-8 -*-
# Identificadores de los tipos
INT = 0
FLOAT = 1
CHAR = 2
STRING = 3
BOOLEAN = 4
ERROR = -1
# El identificador 5 es para void (utilizado en métodos)

# Identificadores de las operaciones
SUMA = 0
RESTA = 1
DIVISION = 2
MULTIPLICACION = 3
CONCATENACION = 4
MAYORQUE = 5
MENORQUE = 6
IGUAL = 7
DIFERENTE = 8
MAYORIGUAL = 9
MENORIGUAL = 10
BWAND = 11
BWOR = 12

# Obtener el código de la operación que se hará
def getNumTypeOperation(op):
    if op == "+":
        return SUMA
    elif op == "-":
        return RESTA
    elif op == "/":
        return DIVISION
    elif op == ".":
        return CONCATENACION
    elif op == ">":
        return MAYORQUE
    elif op == "<":
        return MENORQUE
    elif op == "==":
        return IGUAL
    elif op == "!=":
        return DIFERENTE
    elif op == ">=":
        return MAYORIGUAL
    elif op == "<=":
        return MENORIGUAL
    elif op == "&&":
        return BWAND
    elif op == "||":
        return BWOR
    else:
        return -1

# Semantica de operadores y operandos
CUBO = [
    [ 0, 0,  0,  0,  0,  0, -1,  4,  4,  4,  4,  4,  4, -1, -1 ],
    [ 0, 1,  1,  1,  1,  1, -1,  4,  4,  4,  4,  4,  4, -1, -1 ],
    [ 0, 2, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 0, 3, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 0, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 1, 0,  1,  1,  1,  1, -1,  4,  4,  4,  4,  4,  4, -1, -1 ],
    [ 1, 1,  1,  1,  1,  1, -1,  4,  4,  4,  4,  4,  4, -1, -1 ],
    [ 1, 2, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 1, 3, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 1, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 2, 0, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 2, 1, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 2, 2, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 2, 3, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 2, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 3, 0, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 3, 1, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 3, 2, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 3, 3, -1, -1, -1, -1,  3, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 3, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 4, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 4, 1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 4, 2, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 4, 3, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1 ],
    [ 4, 4, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1,  4,  4 ] ]

###########################################################################
#   resultante
#   Encontrar el tipo del resultado de una operación
###########################################################################
def resultante (tipo1, tipo2, operador):
    ren = tipo1 * 5 + tipo2
    col = operador + 2
    return CUBO[ren][col]

# print resultante(2, 3, 4)

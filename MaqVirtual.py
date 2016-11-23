# -*- coding: utf-8 -*-

import Parser
import json

"""
def insertValues(diccionario):
	print diccionario['parametro_1']
	print diccionario['parametro_2']
variables = dict()
lista_cuadruplos = [[3, 1500, 1500, 2500],
					[1, 2000, 3000, 2500],
					["GOTF", 9000, None, 5],
					[4, "hello", "world", 5001],
					["READ", 24, 5000],
					["PRINT", None, None, 5001],
					["RET", None, None, None]]

variables = {1500 : 4, 2000 : 3, 3000 : 7, 2500: 0, 9000: True, 5000: 4, 8000: 10}
listaVariables = [9000, 5000, 1500]
print variables.keys()
"""

# Método principal
def main():
	cont = 1
	for cuadruplo in Parser.lista_cuadruplos:
		print cont, "\t", cuadruplo
		cont += 1
    # print "\n\n", json.dumps(Parser.lista_cuadruplos), "\n\n", Parser.diccionario_metodos

if __name__ == "__main__":
    main()

def operacionCuadruplos(lista_cuadruplos):
	cuadruploActual = 0
	while cuadruploActual != len(lista_cuadruplos):
		cuadruplo = lista_cuadruplos[cuadruploActual]
		if cuadruplo[0] == 0:
			variables[cuadruplo[3]] = variables[cuadruplo[1]] + variables[cuadruplo[2]]
		elif cuadruplo[0] == 1:
			variables[cuadruplo[3]] = variables[cuadruplo[1]] - variables[cuadruplo[2]]
		elif cuadruplo[0] == 2:
			variables[cuadruplo[3]] = variables[cuadruplo[1]] / variables[cuadruplo[2]]
		elif cuadruplo[0] == 3:
			variables[cuadruplo[3]] = variables[cuadruplo[1]] * variables[cuadruplo[2]]
		elif cuadruplo[0] == 4:
			variables[cuadruplo[3]] = cuadruplo[1] + cuadruplo[2]
		elif cuadruplo[0] == 5:
			if (variables[cuadruplo[1]] > variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 6:
			if (variables[cuadruplo[1]] < variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 7:
			if (variables[cuadruplo[1]] == variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 8:
			if (variables[cuadruplo[1]] != variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 9:
			if (variables[cuadruplo[1]] >= variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 10:
			if (variables[cuadruplo[1]] <= variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 11:
			if (variables[cuadruplo[1]] and variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == 12:
			if (variables[cuadruplo[1]] or variables[cuadruplo[2]]):
				variables[cuadruplo[3]] =  true
			else :
				variables[cuadruplo[3]] = false
		elif cuadruplo[0] == "READ":
			variables[cuadruplo[2]] = cuadruplo [1];
		elif cuadruplo[0] == "PRINT":
			print variables[cuadruplo[3]]
		elif cuadruplo[0] == "GOTOF":
			if(variables[cuadruplo[1]] == True):
				cuadruploActual = cuadruplo[3]
		elif cuadruplo[0] == "GOTOT":
			if(variables[cuadruplo[1]] == True):
				cuadruploActual = cuadruplo[3]
		elif cuadruplo[0] == "GOTO":
			cuadruploActual = cuadruplo[3]
		elif cuadruplo[0] == "RETURN":
			return variables[cuadruplo[3]]
		elif cuadruplo[0] == "RET":
			for variable in listaVariables:
				variables.pop(variable,None)
			listaVariables[:] =[]
		"""elif cuadruplo[0] == "ERA":
			for variables in listaVariables:
		elif cuadruplo[0] == "PARAMETRO":
			variables[param] = cuadruplo[1]
		elif cuadruplo[0] == "GOSUB":
			"""
		if cuadruplo[0] != "GOTO" or cuadruplo[0] != "GOTOF":
			cuadruploActual = cuadruploActual + 1
# operacionCuadruplos(lista_cuadruplos)
# print variables.keys()
# print lista_cuadruplos[1]

# -*- coding: utf-8 -*-

import Parser
import json

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
		if cuadruplo[0] != "GOTO" or cuadruplo[0] != "GOTOF":
			cuadruploActual = cuadruploActual + 1

# -*- coding: utf-8 -*-
import Parser
from Parser import globales_int
from Parser import globales_float
from Parser import globales_char
from Parser import globales_string
from Parser import globales_boolean
from Parser import constantes_int
from Parser import constantes_float
from Parser import constantes_char
from Parser import constantes_string
from Parser import constantes_boolean
from Parser import diccionario_metodos
from Parser import contTemp

dicGlobal = {}
dicMetodos = {}
varGlobales = [[],[],[],[],[]]
temporales = []
listPos = []

funcMem = []
Scope = 0

##########################################################################
#	memoriaGlobal()
# 	Mete al diccionario de memoria global, el tipo y el numero de variable de ese tipo
##########################################################################
def memoriaGlobal():

	contInt = 0
	for key in globales_int:
		dicGlobal[key] = [0, contInt]
		contInt = contInt + 1
	contFloat = 0
	for key in globales_float:
		dicGlobal[key] = [1 , contFloat]
		contFloat = contFloat + 1
	contChar = 0
	for key in globales_char:
		dicGlobal[key] = [2 , contChar]
		contChar = contChar + 1
	contString = 0
	for key in globales_string:
		dicGlobal[key] = [3 , contString]
		contString = contString + 1
	contBoolean = 0
	for key in globales_boolean:
		dicGlobal[key] = [4 , contBoolean]
		contBoolean = contBoolean + 1

	for i in range(contTemp - 2000):
		temporales.append(None)

##########################################################################
#	memoriaFuncion( funcion )
#
##########################################################################

def memoriaFuncion(funcion):

	dicFun = {}  				#Diccionario de funciones
	varFun = [[],[],[],[],[]]
	func = diccionario_metodos.get(funcion) #Guarda la funcion temporalmente
	variables = func.get("vars") #Guarda las variables de la funcion temporalmente

	#Recorre todas las varibales de la funcion
	for v in variables:
		direccion = variables.get(v).get("direccionMemoria")
		#valor = variables.get(v).get("valor")

		# Guarda  dicFun[ direccion ] = [tipo, posicion]
		# Agrega  en VarFun = [[],[],[],[]] el valor en el la lista correspondiente
		if variables.get(v).get("type") == 0:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]
			#varFun[variables.get(v).get("type")].append(valor)

		elif variables.get(v).get("type") == 1:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]

		elif variables.get(v).get("type") == 2:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]

		elif variables.get(v).get("type") == 3:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]

		elif variables.get(v).get("type") == 4:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]

	#Inicializa las variables con un valor default y las guarda en la lista de variables por tipo, de funciones.
	for k in dicFun:
		if dicFun.get(k)[0] == 0:
			varFun[dicFun.get(k)[0]].append(0)
		elif dicFun.get(k)[0] == 1:
			varFun[dicFun.get(k)[0]].append(0.0)
		elif dicFun.get(k)[0] == 2:
			varFun[dicFun.get(k)[0]].append('')
		elif dicFun.get(k)[0] == 3:
			varFun[dicFun.get(k)[0]].append("")
		elif dicFun.get(k)[0] == 4:
			varFun[dicFun.get(k)[0]].append(False)

	'''for i in range(func.get("temporales")):
		listTemp.append(None)'''

	funcMem.append([dicFun, varFun]) #Guarda en la lista de funciones el [ diccionario de variables y
									 #la lista de variables de la función ], temporalmente
									 #funcMen = [ [ dic[direccion]=[tipo,posicion], varFun=[[valor,valor,...],[valor]..] ],  [ dic[direccion]=[tipo,posicion], varFun =[[valor,valor,...],[valor]..] ] ]

##########################################################################
#	scoper(direc)
#
##########################################################################
def scopeVar(direc):

	if funcMem[Scope][0].has_key(direc): #Si existe llave , regresa 1
		return 1

	elif dicGlobal.has_key(direc): #Si encuentra un llave en las variables globales retorna 0
		return 0

	else:
		return -1

#############################################################
#		ValorDireccion(direc)
#		Regresa el valor apartir de una dirección
#
##############################################################
def valorDireccion(direc):
	var = scopeVar(direc)
	#Si var es igual a 0, es una variabel global, y regresa su valor
	if(var == 0):
		dirGlobal = dicGlobal.get(direc)
		return varGlobales[dirGlobal[0]][dirGlobal[1]]

	#Si var es mayor a 0, es una variabel global, y regresa su valor
	elif(var > 0):
		lista = funcMem[Scope][0].get(direc)
		tipo = lista[0]
		pos = lista[1]
		return funcMem[Scope][1][tipo][pos]

	elif(2000 <= direc and direc < 3000):
		return temporales[direc - 2000]

	elif(3000 <= direc and direc < 3200):
		return constantes_int[direc - 3000]

	elif(3200 <= direc and direc < 3400):
		return constantes_float[direc - 3200]

	elif(3400 <= direc and direc < 3600):
		return constantes_char[direc - 3400]

	elif(3600 <= direc and direc < 3800):
		return constantes_string[direc - 3600]

	elif(3800 <= direc and direc < 4000):
		return constantes_boolean[direc - 3800]

	return direc

def asignarTemporales(valor, direc):
	#print(direc)
	temporales[direc - 2000] = valor



"""
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
    print "\n\n", Parser.diccionario_metodos


#def operacionCuadruplos(lista_cuadruplos):
if __name__ == "__main__":
	lista_cuadruplos = Parser.lista_cuadruplos
	main()
	memoriaGlobal()
	memoriaFuncion("main")
	cuadruploActual = 0
	while cuadruploActual < len(lista_cuadruplos):
		cuadruplo = lista_cuadruplos[cuadruploActual]
		val1 = cuadruplo[0]
		val2 = cuadruplo[1]
		val3 = cuadruplo[2]
		val4 = cuadruplo[3]
		if cuadruplo[0] == '+':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 + res2, val4)

		elif cuadruplo[0] == '-':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 - res2, val4)

		elif cuadruplo[0] == '/':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 / res2, val4)

		elif cuadruplo[0] == '*':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 * res2, val4)

		elif cuadruplo[0] == '>':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 > res2, val4)

		elif cuadruplo[0] == '<':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 < res2, val4)

		elif cuadruplo[0] == '==':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 == res2, val4)

		elif cuadruplo[0] == '!=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 != res2, val4)

		elif cuadruplo[0] == '>=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 >= res2, val4)

		elif cuadruplo[0] == '<=':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 <= res2, val4)

		elif cuadruplo[0] == '&&':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 and res2, val4)

		elif cuadruplo[0] == '||':
			res1 = valorDireccion(val2)
			res2 = valorDireccion(val3)
			asignarTemporales(res1 or res2, val4)

		elif cuadruplo[0] == '=':
			res1 = valorDireccion(val2)
			var = scopeVar(val4)
			#print (res1, var, dicGlobal.get(val4),funcMem[Scope][0].get(val4))

			if var == 0:
				lista = dicGlobal.get(val4)
				varGlobales[lista[0]][lista[1]] = res1
			elif var == 1:
				lista = funcMem[Scope][0].get(val4)
				varsFun = funcMem[Scope][1]
				varsFun[lista[0]][lista[1]] = res1
				funcMem[Scope][1] = varsFun
				#funcMem[Scope][1][lista[0]][lista[1]] = res1

		elif cuadruplo[0] == 'READ':
			res1 = float(input())
			var = scopeVar(val4)

			if var == 0:
				lista = dicGlobal.get(val4)
				varGlobales[lista[0]][lista[1]] = res1
			elif var == 1:
				lista = funcMem[Scope][0].get(val4)
				funcMem[Scope][1][lista[0]][lista[1]] = res1

		elif cuadruplo[0] == 'PRINT':
			print valorDireccion(val4)

		elif cuadruplo[0] == 'GOTOFc':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'GOTOFi':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'GOTO':
			cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'RETURN':
			cuadruploActual = cuadruploActual

		elif cuadruplo[0] == 'ERA':
			memoriaFuncion(val4)

		elif cuadruplo[0] == 'PARAMETRO':
			asignarParametros(val2)

		elif cuadruplo[0] == 'GOSUB':
			listPos.append(cuadruploActual)
			cuadruploActual = val4 - 2
			Scope = Scope + 1

		elif cuadruplo[0] == 'ENDPROC':
			print(funcMem)
			funcMem.pop()
			Scope = Scope - 1
			if not len(listPos) == 0:
				cuadruploActual = listPos.pop() - 1
		#if cuadruplo[0] != 'GOTO' and cuadruplo[0] != 'GOTOFc' and cuadruplo[0] != 'GOTOFi' :
		cuadruploActual = cuadruploActual + 1

'''if __name__ == "__main__":
    main()
    operacionCuadruplos(Parser.lista_cuadruplos)'''

# operacionCuadruplos(lista_cuadruplos)
# print variables.keys()
# print lista_cuadruplos[1]

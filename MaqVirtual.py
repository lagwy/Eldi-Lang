# -*- coding: utf-8 -*-
import Parser
import sys
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
listFun = []

funcMem = []
retorno = None
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

	#print(temporales)

##########################################################################
#	memoriaFuncion( funcion )
#
##########################################################################
def memoriaFuncion(funcion):
	dicFun = {}  				#Diccionario de funciones
	varFun = [[],[],[],[],[]]
	func = diccionario_metodos.get(funcion) #Guarda la funcion temporalmente
	funcAct = funcion
	listFun.append(funcion)
	#if func is not None:
	variables = func.get("vars") #Guarda las variables de la funcion temporalmente

	#Recorre todas las varibales de la funcion
	for v in variables:
		direccion = variables.get(v).get("direccionMemoria")
		#valor = variables.get(v).get("valor")

		# Guarda  dicFun[ direccion ] = [tipo, posicion]
		# Agrega  en VarFun = [[],[],[],[]] el valor en el la lista correspondiente
		if variables.get(v).get("type") == 0:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000, variables.get(v).get("tam")]
			#varFun[variables.get(v).get("type")].append(valor)

		elif variables.get(v).get("type") == 1:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1200, variables.get(v).get("tam")]

		elif variables.get(v).get("type") == 2:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1400, variables.get(v).get("tam")]

		elif variables.get(v).get("type") == 3:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1600, variables.get(v).get("tam")]

		elif variables.get(v).get("type") == 4:
			dicFun[direccion] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1800, variables.get(v).get("tam")]

	#Inicializa las variables con un valor default y las guarda en la lista de variables por tipo, de funciones.
	for k in dicFun:
		if dicFun.get(k)[0] == 0:
			varFun[dicFun.get(k)[0]].append(0)
			for i in range(1, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(0)
		elif dicFun.get(k)[0] == 1:
			varFun[dicFun.get(k)[0]].append(0.0)
			for i in range(1, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(0.0)
		elif dicFun.get(k)[0] == 2:
			varFun[dicFun.get(k)[0]].append('')
			for i in range(1, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append('')
		elif dicFun.get(k)[0] == 3:
			varFun[dicFun.get(k)[0]].append("")
			for i in range(1, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append("")
		elif dicFun.get(k)[0] == 4:
			varFun[dicFun.get(k)[0]].append(False)
			for i in range(1, dicFun.get(k)[2]):
				varFun[dicFun.get(k)[0]].append(False)
	funcMem.append([dicFun, varFun]) #Guarda las funciones actuales que se estan usando el [ diccionario de variables y
									 #la lista de variables de la función ], temporalmente
									 #funcMen = [ [ dic[direccion]=[tipo,posicion], varFun=[[valor,valor,...],[valor]..] ],  [ dic[direccion]=[tipo,posicion], varFun =[[valor,valor,...],[valor]..] ] ]

##########################################################################
#	scoper(direc)
# 	Vericfica de que tipo e una variable, local o global
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
	elif(isinstance(direc, list)):
		return funcMen[Scope][1][direc[0]][direc[1]]

	return direc

def asignarTemporales(valor, direc):
	#print(direc)
	temporales[direc - 2000] = valor

def asignarParametros(valor, param):
	pos = int(param[5:])
	#print(pos, listFun)
	func = diccionario_metodos.get(listFun[len(listFun) - 1])
	func = func.get("vars")
	for v in func:
		if func.get(v).get("posicion") == pos:
			direc = func.get(v).get("direccionMemoria")
	lista = funcMem[Scope + 1][0].get(direc)
	funcMem[Scope + 1][1][lista[0]][lista[1]] = valorDireccion(valor)

# Método principal
def main():
	pass
    #print "\n\n", Parser.diccionario_metodos

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
			#print(val2, val4)
			res1 = valorDireccion(val2)
			var = scopeVar(val4)
			#print (res1, var, dicGlobal.get(val4),funcMem[Scope][0].get(val4))
			if var == 0:
				lista = dicGlobal.get(val4)
				if retorno is not None:
					varGlobales[lista[0]][lista[1]] = retorno
					retorno = None
				else:
					varGlobales[lista[0]][lista[1]] = res1
			elif var == 1:
				lista = funcMem[Scope][0].get(val4)
				varsFun = funcMem[Scope][1]
				if retorno is not None:
					varsFun[lista[0]][lista[1]] = retorno
					retorno = None
				else:
					varsFun[lista[0]][lista[1]] = res1
				funcMem[Scope][1] = varsFun
			elif(isinstance(valorDireccion(val4), list)):
				funcMem[Scope][1][direc[0]][direc[1]] = res1
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
			val = valorDireccion(val4)
			if isinstance(val, list):
				val = funcMem[Scope][1][val[0]][val[1]]
			print val

		elif cuadruplo[0] == 'GOTOFc':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'GOTOFi':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'GOTO':
			cuadruploActual = val4 - 2

		elif cuadruplo[0] == 'RETURN':
			retorno = valorDireccion(val4)
			cuadruploActual = cuadruploActual

		elif cuadruplo[0] == 'ERA':
			memoriaFuncion(val2)

		elif cuadruplo[0] == 'PARAM':
			asignarParametros(val2, val4)

		elif cuadruplo[0] == 'GOSUB':
			listPos.append(cuadruploActual + 1)
			cuadruploActual = val2 - 1
			Scope = Scope + 1

		elif cuadruplo[0] == 'ENDPROC':
			#print(funcMem)
			Scope = Scope - 1
			funcMem.pop()
			listFun.pop()
			if(len(listFun) > 0):
				funcAct = listFun[len(listFun) - 1]
			if not len(listPos) == 0:
				cuadruploActual = listPos.pop() - 1
		elif cuadruplo[0] == 'VAL':
			if funcMem[Scope][0].get(val2)[2] > 0:
				asignarTemporales(True, val4)
			else:
				print "Error variable tratada de accesar como arreglo"
				sys.exit(1)
		elif cuadruplo[0] == 'VER':
			pos = valorDireccion(val3)
			if pos > -1 and pos < funcMem[Scope][0].get(val2)[2]:
				asignarTemporales(pos, val4)
			else:
				print "Indice fuera de los limites en arreglo"
				sys.exit(1)
		elif cuadruplo[0] == 'RES':
			lista = funcMem[Scope][0].get(val2)
			direc = [lista[0],lista[1] + valorDireccion(val3)]
			asignarTemporales(direc, val4)

		elif cuadruplo[0] == 'END':
			cuadruploActual = cuadruploActual
		#if cuadruplo[0] != 'GOTO' and cuadruplo[0] != 'GOTOFc' and cuadruplo[0] != 'GOTOFi' :
		cuadruploActual = cuadruploActual + 1

'''if __name__ == "__main__":
    main()
    operacionCuadruplos(Parser.lista_cuadruplos)'''

# operacionCuadruplos(lista_cuadruplos)
# print variables.keys()
# print lista_cuadruplos[1]

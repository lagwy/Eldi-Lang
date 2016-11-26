# -*- coding: utf-8 -*-
import Parser

# Listas y diccionarios de pruebas
cuadruplos = []
dicGlobal = {}
dicMetodos = {}
varGlobales = [[],[],[],[],[]]
temporales = []
dicMain =  {}
varMain = [[],[],[],[],[]]
listPos = []
funcMem = []
Scope = 0

constantes_int = Parser.constantes_int
constantes_float = Parser.constantes_float
constantes_char = Parser.constantes_char
constantes_string = Parser.constantes_string
constantes_boolean = Parser.constantes_boolean

##########################################################################
#	memoriaGlobal()
# 	Añadir todas las variables globales a un sólo diccionario
##########################################################################
def memoriaGlobal():
	contInt = 0
	contFloat = 0
	contChar = 0
	contString = 0
	contBoolean = 0
	# print Parser.globales_int
	# print Parser.globales_float
	# print Parser.globales_char
	# print Parser.globales_string
	# print Parser.globales_boolean
	for key in Parser.globales_int:
		dicGlobal[key] = [0, contInt]
		contInt += 1
	for key in Parser.globales_float:
		dicGlobal[key] = [1 , contFloat]
		contFloat += 1
	for key in Parser.globales_char:
		dicGlobal[key] = [2 , contChar]
		contChar += 1
	for key in Parser.globales_string:
		dicGlobal[key] = [3 , contString]
		contString += 1
	for key in Parser.globales_boolean:
		dicGlobal[key] = [4 , contBoolean]
		contBoolean += 1
	# print "diccionario"
	# print "diccionario global ", dicGlobal

##########################################################################
#	memoriaFuncion( funcion )
#	Memoria de una función local
##########################################################################
def memoriaFuncion(funcion):

	dicFun = {}  				#Diccionario de funciones
	varFun = [[],[],[],[],[]]
	func = Parser.diccionario_metodos.get(funcion) #Guarda la funcion temporalmente
	variables = func.get("vars") #Guarda las variables de la funcion temporalmente

	#Recorre todas las varibales de la funcion
	for v in variables:
		# Guarda  dicFun[ nombreVariable ] = [tipo, posicion]
		if variables.get(v).get("type") == 0:
			dicFun[v] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1000]
		elif variables.get(v).get("type") == 1:
			dicFun[v] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1200]
		elif variables.get(v).get("type") == 2:
			dicFun[v] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1400]
		elif variables.get(v).get("type") == 3:
			dicFun[v] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1600]
		elif variables.get(v).get("type") == 4:
			dicFun[v] = [variables.get(v).get("type"),  variables.get(v).get("direccionMemoria") - 1800]
	# Inicializa las variables con un valor default y las guarda en la lista de variables por tipo, de funciones.
	for v in dicFun:
		if dicFun.get(v)[0] == 0:
			varFun[dicFun.get(v)[0]].append(0)
		elif dicFun.get(v)[0] == 1:
			varFun[dicFun.get(v)[0]].append(0.0)
		elif dicFun.get(v)[0] == 2:
			varFun[dicFun.get(v)[0]].append('')
		elif dicFun.get(v)[0] == 3:
			varFun[dicFun.get(v)[0]].append("")
		elif dicFun.get(v)[0] == 4:
			varFun[dicFun.get(v)[0]].append(False)
	# Guarda en Memoria de funcion el diccionario de variables y
	# la lista de variables de la función, temporalmente
	funcMem.append([dicFun, varFun])

##########################################################################
#	scopeVar
#	Regresa el contexto en el que se encuentra una dirección
##########################################################################
def scopeVar(direc):
	if dicGlobal.has_key(direc): #Si encuentra un llave en las variables globales retorna 0
		return 0
	if funcMem[Scope][0].has_key(direc): #Si tienen de llave
		return 1
	else:
		return -1

##########################################################################
#	valorDireccion
#	Obtener el valor que está contenido en una dirección
##########################################################################
def valorDireccion(direc):
	var = scopeVar(direc)
	# Revisa primero por una variable global y después por locales
	if(var == 0):
		lista = dicGlobal.get(direc)
		return varGlobales[lista[0]][lista[1]]
	elif(var > 0):
		lista = funcMem[Scope][0].get(direc)
		return funcMem[Scope][1][lista[0]][lista[1]]
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

##########################################################################
#	asignarTemporales
#	Controlar la generación de temporales
##########################################################################
def asignarTemporales(valor, direc):
	temporales[direc - 2000] = valor

##########################################################################
#	operacionCuadruplos
#	Procesamiento de cada uno de los cuádruplos, termina hasta que el actual
#	sea igual o mayor al tamaño de la lista
##########################################################################
def operacionCuadruplos(lista_cuadruplos, longitud):
	memoriaGlobal()
	memoriaFuncion("main")
	cuadruploActual = 0
	# print cuadruploActual
	# print lista_cuadruplos
	# print len(Parser.getCuadruplos)
	while cuadruploActual <= longitud:
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
			var = scopeVar(var4)
			if var == 0:
				lista = dicGlobal.get(direc)
				varGlobales[lista[0]][lista[1]] = res1
			else:
				lista = funcMem[Scope][0].get(direc)
				varsFun = funcMem[Scope][1]
				varsFun[lista[0]][lista[1]] = res1
				uncMem[Scope][1] = varsFun
		elif cuadruplo[0] == 'READ':
			leer = input()
			asignarTemporales(leer, val4)
		elif cuadruplo[0] == 'PRINT':
			print valorDireccion(val4)
		elif cuadruplo[0] == 'GOTOFc':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 1
		elif cuadruplo[0] == 'GOTOFi':
			if not valorDireccion(val2):
				cuadruploActual = val4 - 1
		elif cuadruplo[0] == 'GOTO':
			cuadruploActual = val4 - 1
		elif cuadruplo[0] == 'RETURN':
			return variables[cuadruplo[3]]
		elif cuadruplo[0] == 'ERA':
			memoriaFuncion(val4)
		elif cuadruplo[0] == 'PARAMETRO':
			asignarParametros(val2)
		elif cuadruplo[0] == 'GOSUB':
			listPos.append(cuadruploActual + 1)
			cuadruploActual = val4 - 1
			Scope = Scope + 1
		elif cuadruplo[0] == 'ENDPROC':
			funcMem.pop()
			Scope = Scope - 1
			cuadruploActual = listPos.pop()
		if cuadruplo[0] <> 'GOTO' and cuadruplo[0] <> 'GOTOFc' and cuadruplo[0] <> 'GOTOFi':
			cuadruploActual = cuadruploActual + 1

##########################################################################
#	main
#	Método principal de la máquina virtual
##########################################################################
def main():
	cuadruplos = Parser.getCuadruplos()
	print operacionCuadruplos(cuadruplos, len(cuadruplos))

if __name__ == "__main__":
    main()

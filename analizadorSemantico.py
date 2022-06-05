from parsing import Parsing
from tokenizer import tokenize
import queue
import re


class AnalisadorSemantico:

    def __init__(self, nombre_archivo):
        self._parsing = Parsing()
        self._lista_tokens = []
        self.lista_errores = []
        self._tokenize(nombre_archivo)

    def _tokenize(self, _nombre_archivo):
        archivo = open(_nombre_archivo, 'r')
        contador_linea = 1
        for linea in archivo.readlines():
            tokens = tokenize(linea)
            self._lista_tokens.append({'linea': contador_linea, 'tokens': tokens})
            contador_linea += 1

    def analizar(self):
        self.parse()
        tabla = self._parsing.obtenerTabla()
        self._analisis_semantico_declaraciones(tabla)
        self._analisis_semantico_identificadores(tabla)
        self._mostrar_errores()

    def parse(self):
        for i in self._lista_tokens:
            linea = i['linea']
            tokens = i['tokens']
            error = self._parsing.parse(tokens, linea)
            if (error != ""):
                self.lista_errores.append(error)

    def analisis_semantico_declaraciones(self, tabla):
        self._analisis_semantico_declaraciones(tabla)

    def _analisis_semantico_identificadores(self, tabla):
        '''
        Verifica que las variables se encuentren declaradas y su ambito sea el correspondiente
        '''
        interes = {'int', 'string', 'float', 'identificador'}
        for tokens in self._lista_tokens:
            if (tokens['tokens']):
                resultado = self._analizador_elementos(tokens['tokens'])

                if resultado == 'ASIGNACION':
                    llave = tabla.buscar_simbolo(
                        tokens['tokens'][0][0])  # verifica que la variable que esta a la izquierda del
                    # operador de asignacion este en la tabla
                    if llave:
                        lista_asignaciones = self._extraer_asignaciones(tokens['tokens'])
                        for asignacion in lista_asignaciones:
                            if asignacion[1] == 'identificador':
                                valor = tabla.buscar_simbolo(
                                    asignacion[0])  # se verifica que la variable que va a ser asignada este en la tabla
                                if valor:
                                    if not valor['tipo'] == llave['tipo']:
                                        salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(
                                            tokens['linea'], valor['tipo'])
                                        self.lista_errores.append(salida)
                            else:  # si no es una variable es un tipo dato primitivo
                                tipo_valor = self._tipo_dato_checker(llave['tipo'], asignacion[0])
                                if not tipo_valor:
                                    salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(
                                        tokens['linea'], llave['tipo'])
                                    self.lista_errores.append(salida)
                    else:
                        salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                     tokens['tokens'][0][0])
                        self.lista_errores.append(salida)

                elif resultado == 'CONDICIONAL':
                    lista_asignaciones = self._extraer_asignaciones(tokens['tokens'])
                    if len(lista_asignaciones) > 1:  # caso en que hayan dos elementos comparados
                        if lista_asignaciones[0][1] == 'identificador' and lista_asignaciones[1][
                            1] == 'identificador':  # caso de que ambos elementos sean variables
                            elemento1 = tabla.buscar_simbolo(lista_asignaciones[0][0])
                            elemento2 = tabla.buscar_simbolo(lista_asignaciones[1][0])
                            if not elemento1 or not elemento2:
                                if not elemento1:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                                 lista_asignaciones[0][
                                                                                                     0])
                                    self.lista_errores.append(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                                 lista_asignaciones[1][
                                                                                                     0])
                                    self.lista_errores.append(salida)
                        elif lista_asignaciones[0][1] == 'identificador' or lista_asignaciones[1][
                            1] == 'identificador':  # caso de que solo haya una variable y el otro sea algun tipo de dato primitivo
                            elemento1 = lista_asignaciones[0]
                            elemento2 = lista_asignaciones[1]
                            if elemento1[1] == 'identificador':
                                encontrado = tabla.buscar_simbolo(elemento1[0])
                                if encontrado:
                                    if not elemento2[1] == encontrado['tipo']:
                                        salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(
                                            tokens['linea'], encontrado['tipo'])
                                        self.lista_errores.append(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                                 elemento1[0])
                                    self.lista_errores.append(salida)
                            else:
                                encontrado = tabla.buscar_simbolo(elemento2[0])
                                if encontrado:
                                    if not elemento1[1] == encontrado['tipo']:
                                        salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(
                                            tokens['linea'], encontrado['tipo'])
                                        self.lista_errores.append(salida)
                                else:
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                                 elemento2[0])
                                    self.lista_errores.append(salida)
                        else:
                            elemento1 = lista_asignaciones[0]
                            elemento2 = lista_asignaciones[1]
                            if not elemento1[1] == elemento2[
                                2]:  # caso de que los datos primitivos no sean del mismo tipo
                                salida = "Error - linea: {}. Comparacion de tipo '{}' incorrecta.".format(
                                    tokens['linea'], elemento1[1])
                                self.lista_errores.append(salida)
                    else:  # en caso de que el condicional solo tenga un elemento dentro
                        if lista_asignaciones[0][1] == 'identificador':  # caso de que ambos elementos sean variables
                            elemento1 = tabla.buscar_simbolo(lista_asignaciones[0][0])
                            if not elemento1:
                                salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                             lista_asignaciones[0][0])
                                self.lista_errores.append(salida)

                elif resultado == 'ASIGNACION_FUNCION':
                    tipos = {'string', 'int', 'float', 'void'}
                    parametros = []
                    if tokens['tokens'][0][0] in tipos:
                        parametros = self._extraer_parametros(tokens['tokens'])

                        for parametro in parametros:
                            if not parametro in tabla.obtener_tabla().keys():
                                salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'], parametro)
                                self.lista_errores.append(salida)
                            else:
                                if tabla.obtener_tabla()[parametro]['ambito'] != 'global':
                                    salida = "Error - linea: {}. '{}' no esta declarado.".format(tokens['linea'],
                                                                                                 parametro)
                                    self.lista_errores.append(salida)

    def _extraer_parametros(self, linea):

        '''
        Utilizado para extraer los parametros que se encuentran entre parentesis en una funcion
        '''
        lista_parametros = []  # se guardan los parametros de la linea de tokens
        parametro_auxiliar = []
        contador_parentesis = 0

        for i in range(0, len(linea) + 1):  # recorre la linea de tokens
            if linea[i][1] == 'parentesis':
                if contador_parentesis < 1:
                    contador_parentesis += 1
                else:  # si el token vuelve a ser un parentesis significa que es el parentesis que cierra
                    lista_parametros += parametro_auxiliar  # lo que este en parametro_auxiliar se agrega a la lista de parametros
                    break
            elif contador_parentesis > 0:
                if linea[i][1] == 'coma':
                    if len(parametro_auxiliar) > 0:
                        lista_parametros.append(parametro_auxiliar)
                        parametro_auxiliar = []
                elif linea[i][
                    1] != 'coma':  # si el token actual no es una coma, es parte del parametro (tipo, identificador, =, valor)
                    parametro_auxiliar.append(linea[i][0])  # se agrega al parameto_auxiliar
        return lista_parametros

    def _extraer_asignaciones(self, linea_token):
        interes = {'identificador', 'int', 'string', 'float'}
        lista_asignaciones = []
        for i in range(0, len(linea_token)):
            if linea_token[i][1] in interes:
                lista_asignaciones.append(linea_token[i])

        return lista_asignaciones

    def _analizador_elementos(self, tokens):
        operador_asignacion = False
        condicional = False
        parentesis_abre = False
        parentesis_cierra = False
        palabra_tipo = False

        for token in tokens:
            if token[1] == 'tipo':
                palabra_tipo = True
            if token[1] == 'asignacion':
                operador_asignacion = True
            if token[1] == 'parentesis':
                if token[0] == '(':
                    parentesis_abre = True
                else:
                    parentesis_cierra = True
            if token[1] == 'condicicional':
                condicional = True

        if condicional and parentesis_abre:
            return 'CONDICIONAL'
        elif operador_asignacion and parentesis_abre:
            return 'ASIGNACION_FUNCION'
        elif operador_asignacion and not palabra_tipo:
            return 'ASIGNACION'
        else:
            return 'NONE'

    def _analisis_semantico_declaraciones(self, tabla):
        '''
        Verifica que las asignaciones sean del mismo tipo en las declaraciones
        '''

        errores = queue.Queue()

        for key, value in tabla.obtener_tabla().items():
            tipo = value['tipo']
            valor = value['valor']
            if valor:
                if self._tipo_dato_checker(tipo, valor):
                    continue
                else:
                    if valor in tabla.obtener_tabla():
                        elemento_tabla = tabla.obtener_tabla()[valor]
                        if tipo == elemento_tabla['tipo']:
                            continue
                        else:
                            errores.put(value)
                    else:
                        errores.put(value)
        if not errores.empty():
            while not errores.empty():
                value = errores.get()
                salida = "Error - linea: {}. Asignacion de tipo '{}' incorrecta.".format(value['linea'], value['tipo'])
                self.lista_errores.append(salida)

    def _obtener_tabla(self):
        return self._parsing.obtenerTabla()

    def _tipo_dato_checker(self, tipo, valor):
        if tipo == 'int':
            return self._verifica_int(valor)
        elif tipo == 'float':
            return self._verifica_float(valor)
        elif tipo == 'string':
            return self._verifica_string(valor)

    def _verifica_int(self, int):
        return int.isdigit()

    def _verifica_float(self, entrada):
        try:
            float(entrada)
            return True
        except ValueError:
            return False

    def _verifica_string(self, entrada):
        token = re.compile(r'"[a-zA-Z0-9_]*"')
        objeto_encontrado = token.match(entrada)
        if objeto_encontrado:
            return True
        return False

    def _mostrar_errores(self):
        print()
        if len(self.lista_errores) > 0:
            for error in self.lista_errores:
                print(error)
        else:
            print("El programa se encuentra libre de errores!")
        print()

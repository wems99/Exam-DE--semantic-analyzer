from tablaSimbolos import TablaSimbolos
import queue


class Parsing():

    # Clase encargada clasificar los tokens recibidos segun la tabla de simbolos
    def __init__(self):
        self._pila = queue.LifoQueue()
        self._pila.put("global")
        self._tabla_simbolos = TablaSimbolos()

    def parse(self, tokens, linea):
        if tokens:
            resultado = self._analizador_elementos(tokens)
            if resultado == 'RETURN':
                return self._return(tokens, linea)

            elif resultado == 'ASIGNACION_FUNCION':
                self._asignacion_funcion(tokens, linea)

            elif resultado == 'DECLARACION_VARIABLE':
                self._declaracion_variable(tokens, linea)

            elif resultado == 'FUNCION':
                self._funcion(tokens, linea)

            elif resultado == "CIERRA_AMBITO":
                self._pila.get()

            elif resultado == 'CONDICIONAL':
                ambito = 'condicional_' + tokens[0][0]
                self._pila.put(ambito)
        return ""

    def _asignacion_funcion(self, tokens, linea):
        # verifica si la variable ya estaba declarada antes

        tipos = {'string', 'int', 'float', 'void'}
        tipo = None
        identificador = None
        valor = None
        ambito = self._pila.get()
        self._pila.put(ambito)

        if tokens[0][0] in tipos:  # token[0][0] varible no declarada
            tipo = tokens[0][0]
            identificador = tokens[1][0]
        else:
            tipo = tokens[0][0]
            identificador = tokens[1][0]

        valor_retorno_funcion = self._tabla_simbolos.obtener_tabla()
        valor_retorno_funcion = valor_retorno_funcion[tokens[3][0]]['tipo']

        if valor_retorno_funcion == 'string':
            valor = '"a"'
        elif valor_retorno_funcion == 'int':
            valor = 0
        elif valor_retorno_funcion == 'float':
            valor = 0.0
        elif valor_retorno_funcion == 'void':
            valor = None

        valor = {'tipo': tipo, 'valor': valor, 'linea': linea, 'ambito': ambito}
        self._tabla_simbolos.agregar_simbolo(identificador, valor)

    def imprimir_tabla(self):
        self._tabla_simbolos.imprimir()

    def _analizador_elementos(self, tokens):

        # Forma pensada para identificar el tipo de linea de codigo leida (parametro tokenaisado)

        llaves_abre = False
        llaves_cierra = False
        palabra_tipo = False
        operador_asignacion = False
        condicional = False
        parentesis_abre = False
        parentesis_cierra = False
        _return = False

        for token in tokens:
            if token[1] == 'return':
                _return = True
            if token[1] == 'tipo':
                palabra_tipo = True
            if token[1] == 'asignacion':
                operador_asignacion = True
            if token[1] == 'parentesis':
                if token[0] == '(':
                    parentesis_abre = True
                else:
                    parentesis_cierra = True
            if token[1] == 'llave':
                if token[0] == '{':
                    llaves_abre = True
                else:
                    llaves_cierra = True
            if token[1] == 'condicicional':
                condicional = True
        if _return:
            return 'RETURN'
        elif operador_asignacion and not parentesis_abre and palabra_tipo:
            return 'DECLARACION_VARIABLE'
        elif operador_asignacion and parentesis_abre and not condicional:
            return 'ASIGNACION_FUNCION'
        elif parentesis_abre and operador_asignacion and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and not condicional and palabra_tipo:
            return 'FUNCION'
        elif parentesis_abre and condicional:
            return 'CONDICIONAL'
        elif operador_asignacion and not palabra_tipo and not condicional:
            return 'ASIGNACION'
        elif llaves_cierra:
            return 'CIERRA_AMBITO'
        else:
            return 'NONE'

    def _declaracion_variable(self, tokens, linea):
        tipo = tokens[0][0]
        identificador = tokens[1][0]
        valor = None
        if len(tokens) > 2:
            valor = tokens[3][0]
        ambito = self._pila.get()
        self._pila.put(ambito)
        valor = {'tipo': tipo, 'valor': valor, 'linea': linea, 'ambito': ambito}
        self._tabla_simbolos.agregar_simbolo(identificador, valor)

    def _declaracion_funcion(self, tokens, linea):
        opciones_tipo = {'string', 'int', 'float', 'void'}
        if tokens[0][0] in opciones_tipo:
            pass

    def _return(self, tokens, linea):
        if len(tokens) > 1:
            elemento_retornado = tokens[1]
            if elemento_retornado[1] == 'identificador':
                elemento_en_tabla = self._tabla_simbolos.buscar_simbolo(elemento_retornado[0])
                if elemento_en_tabla:
                    ambito = self.obtenerAmbitoUltimaFuncion()
                    funcion = self._tabla_simbolos.buscar_simbolo(ambito)
                    if not elemento_en_tabla['tipo'] == funcion['tipo']:
                        salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(
                            linea, ambito)
                        return salida
                else:
                    salida = "Error - linea: {}. '{}' no esta declarado.".format(linea, elemento_retornado[0])
                    print(salida)
            else:
                ambito = self.obtenerAmbitoUltimaFuncion()
                funcion = self._tabla_simbolos.buscar_simbolo(ambito)
                if not elemento_retornado[1] == funcion['tipo']:
                    salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(linea,
                                                                                                                  ambito)
                    return salida
        else:
            ambito = self._pila.get()
            self._pila.put(ambito)
            funcion = self._tabla_simbolos.buscar_simbolo(ambito)
            if not funcion['tipo'] == 'void':
                salida = "Error - linea: {}. Valor de retorno no coincide con la declaracion de '{}'.".format(linea,
                                                                                                              ambito)
                return salida
        return ""

    def _funcion(self, tokens, linea):
        tipo = tokens[0][0]
        identificador = tokens[1][0]
        ambito = self._pila.get()
        self._pila.put(ambito)
        valor = {'tipo': tipo, 'valor': None, 'linea': linea, 'ambito': ambito}
        self._tabla_simbolos.agregar_simbolo(identificador, valor)

        ambito = identificador
        self._pila.put(ambito)

        parametros = self._extraer_parametros(tokens)

        while len(parametros) > 0:
            parametro = parametros.pop(0)
            tipo = parametro[0]
            identificador = parametro[1]
            valor = None
            if len(parametro) > 2:
                valor = parametro[4]
            ambito = self._pila.get()
            self._pila.put(ambito)
            valor = {'tipo': tipo, 'valor': valor, 'linea': linea, 'ambito': ambito}
            self._tabla_simbolos.agregar_simbolo(identificador, valor)

    def _extraer_parametros(self, linea):

        lista_parametros = []  # lista utilizada para guardan los parametros de la linea de token
        parametro_auxiliar = []
        contador_parentesis = 0

        for i in range(0, len(linea) + 1):  # recorre la linea de tokens
            if linea[i][1] == 'parentesis':
                if contador_parentesis < 1:
                    contador_parentesis += 1
                else:  # simple, si es parentesis denuevo, entonces cierra
                    lista_parametros.append(parametro_auxiliar)  # lo que este en parametro_auxiliar se agrega a la
                    # lista de parametros
                    break
            elif contador_parentesis > 0:
                # si el token es una "," todo dentro parametro_auxiliar es agregado a una lista de parametros
                if linea[i][1] == 'coma':
                    if len(parametro_auxiliar) > 0:
                        lista_parametros.append(parametro_auxiliar)
                        parametro_auxiliar = []
                elif linea[i][1] != 'coma':  # si el token actual no es ",", es parte del parametro (tipo,
                    # identificador, # =, valor)
                    parametro_auxiliar.append(linea[i][0])
        return lista_parametros

    def obtenerTabla(self):
        return self._tabla_simbolos

    def obtenerAmbitoUltimaFuncion(self):
        # validacion de ambitos como condicionales, funcion hecha para obtenr el ultimo ambito no condicional

        ultima_funcion = None
        cola_ambitos = queue.LifoQueue()
        ambito_extraido = self._pila.get()
        cola_ambitos.put(ambito_extraido)

        while 'condicional' in ambito_extraido:
            ambito_extraido = self._pila.get()
            cola_ambitos.put(ambito_extraido)

        ultima_funcion = ambito_extraido

        while not cola_ambitos.empty():
            self._pila.put(cola_ambitos.get())

        return ultima_funcion

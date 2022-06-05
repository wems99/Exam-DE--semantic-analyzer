import re


def tokenize(linea: str):
    expresiones_regulares = [
        (re.compile(r"(if|while)"), "condicicional"),
        (re.compile(r"(return)"), 'return'),
        (re.compile(r"(void|int|float|string)"), "tipo"),
        (re.compile(r"^[a-zA-Z_][a-zA-Z0-9_]*"), "identificador"),
        (re.compile(r'"[a-zA-Z0-9_]*"'), "string"),
        (re.compile(r"^[0-9]+.[0-9]+"), "float"),
        (re.compile(r"^[0-9]+"), "int"),
        (re.compile(r"^[+*/-]"), "operador_aritmetico"),
        (re.compile(r"^[><]|=="), "operador_logico"),
        (re.compile(r"^="), "asignacion"),
        (re.compile(r"^,"), "coma"),
        (re.compile(r"^[()]"), "parentesis"),
        (re.compile(r"^[{}]"), "llave"),
    ]

    tokens = []

    while len(linea):
        linea = linea.lstrip()

        matched = False

        for token, tipo in expresiones_regulares:
            objeto_encontrado = token.match(linea)
            if objeto_encontrado:
                matched = True
                token = (objeto_encontrado.group(0), tipo)
                tokens.append(token)
                linea = linea.replace(token[0], '', 1)
                linea = linea.lstrip()
                break
        if not matched:
            return
    return tokens

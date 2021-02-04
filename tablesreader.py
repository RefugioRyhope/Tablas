#! python
# -*- coding: utf-8 -*-
import random
import re
import os
from dice import roll
import sys
import inspect

tables_path = "Tablas"

class Response:
    def __init__(self, message="", data=None):
        self.message = message
        self.data = data

class Table:
    def __init__(self, index, system, filename):
        self.index = index
        self.system = system
        self.filename = filename

def rt(chosen_table):

    table_name = chosen_table.filename.replace(".txt", "")
    valid_string = re.search(r"^[a-zA-Z_\sñ0-9]*$", table_name)

    if not valid_string:
        return Response(message="Invalid string", data="")

    table_path= tables_path + "/" + chosen_table.system + "/" + table_name + ".txt"

    with open(table_path, encoding="utf-8", errors="ignore") as f:
        elements = [line.rstrip() for line in f]

    return Response(message="Resultados para '" + table_name + "':", data=random.choice(elements))

def get_tables_by_list(tables, wanted_tables):
    return_tables = []

    for table in tables:
        for wanted_table in wanted_tables:
            if table.index == int(wanted_table):
                return_tables.append(table)
    
    return return_tables

def get_tables(path=tables_path):
    directories = os.listdir(path)
    cont = 0

    tables_to_return = []

    for directory in directories:
        tables = os.listdir(path + "/" + directory)
        for table in tables:
            if ".txt" in table:
                tables_to_return.append(Table(cont, directory.split("/")[-1], table.replace(".txt", "")))
                cont += 1

    return tables_to_return

#lt [filtro]: lista todas las tablas. Si se especifica un filtro, solo se mostrarán aquellas tablas/sistemas cuyo nombre contenga el filtro especificado. Ejemplo: "lt" mostrará todas las tablas. "lt tarot" muestra todas las tablas o sistemas que contengan la palabra tarot
def lt(tables, *argv):
    tables_to_return = []
    
    if len(argv) == 0:
        return Response(message="Tablas disponibles:", data=tables)

    for table in tables:
        flag = True
        for filterstring in argv:
            if filterstring.lower() not in table.system.lower() and filterstring.lower() not in table.filename.lower():
                flag = False
        if flag:
            tables_to_return.append(table)

    return Response(message="Tablas encontradas:", data=tables_to_return)

#rtn número: obtén un elemento aleatorio de la tabla con el número especificado. Este número puede consultarse cuando se listan o buscan tablas. Ejemplo "rtn 1" hará una tirada en la tabla 1
def rtn(tables, table_number):

    valid_number = re.search(r"\d+", str(table_number))

    if not valid_number or int(table_number) < 0:
        return Response(message="Número no válido", data=None)

    if int(table_number) >= len(tables):
        return Response(message="No hay ninguna tabla con ese número", data=None)

    table = tables[int(table_number)]
    
    return rt(table)

#rts nombre: busca el nombre de la tabla o sistemas. Si solo hay una tabla con que contenga ese nombre, elegirá un elemento de ella. Ejemplo: "rts carta"
def rts(tables, search_string):

    matches = [s for s in tables if search_string.lower() in s.filename.lower()]

    if len(matches) == 0:
        return Response(message="No tables found", data=None)

    if len(matches) > 1:
        return Response(message="Multiple tables found", data=matches)

    if len(matches) == 1:
        response = rt(matches[0])

        if response.message == "":
            response.message = "Table found" + matches[0][2]

        return response

#r XdY: lanza X dados de Y caras cada uno. Ejemplo: "r 2d6" lanzará 2 dados de 6 caras
def r(tables, string):
    results = roll(string)
    minimum = None
    maximum = None
    total = 0

    if isinstance(results, int):
        return Response(message="", data=results)

    for dice in results:
        if minimum == None and maximum == None:
            minimum = dice
            maximum = dice
        
        if dice < minimum:
            minimum = dice
        if dice > maximum:
            maximum = dice

        total += dice

    return Response(message="", data=str(results) + "\n\nMinimum=" + str(minimum) + ", Maximum=" + str(maximum) + ", total=" + str(total))

#ayuda: Imprime esta ayuda
def ayuda():
    print("Comandos disponibles:\n")
    this_module = sys.modules[__name__]
    module_functions= inspect.getmembers(this_module, inspect.isfunction)

    text = ""
    for funcion in module_functions:
        ayuda = inspect.getcomments(funcion[1])
        if ayuda != None:
            text += "-" + ayuda.replace("#", "")

    return Response(message="", data=text)

def allowed_function(my_function):
    allowed = inspect.getcomments(my_function) 
    
    if allowed != None:
        return True

    return False

def dynamic_call(tables, call):
    this_module = sys.modules[__name__]
    module_functions = inspect.getmembers(this_module, inspect.isfunction)
    function = call.split(" ")[0].lower()
    parameters = call.split(" ")[1:]
    parameters.insert(0, tables)

    if function not in [x[0] for x in module_functions]:
        response = ayuda()
        response.message = "Orden no encontrada. Por favor, consulta la ayuda:"
        return response
    
    to_be_executed = getattr(this_module, function)

    if not allowed_function(to_be_executed):
        response = ayuda()
        response.message = "Orden incorrecta. Por favor, consulta la ayuda:"
        return response

    return to_be_executed(*parameters)
from tablesreader import *

def print_data(data):
    if isinstance(data, str):
        print(data)
        return
    if isinstance(data, list):
        for table in data:
            if isinstance(table, Table):
                print(str(table.index) + ": (" + table.system + ") " + table.filename)
    
    print("")

def main():
    print("Bienvenido al programa de tablas aleatorias")
    tables = get_tables()
    print(ayuda().data)
    while(1):
        print("Qué quieres hacer?:")
        command = input()
        datos = dynamic_call(tables, command)
        print(datos.message)
        print_data(datos.data)

if __name__ == "__main__":
    main()


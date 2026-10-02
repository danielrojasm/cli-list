import csv
import os

ARCHIVO_TAREAS = "todos.csv"

todos = []
stop = False


def get_todos():
    return todos


def add_one_task(title):
    titulo = title.strip()
    if not titulo:
        print("El titulo de la tarea no puede estar vacio.")
        return False
    todos.append(titulo)
    return True


def print_list():
    if not todos:
        print("No hay tareas pendientes.")
        return
    for posicion, titulo in enumerate(todos, start=1):
        print(f"{posicion}. {titulo}")


def delete_task(number_to_delete):
    # Las posiciones que ve el usuario empiezan en 1
    try:
        posicion = int(number_to_delete)
    except (TypeError, ValueError):
        print("Debes indicar un numero valido.")
        return None
    if posicion < 1 or posicion > len(todos):
        print(f"No existe una tarea en la posicion {posicion}.")
        return None
    return todos.pop(posicion - 1)


def save_todos(ruta_archivo=ARCHIVO_TAREAS):
    with open(ruta_archivo, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.writer(archivo)
        for titulo in todos:
            escritor.writerow([titulo])
    return len(todos)


def load_todos(ruta_archivo=ARCHIVO_TAREAS):
    if not os.path.exists(ruta_archivo):
        print(f"No se encontro el archivo {ruta_archivo}.")
        return 0
    with open(ruta_archivo, newline="", encoding="utf-8") as archivo:
        cargadas = [fila[0] for fila in csv.reader(archivo) if fila and fila[0].strip()]
    # Se reemplaza en el mismo objeto para que otras referencias a `todos` sigan siendo validas
    todos[:] = cargadas
    return len(todos)


MENU = """
Elige una opcion:
    1. Agregar una tarea
    2. Eliminar una tarea
    3. Mostrar la lista de tareas
    4. Guardar tareas en todos.csv
    5. Cargar tareas desde todos.csv
    6. Salir
"""

# Este codigo solo se ejecuta si el archivo de entrada es app.py
if __name__ == "__main__":
    while not stop:
        print(MENU)
        opcion = input().strip()
        if opcion == "1":
            titulo = input("Titulo de la tarea: ")
            if add_one_task(titulo):
                print(f"Tarea agregada: {titulo.strip()}")
        elif opcion == "2":
            print_list()
            numero = input("Numero de la tarea a eliminar: ")
            eliminada = delete_task(numero)
            if eliminada is not None:
                print(f"Tarea eliminada: {eliminada}")
        elif opcion == "3":
            print_list()
        elif opcion == "4":
            cantidad = save_todos()
            print(f"{cantidad} tarea(s) guardada(s) en {ARCHIVO_TAREAS}.")
        elif opcion == "5":
            if os.path.exists(ARCHIVO_TAREAS):
                cantidad = load_todos()
                print(f"{cantidad} tarea(s) cargada(s) desde {ARCHIVO_TAREAS}.")
            else:
                print(f"No se encontro el archivo {ARCHIVO_TAREAS}.")
        elif opcion == "6":
            print("Hasta luego!")
            stop = True
        else:
            print("Opcion invalida, intenta de nuevo.")

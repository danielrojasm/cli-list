import contextlib
import io
import os
import tempfile
import unittest

import app


class PruebasListaDeTareas(unittest.TestCase):
    def setUp(self):
        app.todos.clear()
        self.carpeta_tmp = tempfile.TemporaryDirectory()
        self.ruta_csv = os.path.join(self.carpeta_tmp.name, "todos.csv")

    def tearDown(self):
        self.carpeta_tmp.cleanup()

    def salida_de(self, func, *args):
        buffer = io.StringIO()
        with contextlib.redirect_stdout(buffer):
            func(*args)
        return buffer.getvalue()

    def test_agregar_tarea(self):
        app.add_one_task("Llamar al proveedor")
        app.add_one_task("Revisar entregas")
        self.assertEqual(app.get_todos(), ["Llamar al proveedor", "Revisar entregas"])

    def test_tarea_vacia_es_rechazada(self):
        self.salida_de(app.add_one_task, "   ")
        self.assertEqual(app.todos, [])

    def test_mostrar_lista_con_posiciones(self):
        app.add_one_task("A")
        app.add_one_task("B")
        self.assertEqual(self.salida_de(app.print_list), "1. A\n2. B\n")

    def test_mostrar_lista_vacia(self):
        self.assertIn("No hay tareas", self.salida_de(app.print_list))

    def test_eliminar_tarea_por_posicion(self):
        for titulo in ["A", "B", "C"]:
            app.add_one_task(titulo)
        self.assertEqual(app.delete_task(2), "B")
        self.assertEqual(app.todos, ["A", "C"])
        self.assertEqual(app.delete_task("1"), "A")
        self.assertEqual(app.todos, ["C"])

    def test_eliminar_posicion_invalida(self):
        app.add_one_task("A")
        for invalida in [0, 2, -1, "abc"]:
            self.salida_de(app.delete_task, invalida)
        self.assertEqual(app.todos, ["A"])

    def test_guardar_y_cargar(self):
        titulos = ["Simple", "Con, coma", 'Con "comillas"']
        for titulo in titulos:
            app.add_one_task(titulo)
        app.save_todos(self.ruta_csv)
        app.todos.clear()
        self.assertEqual(app.load_todos(self.ruta_csv), 3)
        self.assertEqual(app.todos, titulos)

    def test_cargar_reemplaza_lista_actual(self):
        app.add_one_task("Guardada")
        app.save_todos(self.ruta_csv)
        app.add_one_task("Sin guardar")
        app.load_todos(self.ruta_csv)
        self.assertEqual(app.todos, ["Guardada"])

    def test_cargar_archivo_inexistente(self):
        app.add_one_task("A")
        inexistente = os.path.join(self.carpeta_tmp.name, "no_existe.csv")
        self.salida_de(app.load_todos, inexistente)
        self.assertEqual(app.todos, ["A"])


if __name__ == "__main__":
    unittest.main()

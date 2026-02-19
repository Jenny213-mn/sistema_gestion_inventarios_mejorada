"""
Sistema de Gestión de Inventarios Mejorado
Autor/a: Jenny Manzano
Descripción: Proyecto académico que implementa persistencia en archivos
y manejo de excepciones en Python.
"""

import os

# ==============================
# CLASE PRODUCTO
# ==============================
class Producto:
    """
    Representa un producto dentro del inventario.
    """

    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto
        self.nombre = nombre
        self.cantidad = cantidad
        self.precio = precio

    def to_line(self):
        """
        Convierte el producto en una línea de texto
        para guardarlo en el archivo.
        """
        return f"{self.id_producto},{self.nombre},{self.cantidad},{self.precio}"

    @staticmethod
    def from_line(linea):
        """
        Convierte una línea del archivo en un objeto Producto.
        Maneja posibles errores de formato.
        """
        try:
            id_producto, nombre, cantidad, precio = linea.strip().split(",")
            return Producto(id_producto, nombre, int(cantidad), float(precio))
        except ValueError:
            raise ValueError("Línea corrupta en el archivo.")


# ==============================
# CLASE INVENTARIO
# ==============================
class Inventario:
    """
    Gestiona los productos y la persistencia en archivo.
    """

    def __init__(self, archivo="inventario.txt"):
        self.archivo = archivo
        self.productos = {}
        self.cargar_desde_archivo()

    def cargar_desde_archivo(self):
        """
        Carga productos desde el archivo.
        Si el archivo no existe, lo crea automáticamente.
        """
        try:
            if not os.path.exists(self.archivo):
                open(self.archivo, "w").close()
                print("📁 Archivo creado automáticamente.")

            with open(self.archivo, "r") as f:
                for linea in f:
                    try:
                        producto = Producto.from_line(linea)
                        self.productos[producto.id_producto] = producto
                    except ValueError:
                        print("⚠ Se encontró una línea corrupta y fue ignorada.")

            print("✅ Inventario cargado correctamente.")

        except PermissionError:
            print("❌ No tienes permisos para leer el archivo.")
        except Exception as e:
            print(f"❌ Error inesperado al cargar archivo: {e}")

    def guardar_en_archivo(self):
        """
        Guarda todos los productos en el archivo.
        """
        try:
            with open(self.archivo, "w") as f:
                for producto in self.productos.values():
                    f.write(producto.to_line() + "\n")
            print("💾 Cambios guardados correctamente.")
        except PermissionError:
            print("❌ No tienes permisos para escribir en el archivo.")
        except Exception as e:
            print(f"❌ Error al guardar: {e}")

    def agregar_producto(self, id_producto, nombre, cantidad, precio):
        if id_producto in self.productos:
            print("❌ El producto ya existe.")
            return

        self.productos[id_producto] = Producto(id_producto, nombre, cantidad, precio)
        self.guardar_en_archivo()
        print("✅ Producto agregado correctamente.")

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto not in self.productos:
            print("❌ Producto no encontrado.")
            return

        if cantidad is not None:
            self.productos[id_producto].cantidad = cantidad
        if precio is not None:
            self.productos[id_producto].precio = precio

        self.guardar_en_archivo()
        print("✅ Producto actualizado.")

    def eliminar_producto(self, id_producto):
        if id_producto not in self.productos:
            print("❌ Producto no encontrado.")
            return

        del self.productos[id_producto]
        self.guardar_en_archivo()
        print("🗑 Producto eliminado.")

    def mostrar_inventario(self):
        if not self.productos:
            print("📭 Inventario vacío.")
            return

        print("\n======= INVENTARIO =======")
        for p in self.productos.values():
            print(f"ID: {p.id_producto} | "
                  f"Nombre: {p.nombre} | "
                  f"Cantidad: {p.cantidad} | "
                  f"Precio: ${p.precio:.2f}")
        print("===========================")


# ==============================
# INTERFAZ DE USUARIO
# ==============================
def menu():
    inventario = Inventario()

    while True:
        print("\n===== SISTEMA DE INVENTARIO =====")
        print("1. Agregar producto")
        print("2. Actualizar producto")
        print("3. Eliminar producto")
        print("4. Mostrar inventario")
        print("5. Salir")

        opcion = input("Seleccione una opción: ")

        try:
            if opcion == "1":
                id_producto = input("ID: ")
                nombre = input("Nombre: ")
                cantidad = int(input("Cantidad: "))
                precio = float(input("Precio: "))
                inventario.agregar_producto(id_producto, nombre, cantidad, precio)

            elif opcion == "2":
                id_producto = input("ID del producto: ")
                cantidad = input("Nueva cantidad (Enter para omitir): ")
                precio = input("Nuevo precio (Enter para omitir): ")

                inventario.actualizar_producto(
                    id_producto,
                    int(cantidad) if cantidad else None,
                    float(precio) if precio else None
                )

            elif opcion == "3":
                id_producto = input("ID del producto: ")
                inventario.eliminar_producto(id_producto)

            elif opcion == "4":
                inventario.mostrar_inventario()

            elif opcion == "5":
                print("👋 Saliendo del sistema...")
                break

            else:
                print("❌ Opción inválida.")

        except ValueError:
            print("❌ Error: Debes ingresar valores numéricos válidos.")
        except Exception as e:
            print(f"❌ Error inesperado: {e}")


if __name__ == "__main__":
    menu()

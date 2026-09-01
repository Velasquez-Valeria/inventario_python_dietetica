"""Operaciones sobre el inventario: agregar, mostrar, actualizar, eliminar,
generar reportes y buscar productos.
"""

from colorama import Fore, Style
from tabulate import tabulate

from . import database
from .utils import (
    confirmar,
    formatear_texto,
    leer_entero,
    leer_flotante,
    leer_texto,
    mostrar_advertencia,
    mostrar_error,
    mostrar_exito,
    mostrar_info,
    volver_al_menu,
)

ENCABEZADOS = ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"]
LIMITE_STOCK_BAJO = 5


def agregar_producto() -> None:
    """Permite agregar un producto al inventario."""
    while True:
        try:
            mostrar_info(
                "\n\tAgregar Producto - Puedes escribir 'salir' en cualquier campo para volver al menú."
            )

            nombre = leer_texto("\n\tNombre del producto: ")
            if nombre is None:
                return
            nombre = formatear_texto(nombre)

            descripcion = leer_texto("\tDescripción del producto: ")
            if descripcion is None:
                return
            descripcion = formatear_texto(descripcion)

            cantidad = leer_entero("\tCantidad del producto: ")
            if cantidad is None:
                return

            precio = leer_flotante("\tPrecio del producto: ")
            if precio is None:
                return

            categoria = leer_texto("\tCategoría del producto: ")
            if categoria is None:
                return
            categoria = formatear_texto(categoria)

            datos = [
                ["NOMBRE", "DESCRIPCIÓN", "CANTIDAD", "PRECIO", "CATEGORÍA"],
                [nombre, descripcion, cantidad, f"${precio:.2f}", categoria],
            ]
            mostrar_info("\n\tVerifica la información antes de guardar:")
            print(tabulate(datos, headers="firstrow", tablefmt="grid", stralign="center", numalign="right"))

            if confirmar("\n\t¿Deseas guardar este producto? (s/n): "):
                with database.obtener_conexion() as conexion:
                    conexion.execute(
                        """
                        INSERT INTO productos (nombre, descripcion, cantidad, precio, categoria)
                        VALUES (?, ?, ?, ?, ?)
                        """,
                        (nombre, descripcion, cantidad, precio, categoria),
                    )
                mostrar_exito(f"\n\tProducto '{nombre}' agregado exitosamente.")
                print()
                return

            mostrar_advertencia("\n\tProducto descartado. Intenta nuevamente.")
            print()
        except Exception as e:
            mostrar_error(f"\n\tError inesperado: {e}")
            print()


def mostrar_productos() -> None:
    """Muestra todos los productos del inventario, ordenados por cantidad."""
    try:
        with database.obtener_conexion() as conexion:
            productos = conexion.execute(
                "SELECT * FROM productos ORDER BY cantidad ASC"
            ).fetchall()

        if not productos:
            mostrar_advertencia("\n\tEl inventario está vacío.")
            print()
            return

        headers = [Fore.BLUE + h + Style.RESET_ALL for h in ENCABEZADOS]
        filas = []
        for i, producto in enumerate(productos):
            id_, nombre, descripcion, cantidad, precio, categoria = producto
            color = Fore.LIGHTCYAN_EX if i % 2 == 0 else Fore.LIGHTWHITE_EX
            cantidad_texto = f"{Fore.RED}{cantidad}{Style.RESET_ALL}" if cantidad < LIMITE_STOCK_BAJO else cantidad

            filas.append(
                [
                    f"{color}{id_}{Style.RESET_ALL}",
                    f"{color}{formatear_texto(nombre) if nombre else 'N/A'}{Style.RESET_ALL}",
                    f"{color}{formatear_texto(descripcion) if descripcion else 'N/A'}{Style.RESET_ALL}",
                    f"{color}{cantidad_texto}{Style.RESET_ALL}",
                    f"{color}${precio:.2f}{Style.RESET_ALL}",
                    f"{color}{formatear_texto(categoria) if categoria else 'N/A'}{Style.RESET_ALL}",
                ]
            )

        mostrar_info("\nInventario Actual:")
        print(tabulate(filas, headers=headers, tablefmt="grid"))
        print()
    except Exception as e:
        mostrar_error(f"\n\tError: {e}")
        print()


def actualizar_producto() -> None:
    """Actualiza la cantidad disponible de un producto."""
    mostrar_productos()
    while True:
        try:
            mostrar_info(
                "\n\tActualizar producto - Puedes escribir 'salir' en cualquier campo para volver al menú."
            )

            producto_id = leer_entero("\n\tIngresa el ID del producto a actualizar: ")
            if producto_id is None:
                return

            with database.obtener_conexion() as conexion:
                producto = conexion.execute(
                    "SELECT id, nombre, descripcion, cantidad FROM productos WHERE id = ?",
                    (producto_id,),
                ).fetchone()

            if not producto:
                mostrar_error("\n\tID de producto no encontrado.")
                print()
                return

            producto_id, nombre, descripcion, cantidad_actual = producto
            nombre = formatear_texto(nombre) if nombre else "N/A"
            descripcion = formatear_texto(descripcion) if descripcion else "N/A"

            nueva_cantidad = leer_entero("\tNueva cantidad disponible: ")
            if nueva_cantidad is None:
                return

            datos = [
                ["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD ACTUAL", "CANTIDAD NUEVA"],
                [producto_id, nombre, descripcion, cantidad_actual, nueva_cantidad],
            ]
            mostrar_info("\n\tVerifica la información antes de actualizar:")
            print(tabulate(datos, headers="firstrow", tablefmt="grid", stralign="center", numalign="right"))

            if not confirmar("\n\t¿Deseas actualizar la cantidad? (s/n): "):
                mostrar_advertencia("\n\tOperación cancelada. No se realizaron cambios.")
                print()
                return

            with database.obtener_conexion() as conexion:
                cursor = conexion.execute(
                    "UPDATE productos SET cantidad = ? WHERE id = ?",
                    (nueva_cantidad, producto_id),
                )

            if cursor.rowcount > 0:
                mostrar_exito("\n\tCantidad actualizada correctamente.")
            else:
                mostrar_error("\n\tNo se pudo actualizar la cantidad. Verifica el ID.")
            print()
            return

        except Exception as e:
            mostrar_error(f"\n\tError: {e}")
            print()


def eliminar_producto() -> None:
    """Elimina un producto del inventario."""
    mostrar_productos()
    while True:
        try:
            mostrar_info(
                "\n\tEliminar producto - Puedes escribir 'salir' en cualquier campo para volver al menú."
            )

            producto_id = leer_entero("\n\tIngresa el ID del producto a eliminar: ")
            if producto_id is None:
                return

            with database.obtener_conexion() as conexion:
                producto = conexion.execute(
                    "SELECT id, nombre, descripcion, cantidad FROM productos WHERE id = ?",
                    (producto_id,),
                ).fetchone()

            if not producto:
                mostrar_error("\n\tID de producto no encontrado.")
                print()
                return

            datos = [["ID", "NOMBRE", "DESCRIPCIÓN", "CANTIDAD"], list(producto)]
            mostrar_info("\n\tVerifica la información antes de eliminar:")
            print(tabulate(datos, headers="firstrow", tablefmt="grid"))

            if not confirmar("\n\t¿Deseas eliminar este producto? (s/n): "):
                mostrar_advertencia("\n\tOperación cancelada. No se realizaron cambios.")
                print()
                return

            with database.obtener_conexion() as conexion:
                cursor = conexion.execute("DELETE FROM productos WHERE id = ?", (producto_id,))

            if cursor.rowcount > 0:
                mostrar_exito("\n\tProducto eliminado correctamente.")
            else:
                mostrar_error("\n\tNo se pudo eliminar el producto. Verifica el ID.")
            print()
            return

        except Exception as e:
            mostrar_error(f"\n\tError: {e}")
            print()


def reporte_bajo_stock() -> None:
    """Genera un reporte de productos con bajo stock."""
    while True:
        try:
            mostrar_info(
                "\n\tReporte de Stock Bajo - Puedes escribir 'salir' en cualquier campo para volver al menú."
            )

            respuesta = leer_texto("\n\t¿Deseas generar el reporte de bajo stock? (s/n): ")
            if respuesta is None:
                return
            if respuesta.lower() == "n":
                volver_al_menu()
                return
            if respuesta.lower() != "s":
                mostrar_error("\n\tEntrada inválida. Por favor, elige 's' o 'n'.")
                print()
                continue

            limite = leer_entero("\n\tIngresa el límite de stock para el reporte: ")
            if limite is None:
                return

            with database.obtener_conexion() as conexion:
                productos = conexion.execute(
                    """
                    SELECT id, nombre, descripcion, cantidad, precio, categoria
                    FROM productos
                    WHERE cantidad <= ?
                    ORDER BY cantidad ASC
                    """,
                    (limite,),
                ).fetchall()

            if productos:
                filas = [
                    [
                        p[0],
                        formatear_texto(p[1]) if p[1] else "N/A",
                        formatear_texto(p[2]) if p[2] else "N/A",
                        f"{Fore.RED}{Style.BRIGHT}{p[3]}{Style.RESET_ALL}",
                        f"${p[4]:.2f}",
                        formatear_texto(p[5]) if p[5] else "N/A",
                    ]
                    for p in productos
                ]
                mostrar_info("\nProductos con bajo stock:")
                print(tabulate(filas, headers=ENCABEZADOS, tablefmt="grid", stralign="center", numalign="right"))
                print()
            else:
                mostrar_advertencia("\n\tNo hay productos con bajo stock.")
                print()

            volver_al_menu()
            return

        except Exception as e:
            mostrar_error(f"\n\tError: {e}")
            print()


def buscar_producto() -> None:
    """Permite buscar productos por ID, nombre o categoría."""
    # (prompt, consulta SQL, si el parámetro es un ID exacto o un texto tipo LIKE)
    opciones_busqueda = {
        "1": ("Ingresa el ID del producto: ", "SELECT * FROM productos WHERE id = ?", True),
        "2": ("Ingresa el nombre del producto: ", "SELECT * FROM productos WHERE nombre LIKE ?", False),
        "3": ("Ingresa la categoría del producto: ", "SELECT * FROM productos WHERE categoria LIKE ?", False),
    }

    while True:
        mostrar_info("\n\t------------------------------------------------")
        mostrar_info("\tBúsqueda de productos")
        mostrar_info("\t------------------------------------------------")
        print("\t1. Buscar por ID")
        print("\t2. Buscar por nombre")
        print("\t3. Buscar por categoría")
        print("\t4. Volver al menú principal")

        opcion = input(Fore.WHITE + Style.BRIGHT + "\n\tSelecciona una opción: " + Style.RESET_ALL).strip()

        if opcion == "4":
            mostrar_exito("\n\tVolviendo al menú principal...")
            print()
            return

        if opcion not in opciones_busqueda:
            mostrar_error("\n\tOpción inválida. Intenta nuevamente.")
            print()
            continue

        prompt, consulta_sql, es_id = opciones_busqueda[opcion]
        try:
            if es_id:
                parametro = leer_entero(f"\t{prompt}")
                if parametro is None:
                    return
            else:
                texto = leer_texto(f"\t{prompt}")
                if texto is None:
                    return
                parametro = f"%{texto}%"

            with database.obtener_conexion() as conexion:
                productos = conexion.execute(consulta_sql, (parametro,)).fetchall()

            if not productos:
                mostrar_advertencia("\n\tNo se encontraron productos que coincidan con la búsqueda.")
                mostrar_exito("\n\tVolviendo al menú principal...")
                print()
                return

            headers = [Fore.BLUE + Style.BRIGHT + h + Style.RESET_ALL for h in ENCABEZADOS]
            filas = []
            for i, producto in enumerate(productos):
                color = Fore.LIGHTCYAN_EX if i % 2 == 0 else Fore.LIGHTWHITE_EX
                filas.append(
                    [
                        f"{color}{producto[0]}{Style.RESET_ALL}",
                        f"{color}{producto[1]}{Style.RESET_ALL}",
                        f"{color}{producto[2]}{Style.RESET_ALL}",
                        f"{color}{producto[3]}{Style.RESET_ALL}",
                        f"{color}${producto[4]:.2f}{Style.RESET_ALL}",
                        f"{color}{producto[5]}{Style.RESET_ALL}",
                    ]
                )

            mostrar_info("\nResultados de la búsqueda:")
            print(tabulate(filas, headers=headers, tablefmt="grid"))
            print()
            mostrar_exito("\n\tVolviendo al menú principal...")
            print()
            return

        except Exception as e:
            mostrar_error(f"\n\tError: {e}")
            print()

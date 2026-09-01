"""Menú principal de la aplicación de gestión de inventario."""

from colorama import Fore, Style
from colorama import init as colorama_init

from . import database
from .productos import (
    actualizar_producto,
    agregar_producto,
    buscar_producto,
    eliminar_producto,
    mostrar_productos,
    reporte_bajo_stock,
)

TITULO = "Menú de Gestión de Inventario de la dietética 'Juntos Saludables'"


def menu() -> None:
    """Muestra el menú principal y gestiona la interacción con el usuario."""
    opciones = {
        "1": agregar_producto,
        "2": mostrar_productos,
        "3": actualizar_producto,
        "4": eliminar_producto,
        "5": reporte_bajo_stock,
        "6": buscar_producto,
    }

    while True:
        print(Fore.BLUE + "\t" + "-" * 100 + Style.RESET_ALL)
        print(Fore.CYAN + f"\t{TITULO}" + Style.RESET_ALL)
        print(Fore.BLUE + "\t" + "-" * 100 + Style.RESET_ALL)
        print("\t1. Agregar producto")
        print("\t2. Mostrar productos")
        print("\t3. Actualizar cantidad de producto")
        print("\t4. Eliminar producto")
        print("\t5. Reporte de bajo stock")
        print("\t6. Buscar producto")
        print("\t7. Salir")

        opcion = input(Fore.WHITE + Style.BRIGHT + "\n\tSelecciona una opción: " + Style.RESET_ALL).strip()

        if opcion == "7":
            print(Fore.GREEN + "\n\tGracias por usar la aplicación. ¡Hasta luego!" + Style.RESET_ALL)
            print()
            break
        elif opcion in opciones:
            try:
                opciones[opcion]()
            except Exception as e:
                print(Fore.RED + f"\n\tError: {e}" + Style.RESET_ALL)
                print()
        else:
            print(Fore.RED + "\n\tOpción inválida. Intenta nuevamente." + Style.RESET_ALL)
            print()


def main() -> None:
    """Punto de entrada de la aplicación."""
    colorama_init()  # Necesario para que los colores funcionen también en Windows
    database.inicializar_base_datos()
    menu()


if __name__ == "__main__":
    main()

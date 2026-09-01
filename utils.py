"""Funciones auxiliares: formato de texto, lectura de entradas y mensajes coloreados.

Centralizar estas funciones evita repetir la misma lógica de validación
(por ejemplo, permitir escribir 'salir' en cualquier campo) en cada
operación del inventario.
"""

from typing import Optional

from colorama import Fore, Style

PALABRA_SALIR = "salir"


def formatear_texto(texto: str) -> str:
    """Formatea un texto para que la primera letra esté en mayúscula y el resto en minúsculas."""
    return texto.strip().capitalize()


def mostrar_info(mensaje: str) -> None:
    print(Fore.CYAN + mensaje + Style.RESET_ALL)


def mostrar_exito(mensaje: str) -> None:
    print(Fore.GREEN + mensaje + Style.RESET_ALL)


def mostrar_error(mensaje: str) -> None:
    print(Fore.RED + mensaje + Style.RESET_ALL)


def mostrar_advertencia(mensaje: str) -> None:
    print(Fore.YELLOW + mensaje + Style.RESET_ALL)


def volver_al_menu() -> None:
    mostrar_info("\n\tVolviendo al menú principal...")
    print()


def leer_texto(prompt: str) -> Optional[str]:
    """Pide un texto. Devuelve None (y vuelve al menú) si el usuario escribe 'salir'."""
    valor = input(prompt).strip()
    if valor.lower() == PALABRA_SALIR:
        volver_al_menu()
        return None
    return valor


def leer_entero(prompt: str, minimo: int = 0) -> Optional[int]:
    """Pide un entero >= minimo. Devuelve None (y vuelve al menú) si escribe 'salir'."""
    while True:
        valor = input(prompt).strip()
        if valor.lower() == PALABRA_SALIR:
            volver_al_menu()
            return None
        if valor.isdigit() and int(valor) >= minimo:
            return int(valor)
        mostrar_error("\tPor favor, ingresa un número entero válido.")
        print()


def leer_flotante(prompt: str, minimo: float = 0.0) -> Optional[float]:
    """Pide un número decimal >= minimo. Devuelve None (y vuelve al menú) si escribe 'salir'."""
    while True:
        valor = input(prompt).strip()
        if valor.lower() == PALABRA_SALIR:
            volver_al_menu()
            return None
        try:
            numero = float(valor)
        except ValueError:
            mostrar_error("\tPor favor, ingresa un número válido.")
            print()
            continue
        if numero >= minimo:
            return numero
        mostrar_error("\tEl valor debe ser un número positivo.")
        print()


def confirmar(prompt: str) -> bool:
    """Devuelve True si el usuario responde 's'."""
    return input(prompt).strip().lower() == "s"

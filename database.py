"""Acceso a la base de datos SQLite del inventario."""

import sqlite3
from contextlib import contextmanager
from pathlib import Path

# La base de datos se guarda en la raíz del proyecto, sin importar
# desde qué carpeta se ejecute el programa.
DB_PATH = Path(__file__).resolve().parent.parent / "inventario.db"


@contextmanager
def obtener_conexion():
    """Abre una conexión a la base de datos y hace commit/close automáticamente."""
    conexion = sqlite3.connect(DB_PATH)
    try:
        yield conexion
        conexion.commit()
    finally:
        conexion.close()


def inicializar_base_datos() -> None:
    """Crea la base de datos y la tabla 'productos' si no existen."""
    with obtener_conexion() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS productos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                cantidad INTEGER NOT NULL,
                precio REAL NOT NULL,
                categoria TEXT
            )
            """
        )

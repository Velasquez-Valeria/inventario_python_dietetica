# 🥗 Gestión de Inventario — Dietética "Juntos Saludables"

Aplicación de consola en Python para gestionar el inventario de una dietética, con
persistencia en SQLite y una interfaz de texto con tablas y colores.

## Funcionalidades

- ➕ Agregar productos (nombre, descripción, cantidad, precio, categoría)
- 📋 Mostrar el inventario completo, ordenado por cantidad
- ✏️ Actualizar la cantidad disponible de un producto
- 🗑️ Eliminar productos
- 📉 Reporte de productos con bajo stock (según un límite configurable)
- 🔎 Buscar productos por ID, nombre o categoría

En cualquier campo de texto se puede escribir `salir` para cancelar la operación
y volver al menú principal.

## Estructura del proyecto

```
inventario_dietetica/
├── inventario/
│   ├── __init__.py
│   ├── database.py     # Conexión e inicialización de la base de datos
│   ├── utils.py         # Formato de texto, lectura de entradas, mensajes
│   ├── productos.py     # Operaciones CRUD, reportes y búsqueda
│   └── main.py           # Menú principal
├── run.py                # Punto de entrada
├── requirements.txt
├── .gitignore
└── README.md
```

## Requisitos

- Python 3.8 o superior
- Dependencias: `tabulate`, `colorama`

## Instalación

```bash
git clone https://github.com/<tu-usuario>/inventario_dietetica.git
cd inventario_dietetica
pip install -r requirements.txt
```

## Uso

```bash
python run.py
```

La base de datos `inventario.db` se crea automáticamente en la raíz del proyecto
la primera vez que se ejecuta el programa.

## Menú principal

```
1. Agregar producto
2. Mostrar productos
3. Actualizar cantidad de producto
4. Eliminar producto
5. Reporte de bajo stock
6. Buscar producto
7. Salir
```

## Manejo de errores

- Las entradas no numéricas en campos de cantidad o precio se rechazan y se
  vuelve a pedir el dato.
- Si el inventario está vacío, se muestra un aviso en lugar de una tabla vacía.
- Cualquier excepción inesperada se captura y se informa sin cerrar el programa.

## Autor

- Valeria Velasquez

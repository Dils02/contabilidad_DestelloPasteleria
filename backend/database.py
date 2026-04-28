# ─────────────────────────────────────────
# BACKEND — Gestión de base de datos SQLite
# ─────────────────────────────────────────
import sqlite3
import os
import pandas as pd

# ── Ruta de la base de datos ──
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH  = os.path.join(BASE_DIR, "data", "ventas.db")


def get_connection():
    """Retorna una conexión a la base de datos."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH)


# ══════════════════════════════════════════
# INICIALIZACIÓN — Crear tablas si no existen
# ══════════════════════════════════════════
def inicializar_db():
    """Crea las tablas de la base de datos si no existen."""
    with get_connection() as conn:
        cursor = conn.cursor()

        # Tabla de productos
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS productos (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre      TEXT    NOT NULL UNIQUE,
                costo_total REAL    NOT NULL
            )
        """)

        # Tabla de ingredientes (relacionada con productos)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ingredientes (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                producto_id      INTEGER NOT NULL,
                nombre           TEXT    NOT NULL,
                unidad           TEXT    NOT NULL,
                cant_comprada    REAL    NOT NULL,
                precio_compra    REAL    NOT NULL,
                cant_usada       REAL    NOT NULL,
                costo_proporcional REAL  NOT NULL,
                FOREIGN KEY (producto_id) REFERENCES productos(id)
            )
        """)

        # Tabla de ventas
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ventas (
                id              INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha           TEXT    NOT NULL,
                producto        TEXT    NOT NULL,
                categoria       TEXT    NOT NULL,
                unidades        INTEGER NOT NULL,
                precio_venta    REAL    NOT NULL,
                ingreso_total   REAL    NOT NULL,
                costo_produccion REAL   NOT NULL,
                ganancia        REAL    NOT NULL,
                vendedor        TEXT    NOT NULL,
                notas           TEXT
            )
        """)

        conn.commit()


# ══════════════════════════════════════════
# PRODUCTOS
# ══════════════════════════════════════════
def guardar_producto_db(nombre: str, costo_total: float, ingredientes: list):
    """Guarda un producto y sus ingredientes en la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO productos (nombre, costo_total)
            VALUES (?, ?)
        """, (nombre, costo_total))

        producto_id = cursor.lastrowid

        for ing in ingredientes:
            cursor.execute("""
                INSERT INTO ingredientes
                    (producto_id, nombre, unidad, cant_comprada,
                     precio_compra, cant_usada, costo_proporcional)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                producto_id,
                ing["Ingrediente"],
                ing["Unidad"],
                ing["Cant. Comprada"],
                ing["Precio Compra"],
                ing["Cant. Usada"],
                ing["Costo Proporcional"]
            ))

        conn.commit()


def cargar_productos_db() -> dict:
    """Carga todos los productos e ingredientes desde la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()

        cursor.execute("SELECT id, nombre, costo_total FROM productos")
        productos_rows = cursor.fetchall()

        productos = {}
        for prod_id, nombre, costo_total in productos_rows:
            cursor.execute("""
                SELECT nombre, unidad, cant_comprada, precio_compra,
                       cant_usada, costo_proporcional
                FROM ingredientes
                WHERE producto_id = ?
            """, (prod_id,))

            ingredientes = []
            for row in cursor.fetchall():
                from backend.logica import clp
                ingredientes.append({
                    "Ingrediente"        : row[0],
                    "Unidad"             : row[1],
                    "Cant. Comprada"     : row[2],
                    "Precio Compra"      : row[3],
                    "Cant. Usada"        : row[4],
                    "Costo Proporcional" : row[5],
                    "Costo (CLP)"        : clp(row[5])
                })

            productos[nombre] = {
                "ingredientes" : ingredientes,
                "costo_total"  : costo_total
            }

    return productos


def producto_existe_db(nombre: str) -> bool:
    """Verifica si un producto ya existe en la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM productos WHERE nombre = ?", (nombre,))
        return cursor.fetchone() is not None


# ══════════════════════════════════════════
# VENTAS
# ══════════════════════════════════════════
def guardar_venta_db(venta: dict):
    """Guarda una venta en la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ventas
                (fecha, producto, categoria, unidades, precio_venta,
                 ingreso_total, costo_produccion, ganancia, vendedor, notas)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            venta["Fecha"],
            venta["Producto"],
            venta["Categoría"],
            venta["Unidades"],
            venta["Precio Venta"],
            venta["Ingreso Total"],
            venta["Costo Producción"],
            venta["Ganancia"],
            venta["Vendedor"],
            venta["Notas"]
        ))
        conn.commit()


def cargar_ventas_db() -> list:
    """Carga todas las ventas desde la base de datos."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, fecha, producto, categoria, unidades, precio_venta,
                   ingreso_total, costo_produccion, ganancia, vendedor, notas
            FROM ventas
        """)
        rows = cursor.fetchall()

    from backend.logica import clp
    ventas = []
    for row in rows:
        ventas.append({
            "id"               : row[0],
            "Fecha"            : row[1],
            "Producto"         : row[2],
            "Categoría"        : row[3],
            "Unidades"         : row[4],
            "Precio Venta"     : row[5],
            "Precio Venta CLP" : clp(row[5]),
            "Ingreso Total"    : row[6],
            "Ingreso CLP"      : clp(row[6]),
            "Costo Producción" : row[7],
            "Costo CLP"        : clp(row[7]),
            "Ganancia"         : row[8],
            "Ganancia CLP"     : clp(row[8]),
            "Vendedor"         : row[9],
            "Notas"            : row[10]
        })

    return ventas


def eliminar_venta_db(venta_id: int):
    """Elimina una venta por su ID."""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM ventas WHERE id = ?", (venta_id,))
        conn.commit()
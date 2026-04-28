# ─────────────────────────────────────────
# BACKEND — Lógica y cálculos
# ─────────────────────────────────────────

def clp(valor: float) -> str:
    """Convierte un número a formato moneda chilena. Ej: 15000 → $15.000"""
    return f"${int(round(valor)):,}".replace(",", ".")


def calcular_costo_proporcional(cantidad_usada: float, cantidad_total: float, precio_total: int) -> float:
    """Calcula el costo proporcional de un ingrediente."""
    if cantidad_total <= 0:
        return 0.0
    return (cantidad_usada / cantidad_total) * precio_total


def crear_ingrediente(nombre, unidad, cantidad_total, precio_total, cantidad_usada) -> dict:
    """Construye el diccionario de un ingrediente con su costo proporcional."""
    costo = calcular_costo_proporcional(cantidad_usada, cantidad_total, precio_total)
    return {
        "Ingrediente"        : nombre,
        "Unidad"             : unidad,
        "Cant. Comprada"     : cantidad_total,
        "Precio Compra"      : precio_total,
        "Cant. Usada"        : cantidad_usada,
        "Costo Proporcional" : costo,
        "Costo (CLP)"        : clp(costo)
    }


def guardar_producto(productos: dict, nombre: str, ingredientes: list) -> tuple[bool, str]:
    """
    Guarda un producto en el diccionario de productos.
    Retorna (éxito: bool, mensaje: str)
    """
    if not nombre.strip():
        return False, "⚠️ Debes ingresar el nombre del producto antes de guardarlo."
    if nombre.strip() in productos:
        return False, f"⚠️ Ya existe un producto llamado '{nombre.strip()}'."

    costo_total = sum(i["Costo Proporcional"] for i in ingredientes)
    productos[nombre.strip()] = {
        "ingredientes" : ingredientes,
        "costo_total"  : costo_total
    }
    return True, f"✅ Producto '{nombre.strip()}' guardado — Costo: {clp(costo_total)}"


def registrar_venta(productos: dict, fecha, producto_elegido, cantidad_vendida,
                    precio_venta, vendedor, categoria, notas) -> tuple[bool, str, dict]:
    """
    Construye el diccionario de una venta con todos sus cálculos.
    Retorna (éxito: bool, mensaje: str, venta: dict)
    """
    if categoria == "Seleccionar..." or not vendedor:
        return False, "⚠️ Por favor completa todos los campos obligatorios.", {}

    costo_prod = productos[producto_elegido]["costo_total"]
    ingreso    = cantidad_vendida * precio_venta
    ganancia   = ingreso - costo_prod

    venta = {
        "Fecha"            : str(fecha),
        "Producto"         : producto_elegido,
        "Categoría"        : categoria,
        "Unidades"         : cantidad_vendida,
        "Precio Venta"     : precio_venta,
        "Precio Venta CLP" : clp(precio_venta),
        "Ingreso Total"    : ingreso,
        "Ingreso CLP"      : clp(ingreso),
        "Costo Producción" : costo_prod,
        "Costo CLP"        : clp(costo_prod),
        "Ganancia"         : ganancia,
        "Ganancia CLP"     : clp(ganancia),
        "Vendedor"         : vendedor,
        "Notas"            : notas
    }
    return True, f"✅ Venta registrada — Ingreso: {clp(ingreso)} | Ganancia: {clp(ganancia)}", venta
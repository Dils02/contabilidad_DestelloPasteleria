# ─────────────────────────────────────────
# FRONT — Componentes visuales Streamlit
# ─────────────────────────────────────────
import streamlit as st
import pandas as pd
from datetime import date
from backend.logica import (
    clp, crear_ingrediente, guardar_producto, registrar_venta
)
from backend.database import (
    guardar_producto_db, guardar_venta_db,
    eliminar_venta_db, producto_existe_db
)


def seccion_crear_producto():
    """Sección: Formulario para crear productos con ingredientes."""

    st.title("🧪 Crear Producto")
    st.markdown("Crea un nuevo producto ingresando su nombre y los ingredientes que lo componen.")
    st.markdown("---")

    with st.expander("➕ Agregar nuevo producto", expanded=True):

        nombre_producto = st.text_input("📦 Nombre del producto", key="nombre_producto_input")
        st.subheader("🧂 Ingredientes del producto")

        with st.form("form_ingrediente", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                ing_nombre        = st.text_input("Nombre del ingrediente")
                ing_unidad        = st.selectbox("Unidad", ["kg", "g", "L", "mL", "unidad", "taza", "otro"])
                ing_precio_total  = st.number_input("💲 Precio de compra total (ej: 1500)", min_value=0, step=1)

            with col2:
                ing_cantidad_total = st.number_input("📦 Cantidad total comprada (ej: 1000)", min_value=0.0, step=0.1, format="%.2f")
                ing_cantidad_usada = st.number_input("🧪 Cantidad usada en el producto (ej: 200)", min_value=0.0, step=0.1, format="%.2f")

            if ing_cantidad_total > 0 and ing_cantidad_usada > 0 and ing_precio_total > 0:
                preview = (ing_cantidad_usada / ing_cantidad_total) * ing_precio_total
                st.info(f"📊 Costo proporcional estimado: **{clp(preview)}** "
                        f"({ing_cantidad_usada} ÷ {ing_cantidad_total} × {clp(ing_precio_total)})")

            agregar = st.form_submit_button("➕ Agregar ingrediente", width='stretch')

            if agregar:
                if not ing_nombre:
                    st.error("⚠️ Ingresa el nombre del ingrediente.")
                elif ing_cantidad_total <= 0:
                    st.error("⚠️ La cantidad total comprada debe ser mayor a 0.")
                elif ing_cantidad_usada > ing_cantidad_total:
                    st.error("⚠️ La cantidad usada no puede ser mayor a la cantidad total comprada.")
                else:
                    ingrediente = crear_ingrediente(
                        ing_nombre, ing_unidad, ing_cantidad_total,
                        ing_precio_total, ing_cantidad_usada
                    )
                    st.session_state.ingredientes_temp.append(ingrediente)
                    st.success(f"✅ '{ing_nombre}' agregado — Costo: {clp(ingrediente['Costo Proporcional'])}")

        if st.session_state.ingredientes_temp:
            st.markdown("#### 🧾 Ingredientes agregados")
            df_ing = pd.DataFrame(st.session_state.ingredientes_temp)
            st.dataframe(
                df_ing[["Ingrediente", "Unidad", "Cant. Comprada", "Cant. Usada", "Costo (CLP)"]],
                width='stretch'
            )

            costo_total = df_ing["Costo Proporcional"].sum()
            st.info(f"💰 Costo total de producción: **{clp(costo_total)}**")

            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Guardar producto", width='stretch'):
                    nombre = nombre_producto.strip()
                    if not nombre:
                        st.error("⚠️ Debes ingresar el nombre del producto.")
                    elif producto_existe_db(nombre):
                        st.error(f"⚠️ Ya existe un producto llamado '{nombre}'.")
                    else:
                        costo = df_ing["Costo Proporcional"].sum()
                        guardar_producto_db(nombre, costo, st.session_state.ingredientes_temp)
                        st.session_state.productos[nombre] = {
                            "ingredientes" : st.session_state.ingredientes_temp.copy(),
                            "costo_total"  : costo
                        }
                        st.session_state.ingredientes_temp = []
                        st.success(f"✅ Producto '{nombre}' guardado — Costo: {clp(costo)}")
                        st.rerun()

            with col2:
                if st.button("🗑️ Limpiar ingredientes", width='stretch'):
                    st.session_state.ingredientes_temp = []
                    st.rerun()

    st.markdown("---")

    with st.expander("📒 Recetas", expanded=False):
        if not st.session_state.productos:
            st.info("Aún no hay productos creados. ¡Crea uno en el apartado de arriba!")
        else:
            for nombre, datos in st.session_state.productos.items():
                st.markdown(f"### 📦 {nombre}")
                df_det = pd.DataFrame(datos["ingredientes"])
                st.dataframe(
                    df_det[["Ingrediente", "Unidad", "Cant. Comprada", "Cant. Usada", "Costo (CLP)"]],
                    width='stretch'
                )
                col1, col2 = st.columns(2)
                col1.metric("💰 Costo total de producción", clp(datos["costo_total"]))
                col2.metric("🧂 N° de ingredientes", len(datos["ingredientes"]))
                st.markdown("---")


def seccion_recetas():
    """Sección: Catálogo de productos y sus recetas."""

    st.title("📒 Recetas")
    st.markdown("Consulta todos los productos creados junto con sus ingredientes y costos.")
    st.markdown("---")

    if not st.session_state.productos:
        st.info("⚠️ Aún no hay productos creados. Ve a **Crear Producto** para agregar uno.")
        return

    col1, col2, col3 = st.columns(3)
    col1.metric("📦 Total de productos", len(st.session_state.productos))
    col2.metric("🧂 Total de ingredientes", sum(
        len(d["ingredientes"]) for d in st.session_state.productos.values()
    ))
    col3.metric("💰 Costo promedio por producto", clp(
        sum(d["costo_total"] for d in st.session_state.productos.values()) /
        len(st.session_state.productos)
    ))

    st.markdown("---")

    for nombre, datos in st.session_state.productos.items():
        with st.expander(f"📦 {nombre}  —  Costo de producción: {clp(datos['costo_total'])}", expanded=False):
            df_det = pd.DataFrame(datos["ingredientes"])
            st.dataframe(
                df_det[["Ingrediente", "Unidad", "Cant. Comprada", "Cant. Usada", "Costo (CLP)"]],
                width='stretch'
            )
            col1, col2 = st.columns(2)
            col1.metric("💰 Costo total de producción", clp(datos["costo_total"]))
            col2.metric("🧂 N° de ingredientes",        len(datos["ingredientes"]))


def seccion_registrar_venta():
    """Sección: Formulario para registrar ventas."""

    st.title("🧾 Registrar Venta")
    st.markdown("Registra una nueva venta seleccionando un producto y completando los datos.")
    st.markdown("---")

    if not st.session_state.productos:
        st.warning("⚠️ Aún no tienes productos creados. Ve a **Crear Producto** primero.")
        return

    with st.expander("➕ Nueva venta", expanded=True):
        with st.form("form_venta", clear_on_submit=True):
            col1, col2 = st.columns(2)

            with col1:
                fecha            = st.date_input("📅 Fecha", value=date.today())
                producto_elegido = st.selectbox("📦 Producto", list(st.session_state.productos.keys()))
                cantidad_vendida = st.number_input("🔢 Unidades producidas / vendidas", min_value=1, step=1)

            with col2:
                precio_venta = st.number_input("💲 Precio de venta por unidad (ej: 3000)", min_value=0, step=1)
                vendedor     = st.text_input("👤 Vendedor")
                categoria    = st.selectbox("🏷️ Categoría", ["Seleccionar...", "Electrónica", "Ropa", "Alimentos", "Servicios", "Otro"])

            notas     = st.text_area("📝 Notas (opcional)")
            submitted = st.form_submit_button("✅ Registrar Venta", width='stretch')

            if submitted:
                exito, mensaje, venta = registrar_venta(
                    st.session_state.productos, fecha, producto_elegido,
                    cantidad_vendida, precio_venta, vendedor, categoria, notas
                )
                if exito:
                    guardar_venta_db(venta)
                    st.session_state.ventas.append(venta)
                    st.success(mensaje)
                else:
                    st.error(mensaje)

    if st.session_state.ventas:
        st.markdown("---")
        st.subheader("📊 Ventas Registradas")

        df_ventas = pd.DataFrame(st.session_state.ventas)

        col1, col2, col3, col4 = st.columns(4)
        col1.metric("🧾 Ventas totales",    len(df_ventas))
        col2.metric("💰 Ingresos totales",  clp(df_ventas["Ingreso Total"].sum()))
        col3.metric("📦 Unidades vendidas", int(df_ventas["Unidades"].sum()))
        col4.metric("📈 Ganancia total",    clp(df_ventas["Ganancia"].sum()))

        st.markdown("---")

        st.markdown("#### 🗑️ Eliminar ventas")
        st.caption("Marca las ventas que deseas eliminar y presiona el botón confirmar.")

        columnas_visibles = ["Fecha", "Producto", "Categoría", "Unidades",
                             "Precio Venta CLP", "Ingreso CLP", "Costo CLP",
                             "Ganancia CLP", "Vendedor", "Notas"]

        df_editor = df_ventas[columnas_visibles].copy()
        df_editor.insert(0, "Eliminar", False)

        df_editado = st.data_editor(
            df_editor,
            width='stretch',
            hide_index=True,
            column_config={
                "Eliminar": st.column_config.CheckboxColumn(
                    label="🗑️",
                    help="Marca para eliminar esta venta",
                    default=False
                )
            },
            disabled=columnas_visibles
        )

        filas_marcadas = df_editado[df_editado["Eliminar"] == True]

        if not filas_marcadas.empty:
            st.warning(f"⚠️ Tienes **{len(filas_marcadas)}** venta(s) marcada(s) para eliminar.")
            if st.button("🗑️ Confirmar eliminación", type="primary", width='stretch'):
                indices = filas_marcadas.index.tolist()
                for i in indices:
                    eliminar_venta_db(st.session_state.ventas[i]["id"])
                st.session_state.ventas = [
                    v for i, v in enumerate(st.session_state.ventas)
                    if i not in indices
                ]
                st.success(f"✅ {len(indices)} venta(s) eliminada(s) correctamente.")
                st.rerun()
# ─────────────────────────────────────────
# INTERFAZ — Punto de entrada principal
# ─────────────────────────────────────────
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
from backend.database import inicializar_db, cargar_productos_db, cargar_ventas_db
from front.componentes import (
    seccion_crear_producto,
    seccion_recetas,
    seccion_registrar_venta
)

from front.estilos import aplicar_estilos

# ── Inicializar ──
inicializar_db()
aplicar_estilos()

st.set_page_config(
    page_title="Sistema de Ventas",
    page_icon="🛒",
    layout="wide"
)

# ── Cargar datos desde la BD al session_state ──
if "productos" not in st.session_state:
    st.session_state.productos = cargar_productos_db()
if "ventas" not in st.session_state:
    st.session_state.ventas = cargar_ventas_db()
if "ingredientes_temp" not in st.session_state:
    st.session_state.ingredientes_temp = []

# ── Sidebar ──
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/shopping-cart.png", width=60)
    st.title("Sistema de Ventas")
    st.markdown("---")

    seccion_activa = st.radio(
        "Navegación",
        options=["🧪 Crear Producto", "📒 Recetas", "🧾 Registrar Venta"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    total_productos = len(st.session_state.productos)
    total_ventas    = len(st.session_state.ventas)
    total_ingresos  = sum(v["Ingreso Total"] for v in st.session_state.ventas)

    st.markdown("### 📊 Resumen")
    st.metric("📦 Productos creados",   total_productos)
    st.metric("🧾 Ventas registradas",  total_ventas)
    st.metric("💰 Ingresos totales",
              f"${int(total_ingresos):,}".replace(",", ".") if total_ingresos > 0 else "$0")

# ── Renderizar sección activa ──
if seccion_activa == "🧪 Crear Producto":
    seccion_crear_producto()
elif seccion_activa == "📒 Recetas":
    seccion_recetas()
elif seccion_activa == "🧾 Registrar Venta":
    seccion_registrar_venta()
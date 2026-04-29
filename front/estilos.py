# ─────────────────────────────────────────
# FRONT — Estilos CSS personalizados
# ─────────────────────────────────────────
import streamlit as st


def aplicar_estilos():
    st.markdown("""
    <style>
    /* ══════════════════════════════════════
       FUENTES
    ══════════════════════════════════════ */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

    * {
        font-family: 'Inter', sans-serif;
    }

    /* ══════════════════════════════════════
       FONDO GENERAL — degradado celeste a blanco
    ══════════════════════════════════════ */
    .stApp {
        background: linear-gradient(145deg, #60F2D2 0%, #e0fdf6 30%, #ffffff 70%);
        background-attachment: fixed;
    }

/* ══════════════════════════════════════
   SIDEBAR
══════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0d6e5a 0%, #0f8a72 50%, #11a688 100%) !important;
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,0.15);
}

[data-testid="stSidebar"] * {
    color: #ffffff !important;
}

[data-testid="stSidebar"] [data-testid="stMetric"] {
    background: rgba(255,255,255,0.12);
    border-radius: 12px;
    padding: 12px;
    margin: 6px 0;
    border: 1px solid rgba(255,255,255,0.2);
}

[data-testid="stSidebar"] [data-testid="stMetricValue"] {
    font-size: 1.3rem !important;
    font-weight: 700 !important;
}

/* Radio buttons — alineación */
[data-testid="stSidebar"] .stRadio > div {
    display: flex;
    flex-direction: column;
    gap: 8px;
    width: 100%;
}

[data-testid="stSidebar"] .stRadio > div > label {
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    gap: 12px !important;
    background: rgba(255,255,255,0.1);
    border-radius: 10px;
    padding: 12px 16px !important;
    margin: 0 !important;
    width: 100% !important;
    cursor: pointer;
    font-weight: 500;
    font-size: clamp(0.85rem, 2vw, 1rem);
    transition: background 0.2s ease;
}

[data-testid="stSidebar"] .stRadio > div > label:hover {
    background: rgba(255,255,255,0.25) !important;
}

[data-testid="stSidebar"] .stRadio > div > label > div:first-child {
    width: 18px !important;
    height: 18px !important;
    min-width: 18px !important;
    border-radius: 50% !important;
    border: 2px solid rgba(255,255,255,0.6) !important;
    background: transparent !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
    flex-shrink: 0;
}

[data-testid="stSidebar"] .stRadio > div > label > div:last-child {
    color: #ffffff !important;
    font-weight: 500 !important;
    line-height: 1.2 !important;
}

[data-testid="stSidebar"] .stRadio > label {
    color: rgba(255,255,255,0.7) !important;
    font-size: 0.8rem !important;
    font-weight: 600 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 8px !important;
    display: block !important;
}

    /* ══════════════════════════════════════
       TÍTULOS
    ══════════════════════════════════════ */
    h1 {
        color: #0a4d3c !important;
        font-weight: 700 !important;
        font-size: 2rem !important;
        border-bottom: 3px solid #60F2D2;
        padding-bottom: 10px;
        margin-bottom: 8px !important;
    }

    h2, h3 {
        color: #0d6e5a !important;
        font-weight: 600 !important;
    }

    h4 {
        color: #0f8a72 !important;
        font-weight: 600 !important;
    }

    /* ══════════════════════════════════════
       MÉTRICAS
    ══════════════════════════════════════ */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #ffffff 0%, #e8fdf7 100%);
        border-radius: 16px;
        padding: 20px !important;
        border: 1px solid #b2f0e0;
        box-shadow: 0 4px 15px rgba(96, 242, 210, 0.2);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(96, 242, 210, 0.35);
    }

    [data-testid="stMetricLabel"] {
        color: #0a4d3c !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
    }

    [data-testid="stMetricValue"] {
        color: #0d6e5a !important;
        font-weight: 700 !important;
        font-size: 1.6rem !important;
    }

    /* ══════════════════════════════════════
       BOTONES
    ══════════════════════════════════════ */
    .stButton > button {
        background: linear-gradient(135deg, #60F2D2 0%, #0f8a72 100%);
        color: #ffffff !important;
        border: none;
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 0.95rem;
        transition: all 0.2s ease;
        box-shadow: 0 4px 12px rgba(96, 242, 210, 0.4);
    }

    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(96, 242, 210, 0.6);
        background: linear-gradient(135deg, #3de8c4 0%, #0a6655 100%);
    }

    .stButton > button:active {
        transform: translateY(0px);
    }

    /* Botón primario (confirmar eliminación) */
    .stButton > button[kind="primary"] {
        background: linear-gradient(135deg, #ff6b6b 0%, #c0392b 100%) !important;
        box-shadow: 0 4px 12px rgba(255, 107, 107, 0.4) !important;
    }

    .stButton > button[kind="primary"]:hover {
        background: linear-gradient(135deg, #ff5252 0%, #a93226 100%) !important;
        box-shadow: 0 6px 20px rgba(255, 107, 107, 0.6) !important;
    }

    /* ══════════════════════════════════════
       FORMULARIOS E INPUTS
    ══════════════════════════════════════ */
    [data-testid="stForm"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf9 100%);
        border-radius: 16px;
        padding: 24px !important;
        border: 1px solid #b2f0e0;
        box-shadow: 0 4px 20px rgba(96, 242, 210, 0.15);
    }

    .stTextInput > div > div > input,
    .stNumberInput > div > div > input,
    .stTextArea > div > div > textarea {
        border-radius: 10px !important;
        border: 1.5px solid #b2f0e0 !important;
        background: #ffffff !important;
        padding: 10px 14px !important;
        font-size: 0.95rem !important;
        transition: border-color 0.2s ease, box-shadow 0.2s ease;
    }

    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus {
        border-color: #60F2D2 !important;
        box-shadow: 0 0 0 3px rgba(96, 242, 210, 0.25) !important;
    }

    .stSelectbox > div > div {
        border-radius: 10px !important;
        border: 1.5px solid #b2f0e0 !important;
        background: #ffffff !important;
    }

    /* ══════════════════════════════════════
       EXPANDERS
    ══════════════════════════════════════ */
    [data-testid="stExpander"] {
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf9 100%);
        border-radius: 16px !important;
        border: 1px solid #b2f0e0 !important;
        box-shadow: 0 4px 15px rgba(96, 242, 210, 0.15);
        margin-bottom: 16px;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary {
        font-weight: 600 !important;
        color: #0a4d3c !important;
        font-size: 1rem !important;
        padding: 16px 20px !important;
        background: linear-gradient(135deg, #e8fdf7 0%, #ffffff 100%);
    }

    [data-testid="stExpander"] summary:hover {
        background: linear-gradient(135deg, #d0f9ee 0%, #f0fdf9 100%);
    }

    /* ══════════════════════════════════════
       TABLAS / DATAFRAMES
    ══════════════════════════════════════ */
    [data-testid="stDataFrame"],
    [data-testid="stDataEditor"] {
        border-radius: 12px !important;
        border: 1px solid #b2f0e0 !important;
        overflow: hidden;
        box-shadow: 0 4px 15px rgba(96, 242, 210, 0.15);
    }

    /* ══════════════════════════════════════
       ALERTAS / MENSAJES
    ══════════════════════════════════════ */
    [data-testid="stInfo"] {
        background: linear-gradient(135deg, #e8fdf7 0%, #d0f9ee 100%) !important;
        border-left: 4px solid #60F2D2 !important;
        border-radius: 10px !important;
        color: #0a4d3c !important;
    }

    [data-testid="stSuccess"] {
        background: linear-gradient(135deg, #d4edda 0%, #c3e6cb 100%) !important;
        border-left: 4px solid #28a745 !important;
        border-radius: 10px !important;
    }

    [data-testid="stWarning"] {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeeba 100%) !important;
        border-left: 4px solid #ffc107 !important;
        border-radius: 10px !important;
    }

    [data-testid="stError"] {
        background: linear-gradient(135deg, #f8d7da 0%, #f5c6cb 100%) !important;
        border-left: 4px solid #dc3545 !important;
        border-radius: 10px !important;
    }

    /* ══════════════════════════════════════
       DIVISORES
    ══════════════════════════════════════ */
    hr {
        border: none !important;
        height: 2px !important;
        background: linear-gradient(90deg, #60F2D2, transparent) !important;
        margin: 20px 0 !important;
    }

    /* ══════════════════════════════════════
       SCROLLBAR
    ══════════════════════════════════════ */
    ::-webkit-scrollbar {
        width: 6px;
        height: 6px;
    }

    ::-webkit-scrollbar-track {
        background: #f0fdf9;
    }

    ::-webkit-scrollbar-thumb {
        background: #60F2D2;
        border-radius: 10px;
    }

    ::-webkit-scrollbar-thumb:hover {
        background: #0f8a72;
    }

    /* ══════════════════════════════════════
       CAPTION / TEXTO PEQUEÑO
    ══════════════════════════════════════ */
    .stCaption {
        color: #4a9e8a !important;
        font-size: 0.85rem !important;
    }

    </style>
    """, unsafe_allow_html=True)
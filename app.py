import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# Configuración de página
st.set_page_config(page_title="Gestión del Hogar", layout="wide")

# --- DISEÑO CÁLIDO Y MODERNO (CSS CUSTOM) ---
st.markdown("""
    <style>
    /* Fondo general cálido/tecnológico */
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    /* Tarjetas blancas redondeadas */
    div[data-testid="stMetric"] {
        background-color: rgba(255, 255, 255, 0.8);
        border-radius: 20px;
        padding: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.18);
    }

    /* Botones redondeados y modernos */
    .stButton>button {
        border-radius: 25px !important;
        background: linear-gradient(45deg, #28a745, #85e085);
        color: white;
        border: none;
        padding: 10px 25px;
        font-weight: bold;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(40, 167, 69, 0.4);
    }

    /* Inputs redondeados */
    .stTextInput>div>div>input, .stNumberInput>div>div>input, .stSelectbox>div>div>div {
        border-radius: 15px !important;
    }

    /* Sidebar con estilo */
    section[data-testid="stSidebar"] {
        background-color: rgba(255, 255, 255, 0.5);
    }
    </style>
    """, unsafe_allow_html=True)

# Inicialización de datos
if 'movimientos' not in st.session_state:
    st.session_state.movimientos = pd.DataFrame(columns=['Fecha', 'Tipo', 'Categoría', 'Monto', 'Nota'])

# --- SIDEBAR ---
with st.sidebar:
    st.title("🏦 TechFin")
    menu = st.radio("Navegación", ["Dashboard", "Añadir Registro"])
    st.markdown("---")
    st.write("Administración del Hogar v2.0")

df = st.session_state.movimientos
total_ingresos = df[df['Tipo'] == 'Ingreso']['Monto'].sum()
total_gastos = df[df['Tipo'] == 'Gasto']['Monto'].sum()
balance = total_ingresos - total_gastos

# --- LÓGICA DE MENÚS ---
if menu == "Dashboard":
    st.markdown("<h1 style='text-align: center; color: #2c3e50;'>Resumen General</h1>", unsafe_allow_html=True)
    
    # Métricas en tarjetas
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos", f"{total_ingresos} €")
    c2.metric("Gastos", f"-{total_gastos} €")
    c3.metric("Balance", f"{balance} €")

    st.write("##") # Espaciado

    if not df.empty:
        col_left, col_right = st.columns([1, 1])
        with col_left:
            # Gráfico con colores cálidos
            fig = px.pie(df[df['Tipo']=='Gasto'], values='Monto', names='Categoría', 
                         hole=0.5, title="Gastos por Categoría",
                         color_discrete_sequence=px.colors.qualitative.Pastel)
            fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        
        with col_right:
            st.subheader("Últimos Movimientos")
            st.dataframe(df.sort_values(by='Fecha', ascending=False), use_container_width=True)
    else:
        st.info("Aún no tienes registros. ¡Empieza en el menú lateral!")

elif menu == "Añadir Registro":
    st.markdown("<h2 style='color: #2c3e50;'>Registrar Movimiento</h2>", unsafe_allow_html=True)
    
    with st.expander("Abrir Formulario de Registro", expanded=True):
        tipo = st.radio("Selecciona tipo:", ["Gasto", "Ingreso"], horizontal=True)
        
        col1, col2 = st.columns(2)
        with col1:
            if tipo == "Gasto":
                cat = st.selectbox("Categoría", ["Supermercado", "Alquiler", "Luz/Agua", "Ocio", "Transporte", "Suscripciones"])
            else:
                cat = st.selectbox("Categoría", ["Nómina", "Venta Extra", "Regalo"])
            monto = st.number_input("Cantidad (€)", min_value=0.0)
        
        with col2:
            fecha = st.date_input("Fecha", datetime.now())
            nota = st.text_input("Descripción corta")

        if st.button("Guardar en mi cuenta"):
            nuevo = pd.DataFrame([[fecha, tipo, cat, monto, nota]], columns=df.columns)
            st.session_state.movimientos = pd.concat([st.session_state.movimientos, nuevo], ignore_index=True)
            st.balloons() # Animación tecnológica de éxito

            st.success("Guardado correctamente")


import streamlit as st
import pandas as pd
import plotly.express as px
import os

# -------------------------------------------------
# CONFIGURACIÓN GENERAL
# -------------------------------------------------
st.set_page_config(
    page_title="Conectividad Digital Colombia",
    page_icon="📡",
    layout="wide"
)

# -------------------------------------------------
# FUNCIONES
# -------------------------------------------------
@st.cache_data(ttl=3600)
def load_data():
    data_path = "data/"  # carpeta donde estarán los CSV en el repo
    try:
        def clean_cols(df):
            df.columns = (
                df.columns
                .str.strip()
                .str.lower()
                .str.replace(" ", "_")
                .str.replace("ñ", "n")
            )
            return df

        df1 = clean_cols(pd.read_csv(os.path.join(data_path, "q1_departamentos.csv")))
        df2 = clean_cols(pd.read_csv(os.path.join(data_path, "q2_municipios.csv")))
        df3 = clean_cols(pd.read_csv(os.path.join(data_path, "q3_tecnologia.csv")))
        df4 = clean_cols(pd.read_csv(os.path.join(data_path, "q4_velocidades.csv")))
        df5 = clean_cols(pd.read_csv(os.path.join(data_path, "q5_proveedores.csv")))
        return df1, df2, df3, df4, df5
    except Exception as e:
        st.error(f"Error al cargar CSV: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()


# -------------------------------------------------
# CARGA
# -------------------------------------------------
df1, df2, df3, df4, df5 = load_data()

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.title("Panel de Control")
st.sidebar.markdown("Proyecto de Analítica de Datos")

if not df1.empty and "anio" in df1.columns:
    anio_opciones = sorted(df1["anio"].dropna().unique())
    anio_sel = st.sidebar.selectbox("Seleccionar Año", anio_opciones)
    df1 = df1[df1["anio"] == anio_sel]
else:
    st.sidebar.warning("No se encontró columna 'anio'")

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
st.title("📡 Dashboard de Conectividad Digital")
st.markdown("Análisis de accesos a Internet por regiones, tecnologías y proveedores")

# -------- SECCIÓN 1 --------
st.header("Accesos por Departamento")
if not df1.empty:
    st.dataframe(df1, use_container_width=True)
    if len(df1.columns) >= 2:
        fig1 = px.bar(df1, x=df1.columns[1], y="accesos", title="Accesos por Departamento")
        st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 2 --------
st.header("Top Municipios con Más Accesos")
if not df2.empty:
    st.dataframe(df2, use_container_width=True)
    if len(df2.columns) >= 2:
        fig2 = px.bar(df2.head(10), x="accesos", y=df2.columns[1], orientation='h', title="Top Municipios")
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 3 --------
st.header("Distribución por Tecnología")
if not df3.empty:
    st.dataframe(df3, use_container_width=True)
    if len(df3.columns) >= 2:
        fig3 = px.pie(df3, names=df3.columns[1], values="accesos", title="Participación por Tecnología")
        st.plotly_chart(fig3, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 4 --------
st.header("Velocidad Promedio por Segmento")
if not df4.empty:
    st.dataframe(df4, use_container_width=True)
    if {"velocidad_bajada", "velocidad_subida"}.issubset(df4.columns):
        fig4 = px.bar(
            df4,
            x=df4.columns[1],
            y=["velocidad_bajada", "velocidad_subida"],
            barmode="group",
            title="Velocidades Promedio"
        )
        st.plotly_chart(fig4, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 5 --------
st.header("Proveedores con Más Accesos")
if not df5.empty:
    st.dataframe(df5, use_container_width=True)
    if len(df5.columns) >= 2:
        fig5 = px.bar(df5.head(10), x=df5.columns[1], y="accesos", title="Top Proveedores")
        st.plotly_chart(fig5, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------------------------------------------------
# PIE
# -------------------------------------------------
st.markdown("---")
st.caption("Proyecto de Análisis de Datos — Conectividad Digital en Colombia")

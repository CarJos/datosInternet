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

filtro = st.sidebar.selectbox(
    "Filtrar por Departamento",
    df1[df1.columns[1]].unique()
)

df1 = df1[df1[df1.columns[1]] == filtro]

# -------------------------------------------------
# DASHBOARD
# -------------------------------------------------
st.title("📡 Dashboard de Conectividad Digital")
st.markdown("Análisis de accesos a Internet por regiones, tecnologías y proveedores")

# -------- SECCIÓN 1 --------
st.header("Accesos por Departamento")
fig1 = px.bar(
    df1.sort_values("accesos", ascending=False),
    x="accesos",
    y=df1.columns[1],
    orientation="h",
    title="📊 Accesos por Departamento",
    color="accesos",
    color_continuous_scale="Teal"
)

fig1.update_layout(
    template=TEMPLATE,
    title_x=0.3,
    height=500
)

st.plotly_chart(fig1, use_container_width=True)

# -------- SECCIÓN 2 --------
st.header("Top Municipios con Más Accesos")
top_mun = df2.sort_values("accesos", ascending=False).head(10)

fig2 = px.bar(
    top_mun,
    x="accesos",
    y=top_mun.columns[1],
    orientation='h',
    text="accesos",
    title="🏆 Top 10 Municipios"
)

fig2.update_traces(textposition="outside")

fig2.update_layout(
    template=TEMPLATE,
    height=500
)

st.plotly_chart(fig2, use_container_width=True)

# -------- SECCIÓN 3 --------
st.header("Distribución por Tecnología")
fig3 = px.pie(
    df3,
    names=df3.columns[1],
    values="accesos",
    hole=0.4,  # donut 🔥
    title="📡 Distribución por Tecnología"
)

fig3.update_layout(template=TEMPLATE)

st.plotly_chart(fig3, use_container_width=True)

# -------- SECCIÓN 4 --------
st.header("Velocidad Promedio por Segmento")
fig4 = px.line(
    df4,
    x=df4.columns[1],
    y=["velocidad_bajada", "velocidad_subida"],
    markers=True,
    title="🚀 Velocidades Promedio"
)

fig4.update_layout(template=TEMPLATE)

st.plotly_chart(fig4, use_container_width=True)

# -------- SECCIÓN 5 --------
st.header("Proveedores con Más Accesos")
top_prov = df5.sort_values("accesos", ascending=False).head(10)

fig5 = px.bar(
    top_prov,
    x="accesos",
    y=top_prov.columns[1],
    orientation="h",
    color="accesos",
    color_continuous_scale="Viridis",
    title="🏢 Top Proveedores"
)

fig5.update_layout(template=TEMPLATE)

st.plotly_chart(fig5, use_container_width=True)

# -------------------------------------------------
# PIE
# -------------------------------------------------
st.markdown("---")
st.caption("Proyecto de Análisis de Datos — Conectividad Digital en Colombia")

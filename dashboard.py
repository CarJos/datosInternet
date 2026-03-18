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
    data_path = "data/"
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

# FILTRO GENERAL + DEPARTAMENTO
if not df1.empty and "departamento" in df1.columns:
    depto_opciones = ["Todos"] + sorted(df1["departamento"].dropna().unique())
    depto_sel = st.sidebar.selectbox("Seleccionar Departamento", depto_opciones)

    # Aplicar filtro solo si NO es "Todos"
    if depto_sel != "Todos":
        df1 = df1[df1["departamento"] == depto_sel]

        if "departamento" in df2.columns:
            df2 = df2[df2["departamento"] == depto_sel]
        if "departamento" in df3.columns:
            df3 = df3[df3["departamento"] == depto_sel]
        if "departamento" in df4.columns:
            df4 = df4[df4["departamento"] == depto_sel]
        if "departamento" in df5.columns:
            df5 = df5[df5["departamento"] == depto_sel]

else:
    st.sidebar.warning("No se encontró columna 'departamento'")

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
        fig1 = px.bar(df1, x="departamento", y="accesos", title="Accesos por Departamento")
        st.plotly_chart(fig1, use_container_width=True)
else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 2 --------
st.header("Top Municipios con Más Accesos")

if not df2.empty:
    st.dataframe(df2, use_container_width=True)

    # Ordenar y tomar top 10
    df_top = df2.sort_values(by="accesos", ascending=False).head(10)

    # Crear etiqueta más clara (municipio + departamento)
    if "departamento" in df_top.columns:
        df_top["label"] = df_top["municipio"] + " (" + df_top["departamento"] + ")"
    else:
        df_top["label"] = df_top["municipio"]

    fig2 = px.bar(
        df_top.sort_values("accesos"),  # para que el mayor quede arriba
        x="accesos",
        y="label",
        orientation="h",
        text="accesos",
        title="Top 10 Municipios con Más Accesos a Internet",
        color="accesos",
        color_continuous_scale="blues"
    )

    # Mejorar formato visual
    fig2.update_traces(
        texttemplate='%{text:,.0f}',  # formato con comas
        textposition='outside'
    )

    fig2.update_layout(
        yaxis_title="Municipio",
        xaxis_title="Número de accesos",
        title_x=0.5,
        height=500
    )

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

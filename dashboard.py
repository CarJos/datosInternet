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

    if {"departamento", "accesos"}.issubset(df1.columns):

        df1_sorted = df1.sort_values("accesos", ascending=False)

        fig1 = px.pie(
            df1_sorted,
            names="departamento",
            values="accesos",
            title="Participación de Accesos por Departamento",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        fig1.update_traces(
            texttemplate='%{label}<br>%{percent}',
            textposition='inside'
        )

        fig1.update_layout(
            title_x=0.5,
            height=520,
            legend_title="Departamento"
        )

        st.plotly_chart(fig1, use_container_width=True)

else:
    st.warning("Sin datos disponibles")
# -------- SECCIÓN 2 --------
st.header("Top Municipios con Más Accesos")

if not df2.empty:
    st.dataframe(df2, use_container_width=True)

    df_top = df2.sort_values(by="accesos", ascending=False).head(10)

    if "departamento" in df_top.columns:
        df_top["label"] = df_top["municipio"] + " (" + df_top["departamento"] + ")"
    else:
        df_top["label"] = df_top["municipio"]

    fig2 = px.bar(
        df_top,
        x="label",
        y="accesos",
        text="accesos",
        title="Top 10 Municipios con Más Accesos a Internet",
        color="accesos",
        color_continuous_scale="Blues"
    )

    fig2.update_traces(
        texttemplate='%{text:,.0f}',
        textposition='outside'
    )

    fig2.update_layout(
        title_x=0.5,
        height=520,
        xaxis_title="Municipio",
        yaxis_title="Número de accesos",
        xaxis_tickangle=-35,
        bargap=0.25
    )

    st.plotly_chart(fig2, use_container_width=True)

else:
    st.warning("Sin datos disponibles")
    
# -------- SECCIÓN 3 --------
st.header("Distribución por Tecnología")

if not df3.empty:
    st.dataframe(df3, use_container_width=True)

    if {"accesos"}.issubset(df3.columns):

        col_tec = "tecnologia"
        df3_sorted = df3.sort_values("accesos", ascending=False)

        fig3 = px.pie(
            df3_sorted,
            names=col_tec,          # ← tecnología
            values="accesos",
            hole=0.55,
            title="Participación de Accesos por Tecnología",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        # Mostrar SOLO nombre + porcentaje
        fig3.update_traces(
            textinfo='percent',
            textposition='inside',
            hovertemplate='<b>%{label}</b><br>Participación: %{percent}<extra></extra>'
        )

        fig3.update_layout(
            title_x=0.5,
            height=620,
            legend_title="tecnologia"
        )

        st.plotly_chart(fig3, use_container_width=True)

else:
    st.warning("Sin datos disponibles")
# -------- SECCIÓN 4 --------
st.header("Velocidad Promedio por Segmento")

if not df4.empty:
    st.dataframe(df4, use_container_width=True)

    if {"velocidad_bajada", "velocidad_subida"}.issubset(df4.columns):

        col_segmento = df4.columns[1]

        df4_long = df4.melt(
            id_vars=[col_segmento],
            value_vars=["velocidad_bajada", "velocidad_subida"],
            var_name="tipo",
            value_name="velocidad"
        )

        fig4 = px.bar(
            df4_long,
            x=col_segmento,
            y="velocidad",
            color="tipo",
            barmode="group",
            text="velocidad",
            title="Velocidad Promedio de Bajada vs Subida por Segmento",
            color_discrete_sequence=px.colors.sequential.Blues_r
        )

        fig4.update_traces(
            texttemplate='%{text:.1f}',
            textposition='outside'
        )

        fig4.update_layout(
            title_x=0.5,
            height=560,
            xaxis_title="Segmento",
            yaxis_title="Velocidad (Mbps)",
            legend_title="Tipo de Velocidad",
            xaxis_tickangle=-20,
            bargap=0.25
        )

        st.plotly_chart(fig4, use_container_width=True)

else:
    st.warning("Sin datos disponibles")

# -------- SECCIÓN 5 --------
st.header("Proveedores con Más Accesos")

if not df5.empty:
    st.dataframe(df5, use_container_width=True)

    if {"accesos"}.issubset(df5.columns):

        col_prov = df5.columns[1]
        df5_sorted = df5.sort_values("accesos", ascending=False).head(20)

        fig5 = px.treemap(
            df5_sorted,
            path=[col_prov],
            values="accesos",
            color="accesos",
            color_continuous_scale="Blues",
            title="Distribución de Accesos por Proveedor"
        )

        fig5.update_traces(
            texttemplate='<b>%{label}</b><br>%{value:,.0f}',
            textposition="middle center"
        )

        fig5.update_layout(
            title_x=0.5,
            height=620,
            margin=dict(t=60, l=20, r=20, b=20),
            coloraxis_colorbar=dict(title="Accesos")
        )

        st.plotly_chart(fig5, use_container_width=True)

else:
    st.warning("Sin datos disponibles")

# -------------------------------------------------
# PIE
# -------------------------------------------------
st.markdown("---")
st.caption("Proyecto de Análisis de Datos — Conectividad Digital en Colombia")

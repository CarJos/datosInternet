# dashboard.py
import streamlit as st
import pandas as pd
import plotly.express as px
import os

# --- 1. CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(
    page_title="Conectividad Digital - Región Paisa",
    page_icon="🌐",
    layout="wide"
)

# --- 2. CARGA DE DATOS LOCALES ---
@st.cache_data(ttl=3600)
def load_data():
    data_path = "data/"  # Carpeta donde estarán los CSV
    try:
        df1 = pd.read_csv(os.path.join(data_path, "q1_departamentos.csv"))
        df2 = pd.read_csv(os.path.join(data_path, "q2_municipios.csv"))
        df3 = pd.read_csv(os.path.join(data_path, "q3_tecnologia.csv"))
        df4 = pd.read_csv(os.path.join(data_path, "q4_velocidades.csv"))
        df5 = pd.read_csv(os.path.join(data_path, "q5_proveedores.csv"))
        return df1, df2, df3, df4, df5
    except Exception as e:
        st.error(f"Error al cargar los CSV: {e}")
        return pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()

df1, df2, df3, df4, df5 = load_data()

# --- 3. GESTIÓN DE VISTAS ---
if 'view' not in st.session_state:
    st.session_state.view = 'home'

# --- VISTA: INICIO ---
if st.session_state.view == 'home':
    st.title("🚀 Dashboard de Conectividad Digital")
    st.subheader("Proyecto Analítico - Región Paisa / Colombia")
    
    portada = "data/internet-que-es-portada-890x445-1.jpg"
    if os.path.exists(portada):
        st.image(portada, use_container_width=True, caption="Transformación Digital")
    else:
        st.image("https://www.cursosaula21.com/wp-content/uploads/2021/03/internet-que-es-portada-890x445-1.jpg", use_container_width=True)
    
    if st.button("📊 Entrar al Dashboard", use_container_width=True):
        st.session_state.view = 'dashboard'
        st.rerun()

# --- VISTA: DASHBOARD ---
else:
    st.sidebar.header("Panel de Control")
    if st.sidebar.button("🏠 Volver al Inicio"):
        st.session_state.view = 'home'
        st.rerun()

    st.title("📊 Dashboard Interactivo - Conectividad Digital")

    # --- FILTROS GLOBALES ---
    año_opciones = sorted(df1["anio"].dropna().unique()) if not df1.empty else []
    año_sel = st.sidebar.selectbox("Filtrar por Año:", año_opciones, index=0)

    deptos_opciones = sorted(df1[df1["anio"]==año_sel][df1.columns[1]].unique()) if not df1.empty else []
    depto_sel = st.sidebar.multiselect("Filtrar por Departamento:", deptos_opciones, default=deptos_opciones)

    tab1, tab2 = st.tabs(["📈 Visualización", "📋 Datos y Descarga"])

    with tab1:
        col1, col2 = st.columns(2)

        # --- Gráfico Departamentos ---
        with col1:
            if not df1.empty:
                df_dep = df1[df1[df1.columns[1]].isin(depto_sel) & (df1["anio"]==año_sel)]
                fig_dep = px.bar(df_dep, x=df_dep.columns[1], y="accesos", title="Accesos por Departamento")
                st.plotly_chart(fig_dep, use_container_width=True)

        # --- Top Municipios ---
        with col2:
            if not df2.empty:
                df_mun = df2[df2[df2.columns[1]].isin(depto_sel) & (df2["anio"]==año_sel)]
                top_munis = df_mun.sort_values("accesos", ascending=False).head(10)
                fig_munis = px.bar(top_munis, x="accesos", y=top_munis.columns[1], orientation='h', title="Top 10 Municipios")
                st.plotly_chart(fig_munis, use_container_width=True)

        # --- Accesos por Tecnología ---
        if not df3.empty:
            df_tec = df3[df3["anio"]==año_sel]
            fig_tec = px.pie(df_tec, values="accesos", names=df_tec.columns[1], title="Accesos por Tecnología", hole=0.3)
            st.plotly_chart(fig_tec, use_container_width=True)

        # --- Velocidad promedio por segmento ---
        if not df4.empty:
            df_vel = df4[df4["anio"]==año_sel]
            fig_vel = px.bar(df_vel, x=df_vel.columns[1], y="VELOCIDAD_BAJADA", title="Velocidad Promedio por Segmento (Bajada)")
            st.plotly_chart(fig_vel, use_container_width=True)

        # --- Proveedores sobre promedio ---
        if not df5.empty:
            df_prov = df5[df5["anio"]==año_sel]
            fig_prov = px.bar(df_prov, x=df_prov.columns[1], y="accesos", title="Proveedores sobre Promedio Global")
            st.plotly_chart(fig_prov, use_container_width=True)

    with tab2:
        st.write("### Tablas de Datos")
        for i, df in enumerate([df1, df2, df3, df4, df5], start=1):
            if not df.empty:
                st.write(f"#### Dataset Q{i}")
                st.dataframe(df, use_container_width=True)
                csv = df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label=f"📥 Descargar Q{i} como CSV",
                    data=csv,
                    file_name=f'q{i}.csv',
                    mime='text/csv'
                )

st.markdown("<br><hr><center style='color:gray'>Proyecto Analítico - Región Paisa 2026</center>", unsafe_allow_html=True)

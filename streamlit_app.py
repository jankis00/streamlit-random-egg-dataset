import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

# Configuración de la página
st.set_page_config(
    page_title="Estadísticas Huevos",
    page_icon="🥚",
    layout="wide"
)

# Funciones auxiliares
@st.cache_data
def procesar_datos(df):
    """Limpia y procesa los datos del DataFrame."""
    if df is not None:
        # Convertir columnas a numérico
        df['Resistencia Cascara'] = pd.to_numeric(df['Resistencia Cascara'], errors='coerce')
        df.loc[df['Resistencia Cascara'] < 2.0, 'Resistencia Cascara'] = np.nan
        df['SEMANA correlativa'] = df['SEMANA correlativa'].astype(int)
        return df
    return None

def valores_muestra_pabellon(df):
    
    pabellones=df["Pabellón N°"].unique()
    for pabellon in pabellones:
        cantidad=[]
        semana_estudio_pos=[]
        pabellon_pos=[]
        semana_pos=[]
        Peso_Huevo=[]
        HU=[]
        Resistencia_Cascara=[]
        Espesor_Cascara=[]
        cantidad_D=[]
        semana_estudio_pos_D=[]
        pabellon_pos_D=[]
        semana_pos_D=[]
        Peso_Huevo_D=[]
        HU_D=[]
        Resistencia_Cascara_D=[]
        Espesor_Cascara_D=[]
        
        st.markdown(f"## 🛖 Pabellón {pabellon}")
        df_temp=df[df["Pabellón N°"]==pabellon]
        semanas=df_temp["SEMANA correlativa"].unique()
        for semana in semanas:
            df_temp2=df_temp[df_temp["SEMANA correlativa"]==semana]
            df_temp3=df_temp2  # Simplificamos ya que semana y semana_estudio son lo mismo
            
            cantidad.append(len(df_temp3))
            semana_estudio_pos.append(semana)
            pabellon_pos.append(pabellon)
            semana_pos.append(semana)
            
            # Calcular medias con manejo de errores
            Peso_Huevo.append(df_temp3["Peso huevo"].mean())
            HU.append(pd.to_numeric(df_temp3["HU"], errors='coerce').mean())
            Resistencia_Cascara.append(pd.to_numeric(df_temp3["Resistencia Cascara"], errors='coerce').mean())
            Espesor_Cascara.append(pd.to_numeric(df_temp3["Espesor Cascara"], errors='coerce').mean())

            df_temp2=df_temp[df_temp["SEMANA correlativa"]==semana]
            df_temp3=df_temp2  # Simplificamos ya que semana y semana_estudio son lo mismo
            
            cantidad_D.append(len(df_temp3))
            semana_estudio_pos_D.append(semana)
            pabellon_pos_D.append(pabellon)
            semana_pos_D.append(semana)
            
            # Calcular desviaciones estándar con manejo de errores
            Peso_Huevo_D.append(df_temp3["Peso huevo"].std())
            HU_D.append(pd.to_numeric(df_temp3["HU"], errors='coerce').std())
            Resistencia_Cascara_D.append(pd.to_numeric(df_temp3["Resistencia Cascara"], errors='coerce').std())
            Espesor_Cascara_D.append(pd.to_numeric(df_temp3["Espesor Cascara"], errors='coerce').std())



        df_m=pd.DataFrame({
            "cantidad": cantidad,
            "Semana estudio": semana_estudio_pos,
            "Pabellon": pabellon_pos,
            "SEMANA correlativa": semana_pos,
            "Peso Huevo": Peso_Huevo,
            "HU": HU,
            "Resistencia_Cascara": Resistencia_Cascara,
            "Espesor Cascara": Espesor_Cascara,

        })
        st.markdown(f"### Medias por semana")
        df_m_sorted = df_m.sort_values(by='SEMANA correlativa', ascending=True)
        st.dataframe(df_m_sorted)

            
        df_d=pd.DataFrame({
            "cantidad": cantidad_D,
            "Semana estudio": semana_estudio_pos_D,
            "Pabellon": pabellon_pos_D,
            "SEMANA correlativa": semana_pos_D,
            "Peso Huevo": Peso_Huevo_D,
            "HU": HU_D,
            "Resistencia_Cascara": Resistencia_Cascara_D,
            "Espesor Cascara": Espesor_Cascara,
        })

        st.markdown(f"### Desviaciones por semana")
        df_d_sorted = df_d.sort_values(by='SEMANA correlativa', ascending=True)
        st.dataframe(df_d_sorted)
        st.markdown(f"### Descripción de la muestra")
        st.dataframe(df_temp2.describe())
        st.divider()


def mostrar_tabla_datos(df):
    """Muestra estadísticas descriptivas de los datos."""
    st.subheader("🎫 Datos sin procesar")
    st.dataframe(df)

def crear_histograma(df):
    """Crea un gráfico de distribución para una columna específica."""
    st.markdown(f"## Histograma")
    col1, col2 = st.columns(2)
    with col1:
        columna_seleccionada = st.selectbox(
                "Selecciona una columna para visualizar:",
                options=df.select_dtypes(include=['float64', 'int64']).columns
            )
    with col2:
        marginal_seleccionado = st.radio(
                    "Elige el tipo de gráfica marginal",
                    ["box", "violin", "rug"],
                    index = 0,
                    )
    fig = px.histogram(df, x=columna_seleccionada, color="Pabellón N°",
                   marginal=marginal_seleccionado, # or violin, rug
                   hover_data=df.columns)
    st.plotly_chart(fig, use_container_width=True)
    st.divider()


def crear_dispersion(df):
    """Crea un gráfico de distribución para una columna específica."""
    st.markdown(f"## Dispersión de valores")
    col1, col2 = st.columns(2)
    with col1:
        columna_seleccionada_x = st.selectbox(
                "Selecciona eje X:",
                options=df.columns
            )
    with col2:
        columna_seleccionada_y = st.selectbox(
                "Selecciona eje Y:",
                options=df.columns
            )
    
    fig = px.scatter(df, x=columna_seleccionada_x, y=columna_seleccionada_y, color="Pabellón N°")
    st.plotly_chart(fig, use_container_width=True)
    st.divider()

def crear_media_valores_en_semana(df):
    """Crea un gráfico de línea mostrando la evolución de valores por semana."""
    st.markdown("## Evolución temporal de valores")
    
    # Seleccionar la variable a analizar
    columna_seleccionada = st.selectbox(
        "Selecciona la variable a analizar:",
        options=df.select_dtypes(include=['float64', 'int64']).columns,
        key="variable_temporal"
    )

    # Agrupar por semana y pabellón, calculando la media de la variable seleccionada
    df_agrupado = df.groupby(['SEMANA correlativa', 'Pabellón N°'])[columna_seleccionada].mean().reset_index()

    # Crear el gráfico de líneas
    fig = px.line(
        df_agrupado, 
        x='SEMANA correlativa', 
        y=columna_seleccionada, 
        color='Pabellón N°',
        title=f'Evolución de {columna_seleccionada} por semana y pabellón',
        labels={'SEMANA correlativa': 'Semana', columna_seleccionada: f'Media de {columna_seleccionada}'}
    )
    
    # Personalizar el diseño del gráfico
    fig.update_layout(
        xaxis_title="Semana",
        yaxis_title=f"Media de {columna_seleccionada}",
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Mostrar tabla con los valores
    st.markdown("## Tabla de valores")
    st.dataframe(df_agrupado.sort_values(['Pabellón N°', 'SEMANA correlativa']))
    st.divider()

def crear_relación_HU_Resistencia_Cascara(df):
    """Crea un gráfico de distribución para una columna específica."""
    st.markdown(f"## Dispersión de valores")
    
    # Filtro de color de huevo
    colores_huevo = df['Color huevo'].unique()
    colores_seleccionados = st.multiselect(
        "Colores de huevo:",
        options=colores_huevo,
        default=colores_huevo
    )
    df_temp=df[df["Color huevo"].isin(colores_seleccionados)]
    
    fig = px.scatter_3d(df_temp, x='SEMANA correlativa', y='Resistencia Cascara', z='Espesor Cascara',color='SEMANA correlativa')
    st.plotly_chart(fig, use_container_width=True)
    st.divider()


# Interfaz principal
def main():
    st.title("🥚 Estadísticas Huevos")
    as1, as2 = st.columns(2)
    with as1:
        st.markdown("#### Para hacer funcionar este dashboard puedes descargar el archivo de ejemplo y crear uno nuevo en [Google COLAB](https://colab.research.google.com/drive/18LTolzqH2MqrHk7-FEoGMdtpEU9oB0pe?usp=sharing)")
    with as2:
        st.download_button(
            label="📥 Descargar archivo de ejemplo",
            data=open("df.xlsx", "rb"),
            file_name="ejemplo_datos_huevos.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            help="Archivo de ejemplo para hacer funcionar el dashboard"
        )
    # Pestañas para diferentes vistas
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["📋 Datos", "📊 Estadísticas", "🏦 Histograma", "👨‍👩‍👦‍👦 Dispersión", "🔍 Evolución de las medias", "🔍 Evolución de la cascara"])
    
    with tab1:
        # Sección de carga de archivo
        st.markdown("# Carga de Datos 📊")
        uploaded_file = st.file_uploader(
            "Cargar archivo Excel",
            type=['xlsx', 'xls'],
            help="Selecciona un archivo Excel con los datos de los huevos"
        )
        
        if uploaded_file is not None:
            df = pd.read_excel(uploaded_file)
            df = procesar_datos(df)
            if df is not None:
                st.session_state['datos_huevos'] = df
                st.success("✅ Archivo cargado exitosamente")
                mostrar_tabla_datos(df)
    
    # Verificar si hay datos cargados para mostrar el resto de las pestañas
    if 'datos_huevos' in st.session_state:
        df = st.session_state['datos_huevos']
        
        # Sidebar con filtros
        st.sidebar.title("⚙️ Filtros")
        
        # Filtro de pabellón
        pabellones = df['Pabellón N°'].unique()
        pabellones_seleccionados = st.sidebar.multiselect(
            "Pabellones disponibles",
            options=pabellones,
            default=pabellones
        )
        
        # Aplicar filtros
        df_filtrado = df[
            (df['Pabellón N°'].isin(pabellones_seleccionados))
        ]
        
        with tab2:
            valores_muestra_pabellon(df_filtrado)
        
        with tab3:
            crear_histograma(df_filtrado)

        with tab4:
            crear_dispersion(df_filtrado)
            
        with tab5:
            crear_media_valores_en_semana(df_filtrado)
            
        with tab6:
            crear_relación_HU_Resistencia_Cascara(df_filtrado)
    else:
        with tab2:
            st.info("👆 Por favor, carga primero los datos en la pestaña 'Datos'")
        with tab3:
            st.info("👆 Por favor, carga primero los datos en la pestaña 'Datos'")
        with tab4:
            st.info("👆 Por favor, carga primero los datos en la pestaña 'Datos'")
        with tab5:
            st.info("👆 Por favor, carga primero los datos en la pestaña 'Datos'")
        with tab6:
            st.info("👆 Por favor, carga primero los datos en la pestaña 'Datos'")

if __name__ == "__main__":
    main()



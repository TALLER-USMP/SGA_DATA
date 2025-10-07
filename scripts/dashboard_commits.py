#!/usr/bin/env python3
"""
Dashboard Interactivo de Commits GitHub - Streamlit
=================================================

Dashboard web interactivo que muestra estadísticas y visualizaciones
de los commits extraídos de Slack en formato Excel.

Características:
- Carga automática de archivos Excel
- Gráficos interactivos con Plotly
- Filtros dinámicos
- Métricas en tiempo real
- Tablas explorables
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import glob
import os
from datetime import datetime, timedelta
import numpy as np
import re


# Configuración de la página
st.set_page_config(
    page_title="📊 Dashboard de Commits GitHub",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

class CommitsDashboard:
    """
    Clase principal del dashboard de commits
    """
    
    def __init__(self):
        self.df = None
        self.archivos_disponibles = []

        
    def cargar_archivos_excel(self):
        """
        Busca y carga archivos Excel disponibles en la carpeta 'data'.
        """
        carpeta_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        if not os.path.exists(carpeta_data):
            return []
        archivos_excel = glob.glob(os.path.join(carpeta_data, "*.xlsx"))
        # Filtrar archivos que probablemente contengan datos de commits
        archivos_commits = [os.path.basename(f) for f in archivos_excel if any(keyword in os.path.basename(f).lower() 
                           for keyword in ['registro', 'commit', 'github', 'back', 'front'])]
        return archivos_commits
    
    def leer_excel_commits(self, archivo):
        """
        Lee un archivo Excel y extrae los datos de commits desde la carpeta 'data'.
        """
        try:
            carpeta_data = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
            ruta_archivo = os.path.join(carpeta_data, archivo)
            # Intentar leer la hoja "Todos_los_Commits" primero
            try:
                df = pd.read_excel(ruta_archivo, sheet_name='Todos_los_Commits')
            except:
                # Si no existe, leer la primera hoja
                df = pd.read_excel(ruta_archivo, sheet_name=0)
            # Verificar que tenga las columnas esperadas
            columnas_requeridas = ['repository', 'author_display', 'commit_message']
            if not all(col in df.columns for col in columnas_requeridas):
                # Intentar con nombres alternativos
                df = df.rename(columns={
                    'author_username': 'author_display',
                    'message': 'commit_message',
                    'repo': 'repository'
                })
            return df
        except Exception as e:
            st.error(f"Error al leer {archivo}: {e}")
            return None
    
    def procesar_timestamps(self, df):
        """
        Procesa las columnas de timestamp para análisis temporal
        """
        if 'slack_timestamp' in df.columns:
            try:
                df['slack_timestamp'] = pd.to_datetime(df['slack_timestamp'])
                df['fecha'] = df['slack_timestamp'].dt.date
                df['hora'] = df['slack_timestamp'].dt.hour
                df['dia_semana'] = df['slack_timestamp'].dt.day_name()
            except:
                pass
        
        return df
    

    def analizar_pull_requests(self, df):
        """
        Analiza los commits para detectar Pull Requests basándose en patrones de mensajes
        """
        if 'commit_message' not in df.columns:
            return df
        
        # Patrones comunes de Pull Requests
        patrones_pr = [
            r'merge pull request #(\d+)',
            r'merged? pr #(\d+)',
            r'merge.*#(\d+)',
            r'pull request.*#(\d+)',
            r'merged.*into.*',
            r'merge branch.*into.*',
            r'merge.*from.*',
            r'merged.*branch.*',
            r'auto.*merge',
            r'automatic merge'
        ]
        
        # Crear columna para indicar si es PR
        df['es_pull_request'] = False
        df['numero_pr'] = None
        df['tipo_commit'] = 'Commit Regular'
        
        for idx in df.index:
            mensaje = str(df.loc[idx, 'commit_message']).lower()
            
            # Buscar patrones de PR
            for patron in patrones_pr:
                import re
                match = re.search(patron, mensaje, re.IGNORECASE)
                if match:
                    df.loc[idx, 'es_pull_request'] = True
                    df.loc[idx, 'tipo_commit'] = 'Pull Request'
                    
                    # Extraer número de PR si está disponible
                    if match.groups():
                        try:
                            df.loc[idx, 'numero_pr'] = int(match.group(1))
                        except:
                            pass
                    break
        
        return df
    
    def crear_grafico_tipo_commits(self, df):
        """
        Crea gráfico de distribución entre commits regulares y PRs
        """
        if 'tipo_commit' in df.columns:
            tipo_commits = df['tipo_commit'].value_counts().reset_index()
            tipo_commits.columns = ['Tipo', 'Cantidad']
            
            fig = px.pie(
                tipo_commits,
                values='Cantidad',
                names='Tipo',
                title="🔄 Distribución: Commits vs Pull Requests",
                color_discrete_map={
                    'Commit Regular': '#3498db',
                    'Pull Request': '#e74c3c'
                }
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label+value')
            
            return fig
        return None
    
    def crear_metricas_pull_requests(self, df):
        """
        Crea métricas específicas de Pull Requests
        """
        if 'es_pull_request' not in df.columns:
            return
        
        col1, col2, col3, col4 = st.columns(4)
        
        total_prs = df['es_pull_request'].sum()
        total_commits_regulares = (~df['es_pull_request']).sum()
        ratio_pr = (total_prs / len(df) * 100) if len(df) > 0 else 0
        
        with col1:
            st.metric(
                label="🔄 Pull Requests",
                value=int(total_prs),
                delta=f"{ratio_pr:.1f}% del total"
            )
        
        with col2:
            st.metric(
                label="📝 Commits Regulares",
                value=int(total_commits_regulares)
            )
        
        with col3:
            # PRs únicos (por número)
            prs_unicos = df[df['es_pull_request'] & df['numero_pr'].notna()]['numero_pr'].nunique()
            st.metric(
                label="🆔 PRs Únicos",
                value=prs_unicos if prs_unicos > 0 else "N/A"
            )
        
        with col4:
            # Promedio de commits por PR (si hay PRs numerados)
            if total_prs > 0 and prs_unicos > 0:
                avg_commits_por_pr = total_prs / prs_unicos
                st.metric(
                    label="📊 Avg Commits/PR",
                    value=f"{avg_commits_por_pr:.1f}"
                )
            else:
                st.metric(
                    label="📊 Avg Commits/PR",
                    value="N/A"
                )
    
    def crear_metricas_principales(self, df):
        """
        Crea las métricas principales del dashboard
        """
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_commits = len(df)
            st.metric(
                label="📝 Total Commits",
                value=total_commits,
                delta=f"+{total_commits} nuevos"
            )
        
        with col2:
            total_repos = df['repository'].nunique() if 'repository' in df.columns else 0
            st.metric(
                label="📁 Repositorios",
                value=total_repos
            )
        
        with col3:
            total_autores = df['author_display'].nunique() if 'author_display' in df.columns else 0
            st.metric(
                label="👥 Autores",
                value=total_autores
            )
        
        with col4:
            archivos_origen = df['archivo_origen'].nunique() if 'archivo_origen' in df.columns else 1
            st.metric(
                label="📄 Archivos Fuente",
                value=archivos_origen
            )
    
    def crear_grafico_commits_por_autor(self, df):
        """
        Crea gráfico de commits por autor
        """
        if 'author_display' in df.columns:
            commits_por_autor = df['author_display'].value_counts().reset_index()
            commits_por_autor.columns = ['Autor', 'Commits']
            
            fig = px.bar(
                commits_por_autor.head(10),
                x='Commits',
                y='Autor',
                orientation='h',
                title="🏆 Top 10 Autores por Commits",
                color='Commits',
                color_continuous_scale='viridis'
            )
            
            fig.update_layout(
                height=400,
                yaxis={'categoryorder': 'total ascending'}
            )
            
            return fig
        return None
    
    def crear_grafico_commits_por_repo(self, df):
        """
        Crea gráfico de commits por repositorio
        """
        if 'repository' in df.columns:
            commits_por_repo = df['repository'].value_counts().reset_index()
            commits_por_repo.columns = ['Repositorio', 'Commits']
            
            fig = px.pie(
                commits_por_repo,
                values='Commits',
                names='Repositorio',
                title="📊 Distribución de Commits por Repositorio"
            )
            
            fig.update_traces(textposition='inside', textinfo='percent+label')
            
            return fig
        return None
    
    def crear_timeline_commits(self, df):
        """
        Crea timeline de commits por fecha
        """
        if 'slack_timestamp' in df.columns:
            try:
                df['fecha'] = pd.to_datetime(df['slack_timestamp']).dt.date
                commits_por_fecha = df.groupby('fecha').size().reset_index()
                commits_por_fecha.columns = ['Fecha', 'Commits']
                
                fig = px.line(
                    commits_por_fecha,
                    x='Fecha',
                    y='Commits',
                    title="📈 Timeline de Commits",
                    markers=True
                )
                
                fig.update_layout(
                    height=400,
                    xaxis_title="Fecha",
                    yaxis_title="Número de Commits"
                )
                
                return fig
            except:
                pass
        return None
    
    def crear_heatmap_actividad(self, df):
        """
        Crea heatmap de actividad por día y hora
        """
        if 'slack_timestamp' in df.columns:
            try:
                df_temp = df.copy()
                df_temp['timestamp'] = pd.to_datetime(df_temp['slack_timestamp'])
                df_temp['dia'] = df_temp['timestamp'].dt.day_name()
                df_temp['hora'] = df_temp['timestamp'].dt.hour
                
                # Crear matriz de actividad
                actividad = df_temp.groupby(['dia', 'hora']).size().unstack(fill_value=0)
                
                # Reordenar días de la semana
                dias_orden = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
                actividad = actividad.reindex(dias_orden)
                
                fig = px.imshow(
                    actividad.values,
                    x=actividad.columns,
                    y=actividad.index,
                    title="🔥 Heatmap de Actividad (Día vs Hora)",
                    color_continuous_scale='YlOrRd',
                    aspect='auto'
                )
                
                fig.update_layout(
                    xaxis_title="Hora del Día",
                    yaxis_title="Día de la Semana",
                    height=400
                )
                
                return fig
            except Exception as e:
                st.write(f"Debug: Error en heatmap: {e}")
        return None
    
    def crear_tabla_filtrable(self, df):
        """
        Crea tabla filtrable de commits
        """
        st.subheader("🔍 Explorador de Commits")
        
        # Filtros en dos filas
        st.markdown("**Filtros de búsqueda:**")
        
        # Primera fila de filtros
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if 'repository' in df.columns:
                repos_seleccionados = st.multiselect(
                    "📁 Repositorio:",
                    options=df['repository'].unique(),
                    default=df['repository'].unique()
                )
            else:
                repos_seleccionados = []
        
        with col2:
            if 'author_display' in df.columns:
                autores_seleccionados = st.multiselect(
                    "👤 Autor:",
                    options=df['author_display'].unique(),
                    default=df['author_display'].unique()
                )
            else:
                autores_seleccionados = []
        
        with col3:
            if 'archivo_origen' in df.columns:
                archivos_seleccionados = st.multiselect(
                    "📄 Archivo:",
                    options=df['archivo_origen'].unique(),
                    default=df['archivo_origen'].unique()
                )
            else:
                archivos_seleccionados = []
        
        # Segunda fila de filtros (Pull Requests)
        col4, col5, col6 = st.columns(3)
        
        with col4:
            if 'tipo_commit' in df.columns:
                tipos_seleccionados = st.multiselect(
                    "🔄 Tipo de Commit:",
                    options=df['tipo_commit'].unique(),
                    default=df['tipo_commit'].unique()
                )
            else:
                tipos_seleccionados = []
        
        with col5:
            # Filtro por texto en mensaje
            filtro_mensaje = st.text_input(
                "🔍 Buscar en mensaje:",
                placeholder="Ej: fix, feature, merge..."
            )
        
        with col6:
            # Filtro por rango de fechas (si hay timestamps)
            if 'slack_timestamp' in df.columns:
                usar_filtro_fecha = st.checkbox("📅 Filtrar por fecha")
                if usar_filtro_fecha:
                    fecha_min = df['slack_timestamp'].min().date()
                    fecha_max = df['slack_timestamp'].max().date()
                    
                    rango_fechas = st.date_input(
                        "Seleccionar rango:",
                        value=(fecha_min, fecha_max),
                        min_value=fecha_min,
                        max_value=fecha_max
                    )
                else:
                    rango_fechas = None
            else:
                rango_fechas = None
        
        # Aplicar filtros
        df_filtrado = df.copy()
        
        if repos_seleccionados and 'repository' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['repository'].isin(repos_seleccionados)]
        
        if autores_seleccionados and 'author_display' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['author_display'].isin(autores_seleccionados)]
        
        if archivos_seleccionados and 'archivo_origen' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['archivo_origen'].isin(archivos_seleccionados)]
        
        if tipos_seleccionados and 'tipo_commit' in df.columns:
            df_filtrado = df_filtrado[df_filtrado['tipo_commit'].isin(tipos_seleccionados)]
        
        if filtro_mensaje and 'commit_message' in df.columns:
            df_filtrado = df_filtrado[
                df_filtrado['commit_message'].str.contains(filtro_mensaje, case=False, na=False)
            ]
        
        if rango_fechas and len(rango_fechas) == 2:
            fecha_inicio, fecha_fin = rango_fechas
            df_filtrado = df_filtrado[
                (df_filtrado['slack_timestamp'].dt.date >= fecha_inicio) &
                (df_filtrado['slack_timestamp'].dt.date <= fecha_fin)
            ]
        
        # Mostrar estadísticas del filtro
        col_stats1, col_stats2, col_stats3 = st.columns(3)
        
        with col_stats1:
            st.info(f"📊 **{len(df_filtrado)}** de **{len(df)}** commits")
        
        with col_stats2:
            if 'es_pull_request' in df_filtrado.columns:
                prs_filtrados = df_filtrado['es_pull_request'].sum()
                st.info(f"🔄 **{prs_filtrados}** Pull Requests")
        
        with col_stats3:
            if 'repository' in df_filtrado.columns:
                repos_filtrados = df_filtrado['repository'].nunique()
                st.info(f"📁 **{repos_filtrados}** repositorio(s)")
        
        # Mostrar tabla
        st.dataframe(
            df_filtrado,
            use_container_width=True,
            height=400
        )
    
    def ejecutar_dashboard(self):
        """
        Ejecuta el dashboard principal
        """
        # Header
        st.title("🚀 Dashboard de Commits GitHub")
        st.markdown("---")
        # Sidebar para configuración
        with st.sidebar:
            st.header("📁 Configuración")
            archivos_disponibles = self.cargar_archivos_excel()
            if not archivos_disponibles:
                st.error("❌ No se encontraron archivos Excel")
                st.info("💡 Ejecuta primero el extractor GUI para generar archivos Excel")
                return
            archivo_seleccionado = st.selectbox(
                "Selecciona archivo Excel:",
                archivos_disponibles
            )
            if st.button("🔄 Recargar Datos"):
                st.cache_data.clear()
        # Cargar datos
        if archivo_seleccionado:
            with st.spinner("Cargando datos..."):
                df = self.leer_excel_commits(archivo_seleccionado)
                if df is None or df.empty:
                    st.error("❌ No se pudieron cargar los datos del archivo")
                    return
                # Procesar timestamps
                df = self.procesar_timestamps(df)
                # Analizar Pull Requests
                df = self.analizar_pull_requests(df)
                # Mostrar información del archivo
                st.success(f"✅ Datos cargados desde: {archivo_seleccionado}")
                st.info(f"📊 {len(df)} commits encontrados")
            # Métricas principales
            self.crear_metricas_principales(df)
            # Métricas de Pull Requests
            st.markdown("### 🔄 Análisis de Pull Requests")
            self.crear_metricas_pull_requests(df)
            st.markdown("---")
            # Gráficos principales
            col1, col2 = st.columns(2)
            with col1:
                fig_autores = self.crear_grafico_commits_por_autor(df)
                if fig_autores:
                    st.plotly_chart(fig_autores, use_container_width=True)
            with col2:
                fig_tipo = self.crear_grafico_tipo_commits(df)
                if fig_tipo:
                    st.plotly_chart(fig_tipo, use_container_width=True)
            # Segunda fila de gráficos
            col3, col4 = st.columns(2)
            with col3:
                fig_repos = self.crear_grafico_commits_por_repo(df)
                if fig_repos:
                    st.plotly_chart(fig_repos, use_container_width=True)
            with col4:
                fig_timeline = self.crear_timeline_commits(df)
                if fig_timeline:
                    st.plotly_chart(fig_timeline, use_container_width=True)
            # Heatmap (ancho completo)
            fig_heatmap = self.crear_heatmap_actividad(df)
            if fig_heatmap:
                st.plotly_chart(fig_heatmap, use_container_width=True)
            st.markdown("---")
            # Tabla filtrable de commits
            self.crear_tabla_filtrable(df)
            # Footer
            st.markdown("---")
            st.markdown("🔧 **Dashboard creado con Streamlit** | 📊 Datos extraídos con Extractor GUI")

def main():
    """
    Función principal
    """
    dashboard = CommitsDashboard()
    dashboard.ejecutar_dashboard()

if __name__ == "__main__":
    main()
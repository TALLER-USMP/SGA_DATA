#!/usr/bin/env python3
"""
Extractor de Commits con Interfaz Gráfica
=========================================

Versión con interfaz gráfica que permite seleccionar múltiples archivos JSON
de Slack para procesar todos los commits de GitHub en un solo reporte.

Características:
- Selección múltiple de archivos JSON
- Procesamiento combinado de todos los archivos
- Interfaz gráfica amigable
- Reporte Excel consolidado
"""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from pathlib import Path
import threading
from slack_github_extractor import SlackGitHubExtractor
import pandas as pd
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class GitHubExtractorGUI:
    """
    Interfaz gráfica para el extractor de commits de GitHub
    """
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Extractor de Commits GitHub - Slack")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Variables
        self.archivos_seleccionados = []
        self.procesando = False
        
        self.configurar_interfaz()
    
    def configurar_interfaz(self):
        """
        Configura todos los elementos de la interfaz
        """
        # Título principal
        titulo = tk.Label(
            self.root, 
            text="🚀 Extractor de Commits GitHub desde Slack",
            font=("Arial", 16, "bold"),
            fg="darkblue"
        )
        titulo.pack(pady=10)
        
        # Subtítulo
        subtitulo = tk.Label(
            self.root,
            text="Selecciona uno o más archivos JSON de Slack para extraer commits",
            font=("Arial", 10),
            fg="gray"
        )
        subtitulo.pack(pady=(0, 20))
        
        # Frame para selección de archivos
        frame_archivos = tk.LabelFrame(self.root, text="📁 Archivos JSON", font=("Arial", 12, "bold"))
        frame_archivos.pack(fill="both", expand=True, padx=20, pady=10)
        
        # Botón para seleccionar archivos
        btn_seleccionar = tk.Button(
            frame_archivos,
            text="📂 Seleccionar Archivos JSON",
            command=self.seleccionar_archivos,
            bg="lightblue",
            font=("Arial", 10, "bold"),
            height=2
        )
        btn_seleccionar.pack(pady=10)
        
        # Lista de archivos seleccionados
        self.listbox_archivos = tk.Listbox(
            frame_archivos,
            height=6,
            font=("Arial", 9)
        )
        self.listbox_archivos.pack(fill="both", expand=True, padx=10, pady=5)
        
        # Scrollbar para la lista
        scrollbar = tk.Scrollbar(frame_archivos)
        scrollbar.pack(side="right", fill="y")
        self.listbox_archivos.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.listbox_archivos.yview)
        
        # Botón para limpiar selección
        btn_limpiar = tk.Button(
            frame_archivos,
            text="🗑️ Limpiar Selección",
            command=self.limpiar_seleccion,
            bg="lightcoral"
        )
        btn_limpiar.pack(pady=(5, 10))
        
        # Frame para configuración
        frame_config = tk.LabelFrame(self.root, text="⚙️ Configuración", font=("Arial", 12, "bold"))
        frame_config.pack(fill="x", padx=20, pady=10)
        
        # Nombre del archivo de salida
        tk.Label(frame_config, text="📄 Nombre del archivo Excel:").pack(anchor="w", padx=10, pady=(10, 5))
        self.entry_nombre = tk.Entry(frame_config, width=50)
        self.entry_nombre.insert(0, "commits_consolidados.xlsx")
        self.entry_nombre.pack(padx=10, pady=(0, 10))
        
        # Frame para botones principales
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(fill="x", padx=20, pady=20)
        
        # Botón procesar
        self.btn_procesar = tk.Button(
            frame_botones,
            text="🚀 Procesar Archivos",
            command=self.iniciar_procesamiento,
            bg="lightgreen",
            font=("Arial", 12, "bold"),
            height=2
        )
        self.btn_procesar.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        # Botón salir
        btn_salir = tk.Button(
            frame_botones,
            text="❌ Salir",
            command=self.root.quit,
            bg="lightgray",
            font=("Arial", 12, "bold"),
            height=2
        )
        btn_salir.pack(side="right")
        
        # Barra de progreso
        self.progress = ttk.Progressbar(
            self.root,
            mode='indeterminate'
        )
        self.progress.pack(fill="x", padx=20, pady=(0, 10))
        
        # Área de estado
        self.label_estado = tk.Label(
            self.root,
            text="✅ Listo para procesar archivos",
            font=("Arial", 10),
            fg="green"
        )
        self.label_estado.pack(pady=(0, 10))
    
    def seleccionar_archivos(self):
        """
        Abre el diálogo para seleccionar múltiples archivos JSON
        """
        archivos = filedialog.askopenfilenames(
            title="Seleccionar archivos JSON de Slack",
            filetypes=[
                ("Archivos JSON", "*.json"),
                ("Todos los archivos", "*.*")
            ],
            initialdir=os.getcwd()
        )
        
        if archivos:
            self.archivos_seleccionados = list(archivos)
            self.actualizar_lista_archivos()
            self.label_estado.config(
                text=f"✅ {len(archivos)} archivo(s) seleccionado(s)",
                fg="green"
            )
    
    def actualizar_lista_archivos(self):
        """
        Actualiza la lista visual de archivos seleccionados
        """
        self.listbox_archivos.delete(0, tk.END)
        for archivo in self.archivos_seleccionados:
            nombre = Path(archivo).name
            self.listbox_archivos.insert(tk.END, f"📄 {nombre}")
    
    def limpiar_seleccion(self):
        """
        Limpia la selección de archivos
        """
        self.archivos_seleccionados = []
        self.listbox_archivos.delete(0, tk.END)
        self.label_estado.config(
            text="🗑️ Selección limpiada - Listo para seleccionar nuevos archivos",
            fg="blue"
        )
    
    def iniciar_procesamiento(self):
        """
        Inicia el procesamiento en un hilo separado
        """
        if not self.archivos_seleccionados:
            messagebox.showwarning(
                "Advertencia",
                "Por favor selecciona al menos un archivo JSON"
            )
            return
        
        if self.procesando:
            messagebox.showinfo(
                "Información",
                "Ya hay un procesamiento en curso"
            )
            return
        
        # Iniciar procesamiento en hilo separado
        thread = threading.Thread(target=self.procesar_archivos)
        thread.daemon = True
        thread.start()
    
    def procesar_archivos(self):
        """
        Procesa todos los archivos seleccionados
        """
        try:
            self.procesando = True
            self.btn_procesar.config(state="disabled")
            self.progress.start()
            
            # Actualizar estado
            self.root.after(0, lambda: self.label_estado.config(
                text="🔄 Procesando archivos...", fg="blue"
            ))
            
            todos_los_commits = []
            archivos_procesados = 0
            archivos_con_error = []
            
            for archivo in self.archivos_seleccionados:
                try:
                    self.root.after(0, lambda a=archivo: self.label_estado.config(
                        text=f"🔄 Procesando: {Path(a).name}", fg="blue"
                    ))
                    
                    # Crear extractor para este archivo
                    extractor = SlackGitHubExtractor(archivo)
                    slack_data = extractor.load_slack_data()
                    extractor.extract_github_commits(slack_data)
                    
                    # Agregar información del archivo fuente
                    for commit in extractor.commits_data:
                        commit['archivo_origen'] = Path(archivo).name
                    
                    todos_los_commits.extend(extractor.commits_data)
                    archivos_procesados += 1
                    
                except Exception as e:
                    logger.error(f"Error procesando {archivo}: {e}")
                    archivos_con_error.append(Path(archivo).name)
            
            # Generar reporte consolidado
            if todos_los_commits:
                nombre_salida = self.entry_nombre.get().strip()
                if not nombre_salida:
                    nombre_salida = "commits_consolidados.xlsx"
                
                self.generar_reporte_consolidado(todos_los_commits, nombre_salida)
                
                # Mostrar resumen
                resumen = self.generar_resumen(todos_los_commits, archivos_procesados, archivos_con_error)
                
                self.root.after(0, lambda: self.mostrar_resultado_exitoso(resumen, nombre_salida))
            else:
                self.root.after(0, lambda: self.mostrar_sin_commits(archivos_con_error))
                
        except Exception as e:
            self.root.after(0, lambda: self.mostrar_error(str(e)))
        
        finally:
            self.procesando = False
            self.root.after(0, lambda: self.progress.stop())
            self.root.after(0, lambda: self.btn_procesar.config(state="normal"))
    
    def generar_reporte_consolidado(self, commits_data, nombre_archivo):
        """
        Genera un reporte Excel consolidado con todos los commits
        """
        df = pd.DataFrame(commits_data)
        
        # Ordenar por timestamp
        if 'slack_timestamp' in df.columns:
            df = df.sort_values('slack_timestamp', ascending=False)
        
        with pd.ExcelWriter(nombre_archivo, engine='openpyxl') as writer:
            # Hoja principal con todos los commits
            df.to_excel(writer, sheet_name='Todos_los_Commits', index=False)
            
            # Hoja agrupada por archivo fuente
            if 'archivo_origen' in df.columns:
                archivo_summary = df.groupby('archivo_origen').agg({
                    'commit_hash': 'count',
                    'repository': lambda x: ', '.join(x.unique()),
                    'author_display': lambda x: ', '.join(x.unique())
                }).rename(columns={'commit_hash': 'total_commits'})
                archivo_summary.to_excel(writer, sheet_name='Resumen_por_Archivo')
            
            # Hoja agrupada por repositorio
            if not df.empty:
                repo_summary = df.groupby('repository').agg({
                    'commit_hash': 'count',
                    'author_display': lambda x: ', '.join(x.unique()),
                    'archivo_origen': lambda x: ', '.join(x.unique()) if 'archivo_origen' in df.columns else 'N/A'
                }).rename(columns={'commit_hash': 'total_commits'})
                repo_summary.to_excel(writer, sheet_name='Resumen_por_Repositorio')
                
                # Hoja agrupada por autor
                author_summary = df.groupby('author_display').agg({
                    'commit_hash': 'count',
                    'repository': lambda x: ', '.join(x.unique()),
                    'archivo_origen': lambda x: ', '.join(x.unique()) if 'archivo_origen' in df.columns else 'N/A'
                }).rename(columns={'commit_hash': 'total_commits'})
                author_summary.to_excel(writer, sheet_name='Resumen_por_Autor')
    
    def generar_resumen(self, commits_data, archivos_procesados, archivos_con_error):
        """
        Genera un resumen estadístico del procesamiento
        """
        df = pd.DataFrame(commits_data)
        
        return {
            'total_commits': len(df),
            'archivos_procesados': archivos_procesados,
            'archivos_con_error': len(archivos_con_error),
            'repositorios': df['repository'].nunique() if not df.empty else 0,
            'autores': df['author_display'].nunique() if not df.empty else 0,
            'archivos_origen': df['archivo_origen'].nunique() if 'archivo_origen' in df.columns else 0,
            'errores': archivos_con_error
        }
    
    def mostrar_resultado_exitoso(self, resumen, nombre_archivo):
        """
        Muestra el resultado exitoso del procesamiento
        """
        mensaje = f"""🎉 PROCESAMIENTO COMPLETADO EXITOSAMENTE

📊 RESUMEN:
• Total de commits extraídos: {resumen['total_commits']}
• Archivos JSON procesados: {resumen['archivos_procesados']}
• Repositorios únicos: {resumen['repositorios']}
• Autores únicos: {resumen['autores']}
• Archivos fuente: {resumen['archivos_origen']}

📄 Archivo generado: {nombre_archivo}

El archivo Excel contiene:
• Todos_los_Commits - Lista completa
• Resumen_por_Archivo - Estadísticas por archivo JSON
• Resumen_por_Repositorio - Estadísticas por repo
• Resumen_por_Autor - Estadísticas por autor"""

        if resumen['archivos_con_error']:
            mensaje += f"\n\n⚠️ Archivos con errores: {', '.join(resumen['errores'])}"
        
        messagebox.showinfo("¡Éxito!", mensaje)
        
        self.label_estado.config(
            text=f"✅ Completado: {resumen['total_commits']} commits extraídos",
            fg="green"
        )
    
    def mostrar_sin_commits(self, archivos_con_error):
        """
        Muestra mensaje cuando no se encontraron commits
        """
        mensaje = "⚠️ No se encontraron commits de GitHub en los archivos seleccionados.\n\n"
        mensaje += "Verifica que los archivos JSON contengan notificaciones de GitHub."
        
        if archivos_con_error:
            mensaje += f"\n\nArchivos con errores: {', '.join(archivos_con_error)}"
        
        messagebox.showwarning("Sin commits", mensaje)
        
        self.label_estado.config(
            text="⚠️ No se encontraron commits en los archivos",
            fg="orange"
        )
    
    def mostrar_error(self, error):
        """
        Muestra mensaje de error
        """
        messagebox.showerror(
            "Error",
            f"❌ Error durante el procesamiento:\n\n{error}"
        )
        
        self.label_estado.config(
            text="❌ Error durante el procesamiento",
            fg="red"
        )
    
    def ejecutar(self):
        """
        Ejecuta la interfaz gráfica
        """
        self.root.mainloop()

def main():
    """
    Función principal
    """
    # Configurar logging
    logging.basicConfig(level=logging.INFO)
    
    try:
        # Crear y ejecutar la interfaz
        app = GitHubExtractorGUI()
        app.ejecutar()
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        messagebox.showerror("Error", f"Error al iniciar la aplicación:\n{e}")

if __name__ == "__main__":
    main()
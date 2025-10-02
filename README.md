# Extractor de Commits de GitHub desde Slack

Este programa procesa archivos JSON exportados de Slack que contienen notificaciones de commits de GitHub y genera reportes en Excel con información organizada de los commits.

## Características

- 📥 **Procesa archivos JSON de Slack** exportados de canales con notificaciones de GitHub
- 🔍 **Extrae información detallada** de commits incluyendo:
  - Repositorio
  - Autor (username y nombre de display)
  - Rama (branch)
  - Hash del commit
  - Mensaje del commit
  - Timestamp de la notificación en Slack
- 📊 **Genera reportes Excel** con múltiples hojas organizadas
- 📈 **Incluye estadísticas** y resúmenes por repositorio y autor

## Requisitos

- Python 3.7 o superior
- pandas
- openpyxl

## Instalación

1. **Clona o descarga** los archivos en tu directorio de trabajo

2. **Instala las dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

## Uso

### 🎯 Opción 1: Interfaz Gráfica (MÁS FÁCIL - Recomendada)

**Para seleccionar múltiples archivos JSON:**
```bash
python ejecutar_gui.py
```

**Características de la interfaz:**
- 📂 **Selección múltiple** de archivos JSON
- 🎛️ **Configuración del nombre** del archivo de salida  
- 📊 **Procesamiento consolidado** de todos los archivos
- 📋 **Reporte unificado** con estadísticas por archivo fuente
- ✅ **Interfaz amigable** con indicadores de progreso

## Estructura del Archivo Excel Generado

El archivo Excel contiene múltiples hojas organizadas:

### 🎯 **Con Interfaz Gráfica (múltiples archivos):**

#### 1. 📋 Todos_los_Commits
Lista completa de todos los commits encontrados con columnas:
- **repository**: Nombre del repositorio (ej: TALLER-USMP/SGA_BACKEND)
- **author_username**: Username de GitHub del autor
- **author_display**: Nombre de display del autor
- **branch**: Rama donde se hizo el commit
- **commit_hash**: Hash corto del commit
- **commit_message**: Mensaje del commit
- **slack_timestamp**: Fecha y hora de la notificación en Slack
- **commits_count**: Número de commits en el push
- **archivo_origen**: Nombre del archivo JSON fuente

#### 2. 📁 Resumen_por_Archivo
Estadísticas agrupadas por archivo JSON procesado:
- **total_commits**: Total de commits por archivo
- **repository**: Lista de repositorios encontrados en el archivo
- **author_display**: Lista de autores en el archivo

#### 3. 📊 Resumen_por_Repositorio
Estadísticas agrupadas por repositorio:
- **total_commits**: Total de commits por repositorio
- **author_display**: Lista de autores que han contribuido
- **archivo_origen**: Archivos JSON donde aparece el repositorio

#### 4. 👥 Resumen_por_Autor
Estadísticas agrupadas por autor:
- **total_commits**: Total de commits por autor
- **repository**: Lista de repositorios donde ha contribuido
- **archivo_origen**: Archivos JSON donde aparece el autor

### 📄 **Con scripts individuales (un archivo):**

#### 1. 📋 Todos_los_Commits
Lista completa de todos los commits encontrados con columnas:
- **repository**: Nombre del repositorio (ej: TALLER-USMP/SGA_BACKEND)
- **author_username**: Username de GitHub del autor
- **author_display**: Nombre de display del autor
- **branch**: Rama donde se hizo el commit
- **commit_hash**: Hash corto del commit
- **commit_message**: Mensaje del commit
- **slack_timestamp**: Fecha y hora de la notificación en Slack
- **commits_count**: Número de commits en el push

#### 2. 📊 Resumen_por_Repositorio
Estadísticas agrupadas por repositorio:
- **total_commits**: Total de commits por repositorio
- **author_username**: Lista de autores que han contribuido
- **branch**: Lista de ramas utilizadas

#### 3. 👥 Resumen_por_Autor
Estadísticas agrupadas por autor:
- **total_commits**: Total de commits por autor
- **repository**: Lista de repositorios donde ha contribuido
- **branch**: Lista de ramas utilizadas

## Ejemplo de Salida

```
RESUMEN DEL PROCESAMIENTO
============================================================
Total de commits encontrados: 5
Total de repositorios: 2
Total de autores: 2

Repositorios encontrados:
  - TALLER-USMP/wokshop_concept: 4 commits
  - TALLER-USMP/SGA_BACKEND: 1 commits

Autores encontrados:
  - JeanClix: 4 commits
  - Adriancas28: 1 commits

Archivo Excel generado: d:\USMP\taller\Convertir json a exel\reporte_commits_github.xlsx
============================================================
```

## Formato del JSON de Slack

El programa busca mensajes con la siguiente estructura en el JSON:

```json
{
  "attachments": [
    {
      "fallback": "[TALLER-USMP/repo] 1 new commit pushed to _main_ by Author",
      "pretext": "1 new commit pushed to `main` by Author",
      "text": "`hash` - commit message"
    }
  ]
}
```

## Cómo Exportar JSON desde Slack

1. Ve a tu canal de Slack que recibe notificaciones de GitHub
2. Usa la herramienta de exportación de Slack o la API
3. Guarda el archivo como JSON en el directorio del proyecto

## Solución de Problemas

### Error: "No se encontraron commits"
- Verifica que el JSON contenga notificaciones de GitHub
- Asegúrate de que las notificaciones tengan el formato esperado
- Revisa que el canal tenga configurada la integración con GitHub

### Error: "Archivo no encontrado"
- Verifica la ruta del archivo JSON
- Asegúrate de que el archivo tenga extensión `.json`
- Revisa los permisos de lectura del archivo

### Error de dependencias
```bash
pip install --upgrade pandas openpyxl
```

## Personalización

Puedes modificar el código para:
- Cambiar el formato de salida
- Agregar más campos de información
- Filtrar por fechas o repositorios específicos
- Cambiar el formato del reporte Excel

## Archivos del Proyecto

- `extractor_gui.py`: **🎯 Interfaz gráfica principal** (selección múltiple)
- `ejecutar_gui.py`: **🚀 Ejecutor de la interfaz gráfica** (recomendado)
- `slack_github_extractor.py`: Clase principal del extractor
- `ejecutar_extractor.py`: Script simple de ejemplo (un archivo)
- `github_api_enhancer.py`: Enriquecimiento con GitHub API
- `requirements.txt`: Dependencias de Python
- `README.md`: Este archivo de documentación

## Soporte

Si encuentras problemas:
1. Verifica que el archivo JSON tenga el formato correcto
2. Revisa que todas las dependencias estén instaladas
3. Comprueba los logs de error en la consola

---

*Desarrollado para extraer y analizar commits de GitHub desde notificaciones de Slack*

# Actualización del README

- Se ha revisado y actualizado el archivo README.md para reflejar los cambios recientes en el proyecto.
- Se ha asegurado que las instrucciones sean claras y específicas para el uso de la interfaz gráfica (GUI).
- Se han eliminado referencias a scripts o funcionalidades que no están relacionadas con la GUI.
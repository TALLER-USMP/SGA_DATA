#!/usr/bin/env python3
"""
Configurador Automático del Extractor GitHub-Slack
==================================================

Este script configura automáticamente el entorno para usar
el extractor de commits de GitHub desde JSON de Slack.
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_python():
    """Verifica la versión de Python"""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 7:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.7+")
        return False

def instalar_dependencias():
    """Instala las dependencias necesarias"""
    dependencias = ['pandas>=1.5.0', 'openpyxl>=3.0.0', 'requests>=2.25.0']
    
    print("📦 Instalando dependencias...")
    
    try:
        for dep in dependencias:
            print(f"   Instalando {dep}...")
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', dep])
        
        print("✅ Todas las dependencias instaladas correctamente")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias: {e}")
        return False

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén presentes"""
    archivos_requeridos = [
        'slack_github_extractor.py',
        'ejecutar_extractor.py', 
        'github_api_enhancer.py',
        'requirements.txt',
        'README.md'
    ]
    
    print("📁 Verificando archivos del proyecto...")
    
    todos_presentes = True
    for archivo in archivos_requeridos:
        if os.path.exists(archivo):
            print(f"   ✅ {archivo}")
        else:
            print(f"   ❌ {archivo} - FALTANTE")
            todos_presentes = False
    
    return todos_presentes

def verificar_json():
    """Verifica si hay archivos JSON de Slack disponibles"""
    archivos_json = list(Path('.').glob('*.json'))
    
    if archivos_json:
        print(f"📄 Archivos JSON encontrados:")
        for archivo in archivos_json:
            print(f"   ✅ {archivo}")
        return archivos_json
    else:
        print("⚠️  No se encontraron archivos JSON de Slack")
        print("   Asegúrate de colocar tu archivo JSON exportado de Slack en este directorio")
        return []

def ejecutar_test():
    """Ejecuta un test básico del extractor"""
    archivos_json = verificar_json()
    
    if not archivos_json:
        print("⚠️  Sin archivos JSON para probar")
        return False
    
    # Usar el primer archivo JSON encontrado
    archivo_test = archivos_json[0]
    
    print(f"🧪 Ejecutando test con {archivo_test}...")
    
    try:
        # Importar y probar el extractor
        from slack_github_extractor import SlackGitHubExtractor
        
        extractor = SlackGitHubExtractor(archivo_test)
        slack_data = extractor.load_slack_data()
        extractor.extract_github_commits(slack_data)
        
        if extractor.commits_data:
            print(f"✅ Test exitoso - {len(extractor.commits_data)} commits encontrados")
            return True
        else:
            print("⚠️  Test completado pero no se encontraron commits")
            print("   Verifica que el JSON contenga notificaciones de GitHub")
            return True
            
    except Exception as e:
        print(f"❌ Error en el test: {e}")
        return False

def mostrar_resumen():
    """Muestra un resumen de cómo usar el proyecto"""
    print("\n" + "="*60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("="*60)
    
    print("\n📚 CÓMO USAR EL EXTRACTOR:")
    print("\n1. Opción Fácil:")
    print("   python ejecutar_extractor.py")
    
    print("\n2. Opción Personalizada:")
    print("   python slack_github_extractor.py tu_archivo.json -o reporte.xlsx")
    
    print("\n3. Con enriquecimiento de GitHub API:")
    print("   python github_api_enhancer.py tu_archivo.json -t TU_TOKEN")
    
    print("\n4. Demo completo:")
    print("   python demo_completo.py")
    
    print("\n📁 ARCHIVOS QUE SE GENERAN:")
    print("   • reporte_commits_github.xlsx - Reporte principal")
    print("   • Hoja 'Todos_los_Commits' - Lista completa")
    print("   • Hoja 'Resumen_por_Repositorio' - Estadísticas por repo")
    print("   • Hoja 'Resumen_por_Autor' - Estadísticas por autor")
    
    print("\n💡 CONSEJOS:")
    print("   • Coloca tus archivos JSON de Slack en este directorio")
    print("   • Para GitHub API, obtén un token en github.com/settings/tokens")
    print("   • Lee README.md para documentación completa")

def main():
    """Función principal del configurador"""
    print("⚙️  CONFIGURADOR AUTOMÁTICO - EXTRACTOR GITHUB-SLACK")
    print("="*60)
    
    # Verificaciones paso a paso
    pasos = [
        ("🐍 Verificando Python", verificar_python),
        ("📦 Instalando dependencias", instalar_dependencias),
        ("📁 Verificando archivos", verificar_archivos),
        ("🧪 Ejecutando test", ejecutar_test)
    ]
    
    exito_total = True
    
    for nombre, funcion in pasos:
        print(f"\n{nombre}...")
        if not funcion():
            exito_total = False
            break
    
    if exito_total:
        mostrar_resumen()
    else:
        print("\n❌ Configuración incompleta. Revisa los errores anteriores.")
        print("💡 Intenta ejecutar este script nuevamente después de resolver los problemas.")

if __name__ == "__main__":
    main()

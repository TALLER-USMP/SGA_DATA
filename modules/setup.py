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
    if version.major == 3 and version.minor >= 12:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible (3.12+)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Requiere Python 3.12+")
        print("💡 Descarga Python 3.12 desde https://www.python.org/downloads/")
        return False

def instalar_dependencias():
    """Instala las dependencias necesarias"""
    print("📦 Actualizando pip, setuptools y wheel...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '--upgrade', 'pip', 'setuptools', 'wheel'])
        print("✅ pip, setuptools y wheel actualizados")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al actualizar pip/setuptools/wheel: {e}")
        return False

    print("📦 Instalando todas las dependencias desde requirements.txt (raíz)...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'])
        print("✅ Todas las dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error al instalar dependencias desde requirements.txt: {e}")
        print("Pasos recomendados para resolver el problema:\n 1) Usar conda/conda-forge (recomendado):\n    conda create -n sga python=3.12 -y; conda activate sga; conda install -c conda-forge streamlit pyarrow pandas openpyxl requests plotly -y\n 2) O instalar herramientas de compilación en Windows y CMake (requiere reinicio y privilegios de administrador):\n    - Instala 'Visual Studio Build Tools' (C++), y 'CMake' (por ejemplo con winget o desde su web).\n 3) Luego reintenta: pip install -r requirements.txt")
        return False

def verificar_archivos():
    """Verifica que todos los archivos necesarios estén presentes"""
    archivos_requeridos = [
        'README.md',
        'requirements.txt',
        'modules/setup.py'
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

def mostrar_resumen():
    """Muestra un resumen de cómo usar el proyecto"""
    print("\n" + "="*60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("="*60)
    
    print("\n📚 CÓMO USAR EL PROYECTO:")
    print("\n1. Instala las dependencias:")
    print("   pip install -r requirements.txt")
    print("\n2. Lee README.md para la documentación y ejemplos de uso.")

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

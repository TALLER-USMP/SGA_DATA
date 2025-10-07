#!/usr/bin/env python3
"""
Ejecutor simple para la interfaz gráfica del extractor
=====================================================

Script simple que ejecuta la interfaz gráfica del extractor de commits.
Solo haz doble clic en este archivo o ejecútalo desde la terminal.
"""

try:
    from extractor_gui import GitHubExtractorGUI
    import logging
    
    # Configurar logging básico
    logging.basicConfig(level=logging.INFO)
    
    print("🚀 Iniciando interfaz gráfica del extractor...")
    print("📋 Instrucciones:")
    print("   1. Selecciona uno o más archivos JSON")
    print("   2. Configura el nombre del archivo de salida") 
    print("   3. Haz clic en 'Procesar Archivos'")
    print("   4. ¡Espera el resultado!")
    print()
    
    # Crear y ejecutar la interfaz
    app = GitHubExtractorGUI()
    app.ejecutar()
    
    print("👋 Interfaz cerrada. ¡Gracias por usar el extractor!")
    
except ImportError as e:
    print("❌ Error: No se pudo importar la interfaz gráfica")
    print(f"   Detalles: {e}")
    print()
    print("🔧 Solución:")
    print("   1. Asegúrate de que extractor_gui.py esté en la misma carpeta")
    print("   2. Verifica que todas las dependencias estén instaladas:")
    print("      pip install -r requirements.txt")
    input("\nPresiona Enter para salir...")

except Exception as e:
    print(f"❌ Error inesperado: {e}")
    print()
    print("🔧 Si el problema persiste:")
    print("   1. Verifica que Python esté instalado correctamente")
    print("   2. Ejecuta: pip install -r requirements.txt")
    print("   3. Intenta ejecutar: python extractor_gui.py")
    input("\nPresiona Enter para salir...")
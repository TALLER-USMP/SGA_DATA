#!/usr/bin/env python3
"""
Ejecutor del Dashboard de Commits
================================

Script simple para ejecutar el dashboard de Streamlit.
Abre automáticamente el navegador con el dashboard interactivo.
"""

import subprocess
import sys
import os

def ejecutar_dashboard():
    """
    Ejecuta el dashboard de Streamlit
    """
    print("🚀 Iniciando Dashboard de Commits GitHub...")
    print("📊 Streamlit se abrirá en tu navegador automáticamente")
    print("🔗 URL típica: http://localhost:8501")
    print()
    print("💡 Para detener el dashboard: Ctrl+C en esta ventana")
    print("="*50)
    
    try:
        # Ejecutar streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "scripts\dashboard_commits.py",
            "--server.headless", "false",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n👋 Dashboard cerrado por el usuario")
    except Exception as e:
        print(f"❌ Error al ejecutar el dashboard: {e}")
        print("\n🔧 Soluciones:")
        print("1. Verifica que streamlit esté instalado: pip install streamlit")
        print("2. Ejecuta manualmente: streamlit run dashboard_commits.py")

if __name__ == "__main__":
    ejecutar_dashboard()
#!/usr/bin/env python3
"""
Script de ejemplo para usar el extractor de commits de GitHub
============================================================

Este script demuestra cómo usar la clase SlackGitHubExtractor
para procesar un archivo JSON de Slack específico.
"""

from slack_github_extractor import SlackGitHubExtractor
import os

def main():
    """
    Función principal del script de ejemplo
    """
    # Ruta al archivo JSON (ajusta esta ruta según tu archivo)
    json_file = "2025-09-30.json"
    
    # Verificar que el archivo existe
    if not os.path.exists(json_file):
        print(f"Error: El archivo {json_file} no existe en el directorio actual.")
        print("Asegúrate de que el archivo JSON esté en el mismo directorio que este script.")
        return
    
    try:
        print("Iniciando extracción de commits de GitHub desde Slack...")
        print(f"Procesando archivo: {json_file}")
        
        # Crear instancia del extractor
        extractor = SlackGitHubExtractor(json_file)
        
        # Procesar el archivo y generar reporte
        excel_path, summary = extractor.process("reporte_commits_github.xlsx")
        
        # Mostrar resultados
        print("\n" + "="*50)
        print("RESULTADOS DEL PROCESAMIENTO")
        print("="*50)
        
        if summary.get('total_commits', 0) > 0:
            print(f"✅ Commits extraídos exitosamente: {summary['total_commits']}")
            print(f"📁 Repositorios encontrados: {summary['total_repositories']}")
            print(f"👤 Autores únicos: {summary['total_authors']}")
            
            print(f"\n📊 Distribución por repositorio:")
            for repo, count in summary.get('commits_by_repo', {}).items():
                print(f"   • {repo}: {count} commits")
            
            print(f"\n👥 Distribución por autor:")
            for author, count in summary.get('commits_by_author', {}).items():
                print(f"   • {author}: {count} commits")
            
            print(f"\n📄 Archivo Excel generado: {excel_path}")
            print("\nEl archivo Excel contiene 3 hojas:")
            print("   1. Todos_los_Commits - Lista completa de commits")
            print("   2. Resumen_por_Repositorio - Estadísticas por repo")
            print("   3. Resumen_por_Autor - Estadísticas por autor")
        else:
            print("⚠️  No se encontraron commits de GitHub en el archivo JSON")
            print("   Verifica que el archivo contenga notificaciones de GitHub")
        
        print("="*50)
        
    except FileNotFoundError:
        print(f"❌ Error: No se pudo encontrar el archivo {json_file}")
    except Exception as e:
        print(f"❌ Error durante el procesamiento: {e}")

if __name__ == "__main__":
    main()
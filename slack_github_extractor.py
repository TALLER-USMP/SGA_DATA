#!/usr/bin/env python3
"""
Extractor de Commits de GitHub desde JSON de Slack
==================================================

Este programa procesa un archivo JSON exportado de Slack que contiene
notificaciones de commits de GitHub y genera un archivo Excel con la información
de los commits organizados por repositorio, autor y mensaje.

Autor: GitHub Copilot
Fecha: Octubre 2025
"""

import json
import re
import pandas as pd
from datetime import datetime
from pathlib import Path
import argparse
import logging

# Configuración de logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class SlackGitHubExtractor:
    """
    Clase para extraer información de commits de GitHub desde archivos JSON de Slack
    """
    
    def __init__(self, json_file_path):
        """
        Inicializa el extractor con la ruta del archivo JSON
        
        Args:
            json_file_path (str): Ruta al archivo JSON de Slack
        """
        self.json_file_path = Path(json_file_path)
        self.commits_data = []
        
    def load_slack_data(self):
        """
        Carga el archivo JSON de Slack
        
        Returns:
            list: Lista de mensajes de Slack
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"Archivo JSON cargado exitosamente: {len(data)} mensajes encontrados")
                return data
        except FileNotFoundError:
            logger.error(f"Archivo no encontrado: {self.json_file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Error al decodificar JSON: {e}")
            raise
    
    def extract_commit_info_from_attachment(self, attachment):
        """
        Extrae información de commits desde un attachment de GitHub
        
        Args:
            attachment (dict): Attachment del mensaje de Slack
            
        Returns:
            dict: Información del commit extraída
        """
        commit_info = {}
        
        # Extraer información del pretext (repositorio, autor, branch)
        if 'pretext' in attachment:
            pretext = attachment['pretext']
            
            # Patrón para extraer repositorio, commits count, branch y autor
            # Ajustado para manejar URLs con escapes
            repo_pattern = r'github\.com[\/\\]+([^\/\\]+[\/\\][^\/\\]+)[\/\\]'
            author_pattern = r'by <https:[\/\\]+github\.com[\/\\]+([^|]+)\|([^>]+)>'
            branch_pattern = r'pushed to `<[^|]+\|([^>]+)>`'
            commits_count_pattern = r'(\d+) new commits?'
            
            repo_match = re.search(repo_pattern, pretext)
            author_match = re.search(author_pattern, pretext)
            branch_match = re.search(branch_pattern, pretext)
            commits_count_match = re.search(commits_count_pattern, pretext)
            
            if repo_match:
                # Limpiar escapes de la barra diagonal
                repo_name = repo_match.group(1).replace('\\/', '/')
                commit_info['repository'] = repo_name
            
            if author_match:
                commit_info['author_username'] = author_match.group(1)
                commit_info['author_display'] = author_match.group(2)
            
            if branch_match:
                commit_info['branch'] = branch_match.group(1)
                
            if commits_count_match:
                commit_info['commits_count'] = int(commits_count_match.group(1))
        
        # Extraer hash y mensaje del commit desde el text
        if 'text' in attachment:
            text = attachment['text']
            
            # Patrón para extraer hash y mensaje del commit
            # Ajustado para manejar URLs con escapes
            commit_pattern = r'`<[^|]+\|([^>]+)>` - (.+?)(?:\n|$)'
            commit_matches = re.findall(commit_pattern, text, re.MULTILINE)
            
            if commit_matches:
                commit_info['commits'] = []
                for hash_commit, message in commit_matches:
                    commit_info['commits'].append({
                        'hash': hash_commit,
                        'message': message
                    })
        
        return commit_info
    
    def extract_github_commits(self, slack_data):
        """
        Extrae información de commits de GitHub desde los datos de Slack
        
        Args:
            slack_data (list): Lista de mensajes de Slack
        """
        github_commits = []
        
        for message in slack_data:
            # Verificar si el mensaje tiene attachments de GitHub
            if 'attachments' in message:
                for attachment in message['attachments']:
                    # Verificar si es una notificación de GitHub commit
                    fallback_text = attachment.get('fallback', '')
                    if ('new commit' in fallback_text and 
                        ('github.com' in fallback_text or 'TALLER-USMP' in fallback_text)):
                        
                        commit_info = self.extract_commit_info_from_attachment(attachment)
                        
                        if commit_info:
                            # Agregar timestamp del mensaje
                            if 'ts' in message:
                                timestamp = float(message['ts'])
                                commit_info['slack_timestamp'] = datetime.fromtimestamp(timestamp)
                            
                            # Si hay múltiples commits, crear una entrada por cada uno
                            if 'commits' in commit_info and commit_info['commits']:
                                for commit in commit_info['commits']:
                                    commit_entry = {
                                        'repository': commit_info.get('repository', 'N/A'),
                                        'author_username': commit_info.get('author_username', 'N/A'),
                                        'author_display': commit_info.get('author_display', 'N/A'),
                                        'branch': commit_info.get('branch', 'N/A'),
                                        'commit_hash': commit['hash'],
                                        'commit_message': commit['message'],
                                        'slack_timestamp': commit_info.get('slack_timestamp', 'N/A'),
                                        'commits_count': commit_info.get('commits_count', 1)
                                    }
                                    github_commits.append(commit_entry)
                            else:
                                # Si no hay commits específicos, agregar la información general
                                commit_entry = {
                                    'repository': commit_info.get('repository', 'N/A'),
                                    'author_username': commit_info.get('author_username', 'N/A'),
                                    'author_display': commit_info.get('author_display', 'N/A'),
                                    'branch': commit_info.get('branch', 'N/A'),
                                    'commit_hash': 'N/A',
                                    'commit_message': 'N/A',
                                    'slack_timestamp': commit_info.get('slack_timestamp', 'N/A'),
                                    'commits_count': commit_info.get('commits_count', 1)
                                }
                                github_commits.append(commit_entry)
        
        self.commits_data = github_commits
        logger.info(f"Extraídos {len(github_commits)} commits de GitHub")
    
    def generate_excel_report(self, output_file='github_commits_report.xlsx'):
        """
        Genera un reporte en Excel con los commits extraídos
        
        Args:
            output_file (str): Nombre del archivo Excel de salida
        """
        if not self.commits_data:
            logger.warning("No hay datos de commits para generar el reporte")
            return
        
        # Crear DataFrame
        df = pd.DataFrame(self.commits_data)
        
        # Ordenar por timestamp
        if 'slack_timestamp' in df.columns:
            df = df.sort_values('slack_timestamp', ascending=False)
        
        # Crear archivo Excel con múltiples hojas
        output_path = self.json_file_path.parent / output_file
        
        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Hoja principal con todos los commits
            df.to_excel(writer, sheet_name='Todos_los_Commits', index=False)
            
            # Hoja agrupada por repositorio
            if not df.empty:
                repo_summary = df.groupby('repository').agg({
                    'commit_hash': 'count',
                    'author_username': lambda x: ', '.join(x.unique()),
                    'branch': lambda x: ', '.join(x.unique())
                }).rename(columns={'commit_hash': 'total_commits'})
                repo_summary.to_excel(writer, sheet_name='Resumen_por_Repositorio')
                
                # Hoja agrupada por autor
                author_summary = df.groupby('author_display').agg({
                    'commit_hash': 'count',
                    'repository': lambda x: ', '.join(x.unique()),
                    'branch': lambda x: ', '.join(x.unique())
                }).rename(columns={'commit_hash': 'total_commits'})
                author_summary.to_excel(writer, sheet_name='Resumen_por_Autor')
        
        logger.info(f"Reporte Excel generado: {output_path}")
        return output_path
    
    def generate_summary_report(self):
        """
        Genera un resumen estadístico de los commits
        
        Returns:
            dict: Diccionario con estadísticas
        """
        if not self.commits_data:
            return {}
        
        df = pd.DataFrame(self.commits_data)
        
        summary = {
            'total_commits': len(df),
            'total_repositories': df['repository'].nunique(),
            'total_authors': df['author_display'].nunique(),
            'repositories': df['repository'].unique().tolist(),
            'authors': df['author_display'].unique().tolist(),
            'commits_by_repo': df['repository'].value_counts().to_dict(),
            'commits_by_author': df['author_display'].value_counts().to_dict()
        }
        
        return summary
    
    def process(self, output_file='github_commits_report.xlsx'):
        """
        Procesa el archivo JSON completo y genera el reporte
        
        Args:
            output_file (str): Nombre del archivo Excel de salida
            
        Returns:
            tuple: (ruta del archivo Excel, resumen estadístico)
        """
        logger.info("Iniciando procesamiento del archivo JSON de Slack")
        
        # Cargar datos de Slack
        slack_data = self.load_slack_data()
        
        # Extraer commits de GitHub
        self.extract_github_commits(slack_data)
        
        # Generar reporte Excel
        excel_path = self.generate_excel_report(output_file)
        
        # Generar resumen
        summary = self.generate_summary_report()
        
        logger.info("Procesamiento completado")
        
        return excel_path, summary

def main():
    """
    Función principal del programa
    """
    parser = argparse.ArgumentParser(description='Extrae commits de GitHub desde JSON de Slack')
    parser.add_argument('json_file', help='Ruta al archivo JSON de Slack')
    parser.add_argument('-o', '--output', default='github_commits_report.xlsx', 
                       help='Nombre del archivo Excel de salida')
    
    args = parser.parse_args()
    
    try:
        # Crear extractor
        extractor = SlackGitHubExtractor(args.json_file)
        
        # Procesar archivo
        excel_path, summary = extractor.process(args.output)
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("RESUMEN DEL PROCESAMIENTO")
        print("="*60)
        print(f"Total de commits encontrados: {summary.get('total_commits', 0)}")
        print(f"Total de repositorios: {summary.get('total_repositories', 0)}")
        print(f"Total de autores: {summary.get('total_authors', 0)}")
        
        print(f"\nRepositorios encontrados:")
        for repo in summary.get('repositories', []):
            count = summary.get('commits_by_repo', {}).get(repo, 0)
            print(f"  - {repo}: {count} commits")
        
        print(f"\nAutores encontrados:")
        for author in summary.get('authors', []):
            count = summary.get('commits_by_author', {}).get(author, 0)
            print(f"  - {author}: {count} commits")
        
        print(f"\nArchivo Excel generado: {excel_path}")
        print("="*60)
        
    except Exception as e:
        logger.error(f"Error durante el procesamiento: {e}")
        raise

if __name__ == "__main__":
    main()
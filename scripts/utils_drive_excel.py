"""
Utilidad para listar y descargar archivos Excel de una carpeta de Google Drive usando la API y una cuenta de servicio.
"""

from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import io
from googleapiclient.http import MediaIoBaseDownload

FOLDER_ID = "1cCRPbJNMDU1zYXKnwj0Ysro8eUy75VIp" 
SERVICE_ACCOUNT_FILE = "credentials.json" 
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def listar_excels_drive():
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'",
        fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def descargar_excel_drive(file_id):
    creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    service = build('drive', 'v3', credentials=creds)
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        status, done = downloader.next_chunk()
    fh.seek(0)
    df = pd.read_excel(fh)
    return df

if __name__ == "__main__":
    archivos = listar_excels_drive()
    print("Archivos Excel en la carpeta:")
    for i, f in enumerate(archivos):
        print(f"{i+1}. {f['name']} (ID: {f['id']})")
    if archivos:
        print("\nDescargando el primero como ejemplo...")
        df = descargar_excel_drive(archivos[0]['id'])
        print(df.head())

"""
Utilidad para listar y descargar archivos Excel de una carpeta de Google Drive usando la API y una cuenta de servicio.
"""


import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build
import pandas as pd
import io
from googleapiclient.http import MediaIoBaseDownload

FOLDER_ID = "1cCRPbJNMDU1zYXKnwj0Ysro8eUy75VIp" 
SERVICE_ACCOUNT_FILE = "credentials.json" 
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]

def get_drive_creds():
    """
    Obtiene las credenciales de Google Drive desde variable de entorno o archivo.
    """
    creds = None
    if "GOOGLE_APPLICATION_CREDENTIALS_JSON" in os.environ:
        creds_dict = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])
        creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
    else:
        creds = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    return creds

def listar_excels_drive():
    creds = get_drive_creds()
    service = build('drive', 'v3', credentials=creds)
    results = service.files().list(
        q=f"'{FOLDER_ID}' in parents and mimeType='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'",
        fields="files(id, name)").execute()
    files = results.get('files', [])
    return files

def descargar_excel_drive(file_id):
    creds = get_drive_creds()
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

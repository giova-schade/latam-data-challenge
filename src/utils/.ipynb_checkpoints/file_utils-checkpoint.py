import io
import os
import zipfile

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

# Cargar variables de entorno desde .env
load_dotenv()

# Obtener variables de entorno
SCOPES = ["https://www.googleapis.com/auth/drive.readonly"]
CREDENTIALS_PATH = os.getenv("CREDENTIALS_PATH", "credentials.json")
FILE_ID = os.getenv("FILE_ID")
FILE_NAME = os.getenv("FILE_NAME", "downloaded_file.zip")


def download_file_from_google_drive():
    """Descarga un archivo de Google Drive utilizando las credenciales de autenticación y las variables de entorno."""
    if not FILE_ID:
        raise ValueError(
            "El ID del archivo (FILE_ID) no está definido en el archivo .env."
        )

    # Autenticación y autorización con OAuth 2.0
    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    # Conectar a la API de Google Drive
    service = build("drive", "v3", credentials=creds)

    # Descargar el archivo
    request = service.files().get_media(fileId=FILE_ID)
    fh = io.FileIO(FILE_NAME, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Descargando {int(status.progress() * 100)}%.")

    fh.close()
    print("Descarga completada.")


def download_and_extract_file():
    """Descarga un archivo de Google Drive y lo descomprime en la carpeta data/raw."""
    download_file_from_google_drive()  # Llama a la función existente para descargar

    # Descomprimir el archivo
    raw_data_folder = "data/raw"
    if not os.path.exists(raw_data_folder):
        os.makedirs(raw_data_folder)

    # Descomprimir el archivo zip
    with zipfile.ZipFile(FILE_NAME, "r") as zip_ref:
        zip_ref.extractall(raw_data_folder)
        print(f"Archivos extraídos en: {raw_data_folder}")

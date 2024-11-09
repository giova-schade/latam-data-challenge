import io
import os
import zipfile

from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaIoBaseDownload

load_dotenv()

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

    flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
    creds = flow.run_local_server(port=0)

    service = build("drive", "v3", credentials=creds)

    request = service.files().get_media(fileId=FILE_ID)

    raw_data_folder = os.path.join(os.path.dirname(__file__), "../../data/raw")
    if not os.path.exists(raw_data_folder):
        os.makedirs(raw_data_folder)

    file_path = os.path.join(raw_data_folder, FILE_NAME)
    fh = io.FileIO(file_path, "wb")
    downloader = MediaIoBaseDownload(fh, request)
    done = False

    while not done:
        status, done = downloader.next_chunk()
        print(f"Descargando {int(status.progress() * 100)}%.")

    fh.close()
    return file_path


def download_and_extract_file():
    """Descarga un archivo de Google Drive y lo descomprime en la carpeta data/raw, luego elimina el archivo ZIP."""
    raw_data_folder = os.path.join(os.path.dirname(__file__), "../../data/raw")
    if not os.path.exists(raw_data_folder):
        os.makedirs(raw_data_folder)

    file_path = download_file_from_google_drive()

    with zipfile.ZipFile(file_path, "r") as zip_ref:
        zip_ref.extractall(raw_data_folder)
        print(f"Archivos extraídos en: {raw_data_folder}")

    os.remove(file_path)
    print(f"Archivo ZIP eliminado: {file_path}")

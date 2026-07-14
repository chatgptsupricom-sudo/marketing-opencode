import os, json, sys
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/drive.readonly']
TOKEN_FILE = os.path.join(os.path.dirname(__file__), '..', '.drive_token.json')
CREDS_FILE = os.path.join(os.path.dirname(__file__), '..', '.drive_creds.json')

def get_authenticated_service():
    creds = None
    if os.path.exists(TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(TOKEN_FILE, SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(CREDS_FILE):
                print("ERROR: Necesitas crear .drive_creds.json con credenciales de Google OAuth.")
                print("Ve a https://console.cloud.google.com/ > APIs > Credentials > Crear ID de cliente OAuth")
                print("Tipo: Aplicación de escritorio. Descarga el JSON y guárdalo como .drive_creds.json")
                sys.exit(1)
            flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())
    return build('drive', 'v3', credentials=creds)

def find_folder_id(service, name, parent_id=None):
    query = f"name = '{name}' and mimeType = 'application/vnd.google-apps.folder' and trashed = false"
    if parent_id:
        query += f" and '{parent_id}' in parents"
    results = service.files().list(q=query, fields='files(id, name)').execute()
    files = results.get('files', [])
    if not files:
        return None
    return files[0]['id']

def list_subfolders(service, parent_id):
    results = service.files().list(
        q=f"'{parent_id}' in parents and mimeType = 'application/vnd.google-apps.folder' and trashed = false",
        fields='files(id, name)'
    ).execute()
    return results.get('files', [])

def main():
    service = get_authenticated_service()
    
    # Navigate: CONTENIDO MARKETNG > MES JULIO
    root_id = find_folder_id(service, 'CONTENIDO MARKETNG')
    if not root_id:
        print("ERROR: No se encontró la carpeta 'CONTENIDO MARKETNG'")
        sys.exit(1)
    
    mes_julio_id = find_folder_id(service, 'MES JULIO', root_id)
    if not mes_julio_id:
        print("ERROR: No se encontró la carpeta 'MES JULIO' dentro de CONTENIDO MARKETNG")
        sys.exit(1)
    
    print(f"CONTENIDO MARKETNG: {root_id}")
    print(f"MES JULIO: {mes_julio_id}")
    print(f"URL: https://drive.google.com/drive/folders/{mes_julio_id}")
    print()
    
    # List format folders (CARRUSELES, POST, VIDEOS)
    format_folders = list_subfolders(service, mes_julio_id)
    output = {}
    
    for ff in format_folders:
        print(f"\n=== {ff['name']} ({ff['id']}) ===")
        output[ff['name']] = {}
        subfolders = list_subfolders(service, ff['id'])
        for sf in sorted(subfolders, key=lambda x: x['name']):
            print(f"  {sf['name']}: {sf['id']}")
            output[ff['name']][sf['name']] = sf['id']
    
    # Save mapping file
    mapping_path = os.path.join(os.path.dirname(__file__), '..', 'ESTRATEGA', 'drive_mapping.json')
    with open(mapping_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"\n✅ Mapeo guardado en: {mapping_path}")

if __name__ == '__main__':
    main()

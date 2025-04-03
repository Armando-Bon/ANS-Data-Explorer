import zipfile
import os

def compactar_arquivo(csv_path):
    if not csv_path:
        print("Nenhum CSV para compactar.")
        return

    zip_path = "Teste_anexoI.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write(csv_path, os.path.basename(csv_path))

    print(f"Arquivo compactado: {zip_path}")

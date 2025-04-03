import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

URL_BASE = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

def encontrar_links_pdfs():
    #Varre a página e encontra os links dos PDFs Anexo I e Anexo II.
    response = requests.get(URL_BASE)
    response.raise_for_status()
    
    soup = BeautifulSoup(response.text, "html.parser")
    pdf_links = {}

    # buscar por "Anexo I" e "Anexo II" 
    for link in soup.find_all("a", href=True):
        texto_link = link.text.strip().lower()
        href = link["href"]

        # Busca flexível por "anexo i" ou "anexo ii"
        if "anexo i" in texto_link:
            pdf_links["Anexo I"] = href
        if "anexo ii" in texto_link:
            pdf_links["Anexo II"] = href

    return pdf_links

def baixar_pdfs(save_dir):
    """Baixa os PDFs encontrados na página."""
    os.makedirs(save_dir, exist_ok=True)
    
    pdf_links = encontrar_links_pdfs()
    pdfs_baixados = []

    if not pdf_links:
        print("Nenhum link de PDF encontrado.")
        return []

    for nome, url in pdf_links.items():
        pdf_url = url if url.startswith("http") else urljoin(URL_BASE, url)
        pdf_path = os.path.join(save_dir, f"{nome}.pdf")
        
        if os.path.exists(pdf_path):
            print(f"{nome} já foi baixado.")
            pdfs_baixados.append(pdf_path)
            continue

        print(f"Baixando {nome} de {pdf_url} ...")
        response = requests.get(pdf_url)
        with open(pdf_path, "wb") as f:
            f.write(response.content)

        pdfs_baixados.append(pdf_path)

    return pdfs_baixados

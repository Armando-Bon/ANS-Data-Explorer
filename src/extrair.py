import pdfplumber
import pandas as pd
import os

def extrair_tabela_do_pdf(pasta_pdfs):
    """Extrai a tabela apenas do 'Anexo I', substitui abreviações e salva como CSV."""
    
    pdf_anexo_i = os.path.join(pasta_pdfs, "Anexo I.pdf")
    
    # Verifica se o Anexo I existe antes de continuar
    if not os.path.exists(pdf_anexo_i):
        print(f"Erro: '{pdf_anexo_i}' não encontrado. Baixe o arquivo antes de processá-lo.")
        return None

    csv_file = os.path.splitext(pdf_anexo_i)[0] + ".csv"

    with pdfplumber.open(pdf_anexo_i) as pdf:
        tabelas = []
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                tabelas.extend(table)

    if not tabelas:
        print("Nenhuma tabela encontrada no PDF.")
        return None

    df = pd.DataFrame(tabelas[1:], columns=tabelas[0])

    # Substituir abreviações
    substituicoes = {"OD": "Odontologia", "AMB": "Ambulatorial"}
    df.replace(substituicoes, inplace=True)

    df.to_csv(csv_file, index=False)
    print(f"CSV salvo em {csv_file}")

    return csv_file

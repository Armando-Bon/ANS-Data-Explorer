import os
import pandas as pd
from src.database_config import conectar_banco

DADOS_DIR = "dados_ans"

CREATE_TABLES = {
    "demonstrativos": """
        CREATE TABLE IF NOT EXISTS demonstrativos (
            DATA DATE NULL,
            REG_ANS INT NULL,
            CD_CONTA_CONTABIL BIGINT NULL,
            DESCRICAO TEXT NULL,
            VL_SALDO_INICIAL DECIMAL(20,4) NULL,
            VL_SALDO_FINAL DECIMAL(20,4) NULL
        );
    """,
    "operadoras": """
        CREATE TABLE IF NOT EXISTS operadoras (
            Registro_ANS INT PRIMARY KEY,
            CNPJ BIGINT NULL,
            Razao_Social TEXT NULL,
            Nome_Fantasia TEXT NULL,
            Modalidade TEXT NULL,
            Logradouro TEXT NULL,
            Numero VARCHAR(255) NULL,
            Complemento TEXT NULL,
            Bairro TEXT NULL,
            Cidade TEXT NULL,
            UF CHAR(2) NULL,
            CEP BIGINT NULL,
            DDD INT NULL,
            Telefone BIGINT NULL,
            Fax BIGINT NULL,
            Endereco_eletronico TEXT NULL,
            Representante TEXT NULL,
            Cargo_Representante TEXT NULL,
            Regiao_de_Comercializacao INT NULL,
            Data_Registro_ANS DATE NULL
        );
    """
}

def criar_tabelas():
    conn = conectar_banco()
    cursor = conn.cursor()
    for query in CREATE_TABLES.values():
        cursor.execute(query)
    conn.commit()
    conn.close()
    print("Tabelas criadas/verificadas com sucesso.")

# Função para tratar valores numéricos corretamente
def tratar_valor(valor, coluna=None):
    if pd.isna(valor) or valor in ["", "NULL", "nan", "NaN"]:
        return None  # Converte valores inválidos em NULL
    
    if isinstance(valor, str):
        valor = valor.strip()

        # Se a coluna for "Numero", sempre retornar string sem conversão
        if coluna == "Numero":
            return valor

        # Se for um número formatado, remover separadores
        valor = valor.replace(".", "").replace(",", ".")

        try:
            return float(valor)  # Converte para float 
        except ValueError:
            return valor  # Mantém strings que não forem números
    
    return valor


# Função para importar arquivos CSV
def importar_arquivos():
    conn = conectar_banco()
    cursor = conn.cursor()

    for arquivo in os.listdir(DADOS_DIR):
        caminho_arquivo = os.path.join(DADOS_DIR, arquivo)

        if not arquivo.endswith(".csv"):
            print(f"Arquivo {arquivo} ignorado por não ser CSV.")
            continue

        if "Relatorio_cadop" in arquivo:
            tabela = "operadoras"
            colunas = "Registro_ANS, CNPJ, Razao_Social, Nome_Fantasia, Modalidade, Logradouro, Numero, Complemento, Bairro, Cidade, UF, CEP, DDD, Telefone, Fax, Endereco_eletronico, Representante, Cargo_Representante, Regiao_de_Comercializacao, Data_Registro_ANS"
            query = f"INSERT IGNORE INTO {tabela} ({colunas}) VALUES ({', '.join(['%s'] * 20)})"

            colunas_esperadas = [
                "Registro_ANS", "CNPJ", "Razao_Social", "Nome_Fantasia", "Modalidade",
                "Logradouro", "Numero", "Complemento", "Bairro", "Cidade", "UF", "CEP",
                "DDD", "Telefone", "Fax", "Endereco_eletronico", "Representante",
                "Cargo_Representante", "Regiao_de_Comercializacao", "Data_Registro_ANS"
            ]
        else:
            tabela = "demonstrativos"
            colunas = "DATA, REG_ANS, CD_CONTA_CONTABIL, DESCRICAO, VL_SALDO_INICIAL, VL_SALDO_FINAL"
            query = f"INSERT INTO {tabela} ({colunas}) VALUES ({', '.join(['%s'] * 6)})"

            colunas_esperadas = ["DATA", "REG_ANS", "CD_CONTA_CONTABIL", "DESCRICAO", "VL_SALDO_INICIAL", "VL_SALDO_FINAL"]

        print(f"Importando {arquivo}...")

        try:
            df = pd.read_csv(caminho_arquivo, encoding="latin1", sep=";", dtype=str)
            
            if "Numero" in df.columns:
                df["Numero"] = df["Numero"].astype(str)


            # Remover espaços dos nomes das colunas
            df.columns = df.columns.str.strip()

            # Manter apenas as colunas esperadas
            df = df[[col for col in colunas_esperadas if col in df.columns]]


            # Aplicar tratamento a todas as colunas
            for coluna in df.columns:
                if coluna == "Numero":
                    df[coluna] = df[coluna].astype(str).replace({"nan": None, "NaN": None, "S/N": "S/N", "LOTE": "LOTE"})  # Garante que a coluna "Numero" sempre seja string e trata nulos corretamente
                else:
                    df[coluna] = df[coluna].map(tratar_valor)



            if "Data_Registro_ANS" in df.columns:
                df["Data_Registro_ANS"] = pd.to_datetime(
                    df["Data_Registro_ANS"], format="%Y-%m-%d", errors="coerce"
                    )
                if df["Data_Registro_ANS"].isna().any():
                    df["Data_Registro_ANS"] = pd.to_datetime(
                        df["Data_Registro_ANS"], format="%d/%m/%Y", errors="coerce"
                    )
                df["Data_Registro_ANS"] = df["Data_Registro_ANS"].dt.date

            if "DATA" in df.columns:
            # Para o arquivo 4T2023.csv
                if arquivo == "4T2023.csv":
                    df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")
                else:
                    # Tenta primeiro o formato ISO (AAAA-MM-DD)
                    df["DATA"] = pd.to_datetime(df["DATA"], format="%Y-%m-%d", errors="coerce")

                    # Se houver datas inválidas (NaT), tenta novamente no formato "DD/MM/AAAA"
                    if df["DATA"].isna().any():
                        df["DATA"] = pd.to_datetime(df["DATA"], format="%d/%m/%Y", errors="coerce")

                df["DATA"] = df["DATA"].dt.date  # Converter para apenas data (sem horário)


            # Substituir NaN por None antes da inserção
            df = df.astype(object).where(pd.notna(df), None)  # Converter NaN para None
            df.replace([float('inf'), float('-inf')], None, inplace=True)  # Tratar valores infinitos


            registros = [tuple(x) for x in df.to_numpy()]
            cursor.executemany(query, registros)
            conn.commit()
            print(f"{arquivo} importado com sucesso.")

        except Exception as e:
            print(f"Erro ao importar {arquivo}: {e}")

    cursor.close()
    conn.close()

def estruturar_e_importar():
    criar_tabelas()
    importar_arquivos()

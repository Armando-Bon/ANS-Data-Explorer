from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import os
import logging
import traceback
import json

# Configuração de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
# Configuração mais permissiva de CORS
CORS(app, resources={r"/api/*": {"origins": "*"}})

# Caminho para o arquivo CSV
CSV_PATH = os.path.join("dados_ans", "Relatorio_cadop.csv")

# Cache do DataFrame para evitar leitura repetida do arquivo
df_cache = None

def load_dataframe():
    global df_cache
    if df_cache is None:
        logger.info(f"Carregando arquivo CSV: {CSV_PATH}")
        try:
            # Especificando encoding='utf-8' e tratamento de erros
            df_cache = pd.read_csv(CSV_PATH, encoding='utf-8', sep=';', dtype=str, on_bad_lines='skip')
            logger.info(f"Arquivo CSV carregado com sucesso. Shape: {df_cache.shape}")
            logger.info(f"Colunas encontradas: {df_cache.columns.tolist()}")
        except UnicodeDecodeError:
            # Se falhar com UTF-8, tenta com latin1
            logger.info("Tentando carregar com encoding latin1...")
            df_cache = pd.read_csv(CSV_PATH, encoding='latin1', sep=';', dtype=str, on_bad_lines='skip')
            logger.info(f"Arquivo CSV carregado com sucesso usando. Shape: {df_cache.shape}")
        except Exception as e:
            logger.error(f"Erro ao carregar arquivo CSV: {str(e)}")
            logger.error(traceback.format_exc())
            raise
    return df_cache

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '').lower()
    logger.info(f"Recebida busca com query: {query}")
    
    if not query:
        logger.info("Query vazia, retornando lista vazia")
        return jsonify({'results': []})
    
    try:
        # Carrega o DataFrame 
        df = load_dataframe()
        logger.info("DataFrame carregado do cache")
        
        # Converte todas as colunas para minúsculas para busca
        logger.info("Convertendo colunas para minúsculas")
        df_str = df.copy()
        for col in df_str.columns:
            df_str[col] = df_str[col].fillna('').astype(str).str.lower()
        
        # Realiza a busca em todas as colunas
        logger.info("Realizando busca nas colunas")
        mask = pd.Series(False, index=df.index)
        for col in df_str.columns:
            col_mask = df_str[col].str.contains(query, na=False, regex=False, case=False)
            mask = mask | col_mask
        
        results = df[mask].head(10)
        logger.info(f"Busca concluída. Encontrados {len(results)} resultados")
        
        # Converte os resultados para dicionário
        results_dict = results.to_dict('records')
        
        # Garante que todos os valores são strings
        for result in results_dict:
            for key, value in result.items():
                if pd.isna(value):
                    result[key] = ''
                else:
                    result[key] = str(value)
        
        if len(results_dict) > 0:
            logger.info(f"Primeiro resultado: {results_dict[0]}")
        
        return jsonify({'results': results_dict})
    
    except Exception as e:
        error_msg = f"Erro durante a busca: {str(e)}"
        logger.error(error_msg)
        logger.error(traceback.format_exc())
        return jsonify({'error': error_msg}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    try:
        df = load_dataframe()
        return jsonify({'status': 'ok', 'rows': len(df)})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    logger.info("Iniciando servidor de busca...")
    # Pré-carrega o DataFrame
    try:
        load_dataframe()
        logger.info("DataFrame pré-carregado com sucesso")
    except Exception as e:
        logger.error(f"Erro ao pré-carregar DataFrame: {str(e)}")
        logger.error(traceback.format_exc())
    
    app.run(debug=True, port=5001, host='0.0.0.0') 
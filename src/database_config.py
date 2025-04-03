import mysql.connector

# Função para conectar ao banco, esta com informacoes padroes, lembre de atualizar os dados para seu banco.
def conectar_banco():
    try:
        conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",  
            database="dados_ans"  
        )
        return conn
    except mysql.connector.Error as err:
        print(f"Erro ao conectar: {err}")
        return None

from src.database_config import conectar_banco

# Query para obter as 10 operadoras com maiores despesas no último trimestre
QUERY_ULTIMO_TRIMESTRE = """
        SELECT 
        demonstrativos.REG_ANS, 
        COALESCE(operadoras.Nome_Fantasia, 'Empresa não listada na tabela de operadoras') AS Nome_Fantasia,
        SUM(demonstrativos.VL_SALDO_FINAL) AS Despesa_Total
    FROM demonstrativos
    LEFT JOIN operadoras ON demonstrativos.REG_ANS = operadoras.Registro_ANS
    WHERE demonstrativos.DESCRICAO LIKE '%EVENTOS/SINISTROS%'
    AND demonstrativos.DATA >= DATE_SUB((SELECT MAX(DATA) FROM demonstrativos), INTERVAL 3 MONTH)
    GROUP BY demonstrativos.REG_ANS, operadoras.Nome_Fantasia
    ORDER BY Despesa_Total DESC
    LIMIT 10;
"""

# Query para obter as 10 operadoras com maiores despesas no último ano
QUERY_ULTIMO_ANO = """
    SELECT 
        demonstrativos.REG_ANS, 
        COALESCE(operadoras.Nome_Fantasia, 'Empresa não listada na tabela de operadoras') AS Nome_Fantasia,
        SUM(demonstrativos.VL_SALDO_FINAL) AS Despesa_Total
    FROM demonstrativos
    LEFT JOIN operadoras ON demonstrativos.REG_ANS = operadoras.Registro_ANS
    WHERE demonstrativos.DESCRICAO LIKE '%EVENTOS/SINISTROS CONHECIDOS OU AVISADOS%'
    AND demonstrativos.DATA >= DATE_SUB((SELECT MAX(DATA) FROM demonstrativos), INTERVAL 1 YEAR)
    GROUP BY demonstrativos.REG_ANS, operadoras.Nome_Fantasia
    ORDER BY Despesa_Total DESC
    LIMIT 10;
"""

# Função para executar a consulta e exibir os resultados
def executar_consulta(query, descricao):
    conn = conectar_banco()
    cursor = conn.cursor()
    cursor.execute(query)
    resultados = cursor.fetchall()
    conn.close()

    print(f"\n{descricao}")
    print("=" * len(descricao))

    if not resultados:
        print("Nenhum resultado encontrado.")
        return

    for reg_ans, nome, despesa in resultados:
        print(f"Registro ANS: {reg_ans} | Nome Fantasia: {nome} | Despesa Total: R$ {despesa:,.2f}")

# Função principal da opção 4
def executar_consultas_analiticas():
    executar_consulta(QUERY_ULTIMO_TRIMESTRE, "Top 10 Operadoras - Último Trimestre")
    executar_consulta(QUERY_ULTIMO_ANO, "Top 10 Operadoras - Último Ano")

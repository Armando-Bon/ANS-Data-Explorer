import os
from src.download import baixar_pdfs
from src.extrair import extrair_tabela_do_pdf
from src.comprimir import compactar_arquivo
from src.estruturar_importar import estruturar_e_importar
from src.consultas_analiticas import executar_consultas_analiticas
import sys


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

# Diretório para salvar os PDFs
SAVE_DIR = "pdfs"

if __name__ == "__main__":
    while True:
        print("\nMenu de Opções:")
        print("1 - Baixar Anexo I e Anexo II")
        print("2 - Processar Anexo I e gerar CSV compactado")
        print("3 - Estruturar tabela e importar arquivos .csv")
        print("4 - Exibir top10 operadoras com maiores despesas")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "0":
            print("Saindo do programa...")
            break

        elif opcao == "1":
            baixar_pdfs(SAVE_DIR)

        elif opcao == "2":
            csv_arquivo = extrair_tabela_do_pdf(SAVE_DIR)
            if csv_arquivo:
                compactar_arquivo(csv_arquivo)

        elif opcao == "3":
            estruturar_e_importar()

        elif opcao == "4":
            executar_consultas_analiticas()

        else:
            print("Opção inválida! Tente novamente.")

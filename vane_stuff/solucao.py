import pandas as pd
import os

# Caminhos para os arquivos
pasta_modelo = r"C:\\Users\\Vanessa\\Desktop\\dairy_testes\\modelo-matematico"
caminho_csv_original = os.path.join(pasta_modelo, "variaveis.csv")
caminho_csv_novo = os.path.join(pasta_modelo, "variaveis2.csv")
caminho_excel_novo = os.path.join(pasta_modelo, "variaveis2.xlsx")

# Verificar se o arquivo CSV original existe
if not os.path.isfile(caminho_csv_original):
    print(f"Erro: O arquivo 'variaveis.csv' não foi encontrado.")
    exit(1)

# Ler o arquivo CSV original, ignorando a primeira linha
try:
    # Ignorar a primeira linha (cabeçalho)
    with open(caminho_csv_original, 'r', encoding='utf-8') as file:
        linhas = file.readlines()

    # Ignorar o cabeçalho e processar os dados a partir da segunda linha
    dados = linhas[1:]

    print("Arquivo CSV carregado com sucesso, começando a partir da segunda linha!")

    # Separar cada linha de dados usando "#" e "," como delimitadores
    dados_expandidos = []
    for linha in dados:
        linha_limpa = linha.strip()  # Remove espaços em branco e quebras de linha
        valores = linha_limpa.replace("#", ",").split(",")  # Substitui "#" por "," e depois divide
        dados_expandidos.append(valores)

    # Converter para DataFrame
    df_dados = pd.DataFrame(dados_expandidos)

    # Definir os nomes das colunas com base no número correto de valores
    num_colunas = df_dados.shape[1]
    colunas = ["Variável", "Fábrica", "Produto", "Dia", "Destino", "Veículo", "Quantidade"][:num_colunas]
    df_dados.columns = colunas

except Exception as e:
    print(f"Erro ao processar o arquivo CSV: {e}")
    exit(1)

# Salvar o novo DataFrame em um arquivo CSV
try:
    df_dados.to_csv(caminho_csv_novo, index=False)
    print(f"Arquivo 'variaveis2.csv' salvo com sucesso em: {caminho_csv_novo}")
except Exception as e:
    print(f"Erro ao salvar o arquivo CSV: {e}")

# Salvar o DataFrame em um arquivo Excel
try:
    df_dados.to_excel(caminho_excel_novo, index=False, engine='openpyxl')
    print(f"Arquivo 'variaveis2.xlsx' salvo com sucesso em: {caminho_excel_novo}")
except Exception as e:
    print(f"Erro ao salvar o arquivo Excel: {e}")

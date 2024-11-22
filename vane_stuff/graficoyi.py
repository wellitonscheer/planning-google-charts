import pandas as pd
import matplotlib.pyplot as plt

# Carregar o arquivo Excel fornecido pelo usuário
file_path = r'C:\\Users\\Vanessa\\Desktop\\dairy_testes\\modelo-matematico\\variaveis.xlsx'
df = pd.read_excel(file_path, sheet_name='variaveis')

# Renomear colunas para corresponder às necessidades do código
df.rename(columns={'produzir': 'Variavel', 'fábrica': 'Fabrica', 'produto': 'Produto', 'dia': 'Dia', 'kg': 'Valor'}, inplace=True)

# Função para interpretar a coluna 'Variável' e extrair informações das diferentes variáveis
def interpretar_variavel_completa(variavel):
    partes = variavel.split('#')
    if len(partes) == 4 and partes[0] == 'yi':
        # yi representa produção: produto, fábrica, dia
        tipo = 'Produção'
        produto = int(partes[1])
        fabrica = int(partes[2])
        dia = int(partes[3])
    elif len(partes) == 4 and partes[0] == 'yd':
        # yd representa produção de derivado: produto, fábrica, dia
        tipo = 'Produção Derivada'
        produto = int(partes[1])
        fabrica = int(partes[2])
        dia = int(partes[3])
    elif len(partes) == 4 and partes[0] == 'Q':
        # Q representa quantidade liberada da quarentena: produto, dia, fábrica
        tipo = 'Quarentena'
        produto = int(partes[1])
        fabrica = int(partes[2])
        dia = int(partes[3])
    elif len(partes) == 4 and partes[0] == 'I':
        # I representa estoque: produto, fábrica, dia
        tipo = 'Estoque'
        produto = int(partes[1])
        fabrica = int(partes[2])
        dia = int(partes[3

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Carregar o arquivo CSV fornecido pelo usuário
file_path = "variaveisP.csv"
df = pd.read_csv(file_path, sep=",")

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
        dia = int(partes[3])
    elif len(partes) == 6 and partes[0] == 'x2':
        # x2 representa transporte: produto destino, produto, fábrica destino, fábrica origem, dia
        tipo = 'Transporte'
        produto = int(partes[1])
        fabrica_destino = int(partes[2])
        fabrica_origem = int(partes[3])
        dia = int(partes[4])
        return tipo, produto, fabrica_destino, fabrica_origem, dia
    else:
        return None, None, None, None, None

    return tipo, produto, fabrica, None, dia

# Aplicar a função para interpretar todas as variáveis e criar novas colunas no DataFrame
df[['Tipo', 'Produto', 'Fábrica_Destino', 'Fábrica_Origem', 'Dia']] = df['Variável'].apply(lambda x: pd.Series(interpretar_variavel_completa(x)))

# Filtrar apenas as linhas que foram corretamente interpretadas
df_completo = df.dropna(subset=['Tipo'])

# Explicação das variáveis:
# - Tmax: Valor encontrado no início do arquivo, representando o valor máximo de tempo.
# - yi[f, p, d]: Determina a quantidade produzida do produto p na fábrica f no dia d. Exemplo: yi#1#1#0,0.0 significa: variável de quantidade de produto produzido, produto 1, na fábrica 1, no dia 0, com quantidade 0.0.
# - yd[f, p, d]: Determina a quantidade produzida do produto derivado p na fábrica f no dia d. Exemplo: yd#1#1#6,0.0 significa: variável de quantidade de produto derivado produzido, produto 1, na fábrica 1, no dia 6, com quantidade 0.0.
# - Q[p, d, f]: Determina a quantidade do produto p liberada da quarentena no dia d na fábrica f. Exemplo: Q#1#1#2,0.0 significa: quantidade de produtos em quarentena do produto 1, liberada no dia 1, na fábrica 2, com quantidade 0.0.
# - I[p, f, d]: Representa o estoque do produto p na fábrica f no dia d. Exemplo: I#1#1#2,0.0 significa: estoque do produto 1, na fábrica 1, no dia 2, com quantidade 0.0.
# - x2[p, destino, origem, d]: Determina a quantidade do produto p que chega à fábrica destino vinda da fábrica origem no dia d. Exemplo: x2#3#1#3#1#1,0.0 significa: produto 3, fábrica de destino 1, fábrica de origem 3, no dia 1, com quantidade 0.0.

# Criar um gráfico de linha do tempo para cada produto
produtos = df_completo['Produto'].unique()

for produto in produtos:
    df_produto = df_completo[df_completo['Produto'] == produto]
    plt.figure(figsize=(12, 6))
    
    # Filtrar e plotar cada tipo de variável para o produto
    for tipo in df_produto['Tipo'].unique():
        df_tipo = df_produto[df_produto['Tipo'] == tipo]
        plt.plot(df_tipo['Dia'], df_tipo['Valor'], marker='o', linestyle='-', label=tipo)
    
    # Formatar o eixo X para mostrar os dias
    plt.xlabel('Dia')
    plt.ylabel('Quantidade')
    plt.title(f'Linha do Tempo das Atividades do Produto {int(produto)}')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()
    
    # Salvar o gráfico como imagem
    plt.savefig(f'linha_do_tempo_produto_{int(produto)}.png')
    
    # Mostrar o gráfico
    plt.show()

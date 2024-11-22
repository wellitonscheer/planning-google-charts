import cplex
import matplotlib.pyplot as plt
import pandas as pd
import os

# Caminho para a pasta do modelo
pasta_modelo = r'C:\\Users\\Vanessa\\Desktop\\dairy_testes\\modelo-matematico\\modelo finais'

# Caminhos para o modelo e arquivos de saída
arquivo_lp = os.path.join(pasta_modelo, "modeloP.lp")
arquivo_log = os.path.join(pasta_modelo, "solverP.log")
grafico_pdf = os.path.join(pasta_modelo, "grafico_ganttP.pdf")
arquivo_variaveis = os.path.join(pasta_modelo, "variaveisP.csv")
arquivo_xml = os.path.join(pasta_modelo, "solucaoP.xml")  # Novo caminho para o XML

# Criar uma instância do CPLEX
model = cplex.Cplex()

# Redirecionar o log para o arquivo solver.log
with open(arquivo_log, "w") as log_file:
    model.set_log_stream(log_file)
    model.set_results_stream(log_file)
    model.set_warning_stream(log_file)
    model.set_error_stream(log_file)

    # Ler e resolver o modelo LP
    model.read(arquivo_lp)
    model.solve()

# Extrair a solução
solution = model.solution
objetivo = solution.get_objective_value()
print(f"Valor da função objetivo: {objetivo}")

# Salvar a solução completa como XML
solution.write(arquivo_xml)
print(f"Solução completa salva em: {arquivo_xml}")

# Extrair nomes e valores das variáveis
variaveis = model.variables.get_names()
valores = solution.get_values()

# Criar um DataFrame com todas as variáveis e salvar como CSV
df_variaveis = pd.DataFrame(list(zip(variaveis, valores)), columns=["Variável", "Valor"])
df_variaveis.to_csv(arquivo_variaveis, index=False)

print(f"Arquivo com variáveis salvo em: {arquivo_variaveis}")

# Filtrar variáveis relevantes para o gráfico de Gantt
dados_gantt = [
    {"Tarefa": var, "Inicio": int(var.split(',')[2].strip(']')), "Duracao": 1}
    for var, val in zip(variaveis, valores)
    if var.startswith("x[") or var.startswith("x2[") or var.startswith("y[")
]

# Verificar se há dados suficientes para o gráfico de Gantt
if not dados_gantt:
    print("Nenhuma variável relevante encontrada para gerar o gráfico de Gantt.")
else:
    # Converter para DataFrame
    df_gantt = pd.DataFrame(dados_gantt)

    # Gerar o gráfico de Gantt
    fig, ax = plt.subplots(figsize=(10, 6))

    for i, row in df_gantt.iterrows():
        ax.barh(row["Tarefa"], row["Duracao"], left=row["Inicio"], align='center')

    ax.set_xlabel("Tempo")
    ax.set_ylabel("Tarefa")
    ax.set_title("Gráfico de Gantt - Solução do Modelo")
    ax.grid(True)

    # Salvar o gráfico como PDF
    plt.savefig(grafico_pdf)

    print(f"Gráfico de Gantt salvo em: {grafico_pdf}")
    plt.show()

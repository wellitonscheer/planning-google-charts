import xml.etree.ElementTree as ET
import os

# Caminho para o arquivo XML de solução do CPLEX
caminho_arquivo_xml = "C:\\Users\\Vanessa\\Desktop\\dairy_testes\\modelo-matematico\\modelo finais\\solucaoP.xml"

# Caminho para salvar o plano de produção
caminho_plano = "C:\\Users\\Vanessa\\Desktop\\dairy_testes\\modelo-matematico\\modelo finais\\plano_validacao.txt"

# Função para criar um plano de produção a partir do arquivo XML
def criar_plano_de_producao(caminho_arquivo_xml, caminho_plano):
    try:
        # Carregar o arquivo XML
        tree = ET.parse(caminho_arquivo_xml)
        root = tree.getroot()

        # Extrair o valor de Tmax, se disponível
        Tmax = None
        for var in root.findall(".//variable"):
            if var.get("name") == "Tmax":
                Tmax = float(var.get("value"))
                break

        # Lista para armazenar as ações
        acoes = []

        # Iterar pelas variáveis encontradas no XML
        for var in root.findall(".//variable"):
            name = var.get("name")
            value = float(var.get("value"))

            # Somente considerar valores maiores que zero
            if value > 0:
                partes = name.split("#")
                variavel = partes[0]

                try:
                    # Ações baseadas no tipo de variável
                    if variavel == "yi":
                        fabrica = partes[1]
                        produto = partes[2]
                        dia = partes[3]
                        acoes.append((int(dia), int(fabrica), int(produto), f"No dia {dia}, produzir {value} unidades do produto p{produto} na fábrica f{fabrica}.") )
                    elif variavel == "yd":
                        fabrica = partes[1]
                        produto_primario = partes[2]
                        produto_derivado = partes[3]
                        dia = partes[4]
                        acoes.append((int(dia), int(fabrica), int(produto_derivado), f"No dia {dia}, utilizar {value} unidades do produto primário p{produto_primario} para produzir o derivado p{produto_derivado} na fábrica f{fabrica}.") )
                    elif variavel == "Q":
                        fabrica = partes[1]
                        produto = partes[2]
                        dia = partes[3]
                        acoes.append((int(dia), int(fabrica), int(produto), f"No dia {dia}, liberar {value} unidades do produto p{produto} da quarentena na fábrica f{fabrica}.") )
                    elif variavel == "I":
                        fabrica = partes[1]
                        produto = partes[2]
                        dia = partes[3]
                        acoes.append((int(dia), int(fabrica), int(produto), f"No dia {dia}, o estoque do produto p{produto} na fábrica f{fabrica} é de {value} unidades.") )
                    elif variavel == "x2":
                        fabrica_origem = partes[1]
                        produto = partes[2]
                        dia = partes[3]
                        fabrica_destino = partes[4]
                        acoes.append((int(dia), int(fabrica_origem), int(produto), f"No dia {dia}, transferir {value} unidades do produto p{produto} da fábrica f{fabrica_origem} para a fábrica f{fabrica_destino}.") )
                except IndexError as e:
                    print(f"Erro ao processar a variável '{name}': {e}")

        # Ordenar as ações em ordem cronológica (primeiro por dia, depois por fábrica, depois por produto)
        acoes_ordenadas = sorted(acoes, key=lambda x: (x[0], x[1], x[2]))

        # Abrir o arquivo de plano para escrita
        with open(caminho_plano, 'w') as f:
            f.write("Plano de Produção a partir da Solução do CPLEX\n")
            f.write("=============================================\n\n")

            # Escrever o valor de Tmax no início do arquivo, se encontrado
            if Tmax is not None:
                f.write(f"Tmax: {Tmax}\n\n")

            # Escrever as ações ordenadas no arquivo
            for acao in acoes_ordenadas:
                f.write(acao[3] + "\n")

        print(f"Plano de produção salvo em: {caminho_plano}")

    except ET.ParseError as e:
        print(f"Erro ao processar o arquivo XML: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

# Criar o plano de produção a partir do arquivo XML
criar_plano_de_producao(caminho_arquivo_xml, caminho_plano)

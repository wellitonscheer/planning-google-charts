import xml.etree.ElementTree as ET
import os
import json

SMALL_THRESHOLD = 1e-4

file_name = "solucao.xml"
output_file_name = "data_solucao.json"
# tipos validos
{
    "tipo": "quarentena",
    "tipo": "producao_insumo",
    "tipo": "producao_derivado",
    "tipo": "transporte_destino",
    "tipo": "transporte_origem",
    "tipo": "estoque",
}
# exemplo estrutura dos dados de saida
[
    {
        "tipo": "quarentena",
        "produto": "1",
        "fabrica": "2",
        "dia": "23",
        "valor": "3000",
        "produto_primario": "1",
        "fabrica_origem": "2",
        "fabrica_destino": "4",
        "veiculo": "6",
    },
]

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)
output_file_path = os.path.join(script_dir, output_file_name)

quarentena_tempo = {"1": 20, "3": 3, "5": 5}

tree = ET.parse(file_path)
root = tree.getroot()

variables_element = root.find(".//variables")

data = {}
if variables_element is not None:
    variables = []
    for var in variables_element.findall('variable'):
        name = var.get('name')
        index = var.get('index')
        value = var.get('value')
        partes = name.split("#")
        variavel = partes[0]

        try:
            numeric_value = float(value)
            if abs(numeric_value) < SMALL_THRESHOLD and variavel != "I":
                continue
            rounded_value = round(numeric_value, 4)
        except ValueError:
            continue
        
        if variavel == "Q":
            # Quarentena
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            if produto not in quarentena_tempo:
                continue
            data[index] = {
                "tipo": "quarentena",
                "produto": produto,
                "fabrica": fabrica,
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": None,
                "fabrica_origem": None,
                "fabrica_destino": None,
                "veiculo": None,
            }
        elif variavel == "yi":
            # Produção (produção insumo, queijo peça por exemplo)
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            data[index] = {
                "tipo": "producao_insumo",
                "produto": produto, # produto sendo produzido
                "fabrica": fabrica,
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": None,
                "fabrica_origem": None,
                "fabrica_destino": None,
                "veiculo": None,
            }
        elif variavel == "yd":
            # Produção (produção derivada do insumo, queijo fatiado por exemplo)
            fabrica = partes[1]
            produto_primario = partes[2]
            produto_derivado = partes[3]
            dia = partes[4]
            data[index] = {
                "tipo": "producao_derivado",
                "produto": produto_derivado, # produto sendo produzido
                "fabrica": fabrica,
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": produto_primario,
                "fabrica_origem": None,
                "fabrica_destino": None,
                "veiculo": None,
            }
        elif variavel == "x2":
            # vai dizer quando chega na f de destino
            fabrica_origem = partes[1]
            produto = partes[2]
            dia = partes[3]
            fabrica_recebe = partes[4]
            tipo_transporte = partes[5]
            veiculo = partes[6]
            data[index] = {
                "tipo": "transporte_destino",
                "produto": produto,
                "fabrica": fabrica_recebe, # a fabrica q o produto esta
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": None,
                "fabrica_origem": fabrica_origem,
                "fabrica_destino": fabrica_recebe,
                "veiculo": f't{tipo_transporte}-k{veiculo}',
            }
        elif variavel == "x":
            # vai dizer quando está saindo da fabrica de origem f
            fabrica_origem = partes[1]
            produto = partes[2]
            dia = partes[3]
            fabrica_destino = partes[4]
            tipo_transporte = partes[5]
            veiculo = partes[6]
            data[index] = {
                "tipo": "transporte_origem",
                "produto": produto,
                "fabrica": fabrica_origem, # a fabrica q o produto esta
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": None,
                "fabrica_origem": fabrica_origem,
                "fabrica_destino": fabrica_destino,
                "veiculo": f't{tipo_transporte}-k{veiculo}',
            }
        elif variavel == "I":
            # Estoque
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            data[index] = {
                "tipo": "estoque",
                "produto": produto,
                "fabrica": fabrica,
                "dia": dia,
                "valor": rounded_value,
                "produto_primario": None,
                "fabrica_origem": None,
                "fabrica_destino": None,
                "veiculo": None,
            }

    sorted_variables = sorted(data.values(), key=lambda x: (int(x["produto"]), int(x["fabrica"])))

    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(sorted_variables, file, ensure_ascii=False, indent=2)

else:
    print("No <variables> element found in the XML.")
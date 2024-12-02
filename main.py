import xml.etree.ElementTree as ET
import os

SMALL_THRESHOLD = 1e-4

file_name = "solucao.xml"
output_file_name = "chart_data.html"

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, file_name)
output_file_path = os.path.join(script_dir, output_file_name)

tree = ET.parse(file_path)
root = tree.getroot()

variables_element = root.find(".//variables")

quarentena_tempo = {"1": 20, "3": 3, "5": 5}
numbers_style = {"1": "₁", "2": "₂", "2": "₂", "3": "₃", "4": "₄", "5": "₅", "6": "₆", "7": "₇", "8": "₈", "9": "₉"}

if variables_element is not None:
    variables = []
    colors = []
    for var in variables_element.findall('variable'):
        name = var.get('name')
        index = var.get('index')
        value = var.get('value')

        try:
            numeric_value = float(value)
            if abs(numeric_value) < SMALL_THRESHOLD:
                continue
            rounded_value = round(numeric_value)
        except ValueError:
            continue
            
        partes = name.split("#")
        variavel = partes[0]

        if variavel == "Q":
            # Quarentena
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            if produto not in quarentena_tempo:
                continue
            variables.append([f"p{produto}_f{fabrica}", f"p{numbers_style[produto]} f{numbers_style[fabrica]}", f"{rounded_value}", "color: #B8BAB8", f"new Date(2024, 0, {int(dia) - quarentena_tempo[produto]})", f"new Date(2024, 0, {dia})"])
        elif variavel == "yi":
            # Produção (produção insumo, queijo peça por exemplo)
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            variables.append([f"p{produto}_f{fabrica}", f"p{numbers_style[produto]} f{numbers_style[fabrica]}", f"{rounded_value}", "color: #AEB1F3", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])
        elif variavel == "yd":
            # Produção (produção derivada do insumo, queijo fatiado por exemplo)
            fabrica = partes[1]
            produto_primario = partes[2]
            produto_derivado = partes[3]
            dia = partes[4]
            variables.append([f"p{produto_derivado}_f{fabrica}", f"p{numbers_style[produto_derivado]} f{numbers_style[fabrica]}", f"{rounded_value} p{produto_primario}", "color: #d7a7f3", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])
        elif variavel == "x2":
            # vai dizer quando chega na f de destino
            fabrica_origem = partes[1]
            produto = partes[2]
            dia = partes[3]
            fabrica_recebe = partes[4]
            veiculo = partes[5]
            variables.append([f"p{produto}_f{fabrica_recebe}", f"p{numbers_style[produto]} f{numbers_style[fabrica_recebe]}", f"{rounded_value} f{fabrica_origem} k{veiculo}", "color: #f3dfa2", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])
        elif variavel == "x":
            # vai dizer quando está saindo da fabrica de origem f
            fabrica_origem = partes[1]
            produto = partes[2]
            dia = partes[3]
            fabrica_destino = partes[4]
            veiculo = partes[5]
            variables.append([f"p{produto}_f{fabrica_origem}", f"p{numbers_style[produto]} f{numbers_style[fabrica_origem]}", f"{rounded_value} f{fabrica_destino} k{veiculo}", "color: #ffaf80", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])
        elif variavel == "I":
            # Estoque
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            variables.append([f"p{produto}_f{fabrica}", f"p{numbers_style[produto]} f{numbers_style[fabrica]}", f"{rounded_value}", "color: #cde4ab", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])

        # variables.append({'name': name, 'index': index, 'value': rounded_value})

    sorted_variables = sorted(variables, key=lambda x: (x[0].split('_')[0], x[0].split('_')[1]))
    formatted_data_list = [
        f"[{repr(item[1])}, {repr(item[2])}, {repr(item[3])}, {item[4]}, {item[5]}]"
        for item in sorted_variables
    ]
    result = f"[{', '.join(formatted_data_list)}]"
    print(result)

    first_js_code = """
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1.0" />
            <title>Document</title>
            <script
            type="text/javascript"
            src="https://www.gstatic.com/charts/loader.js"
            ></script>
            <style>
            #chart-container {
                width: 100%;
                height: 100%;
                overflow-x: 4000px;
                margin-bottom: 20px; /* Space between chart and descriptions */
            }

            #descriptions {
                display: flex;
                justify-content: space-between;
                margin-top: 10px;
                padding: 10px;
                flex-wrap: wrap;
            }

            .description {
                width: 30%;
                padding: 10px;
                margin: 5px;
                background-color: #f4f4f4;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            </style>

            <script type="text/javascript">
            google.charts.load("current", { packages: ["timeline"] });
            google.charts.setOnLoadCallback(drawChart);
            function drawChart() {
                var container = document.getElementById("timeline");
                var chart = new google.visualization.Timeline(container);
                var dataTable = new google.visualization.DataTable();
                dataTable.addColumn({ type: "string", id: "p_f" });
                dataTable.addColumn({ type: "string", id: "acao" });
                dataTable.addColumn({ type: 'string', role: 'style' });
                dataTable.addColumn({ type: "date", id: "dia_comeco" });
                dataTable.addColumn({ type: "date", id: "dia_fim" });
                dataTable.addRows(
    """ + result + """
                );
                var options = {
                    hAxis: {
                        format: "d",
                        textStyle: {
                            hAlign: "center",
                            vAlign: "top",
                        },
                    },
                    timeline: {
                        colorByRowLabel: false,
                        groupByRowLabel: true,
                        rowLabelStyle: {
                            fontName: "Cambria Math",
                            fontSize: 18,
                            italic: true,
                            bold: true,
                        },
                        barLabelStyle: {
                            color: "black",
                            bold: true,
                            fontName: "Cambria Math",
                            italic: true,
                            bold: true,
                        },
                    },
                };

                chart.draw(dataTable, options);
            }
            </script>
        </head>
        <body>
            <div id="chart-container">
                <div style="font-family: Arial, sans-serif; display: flex; align-items: center;">
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #AEB1F3;"></div>
                        Produção Insumo
                    </div>
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #d7a7f3;"></div>
                        Produção Derivada
                    </div>
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #ffaf80;"></div>
                        Transporte origem
                    </div>
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #f3dfa2;"></div>
                        Transporte destino
                    </div>
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #B8BAB8;"></div>
                        Quarentena
                    </div>

                   <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #cde4ab;"></div>
                        Estoque
                    </div> 

                </div>

                <div id="timeline" style="height: 1100px; width: 2720px"></div>
            </div>
        </body>
    </html>
"""

    with open(output_file_path, "w") as js_file:
        js_file.write(first_js_code)

    print("JavaScript code has been written to 'chart_data.js'.")

else:
    print("No <variables> element found in the XML.")
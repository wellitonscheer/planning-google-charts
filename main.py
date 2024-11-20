import xml.etree.ElementTree as ET

SMALL_THRESHOLD = 1e-4

file_name = "data/solucao.xml"

tree = ET.parse(file_name)
root = tree.getroot()

variables_element = root.find(".//variables")

quarentena_tempo = {"1": 20, "3": 3, "5": 5}

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
            variables.append([f"p{produto}_f{fabrica}", f"{rounded_value}", "color: #BB4430", f"new Date(2024, 0, {int(dia) - quarentena_tempo[produto]})", f"new Date(2024, 0, {dia})"])
        elif variavel == "yi":
            # Produção (produção insumo, queijo peça por exemplo)
            fabrica = partes[1]
            produto = partes[2]
            dia = partes[3]
            variables.append([f"p{produto}_f{fabrica}", f"{rounded_value}", "color: #5C95FF", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])
        elif variavel == "yd":
            # Produção (produção derivada do insumo, queijo fatiado por exemplo)
            fabrica = partes[1]
            produto_primario = partes[2]
            produto_derivado = partes[3]
            dia = partes[4]
            variables.append([f"p{produto_derivado}_f{fabrica}", f"{rounded_value} p{produto_primario}", "color: #FFD166", f"new Date(2024, 0, {dia})", f"new Date(2024, 0, {int(dia) + 1})"])

        # variables.append({'name': name, 'index': index, 'value': rounded_value})

    sorted_variables = sorted(variables, key=lambda x: (x[0].split('_')[0], x[0].split('_')[1]))
    formatted_data_list = [
        f"[{repr(item[0])}, {repr(item[1])}, {repr(item[2])}, {item[3]}, {item[4]}]"
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
                        barLabelStyle: {
                        color: "black",
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
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #5C95FF;"></div>
                        Produção Insumo
                    </div>
                    <div style="font-size: 16px; margin: 5px 10px 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #FFD166;"></div>
                        Produção Derivada
                    </div>
                    <div style="font-size: 16px; margin: 5px 0; display: inline-flex; align-items: center;">
                        <div style="width: 20px; height: 20px; display: inline-block; margin-right: 8px; border: 1px solid #000; background-color: #BB4430;"></div>
                        Quarentena
                    </div>
                </div>

                <div id="timeline" style="height: 4000px"></div>
            </div>
        </body>
    </html>
"""

    with open("grafico_page/chart_data.html", "w") as js_file:
        js_file.write(first_js_code)

    print("JavaScript code has been written to 'chart_data.js'.")

else:
    print("No <variables> element found in the XML.")
const numbers_style = {
  1: "₁",
  2: "₂",
  2: "₂",
  3: "₃",
  4: "₄",
  5: "₅",
  6: "₆",
  7: "₇",
  8: "₈",
  9: "₉",
};
const quarentena_tempo = { 1: 20, 3: 3, 5: 5 };
let chartData;

function newDate(dia) {
  return new Date(2024, 0, dia);
}
const produtos_usar_chart = [3, 4];

fetch("../data_solucao.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    let extraItems = [];
    chartData = data
      .map((item) => {
        const produto = item["produto"];
        const fabrica = item["fabrica"];
        const produtoFabrica = `p${numbers_style[produto]} f${numbers_style[fabrica]}`;
        const valorString = `${item["valor"]}`;
        const diaInt = Number(item["dia"]);
        if (!produtos_usar_chart.includes(Number(produto))) {
          return;
        }
        // prduto p2 usa p1, e p4 usa p3
        if (Number(fabrica) == 5) {
          return;
        }
        switch (item["tipo"]) {
          // case "quarentena":
          //   return [
          //     produtoFabrica,
          //     valorString,
          //     "color: #B8BAB8",
          //     newDate(diaInt - quarentena_tempo[produto]),
          //     newDate(diaInt),
          //   ];
          case "quarentena":
            const diaInicio = diaInt - quarentena_tempo[produto];
            extraItems.push([
              produtoFabrica,
              `enc ${valorString}`,
              "color: #B8BAB8",
              newDate(diaInicio),
              newDate(diaInicio + 1),
            ]);
            return [
              produtoFabrica,
              `lib ${valorString}`,
              "color: #B8BAB8",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          case "producao_insumo":
            return [
              produtoFabrica,
              valorString,
              "color: #AEB1F3",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          case "producao_derivado":
            return [
              produtoFabrica,
              `${valorString} p${item["produto_primario"]}`,
              "color: #d7a7f3",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          case "transporte_destino":
            return [
              produtoFabrica,
              `${valorString} f${item["fabrica_origem"]} ${item["veiculo"]}`,
              "color: #f3dfa2",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          case "transporte_origem":
            return [
              produtoFabrica,
              `${valorString} f${item["fabrica_destino"]} ${item["veiculo"]}`,
              "color: #ffaf80",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          case "estoque":
            return [
              produtoFabrica,
              valorString,
              "color: #cde4ab",
              newDate(diaInt),
              newDate(diaInt + 1),
            ];
          default:
            console.log("tipo invalido: ", item["tipo"]);
        }
      })
      .filter((value) => !!value);
    chartData = [...chartData, ...extraItems];
  })
  .then(() => {
    google.charts.load("current", { packages: ["timeline"] });
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
      var container = document.getElementById("timeline");
      var chart = new google.visualization.Timeline(container);
      var dataTable = new google.visualization.DataTable();
      dataTable.addColumn({ type: "string", id: "p_f" });
      dataTable.addColumn({ type: "string", id: "acao" });
      dataTable.addColumn({ type: "string", role: "style" });
      dataTable.addColumn({ type: "date", id: "dia_comeco" });
      dataTable.addColumn({ type: "date", id: "dia_fim" });
      dataTable.addRows(chartData);
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
            fontSize: 12,
            fontName: "Cambria Math",
            italic: true,
            bold: true,
          },
        },
      };

      chart.draw(dataTable, options);
    }
  })
  .catch((error) => console.error("Error fetching JSON:", error));

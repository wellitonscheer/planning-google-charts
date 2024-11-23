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

fetch("../data_solucao.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    chartData = data
      .map((item) => {
        console.log(item["tipo"]);
        switch (item["tipo"]) {
          case "quarentena":
            return [
              `p${numbers_style[item["produto"]]} f${
                numbers_style[item["fabrica"]]
              }`,
              `${item["valor"]}`,
              "color: #B8BAB8",
              new Date(
                2024,
                0,
                Number(item["dia"]) - quarentena_tempo[item["produto"]]
              ),
              new Date(2024, 0, Number(item["dia"])),
            ];
          default:
            console.log("tipo invalido", item);
        }
      })
      .filter((value) => !!value);
    console.log(chartData);
  })
  .catch((error) => console.error("Error fetching JSON:", error));

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
        fontName: "Cambria Math",
        italic: true,
        bold: true,
      },
    },
  };

  chart.draw(dataTable, options);
}

google.charts.load("current", { packages: ["timeline"] });
google.charts.setOnLoadCallback(drawChart);
function drawChart() {
  var container = document.getElementById("chart_div");
  var chart = new google.visualization.Timeline(container);
  var dataTable = new google.visualization.DataTable();
  dataTable.addColumn({ type: "string", id: "p_f" });
  dataTable;
  dataTable.addColumn({ type: "string", id: "acao" });
  dataTable.addColumn({ type: "number", id: "dia_comeco" });
  dataTable.addColumn({ type: "number", id: "dia_fim" });
  dataTable.addRows([
    [
      "p1_f1",
      "21420 unidades do produto p1 em quarentena na fábrica f1 por 20 dias",
      "new Date(2024, 0, 2)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p1_f1",
      "680 unidades do produto p1 em quarentena na fábrica f1 por 20 dias",
      "new Date(2024, 0, 3)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p1_f3",
      "18900 unidades do produto p1 em quarentena na fábrica f3 por 20 dias",
      "new Date(2024, 0, 2)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f1",
      "2000 unidades do produto p3 em quarentena na fábrica f1 por 3 dias",
      "new Date(2024, 0, 3)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f4",
      "10000 unidades do produto p3 em quarentena na fábrica f4 por 3 dias",
      "new Date(2024, 0, 2)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f4",
      "10000 unidades do produto p3 em quarentena na fábrica f4 por 3 dias",
      "new Date(2024, 0, 3)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f4",
      "10000 unidades do produto p3 em quarentena na fábrica f4 por 3 dias",
      "new Date(2024, 0, 4)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f4",
      "10000 unidades do produto p3 em quarentena na fábrica f4 por 3 dias",
      "new Date(2024, 0, 5)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p3_f4",
      "5000 unidades do produto p3 em quarentena na fábrica f4 por 3 dias",
      "new Date(2024, 0, 20)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p5_f2",
      "17192 unidades do produto p5 em quarentena na fábrica f2 por 5 dias",
      "new Date(2024, 0, 3)",
      "new Date(2024, 0, {dia})",
    ],
    [
      "p5_f2",
      "16808 unidades do produto p5 em quarentena na fábrica f2 por 5 dias",
      "new Date(2024, 0, 14)",
      "new Date(2024, 0, {dia})",
    ],
  ]);

  chart.draw(dataTable);
}

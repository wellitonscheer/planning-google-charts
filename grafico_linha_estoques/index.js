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
let produtos = [];
let dias = [];
let fabricas = [];
const diasValores = {};
let fabricasDiasValores = {};

function newDate(dia) {
  return new Date(2024, 0, dia);
}

function fillNullValues(data) {
  let lastValidValues = [];

  return data.map((row, rowIndex) => {
    // Process data rows
    return row.map((value, colIndex) => {
      if (colIndex === 0) {
        // First column (day names) remains unchanged
        return value;
      }

      if (value === null) {
        // Replace null with the last valid value for this column
        return lastValidValues[colIndex] ?? null;
      } else {
        // Update the last valid value for this column
        lastValidValues[colIndex] = value;
        return value;
      }
    });
  });
}

fetch("../data_solucao.json")
  .then((response) => {
    if (!response.ok) {
      throw new Error("Network response was not ok");
    }
    return response.json();
  })
  .then((data) => {
    data.forEach((item) => {
      const produto = item["produto"];
      const fabrica = item["fabrica"];
      const diaInt = Number(item["dia"]);
      switch (item["tipo"]) {
        case "estoque":
          if (!produtos.includes(produto)) {
            produtos.push(produto);
          }
          if (!dias.includes(diaInt)) {
            dias.push(diaInt);
          }
          if (!fabricas.includes(fabrica)) {
            fabricas.push(fabrica);
          }
        default:
      }
    });
    fabricas = fabricas.sort((a, b) => Number(a) - Number(b));
    return data;
  })
  .then((data) => {
    fabricas.forEach((f) => {
      fabricasDiasValores[f] = [];
      chartData = data
        .map((item) => {
          const produto = item["produto"];
          const fabrica = item["fabrica"];
          const valorString = `${item["valor"]}`;
          const diaInt = Number(item["dia"]);
          if (Number(fabrica) != Number(f)) {
            return;
          }

          switch (item["tipo"]) {
            case "estoque":
              if (!produtos.includes(produto)) {
                produtos.push(produto);
              }
              if (!dias.includes(diaInt)) {
                dias.push(diaInt);
              }
              return [diaInt, produto, valorString];
            default:
          }
        })
        .filter((value) => !!value);
      dias.forEach((d) => (fabricasDiasValores[f][d] = []));
      chartData.forEach((d) => {
        fabricasDiasValores[f][d[0]].push([Number(d[2]), Number(d[1])]);
      });
    });

    chartData = data
      .map((item) => {
        const produto = item["produto"];
        const fabrica = item["fabrica"];
        const valorString = `${item["valor"]}`;
        const diaInt = Number(item["dia"]);
        if (Number(fabrica) != 5) {
          return;
        }

        switch (item["tipo"]) {
          case "estoque":
            if (!produtos.includes(produto)) {
              produtos.push(produto);
            }
            if (!dias.includes(diaInt)) {
              dias.push(diaInt);
            }
            return [diaInt, produto, valorString];
          default:
        }
      })
      .filter((value) => !!value);
    dias.forEach((d) => (diasValores[d] = []));
    chartData.forEach((d) => {
      diasValores[d[0]].push(Number(d[2]));
    });
  })
  .then(() => {
    google.charts.load("current", { packages: ["line"] });
    google.charts.setOnLoadCallback(drawChart);
    function drawChart() {
      var newDiv = document.createElement("div");
      newDiv.id = "timeline";
      newDiv.style.marginTop = "20px";
      document.body.appendChild(newDiv);
      var chart = new google.charts.Line(newDiv);
      var data = new google.visualization.DataTable();
      data.addColumn("number", "Dia");
      produtos.forEach((p) => data.addColumn("number", `p${p}`));
      data.addRows(
        Object.entries(diasValores).map(([key, value]) => [
          Number(key),
          ...value,
        ])
      );

      var options = {
        chart: {
          title: "Estoque no centro de distribuição por produto",
          subtitle: "em toneladas",
        },
        width: 1300,
        height: 700,
      };
      chart.draw(data, google.charts.Line.convertOptions(options));
    }
  })
  .then(() => {
    google.charts.load("current", { packages: ["line"] });
    google.charts.setOnLoadCallback(drawChart);

    function drawChart() {
      Object.entries(fabricasDiasValores).forEach(([key, value]) => {
        let produtosNaF = [];
        let firstOcurency = {};

        const biggestList = Object.values(value).reduce((largest, current) => {
          current.forEach((c) => {
            if (!produtosNaF.includes(c[1])) {
              produtosNaF.push(c[1]);
              firstOcurency[c[1]] = c[0];
            }
          });
          return current.length > largest.length ? current : largest;
        }, []);

        var newDiv = document.createElement("div");
        newDiv.id = `f${key}`;
        newDiv.style.marginTop = "20px";
        document.body.appendChild(newDiv);
        var chart = new google.charts.Line(newDiv);
        var data = new google.visualization.DataTable();
        data.addColumn("number", "Dia");
        produtosNaF.forEach((p) => data.addColumn("number", `p${p}`));
        data.addRows(
          fillNullValues(
            Object.entries(value).map(([key, value]) => {
              const extendedValue = [
                ...value.map((v) => v[0]),
                ...Array(Math.max(produtosNaF.length - value.length, 0)).fill(
                  null
                ),
              ];
              return [Number(key), ...extendedValue];
            })
          )
        );

        var options = {
          interpolateNulls: true,
          chart: {
            title: `Estoque na f${key}`,
            subtitle: "em toneladas",
          },
          width: 1300,
          height: 700,
        };
        chart.draw(data, google.charts.Line.convertOptions(options));
      });
    }
  })
  .catch((error) => console.error("Error fetching JSON:", error));

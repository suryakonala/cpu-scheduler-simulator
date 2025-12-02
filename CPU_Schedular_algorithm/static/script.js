// let pid = 2;

// function addRow() {
//   const table = document.getElementById("processTable");
//   const row = table.insertRow();
//   row.innerHTML = `
//     <td>${pid}</td>
//     <td><input></td>
//     <td><input></td>
//     <td><input></td>
//   `;
//   pid++;
// }

// function runAlgorithm() {
//   const algo = document.getElementById("algorithm").value;
//   const quantum = document.getElementById("quantum").value || 2;

//   const rows = document.querySelectorAll("#processTable tr");
//   let processes = [];

//   for (let i = 1; i < rows.length; i++) {
//     const cells = rows[i].querySelectorAll("input");
//     processes.push({
//       pid: i,
//       arrival: parseInt(cells[0].value || 0),
//       burst: parseInt(cells[1].value || 1),
//       priority: parseInt(cells[2].value || 0)
//     });
//   }

//   fetch("/run", {
//     method: "POST",
//     headers: {"Content-Type": "application/json"},
//     body: JSON.stringify({
//       processes,
//       algorithm: algo,
//       quantum
//     })
//   })
//   .then(res => res.json())
//   .then(data => {
//     drawGantt(data.gantt);

//     document.getElementById("results").innerHTML =
//       "Average Waiting Time: " + data.avg_wt.toFixed(2) +
//       "<br>Average Turnaround Time: " + data.avg_tat.toFixed(2);
//   });
// }


// /* ✅ ✅ ✅ ANIMATED COLORFUL GANTT */
// function drawGantt(gantt) {
//   const ganttDiv = document.getElementById("gantt");
//   ganttDiv.innerHTML = "";

//   gantt.forEach(block => {
//     const div = document.createElement("div");
//     div.className = `block p${block.pid}`;
//     div.innerText = `P${block.pid} (${block.start} - ${block.end})`;
//     ganttDiv.appendChild(div);
//   });
// }


// /* ✅ ✅ ✅ ALGORITHM COMPARISON FUNCTIONS (NEWLY ADDED) */
// function compareAlgorithms() {
//   const rows = document.querySelectorAll("#processTable tr");
//   let processes = [];

//   for (let i = 1; i < rows.length; i++) {
//     const cells = rows[i].querySelectorAll("input");
//     processes.push({
//       pid: i,
//       arrival: parseInt(cells[0].value || 0),
//       burst: parseInt(cells[1].value || 1),
//       priority: parseInt(cells[2].value || 0)
//     });
//   }

//   fetch("/compare", {
//     method: "POST",
//     headers: {"Content-Type": "application/json"},
//     body: JSON.stringify({ processes })
//   })
//   .then(res => res.json())
//   .then(data => {
//     showComparisonChart(data);
//   });
// }

// function showComparisonChart(data) {
//   const ctx = document.getElementById("compareChart").getContext("2d");

//   // ✅ Clear old chart if exists
//   if (window.compareChartInstance) {
//     window.compareChartInstance.destroy();
//   }

//   window.compareChartInstance = new Chart(ctx, {
//     type: "bar",
//     data: {
//       labels: ["FCFS", "SJF", "PRIORITY", "RR"],
//       datasets: [
//         {
//           label: "Average Waiting Time",
//           data: [
//             data.FCFS.wt,
//             data.SJF.wt,
//             data.PRIORITY.wt,
//             data.RR.wt
//           ]
//         },
//         {
//           label: "Average Turnaround Time",
//           data: [
//             data.FCFS.tat,
//             data.SJF.tat,
//             data.PRIORITY.tat,
//             data.RR.tat
//           ]
//         }
//       ]
//     }
//   });
// }

let pid = 2;
let comparisonVisible = false;
let chartInstance = null;

function addRow() {
  const table = document.getElementById("processTable");
  const row = table.insertRow();
  row.innerHTML = `
    <td>${pid}</td>
    <td><input></td>
    <td><input></td>
    <td><input></td>
  `;
  pid++;
}

function runAlgorithm() {
  const algo = document.getElementById("algorithm").value;
  const quantum = document.getElementById("quantum").value || 2;

  const rows = document.querySelectorAll("#processTable tr");
  let processes = [];

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll("input");
    processes.push({
      pid: i,
      arrival: parseInt(cells[0].value || 0),
      burst: parseInt(cells[1].value || 1),
      priority: parseInt(cells[2].value || 0)
    });
  }

  fetch("/run", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({
      processes,
      algorithm: algo,
      quantum
    })
  })
  .then(res => res.json())
  .then(data => {
    drawGantt(data.gantt);

    document.getElementById("results").innerHTML =
      "Average Waiting Time: " + data.avg_wt.toFixed(2) +
      "<br>Average Turnaround Time: " + data.avg_tat.toFixed(2);

    // ✅ ✅ ✅ AUTO SCROLL TO GANTT SECTION
    document.getElementById("gantt").scrollIntoView({ behavior: "smooth" });
  });
}

/* ✅ ✅ ✅ ANIMATED COLORFUL GANTT */
function drawGantt(gantt) {
  const ganttDiv = document.getElementById("gantt");
  ganttDiv.innerHTML = "";

  gantt.forEach(block => {
    const div = document.createElement("div");
    div.className = `block p${block.pid}`;
    div.innerText = `P${block.pid} (${block.start} - ${block.end})`;
    ganttDiv.appendChild(div);
  });
}

/* ✅ ✅ ✅ TOGGLE ALGORITHM COMPARISON */
function compareAlgorithms() {
  const canvas = document.getElementById("compareChart");

  // ✅ TOGGLE CLOSE
  if (comparisonVisible) {
    canvas.style.display = "none";
    if (chartInstance) {
      chartInstance.destroy();
    }
    comparisonVisible = false;
    return;
  }

  const rows = document.querySelectorAll("#processTable tr");
  let processes = [];

  for (let i = 1; i < rows.length; i++) {
    const cells = rows[i].querySelectorAll("input");
    processes.push({
      pid: i,
      arrival: parseInt(cells[0].value || 0),
      burst: parseInt(cells[1].value || 1),
      priority: parseInt(cells[2].value || 0)
    });
  }

  fetch("/compare", {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ processes })
  })
  .then(res => res.json())
  .then(data => {
    showComparisonChart(data);
    canvas.style.display = "block";
    comparisonVisible = true;
    canvas.scrollIntoView({ behavior: "smooth" });
  });
}

function showComparisonChart(data) {
  const ctx = document.getElementById("compareChart").getContext("2d");

  if (chartInstance) {
    chartInstance.destroy();
  }

  chartInstance = new Chart(ctx, {
    type: "bar",
    data: {
      labels: ["FCFS", "SJF", "PRIORITY", "RR"],
      datasets: [
        {
          label: "Average Waiting Time",
          data: [
            data.FCFS.wt,
            data.SJF.wt,
            data.PRIORITY.wt,
            data.RR.wt
          ]
        },
        {
          label: "Average Turnaround Time",
          data: [
            data.FCFS.tat,
            data.SJF.tat,
            data.PRIORITY.tat,
            data.RR.tat
          ]
        }
      ]
    }
  });
}

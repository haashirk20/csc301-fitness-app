const input_Form = document.getElementById('woForm');
const work_dsp = document.getElementById('work_dsp');
const lift_dsp = document.getElementById('work_dsp2');
const errM = document.getElementById('errMessage');

const date = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'awake'];
const weeks = [];
const barColors = ["red", "orange","yellow", "green", "blue", "purple", "brown", "black"];
const barColors2 = "purple";
const yValues = [];
const yValues2 = [];

let w_chart = new Chart("weekChart", {
    type: "bar",
    data: {
      labels: date,
      datasets: [{
        backgroundColor: barColors,
        data: yValues
      }]
    },
    options: {
      title: {
        display: true,
        text: "Sleep hours per week"
      },
      responsive: true,
      interaction: {
        intersect: false,
      },
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      }
    }
});

let m_chart = new Chart("monthChart", {
    type: "bar",
    data: {
      labels: weeks,
      datasets: [{
        backgroundColor: barColors2,
        data: yValues2
      }]
    },
    options: {
      legend: {display: false}, 
      title: {
        display: true,
        text: "Sleep hours this month"
      },
      responsive: true,
      interaction: {
        intersect: false,
      },
      scales: {
        x: {
          stacked: true,
        },
        y: {
          stacked: true
        }
      }
    }
});

async function updateGraphs() {
  
  const week_data = await fetch('http://127.0.0.1:5000/api/workout/week', {
          method: 'GET',
    credentials: "include",
  });

  const result = await week_data.json();
  const w_workouts = JSON.parse(result["workouts"]);
  const w_total = JSON.parse(result["caloriesBurnedTotal"]);
  console.log(w_total)
  let weights = w_workouts.map((x) => x["tonsLifted"]);
  let calories = w_workouts.map((x) => x["caloriesBurned"]);


  w_chart.data = {
    labels: date,
    datasets: [
        {
            label: 'Tons Lifted',
            data: weights,
            backgroundColor: barColors[0],
            stack: 'Stack 0',
        },
        {
            label: 'Calories Burned',
            data: calories,
            backgroundColor: barColors[1],
            stack: 'Stack 1',
        }
    ]
  };
  w_chart.update();

  const month_data = await fetch('http://127.0.0.1:5000/api/workout/month', {
          method: 'GET',
    credentials: "include",
  });

  const m_result = await month_data.json();
  const m_workouts = JSON.parse(m_result["workouts"]);
  const month_weights = m_workouts.map((x) => x["tonsLifted"]);
  const month_calories = m_workouts.map((x) => x["caloriesBurned"]);
  const month = m_workouts.map((x) => x["date"]);
  console.log(m_result)

  m_chart.data = {
    labels: month,
    datasets: [
        {
            label: 'Tons Lifted',
            data: month_weights,
            backgroundColor: barColors[0],
            stack: 'Stack 0',
            id: "tons",
            label: "tons lifted",
            yAxisID:"right"
        },
        {
            label: 'Calories Burned',
            data: month_calories,
            backgroundColor: barColors[1],
            stack: 'Stack 1',
            id: "calories",
            label: "calories burned",
            yAxisID:"left"
        }
    ]
  };
  m_chart.options = {
    legend: {display: false}, 
    title: {
      display: true,
      text: "Sleep hours this month"
    },
    responsive: true,
    interaction: {
      intersect: false,
    },
    scales: {
      x: [{
        stacked: true,
      }],
      y: {
        stacked: true
      }
    }
  };
  m_chart.update();

}

async function updateWorkouts() {
  if (tody_dsp) {
  
    const today_data = await fetch('http://127.0.0.1:5000/api/workout/today', {
            method: 'GET',
			credentials: "include",
    });

    const result = await today_data.json();
    const cal = JSON.parse(result["caloriesBurned"]);
    const tons = JSON.parse(result["tonsLifted"]);

    if (cal && tons) {
        if (work_dsp.style.display === "none") {
            work_dsp.style.display = "block";
        }
        if (lift_dsp.style.display === "none") {
            lift_dsp.style.display = "block";
        }
        work_dsp.innerHTML = "Calories burned today: " + cal;
        lift_dsp.innerHTML = "Tons Lifted today: " + tons;
    }
    
  }
}

if (input_Form && errM) {
  input_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(input_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/workout', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(Object.fromEntries(formData)),
        credentials: "include",
      });
  
      const result = await response.json();
      const code = await response.status

      if (code == 200) {
          updateWorkouts();
          updateGraphs();

      } else {
          console.log(code)
          if (errM.style.display === "none") {
              errM.style.display = "block";
          }
          errM.innerHTML = "Error: " + result["message"];
          
      }
      
      
  });
}

updateGraphs();
updateWorkouts();
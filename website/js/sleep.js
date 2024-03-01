const input_Form = document.getElementById('stForm');
const goal_Form = document.getElementById('gForm');
const yest_dsp = document.getElementById('yest_dsp');
const tody_dsp = document.getElementById('tody_dsp');
const errM = document.getElementById('errMessage');

const date = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'awake'];
const weeks = [];
const barColors = ["red", "orange","yellow", "green", "blue", "purple", "brown", "black"];
const barColors2 = "purple";
const yValues = [];
const yValues2 = [];

let w_chart = new Chart("weekChart", {
    type: "pie",
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
      }
    }
});

async function updateGraphs() {
  
  const week_data = await fetch('http://127.0.0.1:5000/api/sleep/week', {
          method: 'GET',
    credentials: "include",
  });

  const result = await week_data.json();
  const w_hours = JSON.parse(result["sleep"]);
  const w_total = JSON.parse(result["hoursTotal"]);
  console.log(w_total)
  let hours = w_hours.map((x) => x["hours"]);
  hours.push(168 - w_total)

  console.log(hours)

  w_chart.data = {
    labels: date,
    datasets: [{ 
      data: hours,
      backgroundColor: barColors,
    }]
  };
  w_chart.update();

  const month_data = await fetch('http://127.0.0.1:5000/api/sleep/month', {
          method: 'GET',
    credentials: "include",
  });

  const m_result = await month_data.json();
  const m_sleep = JSON.parse(m_result["sleep"]);
  const month_sleep = m_sleep.map((x) => x["hours"]);
  const month = m_sleep.map((x) => x["date"]);
  console.log(m_result)

  m_chart.data = {
    labels: month,
    datasets: [{ 
      data: month_sleep,
      backgroundColor: barColors2,
    }]
  };
  m_chart.update();

}

async function updateYestHours() {
  if (yest_dsp) {
  
    const week_data = await fetch('http://127.0.0.1:5000/api/sleep/lastnight', {
            method: 'GET',
			credentials: "include",
    });

    const result = await week_data.json();
    const d_sleep = JSON.parse(result["hours"]);

    if (d_sleep) {
      if (yest_dsp.style.display === "none") {
        yest_dsp.style.display = "block";
    }
    yest_dsp.innerHTML = "Sleep hours yesterday: " + d_sleep;
    }
    
  }
}

async function updateGoals() {
  if (tody_dsp) {
  
    const week_data = await fetch('http://127.0.0.1:5000/api/sleep/goal', {
            method: 'GET',
			credentials: "include",
    });

    const result = await week_data.json();
    const d_sleep = JSON.parse(result["goal"]);

    if (d_sleep) {
      if (tody_dsp.style.display === "none") {
        tody_dsp.style.display = "block";
    }
    tody_dsp.innerHTML = "Sleep goal: " + d_sleep;
    }
    
  }
}

if (input_Form && errM) {
  input_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(input_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/sleep', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(Object.fromEntries(formData)),
        credentials: "include",
      });
  
      const result = await response.json();
      const code = await response.status

      if (code == 200) {
          updateYestHours();
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

if (goal_Form && errM) {
  goal_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(goal_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/sleep/goal', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(Object.fromEntries(formData)),
    credentials: "include",
      });
  
      const result = await response.json();
      const code = await response.status

      if (code == 200) {
          updateGoals()

      } else {
          console.log(code)
          if (errM.style.display === "none") {
              errM.style.display = "block";
          }
          errM.innerHTML = "Error: " + result["message"];
          
      }
      
      
  });
}

updateGoals();
updateGraphs();
updateYestHours();
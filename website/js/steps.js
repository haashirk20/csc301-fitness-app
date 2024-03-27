const days = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const steps = [];
const month = []
const month_steps = [];

const input_Form = document.getElementById('stForm');
const step_dsp = document.getElementById('step_dsp');
const errM = document.getElementById('errMessage');

step_dsp.style.display = "none";

let w_chart = new Chart("weekChart", {
  type: "line",
  data: {
    labels: days,
    datasets: [{ 
      data: steps,
      borderColor: "red",
      fill: false
    }]
  },
  options: {
    legend: {display: false}
  }
});

let m_chart = new Chart("monthChart", {
  type: "line",
  data: {
    labels: month,
    datasets: [{ 
      data: month_steps,
      borderColor: "red",
      fill: false
    }]
  },
  options: {
    legend: {display: false}
  }
});

async function updateGraphs() {
  
  const week_data = await fetch('http://127.0.0.1:5000/api/steps/week', {
          method: 'GET',
    credentials: "include",
  });

  const result = await week_data.json();
  const w_steps = JSON.parse(result["steps"]);
  const steps = w_steps.map((x) => x["steps"]);

  w_chart.data = {
    labels: days,
    datasets: [{ 
      data: steps,
      borderColor: "yellow",
      fill: false
    }]
  };
  w_chart.update();

  const month_data = await fetch('http://127.0.0.1:5000/api/steps/month', {
          method: 'GET',
    credentials: "include",
  });

  const m_result = await month_data.json();
  const m_steps = JSON.parse(m_result["steps"]);
  const month_steps = m_steps.map((x) => x["steps"]);
  const month = m_steps.map((x) => x["date"]);

  m_chart.data = {
    labels: month,
    datasets: [{ 
      data: month_steps,
      borderColor: "yellow",
      fill: false
    }]
  };
  m_chart.update();

}

async function updateCurrStep() {
  if (step_dsp) {
  
    const week_data = await fetch('http://127.0.0.1:5000/api/steps/today', {
            method: 'GET',
			credentials: "include",
    });

    const result = await week_data.json();
    const d_steps = JSON.parse(result["steps"]);

    if (d_steps) {
      if (step_dsp.style.display === "none") {
        step_dsp.style.display = "block";
    }
    step_dsp.innerHTML = "Steps today: " + d_steps;
    }
    
  }
}

if (input_Form && errM) {
  input_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(input_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/steps/add', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(Object.fromEntries(formData)),
    credentials: "include",
      });
  
      const result = await response.json();
      const code = await response.status

      if (code == 200) {
          updateCurrStep();
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
updateCurrStep();




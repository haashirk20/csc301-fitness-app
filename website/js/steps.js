const Steps = ["1/11","2/11","3/11","4/11","5/11","6/11","7/11","8/11","9/11","10/11"];
const date = [860,1140,1060,1060,null,1110,1330,2210,7830,2478];

const input_Form = document.getElementById('stForm');
const step_dsp = document.getElementById('step_dsp');

if (input_Form && step_dsp) {
    login_Form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(login_Form).entries()
        const response = await fetch('http://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData)),
			credentials: "include",
        });
    
        const result = await response.json();
        const code = await response.status

        if (code == 200) {
            window.location.replace("home.html");

        } else {
            console.log(code)
            if (errM.style.display === "none") {
                errM.style.display = "block";
            }
            errM.innerHTML = "Error: " + result["message"];
            
        }
    });
}

new Chart("stepsChart", {
    type: "line",
    data: {
      labels: Steps,
      datasets: [{ 
        data: date,
        borderColor: "red",
        fill: false
      }]
    },
    options: {
      legend: {display: false}
    }
  });
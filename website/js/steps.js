const date = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
const month =  ["2024-02-01",
                "2024-02-02",
                "2024-02-03",
                "2024-02-04",
                "2024-02-05",
                "2024-02-06",
                "2024-02-07",
                "2024-02-08",
                "2024-02-09",
                "2024-02-10",
                "2024-02-11",
                "2024-02-12",
                "2024-02-13",
                "2024-02-14",
                "2024-02-15",
                "2024-02-16",
                "2024-02-17",
                "2024-02-18",
                "2024-02-19",
                "2024-02-20",
                "2024-02-21",
                "2024-02-22",
                "2024-02-23",
                "2024-02-24",
                "2024-02-25",
                "2024-02-26",
                "2024-02-27",
                "2024-02-28",
                "2024-02-29"]
const steps = [1060,1121,1110,null,2210,3830,2478];
const month_steps = [3796,
                    3824,
                    3312,
                    2171,
                    3930,
                    2307,
                    3545,
                    1501,
                    3612,
                    3553,
                    3797,
                    2601,
                    2833,
                    1954,
                    2411,
                    null,
                    2140,
                    2597,
                    2325,
                    1846,
                    2359,
                    3295,
                    3840,
                    null,
                    2744,
                    1571,
                    2703,
                    1967,
                    2185,
                    3188];

const input_Form = document.getElementById('stForm');
const step_dsp = document.getElementById('step_dsp');

step_dsp.style.display = "none";


if (input_Form && step_dsp) {
    const week_data = await fetch('http:/127.0.0.1:5000/api/steps/week', {
            method: 'GET',
			credentials: "include",
    });

    const result = await week_data.json();
    const w_steps = await result["steps"]

    console.log(w_steps)
}

new Chart("weekChart", {
    type: "line",
    data: {
      labels: date,
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

new Chart("monthChart", {
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
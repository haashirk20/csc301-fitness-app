const bmi_Form = document.getElementById('bmiForm');

if (bmi_Form) {
  bmi_Form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(bmi_Form).entries()
    const response = await fetch('http://127.0.0.1:5000/api/bmi', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
      credentials: "include",
    });

    const result = await response.json();

    const responseCode = await response.status;

    const result_element = document.getElementById('result');
    if (responseCode == 401) {
      //user not signed in
      result_element.innerHTML = "Please sign in to use this service."
    } else if (responseCode == 400) {
      //missing data
      result_element.innerHTML = "Please enter a valid height and weight."
    } else if (responseCode == 200) {
      //success
      result_element.innerHTML = "Your BMI is: " + result["BMI"][0] + ".\n This is a " + result["BMI"][1] + " weight."
    }
  });
}

const calories_Form = document.getElementById('caloriesForm');

if (calories_Form) {
  calories_Form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(calories_Form).entries()
    const response = await fetch('http://127.0.0.1:5000/api/calories', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
      credentials: "include",
    });

    const result = await response.json();

    const responseCode = await response.status;

    const result_element = document.getElementById('calories_result');
    if (responseCode == 401) {
      //user not signed in
      result_element.innerHTML = "Please sign in to use this service."
    } else if (responseCode == 400) {
      //missing data
      if (result.message == "age invalid") {
        result_element.innerHTML = "Please enter a valid numeric age."
      } else if (result.message == "sex invalid") {
        result_element.innerHTML = "Please select a sex."
      } else if (result.message == "height missing") {
        result_element.innerHTML = "Please enter a valid numeric height in centimeters."
      } else if (result.message == "weight missing") {
        result_element.innerHTML = "Please enter a valid numeric weight in kilograms."
      } else if (result.message == "activity invalid") {
        result_element.innerHTML = "Please select an activity level."
      } else if (result.message == "goal invalid") {
        result_element.innerHTML = "Please select a weight goal."
      }

    } else if (responseCode == 200) {
      //success
      result_element.innerHTML = "Your recommended caloric intake is: " + result.caloriesNeeded + " calories."
    }
  });
}
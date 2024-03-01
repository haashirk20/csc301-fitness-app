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
      result_element.innerHTML = "Your recommended caloric intake is: " + result.caloriesNeeded + " calories per day."
    }
  });
}

const food_Form = document.getElementById('foodForm');

if (food_Form) {
  food_Form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(food_Form).entries()
    const response = await fetch('http://127.0.0.1:5000/api/calories/food', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
      credentials: "include",
    });

    const result = await response.json();

    const responseCode = await response.status;

    const result_element = document.getElementById('food_result');
    if (responseCode == 401) {
      //user not signed in
      result_element.innerHTML = "Please sign in to use this service."
    } else if (responseCode == 400) {
      //missing data
      if (result.message == "food not found") {
        result_element.innerHTML = "Please enter a recognized food dish."
      } else {
        result_element.innerHTML = "An unknown error occurred."
      }

    } else if (responseCode == 200) {
      //success
      result_element.innerHTML = "One serving contains " + result.calories + " calories."
    }
  });
}

const goal_Form = document.getElementById('goalForm');

if (goal_Form) {
    goal_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(goal_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/calories/limit', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(formData)),
        credentials: "include",
      });
  
      const result = await response.json();
  
      const responseCode = await response.status;
  
      const result_element = document.getElementById('goal_result');
      if (responseCode == 401) {
        //user not signed in
        result_element.innerHTML = "Please sign in to use this service."
      } else if (responseCode == 400) {
        //missing data
        if (result.message == "calories invalid") {
          result_element.innerHTML = "Please enter a numeric amount of calories."
        } else {
          result_element.innerHTML = "An unknown error occurred."
        }
  
      } else if (responseCode == 200) {
        //success
        result_element.innerHTML = "Calorie limit updated. Calories remaining today: " + result.caloriesNeeded + " calories."
      }
    });
  }

const reset_Form = document.getElementById('resetForm');

if (reset_Form) {
    reset_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(reset_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/calories/reset', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' },
        credentials: "include",
      });
  
      const result = await response.json();
  
      const responseCode = await response.status;
  
      const result_element = document.getElementById('tracker_result');
      if (responseCode == 401) {
        //user not signed in
        result_element.innerHTML = "Please sign in to use this service."
      } else if (responseCode >= 400) {
        //missing data
        result_element.innerHTML = "An unknown error occurred."
  
      } else if (responseCode == 200) {
        //success
        result_element.innerHTML = "Daily calories reset. Calories remaining today: " + result.caloriesRemaining + " calories."
      }
    });
  }

const tracker_Form = document.getElementById('trackerForm');

if (tracker_Form) {
    tracker_Form.addEventListener('submit', async function (e) {
      e.preventDefault();
      const formData = new FormData(tracker_Form).entries()
      const response = await fetch('http://127.0.0.1:5000/api/calories/reduce', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(Object.fromEntries(formData)),
        credentials: "include",
      });
  
      const result = await response.json();
  
      const responseCode = await response.status;
  
      const result_element = document.getElementById('tracker_result');
      if (responseCode == 401) {
        //user not signed in
        result_element.innerHTML = "Please sign in to use this service."
      } else if (responseCode == 400) {
        //missing data
        if (result.message == "calories invalid") {
          result_element.innerHTML = "Please enter a numeric amount of calories."
        } else {
          result_element.innerHTML = "An unknown error occurred."
        }
  
      } else if (responseCode == 200) {
        //success
        result_element.innerHTML = "Calories submitted. Calories remaining today: " + result.caloriesRemaining + " calories."
      }
    });
  }
const profile_Form = document.getElementById('profileForm');

if (profile_Form) {
  profile_Form.addEventListener('submit', async function (e) {
    e.preventDefault();
    const formData = new FormData(profile_Form).entries()
    const response = await fetch('http://127.0.0.1:5000/api/profile', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
      credentials: "include",
    });

    const result = await response.json();

    const responseCode = await response.status;

    const result_element = document.getElementById('profile_result');
    if (responseCode == 401) {
      //user not signed in
      result_element.innerHTML = "Please sign in to use this service."
    } else if (responseCode == 200) {
      //success
      result_element.innerHTML = "Updating profile information..."
      location.reload()
    }
  });
}

const username = document.getElementById('username');
const useremail = document.getElementById('useremail');
const userage = document.getElementById('userage');

if (username && useremail && userage) {
    const result_element = document.getElementById("profile_result")

    const xhr = new XMLHttpRequest();
    xhr.withCredentials = true;
    xhr.open("GET", "http://127.0.0.1:5000/api/profile");
    xhr.send();
    xhr.responseType = "json";
    xhr.onload = () => {
    if (xhr.readyState == 4 && xhr.status == 200) {
        const result = xhr.response;
        username.innerHTML = "Username: " + result.name;
        useremail.innerHTML = "Email: " + result.email;
        userage.innerHTML = "Age: " + result.age;
    } else {
        result_element.innerHTML = "Error loading account data: " + xhr.response.message
    }
    };
}



const notiForm = document.getElementById("notiForm");

if (notiForm) {
  notiForm.addEventListener("submit", async function (e) {
    e.preventDefault();
    const formData = new FormData(notiForm).entries();
    const data = Object.fromEntries(formData);

    const response = await fetch("http://127.0.0.1:5000/api/notifications", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
      credentials: "include",
    });

    const result = await response.json();
    const responsecode = response.status;

    const result_element = document.getElementById("noti_result");
    if (responsecode == 401) {
      result_element.innerHTML = "Please sign in to use this service.";
      location.href("/login.html");
    } else if (responsecode == 200) {
      result_element.innerHTML = "New notification time: " + result.time;
      document.getElementById("currTime").innerHTML = result.time;
      document.getElementById("notiForm").reset();
    }
  });
}

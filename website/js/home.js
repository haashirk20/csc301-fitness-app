setTimeout(() => {
  fetch("http://127.0.0.1:5000/api/workout/today/", {
    method: "GET",
    headers: { "Content-Type": "application/json" },
    credentials: "include",
  })
    .then((response) => {
      if (response.status === 401) {
        window.location.href = "/login.html";
      } else {
        // Handle the successful response here
      }
    })
    .catch((error) => {
      // Handle any errors that occur during the request
      console.error("Error:", error);
    });
}, 1000);

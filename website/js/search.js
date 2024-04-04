const search_Form = document.getElementById('searchForm');
const main = document.getElementById("search-results-holder");

if (search_Form) {
  search_Form.addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const formData = new FormData(search_Form).entries()
    const response = await fetch('http://127.0.0.1:5000/api/search', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(Object.fromEntries(formData)),
      credentials: "include",
    });

    const result = await response.json();

    const responseCode = await response.status;

    main.innerHTML = "";

    const result_element = document.getElementById('search_result');
    if (responseCode == 401) {
      //user not signed in
      result_element.innerHTML = "Please sign in to use this service."
    } else if (responseCode == 404) {
      //missing data
      if (result.message == "no results found") {
        result_element.innerHTML = "Found 0 users that match your query."
      } else {
        result_element.innerHTML = "An unknown error occurred."
      } 

    } else if (responseCode == 200) {
      //success
      result_element.innerHTML = "Found " + result.results[0].length + " users that match your query."

      var user;
      var text;
      var tag;
      for (i=0; i<result.results[0].length; i++) {
        user = document.createElement("div")
        user.classList.add("graph-container");

        //username
        tag = document.createElement("h2");
        user.appendChild(tag);
        text = document.createTextNode(result.results[0][i])
        tag.appendChild(text);

        //age
        tag = document.createElement("p");
        user.appendChild(tag);
        text = document.createTextNode(result.results[1][i] + "yo")
        tag.appendChild(text);

        //email
        // tag = document.createElement("p");
        // user.appendChild(tag);
        // text = document.createTextNode(result.results[2][i])
        // tag.appendChild(text);

        //calorie goal
        tag = document.createElement("p");
        user.appendChild(tag);
        text = document.createTextNode("Calorie goal: " + result.results[3][i] + "calories/day.")
        tag.appendChild(text);

        //sleep goal
        tag = document.createElement("p");
        user.appendChild(tag);
        text = document.createTextNode("Sleep goal: " + result.results[4][i] + " hours/night.")
        tag.appendChild(text);

        main.appendChild(user);
      }
    }
  });
}
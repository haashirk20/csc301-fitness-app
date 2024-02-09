const signup_Form = document.getElementById('suForm');
const errM = document.getElementById('errMessage');

if (signup_Form && errM) {
    signup_Form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(signup_Form).entries()
        const response = await fetch('http://127.0.0.1:5000/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData)),
			credentials: include,
        });
    
        const result = await response.json();
        const code = await response.status

        if (code == 200) {
            window.location.replace("login.html");

        } else {
            console.log(code)
            if (errM.style.display === "none") {
                errM.style.display = "block";
            }
            errM.innerHTML = "Error: " + result["message"];
            
        }
        
        
    });
}

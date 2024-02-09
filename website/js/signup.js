const signup_Form = document.getElementById('suForm');

if (signup_Form) {
    signup_Form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(signup_Form).entries()
        const response = await fetch('https://127.0.0.1:5000/api/signup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData))
        });
    
        const result = await response.json();
        console.log(result)
    });
}

const login_Form = document.getElementById('liForm');

if (login_Form) {
    login_Form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(login_Form).entries()
        const response = await fetch('https://127.0.0.1:5000/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData))
        });
    
        const result = await response.json();
        console.log(result)
    });
}
const bmi_Form = document.getElementById('bmiForm');

if (bmi_Form) {
    bmi_Form.addEventListener('submit', async function (e) {
        e.preventDefault();
        const formData = new FormData(bmi_Form).entries()
        const response = await fetch('http://127.0.0.1:5000/api/bmi', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(Object.fromEntries(formData))
        });
    
        const result = await response.json();
        console.log(result)
    });
}
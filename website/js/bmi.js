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
        
		const responseCode = result["code"];
		
		const result_element = document.getELementById('result');
		if (responseCode == 401) {
			//user not signed in
			result_element.innerHTML = "Please sign in to use this service."
		} else if (responseCode == 400) {
			//missing data
			result_element.innerHTML = "Please enter a valid height and weight."
		} else if (responseCode == 200) {
			//success
			result_element.innerHTML = "Your BMI is: " + responseCode["BMI"][0] + ".\n This is a " + responseCode["BMI"][1] + " weight."
		}
    });
}
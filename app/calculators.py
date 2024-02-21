def BMICalculator(weight, height):
    # height stored in cm, weight in kg
    height /= 100
    bmi = round(weight / height**2, 2)
    if bmi < 18.5:
        return bmi, "Underweight"
    elif 18.5 <= bmi < 25:
        return bmi, "Healthy weight"
    elif 25 <= bmi < 30:
        return bmi, "Overweight"
    else:
        return bmi, "Obesity"


def RFMCalculator(sex, height, waist_circumfrence):
    # height stored in cm, waist_circumfrence stored in cm
    if sex == "male":
        rfm = round(64 - 20 * (height / waist_circumfrence), 2)
        if rfm < 2:
            return rfm, "Extremely low level of fat"
        elif 2 <= rfm < 6:
            return rfm, "Essential fat"
        elif 6 <= rfm < 14:
            return rfm, "Athletes"
        elif 14 <= rfm < 18:
            return rfm, "Fitness"
        elif 18 <= rfm < 25:
            return rfm, "Average"
        else:
            return "Obese"
    elif sex == "female":
        rfm = round(76 - 20 * (height / waist_circumfrence), 2)
        if rfm < 10:
            return rfm, "Extremely low level of fat"
        elif 10 <= rfm < 14:
            return rfm, "Essential fat"
        elif 14 <= rfm < 21:
            return rfm, "Athletes"
        elif 21 <= rfm < 25:
            return rfm, "Fitness"
        elif 25 <= rfm < 32:
            return rfm, "Average"
        else:
            return rfm, "Obese"
    else:
        # not sure what to do for this case. Can use default as male or female instead maybe.
        return "No RFM available"

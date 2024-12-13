# Validate Indian phone numbers and count valid numbers
def is_valid_phone_number(phone_number):
    if not phone_number or not isinstance(phone_number, str):
        return False
    # Remove leading spaces and check prefixes '+91' or '91' or plain 10 digits
    if phone_number.startswith('+91'):
        number = phone_number[3:]
    elif phone_number.startswith('91'):
        number = phone_number[2:]
    else:
        number = phone_number
    
    # Check if the remaining part is a 10-digit number within valid range
    return number.isdigit() and 6000000000 <= int(number) <= 9999999999

# Add the column isValidMobile
phone_numbers = [entry.get('phoneNumber') for entry in data]
is_valid_mobile = [is_valid_phone_number(num) for num in phone_numbers]
valid_mobile_count = sum(is_valid_mobile)

# Calculate Pearson correlation between prescribed medicines and patient age
import numpy as np

# Extract the number of medicines prescribed for each patient
medicines_count = [len(entry.get('consultationData', {}).get('medicines', [])) for entry in data]

# Calculate patient ages
patient_ages = []
for patient in patient_details:
    birth_date = patient.get('birthDate')
    if birth_date:
        age = datetime.now().year - datetime.fromisoformat(birth_date).year
        patient_ages.append(age)
    else:
        patient_ages.append(None)

# Filter out None values for correlation calculation
filtered_data = [(m_count, age) for m_count, age in zip(medicines_count, patient_ages) if age is not None]
filtered_medicines_count, filtered_patient_ages = zip(*filtered_data)

# Calculate Pearson correlation
pearson_correlation = round(np.corrcoef(filtered_medicines_count, filtered_patient_ages)[0, 1], 2)

# Results
valid_mobile_count, pearson_correlation

import json
from collections import Counter
from datetime import datetime

# Load the data from the provided JSON file
file_path = '/mnt/data/DataEngineeringQ2.json'
with open(file_path, 'r') as f:
    data = json.load(f)

# Extract relevant information for calculations
patient_details = [entry['patientDetails'] for entry in data]
medicines = [med for entry in data for med in entry.get('consultationData', {}).get('medicines', [])]

# Calculate missing percentages for firstName, lastName, and DOB
def calculate_missing_percentage(field_name):
    total = len(patient_details)
    missing = sum(1 for patient in patient_details if not patient.get(field_name) or patient[field_name] in ["", None])
    return round((missing / total) * 100, 2)

first_name_missing = calculate_missing_percentage('firstName')
last_name_missing = calculate_missing_percentage('lastName')
dob_missing = calculate_missing_percentage('birthDate')

# Calculate percentage of female gender after imputation using mode
genders = [patient.get('gender') for patient in patient_details if patient.get('gender')]
mode_gender = Counter(genders).most_common(1)[0][0]
imputed_genders = [patient.get('gender', mode_gender) for patient in patient_details]
female_percentage = round((imputed_genders.count('F') / len(imputed_genders)) * 100, 2)

# Add age group and count Adults
def calculate_age_group(birth_date):
    if not birth_date:
        return None
    age = datetime.now().year - datetime.fromisoformat(birth_date).year
    if age <= 12:
        return 'Child'
    elif 13 <= age <= 19:
        return 'Teen'
    elif 20 <= age <= 59:
        return 'Adult'
    else:
        return 'Senior'

age_groups = [calculate_age_group(patient.get('birthDate')) for patient in patient_details]
adult_count = age_groups.count('Adult')

# Calculate average number of medicines prescribed
average_medicines = round(sum(1 for med in medicines) / len(data), 2)

# Determine the 3rd most frequently prescribed medicine
medicine_names = [med['medicineName'] for med in medicines]
third_most_common = Counter(medicine_names).most_common(3)[2][0]

# Calculate percentage distribution of active and inactive medicines
active_medicines = sum(1 for med in medicines if med.get('isActive'))
inactive_medicines = sum(1 for med in medicines if not med.get('isActive'))
total_medicines = active_medicines + inactive_medicines
active_percentage = round((active_medicines / total_medicines) * 100, 2)
inactive_percentage = round((inactive_medicines / total_medicines) * 100, 2)

# Results
(first_name_missing, last_name_missing, dob_missing, 
 female_percentage, adult_count, average_medicines, 
 third_most_common, active_percentage, inactive_percentage)

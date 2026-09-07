
#smart care: Community Clinic appointment booking system (made by the student)

appointments = []

def is_slot_available(practitioner_name, appointment_time):
    """Check if practioner is free at the given appointment time."""
    for appointment in appointments:
        if appointment['practitioner_name'] == practitioner_name and appointment['appointment_time'] == appointment_time:
            return False
    return True

def book_appointment(patient_name, practitioner_name, appointment_time):
    if not patient_name:
        print ("Error : Patient name cannot be empty.")
        return

    if not practitioner_name:
        print ("Error : Practitioner name cannot be empty.")
        return

    if not appointment_time:
        print ("Error : Appointment time cannot be empty.")
        return

    if is_slot_available(practitioner_name, appointment_time):
        appointments.append({
            'patient_name': patient_name,
            'practitioner_name': practitioner_name,
            'appointment_time': appointment_time
        })
        print("Appointment booked successfully.")
    else:
        print("Sorry, the slot is not available.")

def cancel_appointment(patient_name, practitioner_name, appointment_time):
    for appointment in appointments:
        if (appointment['patient_name'] == patient_name and
            appointment['practitioner_name'] == practitioner_name and
            appointment['appointment_time'] == appointment_time):
            appointments.remove(appointment)
            print(f"Appointment canceled successfully for {patient_name} with {practitioner_name} at {appointment_time}.")
            return
    print(f"No matching appointment found to cancel for {patient_name} with {practitioner_name} at {appointment_time}.")

def find_appointments_by_patient(patient_name):
    matches = [appointment for appointment in appointments if appointment['patient_name'] == patient_name]
    if matches:
        print(f"Appointments for {patient_name}:")
        for appointment in matches:
            print(f"Practitioner: {appointment['practitioner_name']}, Time: {appointment['appointment_time']}")
    else:
        print(f"No appointments found for {patient_name}.")

def find_patient_appointments(patient_name):
    matches = [appointment for appointment in appointments if appointment['patient_name'] == patient_name]
    if matches:
        print(f"Appointments for {patient_name}:")
        for appointment in matches:
            print(f"Practitioner: {appointment['practitioner_name']}, Time: {appointment['appointment_time']}")
    else:
        print(f"No appointments found for {patient_name}.")

def display_appointments():
    if appointments:
        print("All Appointments:")
        for appointment in appointments:
            print(f"Patient: {appointment['patient_name']}, Practitioner: {appointment['practitioner_name']}, Time: {appointment['appointment_time']}")
    else:
        print("No appointments scheduled.")

print("Welcome to the Community Clinic Appointment Booking System")

book_appointment("John Doe", "Dr. Smith", "2024-06-15 10:00 am")
book_appointment("Jane Doe", "Dr. Smith", "2024-06-15 10:00 am")
book_appointment("Alice Johnson", "Dr. Brown", "2024-06-15 11:00 am")

print("\nFinding appointments for John Doe:")
find_appointments_by_patient("John Doe")

print("\n full schedule of appointments:")
display_appointments()

print("\nCanceling appointment for John Doe with Dr. Smith at 2024-06-15 10:00 am:")
cancel_appointment("John Doe", "Dr. Smith", "2024-06-15 10:00 am")

print("\n full schedule of appointments after cancellation:")
display_appointments()
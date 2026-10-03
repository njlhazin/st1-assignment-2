"""
SmartCare system - a simple appointment booking system.
Domain classes for a simple appointment booking system:

    Patient      - a person who books appointments
    Practitioner - a health professional who has available time slots
    Appointment  - links ONE patient to ONE practitioner at a date/time
"""

# Imports
from datetime import date, time, timedelta  # date/time types + date maths for the demo
from enum import Enum                       # lets us define a fixed set of statuses
from typing import Optional                 # type hint for "this value may be None"


# APPOINTMENT STATUS

class AppointmentStatus(Enum):
    SCHEDULED = "Scheduled"   # booked and still to happen
    COMPLETED = "Completed"   # the visit took place
    CANCELLED = "Cancelled"   # the booking was cancelled



# PATIENT CLASS


class Patient:
    """Stores and validates patient information."""

    def __init__(self, patient_id: str, name: str,
                 date_of_birth: date, contact_details: str):
        """Create a patient. Rejects empty text fields and future birth dates."""

        # .strip() removes spaces, so "   " counts as empty too.
        if not patient_id.strip():
            raise ValueError("Patient ID cannot be empty.")
        if not name.strip():
            raise ValueError("Patient name cannot be empty.")

        
        if date_of_birth > date.today():
            raise ValueError("Date of birth cannot be in the future.")
        if not contact_details.strip():
            raise ValueError("Contact details cannot be empty.")

        # Only reached if every check above passed, so stored data is always valid.
        self.patient_id = patient_id
        self.name = name
        self.date_of_birth = date_of_birth
        self.contact_details = contact_details

    def register(self):
        """UML operation register().
        """
        return self

    def update_details(self,
                       name: Optional[str] = None,
                       date_of_birth: Optional[date] = None,
                       contact_details: Optional[str] = None):
       
        if name is not None:
            if not name.strip():
                raise ValueError("Patient name cannot be empty.")
            self.name = name

        if date_of_birth is not None:
            if date_of_birth > date.today():
                raise ValueError("Invalid date of birth.")
            self.date_of_birth = date_of_birth

        if contact_details is not None:
            if not contact_details.strip():
                raise ValueError("Contact details cannot be empty.")
            self.contact_details = contact_details

    def get_details(self):
        return {
            "patient_id": self.patient_id,
            "name": self.name,
            "date_of_birth": self.date_of_birth,
            "contact_details": self.contact_details,
        }



# PRACTITIONER CLASS

class Practitioner:

    def __init__(self, practitioner_id: str, name: str,
                 specialty: str, availability: Optional[set] = None):
        """Create a practitioner. Availability is optional (starts empty)."""
        if not practitioner_id.strip():
            raise ValueError("Practitioner ID cannot be empty.")
        if not name.strip():
            raise ValueError("Practitioner name cannot be empty.")
        if not specialty.strip():
            raise ValueError("Specialty cannot be empty.")

        self.practitioner_id = practitioner_id
        self.name = name
        self.specialty = specialty

        self.availability = set(availability or [])

    def add_availability(self, appointment_date: date,
                         appointment_time: time):
        """Add one bookable slot. Slots in the past are rejected."""
        if appointment_date < date.today():
            raise ValueError("Availability cannot be in the past.")
        self.availability.add((appointment_date, appointment_time))

    def update_details(self, name: Optional[str] = None,
                       specialty: Optional[str] = None):
        if name is not None:
            if not name.strip():
                raise ValueError("Practitioner name cannot be empty.")
            self.name = name

        if specialty is not None:
            if not specialty.strip():
                raise ValueError("Specialty cannot be empty.")
            self.specialty = specialty

    def check_availability(self, appointment_date: date,
                           appointment_time: time) -> bool:
        return (appointment_date, appointment_time) in self.availability

    def get_details(self):
        return {
            "practitioner_id": self.practitioner_id,
            "name": self.name,
            "specialty": self.specialty,
            "availability": self.availability,
        }

# APPOINTMENT CLASS

class Appointment:

    def __init__(self, appointment_id: str, appointment_date: date,
                 appointment_time: time, patient: Patient,
                 practitioner: Practitioner,
                 status: AppointmentStatus = AppointmentStatus.SCHEDULED):

        if not appointment_id.strip():
            raise ValueError("Appointment ID cannot be empty.")
        if appointment_date < date.today():
            raise ValueError("Appointment cannot be in the past.")
        if not isinstance(patient, Patient):
            raise TypeError("A valid Patient object is required.")
        if not isinstance(practitioner, Practitioner):
            raise TypeError("A valid Practitioner object is required.")
        if not isinstance(status, AppointmentStatus):
            raise ValueError("Invalid appointment status.")

        self.appointment_id = appointment_id
        self.date = appointment_date
        self.time = appointment_time
        self.patient = patient            
        self.practitioner = practitioner  
        self._status = status

    @property
    def status(self) -> AppointmentStatus:
        return self._status

    def check_conflict(self, appointments) -> bool:
        for other in appointments:
            # Skip itself, otherwise an appointment would "conflict" with
            # itself (important when rescheduling).
            if other.appointment_id == self.appointment_id:
                continue

            if (other.practitioner.practitioner_id
                    == self.practitioner.practitioner_id
                    and other.date == self.date
                    and other.time == self.time
                    # Cancelled/completed appointments do not block the slot.
                    and other.status == AppointmentStatus.SCHEDULED):
                return True
        return False

    def create(self, appointments):
        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError("A new appointment must be scheduled.")
        if not self.practitioner.check_availability(self.date, self.time):
            raise ValueError("Practitioner is not available at this time.")
        if self.check_conflict(appointments):
            raise ValueError(
                "Practitioner already has an appointment at this time.")
        return self

    def reschedule(self, new_date: date, new_time: time, appointments):
        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled appointments can be rescheduled.")
        if new_date < date.today():
            raise ValueError(
                "Appointment cannot be rescheduled to the past.")
        if not self.practitioner.check_availability(new_date, new_time):
            raise ValueError(
                "Practitioner is not available at the new time.")

        old_date, old_time = self.date, self.time

        # Temporarily apply the new slot so check_conflict() tests IT.
        self.date, self.time = new_date, new_time

        if self.check_conflict(appointments):
            self.date, self.time = old_date, old_time
            raise ValueError(
                "Another appointment already exists at the new time.")

    def cancel(self):
        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled appointments can be cancelled.")
        self._status = AppointmentStatus.CANCELLED

    def update_status(self, new_status: AppointmentStatus):
        if not isinstance(new_status, AppointmentStatus):
            raise ValueError("Invalid appointment status.")
        if self.status != AppointmentStatus.SCHEDULED:
            raise ValueError(
                "Only scheduled appointments can change status.")
        if new_status not in (AppointmentStatus.COMPLETED,
                              AppointmentStatus.CANCELLED):
            raise ValueError("Invalid status transition.")

        self._status = new_status

    def view_details(self):
        return {
            "appointment_id": self.appointment_id,
            "date": self.date,
            "time": self.time,
            "status": self.status.value,        # "Scheduled", not the Enum object
            "patient": self.patient.name,
            "practitioner": self.practitioner.name,
        }


if __name__ == "__main__":
    # create a patient and a practitioner.
    patient1 = Patient("P001", "Alex Smith", date(2000, 5, 15), "0400000000")
    practitioner1 = Practitioner("PR001", "Dr Taylor", "General Practice")

    # give the practitioner a slot one week from today.
    appt_date = date.today() + timedelta(days=7)
    appt_time = time(10, 0)
    practitioner1.add_availability(appt_date, appt_time)

    # build the appointment object.
    appointment1 = Appointment("A001", appt_date, appt_time,
                               patient1, practitioner1)

    # validate it, then store it in a simple in-memory list.
    appointments = []
    appointment1.create(appointments)
    appointments.append(appointment1)

    print("Appointment created:")
    print(appointment1.view_details())

    #cancel it and show the new status.
    appointment1.cancel()
    print("\nAfter cancellation:")
    print(appointment1.view_details())

    #cancelling again must fail; we catch the error and print it.
    try:
        appointment1.cancel()
    except ValueError as error:
        print("\nInvalid action:", error)
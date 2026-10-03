import unittest #Ai generated code to test the classes in smartcare.py
from datetime import date, time, timedelta

from smartcare import (
    Appointment, AppointmentStatus, Patient, Practitioner,
)

FUTURE = date.today() + timedelta(days=7)
FUTURE2 = date.today() + timedelta(days=8)
T10 = time(10, 0)
T11 = time(11, 0)


def make_patient(pid="P001"):
    return Patient(pid, "Alex Smith", date(2000, 5, 15), "0400000000")


def make_practitioner(pid="PR001"):
    p = Practitioner(pid, "Dr Taylor", "General Practice")
    p.add_availability(FUTURE, T10)
    p.add_availability(FUTURE, T11)
    p.add_availability(FUTURE2, T10)
    return p


def make_appt(aid="A001", d=FUTURE, t=T10, patient=None, prac=None):
    return Appointment(aid, d, t, patient or make_patient(),
                       prac or make_practitioner())


class TestPatient(unittest.TestCase):
    def test_valid_patient(self):
        self.assertEqual(make_patient().get_details()["name"], "Alex Smith")

    def test_empty_fields_rejected(self):
        with self.assertRaises(ValueError):
            Patient("", "A", date(2000, 1, 1), "x")
        with self.assertRaises(ValueError):
            Patient("P1", " ", date(2000, 1, 1), "x")
        with self.assertRaises(ValueError):
            Patient("P1", "A", date(2000, 1, 1), "")

    def test_future_dob_rejected(self):
        with self.assertRaises(ValueError):
            Patient("P1", "A", FUTURE, "x")

    def test_update_details(self):
        p = make_patient()
        p.update_details(name="Sam Lee", contact_details="0411111111")
        self.assertEqual(p.name, "Sam Lee")
        self.assertEqual(p.contact_details, "0411111111")

    def test_update_invalid_rejected(self):
        p = make_patient()
        with self.assertRaises(ValueError):
            p.update_details(name="")
        with self.assertRaises(ValueError):
            p.update_details(date_of_birth=FUTURE)
        self.assertEqual(p.name, "Alex Smith")


class TestPractitioner(unittest.TestCase):
    def test_empty_fields_rejected(self):
        with self.assertRaises(ValueError):
            Practitioner("", "Dr", "GP")
        with self.assertRaises(ValueError):
            Practitioner("PR1", "", "GP")
        with self.assertRaises(ValueError):
            Practitioner("PR1", "Dr", "")

    def test_availability(self):
        p = make_practitioner()
        self.assertTrue(p.check_availability(FUTURE, T10))
        self.assertFalse(p.check_availability(FUTURE, time(15, 0)))

    def test_past_availability_rejected(self):
        p = make_practitioner()
        with self.assertRaises(ValueError):
            p.add_availability(date.today() - timedelta(days=1), T10)

    def test_update_details(self):
        p = make_practitioner()
        p.update_details(specialty="Cardiology")
        self.assertEqual(p.specialty, "Cardiology")
        with self.assertRaises(ValueError):
            p.update_details(name="  ")


class TestAppointment(unittest.TestCase):
    def test_create_valid(self):
        a = make_appt()
        self.assertIs(a.create([]), a)
        self.assertEqual(a.status, AppointmentStatus.SCHEDULED)

    def test_invalid_inputs(self):
        with self.assertRaises(ValueError):
            Appointment("", FUTURE, T10, make_patient(),
                        make_practitioner())
        with self.assertRaises(ValueError):
            Appointment("A1", date.today() - timedelta(days=1), T10,
                        make_patient(), make_practitioner())
        with self.assertRaises(TypeError):
            Appointment("A1", FUTURE, T10, "not a patient",
                        make_practitioner())
        with self.assertRaises(TypeError):
            Appointment("A1", FUTURE, T10, make_patient(), "not a prac")

    def test_unavailable_slot_rejected(self):
        a = make_appt(t=time(15, 0))
        with self.assertRaises(ValueError):
            a.create([])

    def test_conflict_detected(self):
        prac = make_practitioner()
        first = make_appt("A001", prac=prac)
        first.create([])
        second = make_appt("A002", patient=make_patient("P002"), prac=prac)
        self.assertTrue(second.check_conflict([first]))
        with self.assertRaises(ValueError):
            second.create([first])

    def test_no_conflict_for_different_practitioner(self):
        first = make_appt("A001", prac=make_practitioner("PR001"))
        second = make_appt("A002", prac=make_practitioner("PR002"))
        self.assertFalse(second.check_conflict([first]))

    def test_cancelled_appointment_frees_slot(self):
        prac = make_practitioner()
        first = make_appt("A001", prac=prac)
        first.cancel()
        second = make_appt("A002", prac=prac)
        self.assertFalse(second.check_conflict([first]))

    def test_cancel_and_repeat_cancel(self):
        a = make_appt()
        a.cancel()
        self.assertEqual(a.status, AppointmentStatus.CANCELLED)
        with self.assertRaises(ValueError):
            a.cancel()

    def test_status_is_read_only(self):
        a = make_appt()
        with self.assertRaises(AttributeError):
            a.status = AppointmentStatus.COMPLETED

    def test_update_status(self):
        a = make_appt()
        a.update_status(AppointmentStatus.COMPLETED)
        self.assertEqual(a.status, AppointmentStatus.COMPLETED)
        with self.assertRaises(ValueError):
            a.update_status(AppointmentStatus.CANCELLED)

    def test_update_status_invalid(self):
        a = make_appt()
        with self.assertRaises(ValueError):
            a.update_status("Completed")
        with self.assertRaises(ValueError):
            a.update_status(AppointmentStatus.SCHEDULED)

    def test_reschedule_success(self):
        a = make_appt()
        a.reschedule(FUTURE, T11, [a])
        self.assertEqual(a.time, T11)

    def test_reschedule_unavailable_keeps_original(self):
        a = make_appt()
        with self.assertRaises(ValueError):
            a.reschedule(FUTURE, time(15, 0), [a])
        self.assertEqual(a.time, T10)

    def test_reschedule_conflict_rolls_back(self):
        prac = make_practitioner()
        first = make_appt("A001", t=T10, prac=prac)
        second = make_appt("A002", t=T11, patient=make_patient("P002"),
                           prac=prac)
        with self.assertRaises(ValueError):
            second.reschedule(FUTURE, T10, [first, second])
        self.assertEqual(second.time, T11)

    def test_reschedule_past_or_cancelled_rejected(self):
        a = make_appt()
        with self.assertRaises(ValueError):
            a.reschedule(date.today() - timedelta(days=1), T10, [a])
        a.cancel()
        with self.assertRaises(ValueError):
            a.reschedule(FUTURE2, T10, [a])

    def test_view_details(self):
        d = make_appt().view_details()
        self.assertEqual(d["status"], "Scheduled")
        self.assertEqual(d["patient"], "Alex Smith")
        self.assertEqual(d["practitioner"], "Dr Taylor")


class TestTypeValidation(unittest.TestCase):
    """Wrong types must give a clear TypeError, not an AttributeError."""

    def test_patient_non_text_rejected(self):
        with self.assertRaises(TypeError):
            Patient(123, "A", date(2000, 1, 1), "x")
        with self.assertRaises(TypeError):
            Patient("P1", None, date(2000, 1, 1), "x")
        with self.assertRaises(TypeError):
            Patient("P1", "A", date(2000, 1, 1), 400000000)

    def test_practitioner_non_text_rejected(self):
        with self.assertRaises(TypeError):
            Practitioner("PR1", "Dr", 5)
        with self.assertRaises(TypeError):
            Practitioner(None, "Dr", "GP")

    def test_appointment_id_non_text_rejected(self):
        with self.assertRaises(TypeError):
            Appointment(42, FUTURE, T10, make_patient(),
                        make_practitioner())

    def test_update_non_text_rejected_and_unchanged(self):
        p = make_patient()
        with self.assertRaises(TypeError):
            p.update_details(name=123)
        self.assertEqual(p.name, "Alex Smith")
        prac = make_practitioner()
        with self.assertRaises(TypeError):
            prac.update_details(specialty=7)
        self.assertEqual(prac.specialty, "General Practice")


if __name__ == "__main__":
    unittest.main()
Reflection 

what did you build before using AI?
befire bringing in Ai, i had a working version of the SmartCare bookingsystem:
- appointments = [] as a storage and is_slot_available(),book_appointment(), cancel_appointment(), find_appointments_by_patient(), and display_appointments(). 
I had six functions in place:
is_slot_available(practitioner_name, appointment_time) — loops through the existing appointments list and checks whether a given practitioner already has a booking at that exact time. Returns True or False.
book_appointment(patient_name, practitioner_name, appointment_time) — the main entry point. Before adding anything, it validates that none of the three fields are blank (using if not patient_name: style checks), then calls is_slot_available() to make sure it isn't double-booking a practitioner. Only if both checks pass does it append the new appointment dictionary to the list.
cancel_appointment(patient_name, practitioner_name, appointment_time) — searches the list for an exact match on all three fields and removes it if found, otherwise prints a "no matching appointment" message.
find_appointments_by_patient(patient_name) — filters the list down to just the appointments belonging to one patient and prints them.
find_patient_appointments(patient_name) — a second version doing the same thing (I later realized during review this was an unintentional duplicate I hadn't caught myself).
display_appointments() — loops through the full list and prints every appointment in a readable, formatted line rather than raw dictionary syntax.
I also ran the program end-to-end with a small demo sequence: booking two appointments, deliberately booking a third that conflicted with the first (to confirm the conflict check worked), searching for one patient's appointments, cancelling a booking, and displaying the schedule again afterward to confirm the cancellation actually removed it.

Did AI make assumptions?
Yes, noticeably more than my own version did. The fuller "AI model" version added appointment duration, cost, unique IDs, a reschedule function, and datetime parsing — none of which the original task asked for. AI tends to expand scope unless told not to; my version stayed closer to the stated requirements (name, practitioner, time — book/cancel/search/display).

How did you verify the AI output?
By actually running it, not just reading it — testing normal bookings, a blank name, a duplicate slot, and None inputs against both my version and the AI/Copilot version side by side, and comparing the real console output rather than trusting a description of what "should" happen.

What engineering work remained for you?
Deciding which single improvement was worth making (rather than accepting every AI suggestion), catching that I had two identical duplicate functions (find_appointments_by_patient / find_patient_appointments) that AI didn't flag on its own, and judging whether the AI's added scope (cost, duration, IDs) actually served the assignment or was unnecessary complexity to prune back out.
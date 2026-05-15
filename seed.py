from datetime import datetime, timedelta
import random

from faker import Faker
import numpy as np

from database import DBModelBase, engine, SessionLocal
from models import Patient, Appointment


# ======================================
# INITIAL SETUP
# ======================================

fake = Faker()

np.random.seed(42)
random.seed(42)


# ======================================
# CONFIGURATION
# ======================================

TOTAL_PATIENTS = 300
TOTAL_APPOINTMENTS = 300
TOTAL_DAYS = 60


PRIMARY_ISSUES = np.array([
    "Checkup",
    "Follow-up",
    "Procedure",
    "Consultation"
])


TIME_SLOTS = np.array([
    "9:00AM",
    "10:00AM",
    "11:00AM",
    "1:00PM",
    "2:00PM",
    "3:00PM",
    "4:00PM"
])


DURATION_RULES = {
    "Checkup": {
        "base_duration": 20,
        "variability": 10
    },

    "Follow-up": {
        "base_duration": 15,
        "variability": 5
    },

    "Procedure": {
        "base_duration": 45,
        "variability": 25
    },

    "Consultation": {
        "base_duration": 30,
        "variability": 15
    },
}


# ======================================
# GENERATE PATIENTS
# ======================================

def generate_patient():

    patient_id = fake.uuid4()

    age = np.random.randint(18, 81)

    primary_issue = np.random.choice(
        PRIMARY_ISSUES
    )

    base_no_show_rate = 0.15

    if primary_issue == "Procedure":
        base_no_show_rate *= 0.70

    no_show_probability = min(
        base_no_show_rate * np.random.uniform(
            low=0.8,
            high=1.2
        ),
        0.30
    )

    return Patient(
        id=patient_id,

        age=int(age),

        primary_issue=str(primary_issue),

        no_show_probability=round(
            float(no_show_probability),
            3
        )
    )


# ======================================
# GENERATE APPOINTMENTS
# ======================================

def generate_appointments(patients):

    appointments = []

    start_date = datetime.today()

    while len(appointments) < TOTAL_APPOINTMENTS:

        patient = random.choice(patients)

        appointment_type = patient.primary_issue

        duration_info = DURATION_RULES[
            appointment_type
        ]

        base_duration = duration_info[
            "base_duration"
        ]

        variability = duration_info[
            "variability"
        ]

        scheduled_duration = base_duration

        duration_noise = np.random.randint(
            -variability,
            variability + 1
        )

        actual_duration = max(
            5,
            min(
                90,
                base_duration + duration_noise
            )
        )

        show_up = np.random.choice(
            [True, False],
            p=[
                1 - patient.no_show_probability,
                patient.no_show_probability
            ]
        )

        if not show_up:
            actual_duration = 0

        duration_difference = (
            actual_duration -
            scheduled_duration
        )

        random_day = random.randint(
            0,
            TOTAL_DAYS
        )

        appointment_date = (
            start_date +
            timedelta(days=random_day)
        )

        time_slot = random.choice(TIME_SLOTS)

        appointment_datetime = datetime.combine(
            appointment_date.date(),

            datetime.strptime(
                str(time_slot),
                "%I:%M%p"
            ).time()
        )

        appointment = Appointment(

            id=fake.uuid4(),

            patient_id=patient.id,

            patient_age=patient.age,

            appointment_type=appointment_type,

            appointment_datetime=appointment_datetime,

            day_of_week=appointment_date.strftime(
                "%A"
            ),

            time_slot=str(time_slot),

            scheduled_duration=int(
                scheduled_duration
            ),

            actual_duration=int(
                actual_duration
            ),

            duration_difference=int(
                duration_difference
            ),

            show_up=bool(show_up)
        )

        appointments.append(appointment)

    return appointments


# ======================================
# SEED DATABASE
# ======================================

def seed_database():

    DBModelBase.metadata.drop_all(engine)

    DBModelBase.metadata.create_all(engine)

    session = SessionLocal()

    patients = [
        generate_patient()
        for _ in range(TOTAL_PATIENTS)
    ]

    session.add_all(patients)

    session.commit()

    appointments = generate_appointments(
        patients
    )

    session.add_all(appointments)

    session.commit()

    session.close()

    print("\n Database seeded successfully!")

    print(
        f"Patients created: {len(patients)}"
    )

    print(
        f"Appointments created: {len(appointments)}"
    )


# ======================================
# RUN SCRIPT
# ======================================

if __name__ == "__main__":
    seed_database()
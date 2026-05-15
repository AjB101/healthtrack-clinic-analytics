# HealthTrack Clinic Analytics Project

## Overview

HealthTrack Clinic Analytics is a healthcare operations analytics project designed to simulate and analyze clinic appointment performance using Python, SQLAlchemy, SQLite, and data analytics workflows.

The project focuses on generating realistic healthcare appointment data and transforming it into actionable operational insights for clinic management teams. It demonstrates how data engineering, analytics, and business intelligence can be applied to improve scheduling efficiency, reduce no-shows, optimize appointment durations, and support data-driven healthcare decisions.

This project was developed as part of a healthcare analytics and data engineering portfolio initiative.

---

# Business Problem

## Healthcare clinics often struggle with:

High patient no-show rates
Inefficient scheduling
Appointment overruns
Underutilized time slots
Long patient wait times
Poor operational visibility

Without analytics, clinics cannot easily identify:

Peak no-show periods
Overbooked schedules
Appointment types causing delays
Time slots with poor utilization

This project addresses those challenges by generating and analyzing structured healthcare appointment data to uncover operational patterns and support smarter scheduling decisions.

---
## Project Objectives

The goals of this project are to:

* Generate realistic synthetic healthcare appointment data
* Store structured appointment records using SQLite and SQLAlchemy
* Analyze clinic scheduling efficiency
* Identify no-show trends and operational bottlenecks
* Measure appointment duration variances
* Create actionable business insights for clinic management
* Demonstrate real-world healthcare analytics workflows

---

| Technology   | Purpose                               |
| ------------ | ------------------------------------- |
| Python       | Core programming language             |
| Pandas       | Data analysis and transformation      |
| SQLAlchemy   | Database ORM                          |
| SQLite       | Local database storage                |
| Faker        | Synthetic healthcare data generation  |
| Matplotlib   | Data visualization                    |
| Seaborn      | Statistical visualization             |
| VS Code      | Development environment               |
| Git & GitHub | Version control and portfolio hosting |


## Project Structure

```
healthtrack-clinic-analytics/
│
├── app.py                    # Streamlit dashboard
├── analysis.py
├── database.py                # Database connection setup
├── models.py                  # Database schema (Product model)
├── seed.py                    # Data seeding with Faker
├── requirements.txt
├── .gitignore
├── healthtrack_appointments.csv
└── README.md
```

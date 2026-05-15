import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

from database import engine


# ======================================
# PAGE CONFIGURATION
# ======================================

st.set_page_config(
    page_title="HealthTrack Clinic Dashboard",
    layout="wide"
)


# ======================================
# LOAD DATA
# ======================================

df = pd.read_sql(
    "SELECT * FROM appointments",
    engine
)


# ======================================
# FORMAT DATETIME
# ======================================

df["appointment_datetime"] = pd.to_datetime(
    df["appointment_datetime"]
)

df["created_at"] = pd.to_datetime(
    df["created_at"]
)


# ======================================
# ORDER DAYS OF WEEK
# ======================================

DAY_ORDER = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

df["day_of_week"] = pd.Categorical(
    df["day_of_week"],
    categories=DAY_ORDER,
    ordered=True
)


# ======================================
# ORDER TIME SLOTS
# ======================================

TIME_ORDER = [
    "9:00AM",
    "10:00AM",
    "11:00AM",
    "1:00PM",
    "2:00PM",
    "3:00PM",
    "4:00PM"
]

df["time_slot"] = pd.Categorical(
    df["time_slot"],
    categories=TIME_ORDER,
    ordered=True
)


# ======================================
# SORT DATAFRAME
# ======================================

df = df.sort_values(
    by=[
        "day_of_week",
        "time_slot"
    ]
)


# ======================================
# DASHBOARD TITLE
# ======================================

st.title(
    "🏥 HealthTrack Clinic Dashboard"
)

st.markdown(
    """
    Interactive healthcare analytics dashboard
    for appointment scheduling, no-show analysis,
    and operational insights.
    """
)


# ======================================
# METRICS
# ======================================

total_appointments = df.shape[0]

no_show_rate = (
    (df["show_up"] == False)
    .mean() * 100
)

avg_actual_duration = (
    df["actual_duration"]
    .mean()
)

avg_patient_age = (
    df["patient_age"]
    .mean()
)


col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Total Appointments",
    total_appointments
)

col2.metric(
    "No-Show Rate",
    f"{no_show_rate:.2f}%"
)

col3.metric(
    "Average Duration",
    f"{avg_actual_duration:.2f} mins"
)

col4.metric(
    "Average Patient Age",
    f"{avg_patient_age:.0f}"
)


# ======================================
# NO-SHOWS BY DAY
# ======================================

st.subheader(
    "📅 No-Show Count by Day of Week"
)

no_show_by_day = (
    df[df["show_up"] == False]
    .groupby("day_of_week")
    .size()
    .sort_index()
)

fig1, ax1 = plt.subplots(
    figsize=(8, 5)
)

no_show_by_day.plot(
    kind="bar",
    ax=ax1
)

ax1.set_xlabel("Day of Week")

ax1.set_ylabel("Number of No-Shows")

ax1.set_title(
    "No-Shows by Day"
)

plt.xticks(rotation=45)

st.pyplot(fig1)


# ======================================
# APPOINTMENT TYPES
# ======================================

st.subheader(
    "🩺 Appointment Types"
)

appointment_counts = (
    df["appointment_type"]
    .value_counts()
)

fig2, ax2 = plt.subplots(
    figsize=(8, 5)
)

appointment_counts.plot(
    kind="bar",
    ax=ax2
)

ax2.set_xlabel(
    "Appointment Type"
)

ax2.set_ylabel(
    "Appointment Count"
)

ax2.set_title(
    "Appointments by Type"
)

plt.xticks(rotation=0)

st.pyplot(fig2)


# ======================================
# DURATION ANALYSIS
# ======================================

st.subheader(
    "⏱️ Scheduled vs Actual Duration"
)

duration_analysis = (
    df.groupby("appointment_type")[
        [
            "scheduled_duration",
            "actual_duration"
        ]
    ]
    .mean()
)

fig3, ax3 = plt.subplots(
    figsize=(10, 6)
)

duration_analysis.plot(
    kind="bar",
    ax=ax3
)

ax3.set_xlabel(
    "Appointment Type"
)

ax3.set_ylabel(
    "Average Duration (Minutes)"
)

ax3.set_title(
    "Scheduled vs Actual Duration"
)

plt.xticks(rotation=0)

st.pyplot(fig3)


# ======================================
# TIME SLOT USAGE
# ======================================

st.subheader(
    "🕒 Appointment Count by Time Slot"
)

time_slot_usage = (
    df["time_slot"]
    .value_counts()
    .sort_index()
)

fig4, ax4 = plt.subplots(
    figsize=(8, 5)
)

time_slot_usage.plot(
    kind="bar",
    ax=ax4
)

ax4.set_xlabel("Time Slot")

ax4.set_ylabel(
    "Number of Appointments"
)

ax4.set_title(
    "Appointment Distribution by Time Slot"
)

plt.xticks(rotation=45)

st.pyplot(fig4)


# ======================================
# DATA PREVIEW
# ======================================

st.subheader(
    "📋 Appointment Dataset Preview"
)


# Format datetime columns nicely
df["appointment_datetime"] = (
    df["appointment_datetime"]
    .dt.strftime("%Y-%m-%d %I:%M %p")
)

df["created_at"] = (
    df["created_at"]
    .dt.strftime("%Y-%m-%d %I:%M %p")
)


# Reorder columns professionally
preview_df = df[
    [
        "id",
        "patient_id",
        "patient_age",
        "appointment_type",
        "appointment_datetime",
        "day_of_week",
        "time_slot",
        "scheduled_duration",
        "actual_duration",
        "duration_difference",
        "show_up",
        "created_at"
    ]
]


# Display dataframe
st.dataframe(
    preview_df,

    use_container_width=True,

    height=500
)


# ======================================
# DOWNLOAD CSV
# ======================================

csv_data = df.to_csv(
    index=False
)

st.download_button(
    label="⬇️ Download Appointment CSV",

    data=csv_data,

    file_name="healthtrack_appointments.csv",

    mime="text/csv"
)
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from database import engine


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
# BASIC INFO
# ======================================

print("Dataset loaded successfully!")

print(f"Rows: {df.shape[0]}")

print(f"Columns: {df.shape[1]}")


print("\nPreview:")

print(df.head())


print("\nMissing values:")

print(df.isna().sum())


# ======================================
# 1. NO-SHOW RATE
# ======================================

no_show_rate = (
    (df["show_up"] == False)
    .mean() * 100
)

print(
    f"\nNo-show rate: {no_show_rate:.2f}%"
)


# ======================================
# 2. NO-SHOWS BY DAY
# ======================================

no_show_by_day = (
    df[df["show_up"] == False]
    .groupby("day_of_week")
    .size()
    .sort_index()
)

print("\nNo-shows by day:")

print(no_show_by_day)


# ======================================
# 3. NO-SHOWS BY APPOINTMENT TYPE
# ======================================

no_show_by_type = (
    df[df["show_up"] == False]
    .groupby("appointment_type")
    .size()
    .sort_values(ascending=False)
)

print("\nNo-shows by appointment type:")

print(no_show_by_type)


# ======================================
# 4. TIME SLOT USAGE
# ======================================

time_slot_usage = (
    df["time_slot"]
    .value_counts()
    .sort_index()
)

print("\nTime slot usage:")

print(time_slot_usage)


# ======================================
# 5. DURATION ANALYSIS
# ======================================

duration_analysis = (
    df.groupby("appointment_type")[
        [
            "scheduled_duration",
            "actual_duration",
            "duration_difference"
        ]
    ]
    .mean()
)

print(
    "\nAverage duration by appointment type:"
)

print(duration_analysis)


# ======================================
# CHART 1
# ======================================

plt.figure(figsize=(8, 5))

no_show_by_day.plot(kind="bar")

plt.title("No-Show Count by Day of Week")

plt.xlabel("Day of Week")

plt.ylabel("Number of No-Shows")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ======================================
# CHART 2
# ======================================

plt.figure(figsize=(8, 5))

no_show_by_type.plot(kind="bar")

plt.title(
    "No-Show Count by Appointment Type"
)

plt.xlabel("Appointment Type")

plt.ylabel("Number of No-Shows")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()


# ======================================
# CHART 3
# ======================================

plt.figure(figsize=(10, 6))

duration_analysis[
    [
        "scheduled_duration",
        "actual_duration"
    ]
].plot(kind="bar")

plt.title(
    "Scheduled vs Actual Duration by Appointment Type"
)

plt.xlabel("Appointment Type")

plt.ylabel("Average Duration")

plt.xticks(rotation=0)

plt.tight_layout()

plt.show()


# ======================================
# CHART 4
# ======================================

plt.figure(figsize=(8, 5))

time_slot_usage.plot(kind="bar")

plt.title("Appointment Count by Time Slot")

plt.xlabel("Time Slot")

plt.ylabel("Number of Appointments")

plt.xticks(rotation=45)

plt.tight_layout()

plt.show()


# ======================================
# CHART 5 — NO-SHOW HEATMAP
# ======================================

heatmap_data = (
    df.groupby(
        [
            "time_slot",
            "appointment_type"
        ]
    )["show_up"]
    .apply(
        lambda x: (x == False).mean() * 100
    )
    .unstack()
)


plt.figure(figsize=(10, 6))

sns.heatmap(
    heatmap_data,

    annot=True,

    fmt=".1f",

    cmap="Reds"
)

plt.title(
    "No-Show Rate Heatmap (%)"
)

plt.xlabel(
    "Appointment Type"
)

plt.ylabel(
    "Time Slot"
)

plt.tight_layout()

plt.show()


# ======================================
# EXPORT CLEAN CSV
# ======================================

export_df = df.copy()

export_df["appointment_datetime"] = (
    export_df["appointment_datetime"]
    .dt.strftime("%Y-%m-%d %I:%M %p")
)

export_df["created_at"] = (
    export_df["created_at"]
    .dt.strftime("%Y-%m-%d %I:%M %p")
)

export_df.to_csv(
    "healthtrack_appointments.csv",
    index=False
)

print(
    "\n✅ CSV exported successfully as healthtrack_appointments.csv"
)
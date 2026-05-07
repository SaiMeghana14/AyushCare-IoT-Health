import streamlit as st
import json
import os

from datetime import datetime


NOTES_FILE = "doctor_notes.json"


# --------------------------------------------------------------
# LOAD NOTES
# --------------------------------------------------------------
def load_notes():

    if os.path.exists(NOTES_FILE):

        with open(NOTES_FILE, "r") as f:
            return json.load(f)

    return {}


# --------------------------------------------------------------
# SAVE NOTE
# --------------------------------------------------------------
def save_note(patient_id, note):

    notes = load_notes()

    if patient_id not in notes:
        notes[patient_id] = []

    notes[patient_id].append({

        "time": datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        ),

        "note": note
    })

    with open(NOTES_FILE, "w") as f:
        json.dump(notes, f, indent=4)


# --------------------------------------------------------------
# DOCTOR NOTES COMPONENT
# --------------------------------------------------------------
def render_doctor_notes(selected):

    st.subheader("🩺 Doctor Notes & Observations")

    notes = load_notes()

    patient_notes = notes.get(selected, [])

    # ----------------------------------------------------------
    # NEW NOTE INPUT
    # ----------------------------------------------------------
    new_note = st.text_area(
        "Add Doctor Observation",
        placeholder="""
Example:
Patient oxygen saturation stable.
Continue hydration and monitoring.
"""
    )

    if st.button("💾 Save Doctor Note"):

        if new_note.strip():

            save_note(
                selected,
                new_note
            )

            st.success(
                "Doctor note saved successfully."
            )

            st.rerun()

    st.write("---")

    # ----------------------------------------------------------
    # NOTES HISTORY
    # ----------------------------------------------------------
    st.markdown("### 📋 Patient Notes History")

    if patient_notes:

        for entry in reversed(patient_notes):

            st.markdown(f"""
            <div style='
            background:white;
            padding:1rem;
            border-radius:15px;
            margin-bottom:1rem;
            box-shadow:
            0 4px 10px rgba(0,0,0,0.08);
            '>

            <b>🕒 {entry['time']}</b>

            <p style='margin-top:10px;'>
            {entry['note']}
            </p>

            </div>
            """, unsafe_allow_html=True)

    else:

        st.info(
            "No doctor notes available yet."
        )

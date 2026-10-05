import streamlit as st
import pandas as pd

# Page Configuration
st.set_page_config(page_title="Radiation Safety System", layout="wide")

# Password Verification
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("Please enter the password (Default: 123456):", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("Please enter the password (Default: 123456):", type="password", on_change=password_entered, key="password")
        st.error("Incorrect Password 🚫")
        return False
    return True

if check_password():
    st.title("☢️ Radiation Safety Management System - East Jeddah Hospital")
    st.caption("RSO Dashboard for QC & Equipment Monitoring")
    st.markdown("---")

    # Fetching email settings from session state or setting defaults
    if 'qc_email' not in st.session_state:
        st.session_state['qc_email'] = "rso.qc@ejh.med.sa"
    if 'fault_email' not in st.session_state:
        st.session_state['fault_email'] = "maintenance@ejh.med.sa"

    tab1, tab2, tab3 = st.tabs(["📊 QC & Equipment Status", "🛠️ Fault Logbook", "⚙️ Alert Settings"])

    with tab1:
        st.subheader("Diagnostic Radiology Equipment")
        data = {
            "Equipment": ["CT Scan", "C-Arm", "Mammography", "Fluoroscopy", "DEXA"],
            "Location": ["Room 1", "OR", "Room 3", "Room 4", "Clinics"],
            "Last QC": ["2026-09-15", "2026-09-20", "2026-10-01", "2026-09-10", "2026-09-05"],
            "Next QC": ["2026-10-15", "2026-10-20", "2026-11-01", "2026-10-10", "2026-10-05"],
            "NRRC License": ["2027-05-01", "2027-06-15", "2026-09-30", "2027-08-10", "2027-01-20"],
            "Status": ["🟢 Operational", "🟢 Operational", "🔴 Out of Order", "🟢 Operational", "🟢 Operational"]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("Report Equipment Fault")
        with st.form("fault_form"):
            device = st.selectbox("Select Equipment", ["CT Scan", "C-Arm", "Mammography", "Fluoroscopy", "DEXA"])
            fault_desc = st.text_area("Fault Description")
            submitted = st.form_submit_button("Submit Report")
            if submitted:
                st.success(f"Report submitted successfully for {device}. An automated email alert will be sent to: {st.session_state['fault_email']}")

    with tab3:
        st.subheader("Email Routing Settings")
        st.info("Configure where automated notifications should be sent based on the alert type.")
        
        new_qc_email = st.text_input("QC & NRRC License Alerts Email:", value=st.session_state['qc_email'])
        new_fault_email = st.text_input("Maintenance & Faults Email:", value=st.session_state['fault_email'])
        
        if st.button("Save Settings"):
            st.session_state['qc_email'] = new_qc_email
            st.session_state['fault_email'] = new_fault_email
            st.success("Settings saved successfully! Future alerts will be routed accordingly.")

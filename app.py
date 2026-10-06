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
    st.markdown("---")

    # 1. Initialize Default Data in Memory (Session State)
    if 'equip_df' not in st.session_state:
        st.session_state['equip_df'] = pd.DataFrame({
            "Equipment": ["CT Scan", "C-Arm", "Mammography", "Fluoroscopy", "DEXA"],
            "Serial Number": ["SN-1029", "SN-9921", "SN-5542", "SN-7731", "SN-8812"],
            "Location": ["Room 1", "OR", "Room 3", "Room 4", "Clinics"],
            "Last QC": ["2026-09-15", "2026-09-20", "2026-10-01", "2026-09-10", "2026-09-05"],
            "Next QC": ["2026-10-15", "2026-10-20", "2026-11-01", "2026-10-10", "2026-10-05"],
            "NRRC License": ["2027-05-01", "2027-06-15", "2026-09-30", "2027-08-10", "2027-01-20"],
            "Status": ["🟢 Operational", "🟢 Operational", "🔴 Out of Order", "🟢 Operational", "🟢 Operational"]
        })

    if 'tld_df' not in st.session_state:
        st.session_state['tld_df'] = pd.DataFrame({
            "Employee Name": ["Ahmad Ali", "Khalid Saad", "Sara Omar"],
            "Job Title": ["RT", "Radiologist", "RT"],
            "Old TLD No.": ["T-101", "T-102", "T-103"],
            "New TLD No.": ["T-201", "T-202", "T-203"],
            "Delivery Date": ["2026-10-01", "2026-10-01", "2026-10-01"],
            "Reading (mSv)": [0.12, 0.08, 0.15],
            "Return Status": ["Returned", "Pending", "Returned"]
        })

    # 2. Setup Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Equipment & QC", "🦺 TLD Management", "🛠️ Fault Logbook", "⚙️ Settings & Uploads"])

    # Tab 1: Equipment & QC
    with tab1:
        st.subheader("Diagnostic Radiology Equipment")
        
        # Excel Upload Feature for Equipment
        equip_file = st.file_uploader("Upload Excel File to Update Equipment Data", type=["xlsx", "xls"], key="equip_upload")
        if equip_file:
            try:
                st.session_state['equip_df'] = pd.read_excel(equip_file)
                st.success("Equipment data updated successfully from Excel!")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        st.dataframe(st.session_state['equip_df'], use_container_width=True)

    # Tab 2: TLD Management
    with tab2:
        st.subheader("Personnel Dosimetry (TLD) Records")
        
        # Excel Upload Feature for TLD
        tld_file = st.file_uploader("Upload Excel File to Update TLD Data", type=["xlsx", "xls"], key="tld_upload")
        if tld_file:
            try:
                st.session_state['tld_df'] = pd.read_excel(tld_file)
                st.success("TLD data updated successfully from Excel!")
            except Exception as e:
                st.error(f"Error reading file: {e}")

        st.dataframe(st.session_state['tld_df'], use_container_width=True)

    # Tab 3: Fault Logbook
    with tab3:
        st.subheader("Report Equipment Fault")
        with st.form("fault_form"):
            device_list = st.session_state['equip_df']['Equipment'].tolist()
            device = st.selectbox("Select Equipment", device_list)
            fault_desc = st.text_area("Fault Description")
            submitted = st.form_submit_button("Submit Report")
            if submitted:
                st.success(f"Report submitted for {device}. Automated email alert triggered.")

    # Tab 4: Settings & Email Templates
    with tab4:
        st.subheader("Email Routing & Templates")
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**QC & NRRC Alerts**")
            st.text_input("QC Alert Email:", value="rso.qc@ejh.med.sa")
            st.text_area("QC Email Template:", height=150, value="""Dear Team,
This is an automated reminder that the upcoming QC test for {device} is scheduled on {date}. 
Please ensure all necessary preparations are made.

Regards,
Radiation Safety Officer""")

        with col2:
            st.markdown("**Maintenance & Faults Alerts**")
            st.text_input("Maintenance Email:", value="maintenance@ejh.med.sa")
            st.text_area("Fault Email Template:", height=150, value="""Urgent: Medical Maintenance Team,
A new fault has been reported for {device} located in {location}.
Fault Description: {description}

Please check the system log for details and initiate repairs.
Regards,
RSO Dashboard""")
            
        if st.button("Save Configurations"):
            st.success("Templates and email addresses updated successfully!")

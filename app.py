import streamlit as st
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="نظام الحماية من الإشعاع", layout="wide")

# دالة التحقق من كلمة المرور
def check_password():
    def password_entered():
        if st.session_state["password"] == "123456":
            st.session_state["password_correct"] = True
            del st.session_state["password"]
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        st.text_input("الرجاء إدخال كلمة المرور (الافتراضية للتجربة: 123456):", type="password", on_change=password_entered, key="password")
        return False
    elif not st.session_state["password_correct"]:
        st.text_input("الرجاء إدخال كلمة المرور (الافتراضية للتجربة: 123456):", type="password", on_change=password_entered, key="password")
        st.error("كلمة المرور غير صحيحة 🚫")
        return False
    return True

if check_password():
    st.title("☢️ نظام إدارة الحماية من الإشعاع")
    st.markdown("---")

    tab1, tab2, tab3 = st.tabs(["📊 حالة الأجهزة (QC)", "🛠️ سجل الأعطال", "⚙️ الإعدادات"])

    with tab1:
        st.subheader("جدول أجهزة الأشعة التشخيصية")
        data = {
            "اسم الجهاز": ["CT Scan", "C-Arm", "Mammography", "Fluoroscopy", "DEXA"],
            "القسم": ["الأشعة - غرفة 1", "العمليات", "الأشعة - غرفة 3", "الأشعة - غرفة 4", "العيادات"],
            "آخر QC": ["2026-09-15", "2026-09-20", "2026-10-01", "2026-09-10", "2026-09-05"],
            "الـ QC القادم": ["2026-10-15", "2026-10-20", "2026-11-01", "2026-10-10", "2026-10-05"],
            "ترخيص NRRC": ["2027-05-01", "2027-06-15", "2026-09-30", "2027-08-10", "2027-01-20"],
            "الحالة": ["🟢 يعمل", "🟢 يعمل", "🔴 معطل", "🟢 يعمل", "🟢 يعمل"]
        }
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)

    with tab2:
        st.subheader("الإبلاغ عن الأعطال")
        with st.form("fault_form"):
            device = st.selectbox("الجهاز", ["CT Scan", "C-Arm", "Mammography", "Fluoroscopy", "DEXA"])
            fault_desc = st.text_area("وصف العطل")
            submitted = st.form_submit_button("إرسال البلاغ")
            if submitted:
                st.success(f"تم تسجيل البلاغ لجهاز {device}. سيتم التنبيه.")

    with tab3:
        st.subheader("إعدادات التنبيهات")
        st.text_input("البريد الإلكتروني لمسؤول الحماية:", value="admin@ejh.med.sa")
        if st.button("حفظ وإرسال بريد تجريبي"):
            st.success("تم حفظ الإعدادات بنجاح!")

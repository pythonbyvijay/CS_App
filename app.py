import streamlit as st
import pandas as pd
import datetime
from questions import users, initial_data

st.set_page_config(page_title="HSC CS Portal 2026", layout="wide")

# --- Persistent State Initialization ---
if 'question_list' not in st.session_state:
    st.session_state.question_list = initial_data
if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = [] # Stores file objects/names

# --- 1. Countdown Logic ---
exam_date = datetime.datetime(2026, 3, 10)
now = datetime.datetime.now()
remaining = exam_date - now
days = remaining.days
hours, remainder = divmod(remaining.seconds, 3600)
minutes, seconds = divmod(remainder, 60)

# --- UI Header ---
st.title("🖥️ Computer Science Paper I (D9)")
st.subheader(f"⏳ Exam Countdown: {days} Days, {hours}h {minutes}m left")
st.progress(max(0, min(100, 100 - (days/365)*100))) # Visual progress bar

# --- Login Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u in users and users[u]["password"] == p:
            st.session_state.logged_in = True
            st.session_state.role = users[u]["role"]
            st.session_state.user = u
            st.rerun()
else:
    # --- ADMIN DASHBOARD ---
    if st.session_state.role == "admin":
        st.sidebar.success(f"Admin: {st.session_state.user}")
        
        menu = st.sidebar.radio("Menu", ["Add Questions", "Upload PDFs", "View All"])

        if menu == "Add Questions":
            st.header("➕ Add New Questions")
            with st.form("q_form", clear_on_submit=True):
                cat = st.selectbox("Type", ["3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
                q = st.text_input("Question")
                a = st.text_area("Answer/Code")
                if st.form_submit_button("Submit"):
                    st.session_state.question_list.append({"category": cat, "question": q, "answer": a})
                    st.success("Question Added to Bank!")

        elif menu == "Upload PDFs":
            st.header("📂 Multi-File Upload")
            new_files = st.file_uploader("Select PDF Files", type="pdf", accept_multiple_files=True)
            if st.button("Save Files to List"):
                if new_files:
                    for f in new_files:
                        if f.name not in [x.name for x in st.session_state.uploaded_files_list]:
                            st.session_state.uploaded_files_list.append(f)
                    st.success(f"Total files in system: {len(st.session_state.uploaded_files_list)}")

        elif menu == "View All":
            st.header("📋 Current System Data")
            st.write("### Questions Added")
            st.table(pd.DataFrame(st.session_state.question_list))

    # --- STUDENT DASHBOARD ---
    else:
        st.sidebar.info(f"Student: {st.session_state.user}")
        mode = st.sidebar.radio("Section", ["Study Questions", "Download Materials"])

        if mode == "Study Questions":
            st.header("📖 Revision Bank")
            cat_choice = st.selectbox("Category", ["3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
            
            # Filter from the session_state list
            items = [x for x in st.session_state.question_list if x['category'] == cat_choice]
            for item in items:
                with st.expander(item['question']):
                    if "Program" in cat_choice:
                        st.code(item['answer'])
                    else:
                        st.write(item['answer'])

        elif mode == "Download Materials":
            st.header("📥 Downloads")
            
            # 1. Download Questions as CSV
            df_qs = pd.DataFrame(st.session_state.question_list)
            csv = df_qs.to_csv(index=False).encode('utf-8')
            st.download_button("Download All Questions (CSV)", csv, "questions.csv", "text/csv")
            
            st.divider()
            
            # 2. Access All Uploaded PDFs
            st.subheader("Reference PDFs")
            if st.session_state.uploaded_files_list:
                for f in st.session_state.uploaded_files_list:
                    st.download_button(f"📄 Download {f.name}", f.getvalue(), file_name=f.name)
            else:
                st.write("No PDFs uploaded by professor yet.")

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
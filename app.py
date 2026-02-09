import streamlit as st
import pandas as pd
import datetime
from questions import users, initial_data

st.set_page_config(page_title="HSC CS Portal 2026", layout="wide")

# --- 1. Countdown Logic (Fixed Progress Bar) ---
exam_date = datetime.datetime(2026, 3, 10)
days_left = (exam_date - datetime.datetime.now()).days

st.title("🖥️ Computer Science Paper I (D9)")
st.subheader(f"⏳ Exam Countdown: {days_left} Days Remaining")

# FIX: Convert to int to ensure value is in the 0-100 range for Streamlit
progress_val = int(max(0, min(100, 100 - (days_left/365)*100)))
st.progress(progress_val, text=f"Preparation Progress: {progress_val}%")

# --- 2. Persistent State Management ---
if 'question_list' not in st.session_state:
    st.session_state.question_list = initial_data
if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = []

# --- 3. Login System ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("login_form"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u in users and users[u]["password"] == p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, users[u]["role"], u
                st.rerun()
            else: st.error("Invalid credentials")
else:
    # --- Sidebar ---
    st.sidebar.write(f"Logged in as: **{st.session_state.user.upper()}**")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN VIEW ---
    if st.session_state.role == "admin":
        st.title("👨‍🏫 Professor Dashboard")
        menu = st.sidebar.selectbox("Admin Menu", ["Add Questions", "Upload Resources"])
        
        if menu == "Add Questions":
            with st.form("add_q", clear_on_submit=True):
                cat = st.selectbox("Category", ["3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
                q = st.text_input("Question")
                a = st.text_area("Answer/Code")
                if st.form_submit_button("Save Question"):
                    st.session_state.question_list.append({"category": cat, "question": q, "answer": a})
                    st.success("Question saved!")

        elif menu == "Upload Resources":
            # Multi-file uploader logic
            uploaded = st.file_uploader("Upload Multiple PDFs", type="pdf", accept_multiple_files=True)
            if st.button("Commit Uploads"):
                for f in uploaded:
                    # Avoid duplicates
                    if f.name not in [x['name'] for x in st.session_state.uploaded_files_list]:
                        st.session_state.uploaded_files_list.append({"name": f.name, "content": f.getvalue()})
                st.success(f"Successfully added {len(uploaded)} files.")

    # --- SHARED VIEW FOR STUDENT & ADMIN ---
    st.divider()
    view_mode = st.radio("Switch Section:", ["Revision Bank", "Download Center"], horizontal=True)

    if view_mode == "Revision Bank":
        st.header("📖 Study Materials")
        for q in st.session_state.question_list:
            with st.expander(f"[{q['category']}] {q['question']}"):
                if "Program" in q['category']: st.code(q['answer'], language="cpp")
                else: st.write(q['answer'])

    elif view_mode == "Download Center":
        st.header("📥 Student Download Area")
        # 1. Download Question Bank
        q_df = pd.DataFrame(st.session_state.question_list)
        st.download_button("📥 Download All Questions (CSV)", q_df.to_csv(index=False), "CS_Questions.pdf")
        
        st.divider()
        st.subheader("Reference PDFs")
        if st.session_state.uploaded_files_list:
            for f in st.session_state.uploaded_files_list:
                st.download_button(f"📄 Download {f['name']}", f['content'], file_name=f['name'])
        else:
            st.info("No PDF resources available yet.")
import streamlit as st
import pandas as pd
import datetime
from questions import users, initial_data

st.set_page_config(page_title="HSC CS Portal - Vijay Shinde", layout="wide")

# --- Countdown Logic ---
exam_date = datetime.datetime(2026, 3, 10)
days_left = (exam_date - datetime.datetime.now()).days
st.title("🖥️ CS Paper I (D9) Portal")
st.subheader(f"⏳ Exam Countdown: {days_left} Days")
progress_val = int(max(0, min(100, 100 - (days_left/365)*100)))
st.progress(progress_val, text=f"Syllabus Progress: {progress_val}%")

# --- Persistent State ---
if 'question_list' not in st.session_state:
    st.session_state.question_list = initial_data
if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = []

# --- Login Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Login"):
        if u in users and users[u]["password"] == p:
            st.session_state.logged_in, st.session_state.role, st.session_state.user = True, users[u]["role"], u
            st.rerun()
else:
    # --- ADMIN DASHBOARD ---
    if st.session_state.role == "admin":
        st.sidebar.success(f"Welcome Prof. Vijay Shinde")
        menu = st.sidebar.selectbox("Menu", ["Add Questions", "Upload Resources"])
        
        if menu == "Add Questions":
            with st.form("add_q", clear_on_submit=True):
                cat = st.selectbox("Category", ["1 Mark MCQ", "3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
                q = st.text_input("Question Text")
                
                # Dynamic inputs for MCQ
                options = []
                correct_ans = ""
                if cat == "1 Mark MCQ":
                    col1, col2 = st.columns(2)
                    with col1:
                        opt_a = st.text_input("Option A")
                        opt_b = st.text_input("Option B")
                    with col2:
                        opt_c = st.text_input("Option C")
                        opt_d = st.text_input("Option D")
                    options = [opt_a, opt_b, opt_c, opt_d]
                    correct_ans = st.selectbox("Select Correct Answer", options)
                else:
                    correct_ans = st.text_area("Model Answer / Code")
                
                if st.form_submit_button("Save Question"):
                    entry = {"category": cat, "question": q, "answer": correct_ans}
                    if cat == "1 Mark MCQ":
                        entry["options"] = options
                    st.session_state.question_list.append(entry)
                    st.success("Question Added!")

    # --- STUDENT VIEW ---
    st.divider()
    view_mode = st.radio("Go to:", ["Revision Bank", "Download Center"], horizontal=True)

    if view_mode == "Revision Bank":
        st.header("📖 Study Materials")
        for q in st.session_state.question_list:
            with st.container(border=True):
                st.write(f"**[{q['category']}]** {q['question']}")
                
                if q['category'] == "1 Mark MCQ":
                    # Radio button for student practice
                    user_choice = st.radio("Select your answer:", q['options'], key=q['question'])
                    if st.button("Check Answer", key=f"btn_{q['question']}"):
                        if user_choice == q['answer']:
                            st.success("Correct!")
                        else:
                            st.error(f"Wrong! Correct answer is: {q['answer']}")
                else:
                    with st.expander("Show Solution"):
                        if "Program" in q['category']:
                            st.code(q['answer'], language="cpp")
                        else:
                            st.write(q['answer'])

    elif view_mode == "Download Center":
        st.header("📥 Resources")
        # PDF download logic remains same as previous version...
        if st.session_state.uploaded_files_list:
            for f in st.session_state.uploaded_files_list:
                st.download_button(f"📄 {f['name']}", f['content'], file_name=f['name'])
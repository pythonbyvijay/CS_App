import streamlit as st
import pandas as pd
import datetime
from questions import users, initial_data

st.set_page_config(page_title="HSC CS Portal - Vijay Shinde", layout="wide")

# --- 1. Countdown Logic ---
exam_date = datetime.datetime(2026, 3, 10)
days_left = (exam_date - datetime.datetime.now()).days
st.title("🖥️ CS Paper I (D9) Portal")
st.subheader(f"⏳ Exam Countdown: {days_left} Days")

progress_val = int(max(0, min(100, 100 - (days_left/365)*100)))
st.progress(progress_val, text=f"Preparation Progress: {progress_val}%")

# --- 2. Session State Initialization ---
if 'question_list' not in st.session_state:
    st.session_state.question_list = initial_data
if 'uploaded_files_list' not in st.session_state:
    st.session_state.uploaded_files_list = []

# --- 3. Login Logic ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    with st.form("Login"):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.form_submit_button("Login"):
            if u in users and users[u]["password"] == p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, users[u]["role"], u
                st.rerun()
            else: st.error("Access Denied")
else:
    # --- SIDEBAR NAVIGATION ---
    st.sidebar.title(f"Welcome Prof. {st.session_state.user.capitalize()}")
    
    # Define menu based on role
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation", ["Add Questions", "Upload Resources", "Revision Bank", "Download Center"])
    else:
        menu = st.sidebar.radio("Navigation", ["Revision Bank", "Download Center"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN: ADD QUESTIONS ---
    if menu == "Add Questions" and st.session_state.role == "admin":
        st.header("➕ Add New Content")
        with st.form("q_form", clear_on_submit=True):
            cat = st.selectbox("Category", ["1 Mark MCQ", "3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
            q_text = st.text_input("Enter Question")
            
            options = []
            correct_ans = ""
            
            if cat == "1 Mark MCQ":
                col1, col2 = st.columns(2)
                with col1:
                    a = st.text_input("Option A")
                    b = st.text_input("Option B")
                with col2:
                    c = st.text_input("Option C")
                    d = st.text_input("Option D")
                options = [a, b, c, d]
                correct_ans = st.selectbox("Correct Answer", options)
            else:
                correct_ans = st.text_area("Model Answer / Code Snippet")

            if st.form_submit_button("Save to Database"):
                new_entry = {"category": cat, "question": q_text, "answer": correct_ans}
                if cat == "1 Mark MCQ":
                    new_entry["options"] = options
                st.session_state.question_list.append(new_entry)
                st.success("Successfully Added!")

    # --- ADMIN: UPLOAD RESOURCES ---
    elif menu == "Upload Resources" and st.session_state.role == "admin":
        st.header("📂 Resource Manager")
        uploaded_pdfs = st.file_uploader("Upload Multiple PDFs (Notes/Papers)", type="pdf", accept_multiple_files=True)
        
        if st.button("Save Uploaded Files"):
            if uploaded_pdfs:
                for pdf in uploaded_pdfs:
                    if pdf.name not in [f['name'] for f in st.session_state.uploaded_files_list]:
                        st.session_state.uploaded_files_list.append({"name": pdf.name, "content": pdf.getvalue()})
                st.success(f"Stored {len(uploaded_pdfs)} files.")

    # --- SHARED: REVISION BANK ---
    elif menu == "Revision Bank":
        st.header("📖 Revision Bank")
        for idx, item in enumerate(st.session_state.question_list):
            with st.container(border=True):
                st.write(f"**{item['category']}**: {item['question']}")
                
                if item['category'] == "1 Mark MCQ":
                    choice = st.radio(f"Select Option (Q{idx})", item['options'], key=f"mcq_{idx}")
                    if st.button(f"Check Answer (Q{idx})"):
                        if choice == item['answer']: st.success("Correct!")
                        else: st.error(f"Incorrect! Answer: {item['answer']}")
                else:
                    with st.expander("View Answer"):
                        if "Program" in item['category']: st.code(item['answer'])
                        else: st.write(item['answer'])

    # --- SHARED: DOWNLOAD CENTER ---
    elif menu == "Download Center":
        st.header("📥 Downloads")
        
        # Download all questions as CSV
        df = pd.DataFrame(st.session_state.question_list)
        st.download_button("📥 Download Question Bank (CSV)", df.to_pdf(index=False), "CS_Questions.pdf")
        
        st.divider()
        st.subheader("PDF Documents")
        if st.session_state.uploaded_files_list:
            for f in st.session_state.uploaded_files_list:
                st.download_button(f"📄 Download {f['name']}", f['content'], file_name=f['name'])
        else:
            st.info("No PDF files available yet.")
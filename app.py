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
    # --- NAVIGATION MENU ---
    st.sidebar.title(f"Welcome Prof. {st.session_state.user.capitalize()}")
    
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation", ["Add Questions", "Upload Resources", "Revision Bank", "Test Section", "Download Center"])
    else:
        menu = st.sidebar.radio("Navigation", ["Revision Bank", "Test Section", "Download Center"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN: UPLOAD RESOURCES (With Categorization) ---
    if menu == "Upload Resources" and st.session_state.role == "admin":
        st.header("📂 Resource Manager")
        st.write("Tag and upload your PDFs for students.")
        
        with st.form("upload_form"):
            file_cat = st.selectbox("Select File Category", [
                "Previous Year Question Papers",
                "1 Mark Questions PDF",
                "Notes: Operating System",
                "Notes: Data Structure",
                "Notes: C++",
                "Notes: HTML"
            ])
            uploaded_pdfs = st.file_uploader("Select PDF Files", type="pdf", accept_multiple_files=True)
            submit_upload = st.form_submit_button("Save to System")
            
            if submit_upload and uploaded_pdfs:
                for pdf in uploaded_pdfs:
                    st.session_state.uploaded_files_list.append({
                        "name": pdf.name, 
                        "content": pdf.getvalue(),
                        "category": file_cat
                    })
                st.success(f"Successfully uploaded {len(uploaded_pdfs)} files under {file_cat}")

    # --- SHARED: DOWNLOAD CENTER (Organized for Students) ---
    elif menu == "Download Center":
        st.header("📥 Student Download Center")
        
        # Helper function to filter and display buttons
        def display_category(label, category_name):
            files = [f for f in st.session_state.uploaded_files_list if f['category'] == category_name]
            with st.expander(label, expanded=True):
                if files:
                    for f in files:
                        st.download_button(f"📄 Download {f['name']}", f['content'], file_name=f['name'], key=f['name']+category_name)
                else:
                    st.info("No files uploaded yet in this section.")

        # 1. Previous Year Papers
        display_category("📅 1. Previous Year Question Papers", "Previous Year Question Papers")
        
        # 2. 1 Mark Questions
        display_category("🔢 2. Download 1 Mark Questions", "1 Mark Questions PDF")
        
        # 3. Notes (Nested)
        st.subheader("📝 3. Download Notes")
        display_category("📁 Chapter 1: Operating System", "Notes: Operating System")
        display_category("📁 Chapter 2: Data Structure", "Notes: Data Structure")
        display_category("📁 Chapter 3: C++", "Notes: C++")
        display_category("📁 Chapter 4: HTML", "Notes: HTML")

    # --- [Keep "Add Questions", "Revision Bank", "Test Section" as per previous code] ---
    elif menu == "Add Questions":
        st.header("➕ Add New Questions")
        with st.form("q_form", clear_on_submit=True):
            cat = st.selectbox("Category", ["1 Mark MCQ", "3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
            q_text = st.text_input("Question")
            if cat == "1 Mark MCQ":
                c1, c2 = st.columns(2)
                opts = [c1.text_input("Opt A"), c1.text_input("Opt B"), c2.text_input("Opt C"), c2.text_input("Opt D")]
                ans = st.selectbox("Correct Answer", opts)
            else:
                ans = st.text_area("Answer/Code")
            if st.form_submit_button("Save"):
                entry = {"category": cat, "question": q_text, "answer": ans}
                if cat == "1 Mark MCQ": entry["options"] = opts
                st.session_state.question_list.append(entry)
                st.success("Saved!")

    elif menu == "Revision Bank":
        st.header("📖 Revision Bank")
        for q in st.session_state.question_list:
            with st.expander(f"{q['category']}: {q['question']}"):
                if "Program" in q['category']: st.code(q['answer'], language="cpp")
                else: st.write(q['answer'])

    elif menu == "Test Section":
        st.header("📝 Student Practice Test")
        for idx, q in enumerate(st.session_state.question_list):
            st.write(f"**Q{idx+1}: {q['question']}**")
            if q['category'] == "1 Mark MCQ":
                st.radio("Select Answer", q['options'], key=f"test_{idx}")
            else:
                st.text_area("Type Answer", key=f"test_{idx}")
import streamlit as st
import pandas as pd
import datetime
import os
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
            else: 
                st.error("Access Denied")
else:
    # --- NAVIGATION MENU ---
    st.sidebar.title(f"Welcome Prof. {st.session_state.user.capitalize()}")
    
    # "Upload Resources" has been removed from Admin menu as requested
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation", ["Add Questions", "Revision Bank", "Test Section", "Download Center"])
    else:
        menu = st.sidebar.radio("Navigation", ["Revision Bank", "Test Section", "Download Center"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

   # --- SHARED: DOWNLOAD CENTER ---
    if menu == "Download Center":
        st.header("📥 Student Download Center")
        
        resource_map = {
            "📅 1. Previous Year Question Papers": "papers",
            "📁 Chapter 1: Operating System": "Operating System Notes",
            "📁 Chapter 2: Data Structure": "Data Structure Notes",
            "📁 Chapter 3: C++": "C++ Notes",
            "📁 Chapter 4: HTML": "HTML Notes"
        }

        for label, folder_path in resource_map.items():
            with st.expander(label, expanded=True):
                if os.path.exists(folder_path):
                    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
                    if files:
                        for filename in files:
                            file_path = os.path.join(folder_path, filename)
                            
                            # Row Layout: Filename | View Button | Download Button
                            col_name, col_view, col_dl = st.columns([0.5, 0.25, 0.25])
                            
                            with col_name:
                                st.write(f"📄 {filename}")
                            
                            with col_view:
                                # Reading file for the View/Download actions
                                with open(file_path, "rb") as f:
                                    pdf_bytes = f.read()
                                
                                # Using a Link styled as a button for "View" to avoid browser blocking
                                import base64
                                base64_pdf = base64.b64encode(pdf_bytes).decode('utf-8')
                                
                                # This creates a cleaner HTML link that acts as a view button
                                view_html = f'''
                                    <a href="data:application/pdf;base64,{base64_pdf}" target="_blank" style="text-decoration: none;">
                                        <div style="background-color: #ff4b4b; color: white; padding: 0.5rem; text-align: center; border-radius: 0.5rem; font-size: 0.8rem; font-weight: bold;">
                                            👁️ VIEW
                                        </div>
                                    </a>
                                '''
                                st.markdown(view_html, unsafe_allow_html=True)
                            
                            with col_dl:
                                st.download_button(
                                    label="💾 DOWNLOAD",
                                    data=pdf_bytes,
                                    file_name=filename,
                                    key=f"dl_{folder_path}_{filename}",
                                    use_container_width=True
                                )
                            st.write("") # Small spacing
                    else:
                        st.write("No PDF files found.")
    # --- ADMIN: ADD QUESTIONS ---
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
                st.success("Question added!")

    # --- SHARED: REVISION BANK ---
    elif menu == "Revision Bank":
        st.header("📖 Revision Bank")
        for q in st.session_state.question_list:
            with st.expander(f"{q['category']}: {q['question']}"):
                if "Program" in q['category']: 
                    st.code(q['answer'], language="cpp")
                else: 
                    st.write(q['answer'])

    # --- SHARED: TEST SECTION ---
    elif menu == "Test Section":
        st.header("📝 Student Practice Test")
        for idx, q in enumerate(st.session_state.question_list):
            st.write(f"**Q{idx+1}: {q['question']}**")
            if q['category'] == "1 Mark MCQ":
                st.radio("Select Answer", q['options'], key=f"test_{idx}")
            else:
                st.text_area("Type Answer", key=f"test_{idx}")
import streamlit as st
import pandas as pd
import datetime
from fpdf import FPDF
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

# --- 3. PDF Generator Function ---
def create_pdf(questions):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="HSC CS Paper I - Question Bank", ln=True, align='C')
    pdf.ln(10)
    
    for idx, q in enumerate(questions):
        pdf.set_font("Arial", 'B', 12)
        pdf.multi_cell(0, 10, txt=f"Q{idx+1}. {q['question']} [{q['category']}]")
        pdf.set_font("Arial", '', 11)
        
        if q['category'] == "1 Mark MCQ":
            pdf.multi_cell(0, 8, txt=f"Options: {', '.join(q['options'])}")
            pdf.set_text_color(0, 128, 0)
            pdf.cell(0, 8, txt=f"Correct Answer: {q['answer']}", ln=True)
            pdf.set_text_color(0, 0, 0)
        else:
            pdf.multi_cell(0, 8, txt=f"Answer: {q['answer']}")
        pdf.ln(5)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(5)
    return pdf.output(dest='S').encode('latin-1')

# --- 4. Login Logic ---
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
    
    # Same menu for Admin; Students see limited options
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation", ["Add Questions", "Upload Resources", "Revision Bank", "Test Section", "Download Center"])
    else:
        menu = st.sidebar.radio("Navigation", ["Revision Bank", "Test Section", "Download Center"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADD QUESTIONS ---
    if menu == "Add Questions":
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
                st.success("Saved to Question Bank!")

    # --- UPLOAD RESOURCES ---
    elif menu == "Upload Resources":
        st.header("📂 Upload Readymade PDFs")
        files = st.file_uploader("Upload PDFs", type="pdf", accept_multiple_files=True)
        if st.button("Save Files"):
            for f in files:
                st.session_state.uploaded_files_list.append({"name": f.name, "content": f.getvalue()})
            st.success("Files ready for students!")

    # --- REVISION BANK ---
    elif menu == "Revision Bank":
        st.header("📖 Revision Bank")
        for q in st.session_state.question_list:
            with st.expander(f"{q['category']}: {q['question']}"):
                st.write(q['answer'])

    # --- TEST SECTION (LATER USE) ---
    elif menu == "Test Section":
        st.header("📝 Student Practice Test")
        st.info("Questions added in 'Add Questions' appear here automatically.")
        for idx, q in enumerate(st.session_state.question_list):
            st.write(f"**Q{idx+1}: {q['question']}**")
            if q['category'] == "1 Mark MCQ":
                st.radio("Select Answer", q['options'], key=f"test_{idx}")
            else:
                st.text_area("Type Answer", key=f"test_{idx}")
        st.button("Submit Test (Results feature coming soon)")

    # --- DOWNLOAD CENTER ---
    elif menu == "Download Center":
        st.header("📥 Download Center")
        
        # 1. Download the generated PDF of all typed questions
        if st.session_state.question_list:
            pdf_data = create_pdf(st.session_state.question_list)
            st.download_button("📥 Download Generated Question Bank (PDF)", pdf_data, "Question_Bank.pdf", "application/pdf")
        
        st.divider()
        st.subheader("Readymade PDFs from Professor")
        for f in st.session_state.uploaded_files_list:
            st.download_button(f"📄 Download {f['name']}", f['content'], file_name=f['name'])
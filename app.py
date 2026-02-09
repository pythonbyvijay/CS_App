import streamlit as st
import pandas as pd
import os
import datetime
from questions import initial_data, users

st.set_page_config(page_title="HSC CS Paper I Portal", layout="wide")

# --- Persistent Data Management ---
DB_FILE = "question_bank.csv"
RESULTS_FILE = "student_results.csv"

# Initialize local CSV files if they don't exist
if not os.path.exists(DB_FILE):
    pd.DataFrame(initial_questions).to_csv(DB_FILE, index=False)
if not os.path.exists(RESULTS_FILE):
    pd.DataFrame(columns=["Student", "Score", "Total", "Date"]).to_csv(RESULTS_FILE, index=False)

def load_data(file):
    return pd.read_csv(file)

# --- Session State for Login ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- LOGIN UI ---
if not st.session_state.logged_in:
    st.title("🖥️ HSC CS Paper I (D9) Portal")
    with st.container(border=True):
        u = st.text_input("Username")
        p = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if u in users and users[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.role = users[u]["role"]
                st.session_state.username = u
                st.rerun()
            else:
                st.error("Wrong Username or Password")
else:
    # --- AUTHENTICATED SIDEBAR ---
    st.sidebar.title(f"Welcome, {st.session_state.username}")
    st.sidebar.caption(f"Role: {st.session_state.role.upper()}")
    
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- ADMIN VIEW ---
    if st.session_state.role == "admin":
        st.title("👨‍🏫 Professor Control Panel")
        tab1, tab2, tab3 = st.tabs(["Manage Questions", "Student Results", "Upload PDF"])
        
        with tab1:
            st.subheader("Add New Question")
            with st.form("add_q_form", clear_on_submit=True):
                cat = st.selectbox("Category", ["3 Marks Theory", "4 Marks Theory", "C++ Programs", "HTML Programs"])
                ques = st.text_area("Question Text")
                ans = st.text_area("Model Answer / Code")
                if st.form_submit_button("Add to Question Bank"):
                    new_q = pd.DataFrame([{"category": cat, "question": ques, "answer": ans}])
                    new_q.to_csv(DB_FILE, mode='a', header=False, index=False)
                    st.success("Question Added!")

        with tab2:
            st.subheader("Student Performance")
            st.dataframe(load_data(RESULTS_FILE), use_container_width=True)

        with tab3:
            st.info("To share a PDF, upload it to GitHub or your server and provide the link here.")
            st.file_uploader("Upload Notes (PDF)", type="pdf")

    # --- STUDENT VIEW ---
    else:
        st.title("🎓 Student Revision Portal")
        df_qs = load_data(DB_FILE)
        
        mode = st.sidebar.selectbox("Go to:", ["Learning Center", "Practice Test", "Downloads"])

        if mode == "Learning Center":
            st.header("Study Notes by Category")
            cat_filter = st.radio("Select Category", df_qs['category'].unique(), horizontal=True)
            filtered = df_qs[df_qs['category'] == cat_filter]
            
            for _, row in filtered.iterrows():
                with st.expander(f"📌 {row['question']}"):
                    if "Programs" in cat_filter:
                        st.code(row['answer'], language="cpp" if "C++" in cat_filter else "html")
                    else:
                        st.write(row['answer'])

        elif mode == "Practice Test":
            st.header("📝 Quick Mock Test")
            test_items = df_qs.sample(n=min(len(df_qs), 3)) # Test with 3 random qs
            score = 0
            
            with st.form("quiz_form"):
                for i, row in test_items.iterrows():
                    st.write(f"**Q: {row['question']}**")
                    st.text_area("Your Answer", key=f"q_{i}")
                
                if st.form_submit_button("Submit Test"):
                    # Basic scoring logic for a manual test
                    res = pd.DataFrame([{
                        "Student": st.session_state.username,
                        "Score": "Submitted", 
                        "Total": len(test_items),
                        "Date": datetime.date.today()
                    }])
                    res.to_csv(RESULTS_FILE, mode='a', header=False, index=False)
                    st.success("Answers submitted for Professor review!")

        elif mode == "Downloads":
            st.header("📂 Resource Library")
            st.write("Download PDFs provided by your Professor.")
            # Example Download button
            st.download_button("Download Syllabus (Sample)", "PDF Content here", "syllabus.pdf")
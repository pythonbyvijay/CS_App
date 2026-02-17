import streamlit as st
import pandas as pd
import datetime
import os
import base64
from questions import users, initial_data

# --- 1. PAGE CONFIG ---
st.set_page_config(page_title="HSC CS Portal", layout="centered")

# --- 2. UTILITY FUNCTIONS ---
def get_base64_of_bin_file(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""

def set_background(png_file):
    bin_str = get_base64_of_bin_file(png_file)
    bg_style = f'''
    <style>
    html, body, [data-testid="stAppViewContainer"] {{
        overflow: hidden !important;
        height: 100vh;
    }}
    .stApp {{
        background: url("data:image/png;base64,{bin_str}") no-repeat center center fixed;
        background-size: cover;
    }}
    [data-testid="stMainView"] {{
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }}
    .main .block-container {{
        max-width: 30% !important;
        min-width: 330px !important;
        padding: 0 !important;
        margin: auto !important;
    }}
    .login-card {{
        background: rgba(15, 25, 45, 0.75);
        backdrop-filter: blur(25px);
        -webkit-backdrop-filter: blur(25px);
        border-radius: 20px;
        border: 1px solid rgba(255, 255, 255, 0.15);
        padding: 35px;
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.9);
        text-align: center;
        width: 100%;
    }}
    .header-bar {{
        background: rgba(255, 255, 255, 0.1);
        height: 60px;
        width: 100%;
        border-radius: 12px;
        margin-bottom: 20px;
    }}
    h1, h2, h3, label, p {{ color: white !important; font-family: 'Segoe UI', sans-serif; }}
    .stTextInput label {{
        display: flex !important;
        justify-content: flex-start !important;
        font-size: 0.85em !important;
    }}
    .stTextInput input {{
        background-color: #f1f3f4 !important;
        color: #222 !important;
        border-radius: 8px !important;
        height: 42px !important;
    }}
    div.stButton > button {{
        width: 100px !important;
        background-color: #007bff !important;
        color: white !important;
        border: none !important;
        height: 40px !important;
    }}
    div.stButton {{ display: flex; justify-content: flex-start; }}
    header, footer, [data-testid="stHeader"] {{ visibility: hidden !important; }}
    </style>
    '''
    st.markdown(bg_style, unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if 'question_list' not in st.session_state:
    st.session_state.question_list = initial_data
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- 4. LOGIN INTERFACE ---
if not st.session_state.logged_in:
    set_background('background.jpg')
    
    st.markdown('<div class="login-card">', unsafe_allow_html=True)
    st.markdown('<div class="header-bar"></div>', unsafe_allow_html=True)
    
    st.markdown("""
        <div style='text-align: center; line-height: 0.75; margin-bottom: 10px;'>
            <h1 style='font-size: 2.3em; margin: 0; padding: 0; font-weight: 800; letter-spacing: -1px;'>VIREXON</h1>
            <h2 style='font-size: 1.9em; margin: 0; padding: 0; font-weight: 600;'>Intelligences</h2>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("<h3 style='font-size: 1.2em; font-weight: 400; margin-bottom: 30px;'>HSC CS Portal</h3>", unsafe_allow_html=True)

    u = st.text_input("Username", placeholder="Username")
    p = st.text_input("Password", type="password", placeholder="Password")

    if st.button("LOGIN"):
        with st.spinner("Authenticating..."):
            if u in users and users[u]["password"] == p:
                st.session_state.logged_in, st.session_state.role, st.session_state.user = True, users[u]["role"], u
                st.rerun()
            else:
                st.error("Access Denied")

    st.markdown(f'''
        <div style="margin-top: 40px; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 20px;">
            <p style="font-size: 0.75em; opacity: 0.8; margin: 0;">copyright @Vijay Shinde</p>
            <p style="font-size: 0.75em; opacity: 0.8; margin: 5px 0 0 0;">📞 +91 9730145654</p>
        </div>
    ''', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# --- 5. MAIN PORTAL CONTENT ---
else:
    st.markdown("<style>[data-testid='stMainView'] { display: block !important; } .stApp { background: #eef2ff; overflow: auto; } header { visibility: visible !important; }</style>", unsafe_allow_html=True)
    
    # --- Sidebar & Navigation ---
    st.sidebar.title(f"Welcome . {st.session_state.user.capitalize()}")
    
    if st.session_state.role == "admin":
        menu = st.sidebar.radio("Navigation", ["Add Questions", "Revision Bank", "Test Section", "Download Center"])
    else:
        menu = st.sidebar.radio("Navigation", ["Download Center"])

    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    # --- Header: Countdown ---
    exam_date = datetime.datetime(2026, 3, 10)
    days_left = (exam_date - datetime.datetime.now()).days
    st.title("🖥️ Computer Science  Portal")
    st.subheader(f"⏳ Exam Countdown: {days_left} Days")
    progress_val = int(max(0, min(100, 100 - (days_left/365)*100)))
    st.progress(progress_val, text=f"Preparation Progress: {progress_val}%")

    # --- OPTIMIZED DOWNLOAD CENTER ---
    if menu == "Download Center":
        st.header("📥 Student Download Center")
        
        resource_map = {
            "📅 1. Previous Year Question Papers": "papers",
            "📁 Chapter 1: Operating System": "Operating System Notes",
            "📁 Chapter 2: Data Structure": "Data Structure Notes",
            "📁 Chapter 3: C++": "C++ Notes",
            "📁 Chapter 4: HTML": "HTML Notes",
	    "📁 C++ Programs": "C++ Programs",
	    "📁 HTML Programs": "HTML Programs"


        }

        for label, folder_path in resource_map.items():
            # Setting expanded=False prevents the app from scanning files until clicked
            with st.expander(label, expanded=False):
                if os.path.exists(folder_path):
                    files = [f for f in os.listdir(folder_path) if f.lower().endswith(".pdf")]
                    if files:
                        for filename in files:
                            file_path = os.path.join(folder_path, filename)
                            col_name, col_view, col_dl = st.columns([0.5, 0.25, 0.25])
                            
                            with col_name:
                                st.write(f"📄 {filename}")
                            
                            # PERFORMANCE FIX: We only open the file inside the active expander
                            with open(file_path, "rb") as f:
                                pdf_bytes = f.read()
                            
                            with col_view:
                                b64 = base64.b64encode(pdf_bytes).decode('utf-8')
                                view_html = f'''<a href="data:application/pdf;base64,{b64}" target="_blank" style="text-decoration: none;"><div style="background-color: #ff4b4b; color: white; padding: 0.5rem; text-align: center; border-radius: 0.5rem; font-size: 0.8rem; font-weight: bold;">👁️ VIEW</div></a>'''
                                st.markdown(view_html, unsafe_allow_html=True)
                            
                            with col_dl:
                                st.download_button(label="💾 DOWNLOAD", data=pdf_bytes, file_name=filename, key=f"dl_{folder_path}_{filename}", use_container_width=True)
                    else:
                        st.write("No PDF files found.")
                else:
                    st.error(f"Folder '{folder_path}' not found.")
    # --- OTHER SECTIONS ---
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
                st.session_state.question_list.append({"category": cat, "question": q_text, "answer": ans})
                st.success("Question added!")

    elif menu == "Revision Bank":
        st.header("📖 Revision Bank")
        for q in st.session_state.question_list:
            with st.expander(f"{q['category']}: {q['question']}"):
                st.write(q['answer'])

    elif menu == "Test Section":
        st.header("📝 Student Practice Test")
        for idx, q in enumerate(st.session_state.question_list):
            st.write(f"**Q{idx+1}: {q['question']}**")
            st.text_area("Type Answer", key=f"test_{idx}")
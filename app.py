import streamlit as st

# =========================================
# 🔐 LOGIN CONFIG (CHANGE IF NEEDED)
# =========================================

USERNAME = "student1"
PASSWORD = "1234"

# =========================================
# 🧠 SESSION STATE
# =========================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


# =========================================
# 🔐 LOGIN PAGE WITH BACKGROUND IMAGE
# =========================================

def login_page():

    st.set_page_config(
        page_title="Login - CSD Library",
        page_icon="🔐",
        layout="centered"
    )

    # 🔥 Background Image CSS
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("background.jpg");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
        }

        .login-box {
            background: rgba(0,0,0,0.65);
            padding: 40px;
            border-radius: 15px;
            color: white;
        }

        .copyright {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: white;
            font-size: 14px;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # 🔐 Login UI
    st.markdown('<div class="login-box">', unsafe_allow_html=True)

    st.title("🔐 Login Required")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == USERNAME and password == PASSWORD:
            st.session_state.logged_in = True
            st.success("Login successful ✅")
            st.rerun()
        else:
            st.error("Invalid username or password ❌")

    st.markdown("</div>", unsafe_allow_html=True)

    # 📞 Copyright
    st.markdown(
        '<div class="copyright">© Vijay Shinde 📞 +91 9730145654</div>',
        unsafe_allow_html=True
    )


# =========================================
# 📚 MAIN APP (PDF LIBRARY)
# =========================================

def main_app():

    st.set_page_config(
        page_title="CSD PDF Library",
        page_icon="📚",
        layout="wide"
    )

    if st.button("🚪 Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("📚 CSD Question Papers & Notes")
    st.write("Fast Google Drive Based Library")

    pdfs = {
	"2014": "1EbgTIkFqA1InoTUhz3W4X5yL1J6U0ZYG",
	"2015": "1J8HPOyUZiK16147Sl5rawNka-JrrDUA_",
	"2016": "1hy4o9-bWOZnTYP2Xbz4uZittn0uUZax-",
	"2017": "1-yKGRmnWNGZQFXn463gWD8SMCrWQaeCq",
	"2018": "1FANxChrPnWIs1lBhxY5kq6emQUTYzL4a",
	"2019": "",
	"2020": "",
	"2021": "",
	"2022": "10XV1MB-yjA3OamGtjBy74tijNe1Qscu5",
	"2023": "1loXzWNSl3fCzrgWDoogR75i_KXEKGnFC",
	"2024": "1eHojj7Edyk4SBOCKS6c4gZvT1Zkvtira",
	"2025": "1GeLqO2C9JlKc5j1DGeL4JZ5e8AbU_Tyi",
	"programs": "1bbg4qUAuQRlmUzsYFegVTJwtMTg6Evp4",
        "1. Operating System": "1rDubBX_cgHA5j_GQVxSOzguLbtc9ZAD2",
        "2. Data Structure": "1NEBWa3plmhmEyykahyH2sB9YwSKxyRTa",
        "3. C++": "1LDU6oVsRRSgj-S-MdFrOuxq_VHNdjXvg",
        "4. HTML": "1CIcF7_TMKa_hkgQxgX11H8EGoJjAbmSG"
    }

    search = st.text_input("🔎 Search PDF")

    filtered = {
        name: fid for name, fid in pdfs.items()
        if search.lower() in name.lower()
    }

    if not filtered:
        st.warning("No files found")

    for name, fid in filtered.items():

        view_link = f"https://drive.google.com/file/d/{fid}/preview"
        download_link = f"https://drive.google.com/uc?id={fid}&export=download"

        st.markdown(f"### 📘 {name}")

        col1, col2 = st.columns([1, 1])

        with col1:
            st.link_button("👁️ View Full Screen", view_link)

        with col2:
            st.link_button("⬇️ Download", download_link)

        st.components.v1.iframe(view_link, height=600)

        st.divider()

    st.success("All files loaded from Google Drive ⚡")


# =========================================
# 🚀 CONTROLLER
# =========================================

if st.session_state.logged_in:
    main_app()
else:
    login_page()
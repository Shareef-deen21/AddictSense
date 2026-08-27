
import streamlit as st
from utils import inject_css, PALETTE as P

st.set_page_config(
    page_title="AddictSence Login",
    page_icon="",
    layout="centered",
    initial_sidebar_state="collapsed",
)

inject_css()

#Hide sidebar toggle
st.markdown("""
<style>
[data-testid="collapsedControl"] { display: none !important; }
.block-container { max-width: 440px !important; padding-top: 4rem !important; }
</style>
""", unsafe_allow_html=True)

#If already logged in, skip to predict
if st.session_state.get("authenticated"):
    st.switch_page("pages/3_Predict.py")

#Logo
st.markdown(f"""
<div style="text-align:center;margin-bottom:2.5rem;">
    <div style="font-family:'Space Grotesk',sans-serif;font-size:1.8rem;
                font-weight:800;color:{P['white']};letter-spacing:-0.02em;">
        Addict<span style="color:{P['primary_lt']};">Sence</span>
    </div>
    <div style="color:{P['muted']};font-size:0.88rem;margin-top:0.3rem;">
        Sign in to access the prediction system
    </div>
</div>
""", unsafe_allow_html=True)

#Demo credentials hint
st.markdown(f"""
<div style="background:{P['primary']}15;border:1px solid {P['primary']}33;
            border-radius:10px;padding:0.7rem 1rem;margin-bottom:1.4rem;
            font-size:0.82rem;color:{P['primary_lt']};">
    <strong>Demo credentials</strong><br>
    Username: <code style="background:{P['surface']};padding:0.1rem 0.35rem;
    border-radius:4px;">admin</code> &nbsp; Password: <code style="background:{P['surface']};
    padding:0.1rem 0.35rem;border-radius:4px;">addictsense2026</code>
</div>
""", unsafe_allow_html=True)

#Form
username = st.text_input("Username", placeholder="Enter your username", key="login_user")
password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_pass")

# Validation state
errors = []
if "login_attempted" not in st.session_state:
    st.session_state.login_attempted = False

col_login, _ = st.columns([1, 0.01])
with col_login:
    login_clicked = st.button("Sign In →", use_container_width=True)

if login_clicked:
    st.session_state.login_attempted = True
    errors = []

    # Input validation
    if not username.strip():
        errors.append("Username is required.")
    if not password:
        errors.append("Password is required.")

    if not errors:
        VALID_USERS = {
            "admin": "addictsense2026",
            "shareef": "shareef2026",
            "demo": "demo123",
        }
        if username.strip().lower() in VALID_USERS and password == VALID_USERS[username.strip().lower()]:
            st.session_state.authenticated = True
            st.session_state.username = username.strip()
            st.switch_page("pages/3_Predict.py")
        else:
            errors.append("Incorrect username or password. Please try again.")

    if errors:
        for err in errors:
            st.markdown(f'<div class="as-error">{err}</div>', unsafe_allow_html=True)
            st.markdown("<div style='margin-top:0.4rem;'></div>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

#Back to home
st.markdown(f"""
<div style="text-align:center;margin-top:1.2rem;">
    <a href="/" target="_self"
       style="color:{P['muted']};font-size:0.85rem;text-decoration:none;">
        ← Back to Home
    </a>
</div>
""", unsafe_allow_html=True)

#Footer note
st.markdown(f"""
<div style="text-align:center;margin-top:3rem;color:{P['border']};font-size:0.75rem;">
    AddiSence | Social Media Addiction Prediction System | 2026
</div>
""", unsafe_allow_html=True)

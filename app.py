import streamlit as st
import json
import os

# ================= PAGE CONFIG =================
st.set_page_config(
    page_title="Reservation System",
    page_icon="✈️",
    layout="wide"
)

# ================= STYLES =================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:wght@400;600;700&family=Jost:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'Jost', sans-serif;
}

.stApp {
    background: #0a0a0a;
}

/* Hide default streamlit elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 0 !important; max-width: 100% !important; }

/* ---- TOP BAR ---- */
.topbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #d0d0d0;
    padding: 0 24px;
    height: 60px;
    border-bottom: 1px solid #aaa;
}
.topbar-home { font-weight: 700; color: black; font-size: 14px; letter-spacing: 2px; }
.topbar-title { font-weight: 700; color: black; font-size: 15px; letter-spacing: 3px; }
.topbar-menu { font-size: 26px; color: black; cursor: pointer; }

/* ---- HERO ---- */
.hero-section {
    position: relative;
    width: 100%;
    min-height: 380px;
    background: linear-gradient(135deg, #1a3a2a 0%, #0d1f17 40%, #162d22 70%, #0a1a10 100%);
    display: flex;
    align-items: center;
    overflow: hidden;
}

.hero-section::before {
    content: '';
    position: absolute;
    inset: 0;
    background:
        radial-gradient(ellipse at 20% 50%, rgba(65,166,126,0.15) 0%, transparent 60%),
        radial-gradient(ellipse at 80% 20%, rgba(65,166,126,0.08) 0%, transparent 50%);
}

.hero-section::after {
    content: '';
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(65,166,126,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(65,166,126,0.03) 1px, transparent 1px);
    background-size: 60px 60px;
}

.hero-content {
    position: relative;
    z-index: 2;
    padding: 60px 60px;
    background: rgba(0,0,0,0.45);
    border-radius: 18px;
    margin: 40px 60px;
    border: 1px solid rgba(65,166,126,0.2);
    backdrop-filter: blur(4px);
}

.hero-line1 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 52px;
    font-weight: 700;
    color: white;
    line-height: 1.1;
    margin: 0;
}

.hero-line2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 34px;
    font-weight: 400;
    color: rgba(255,255,255,0.85);
    line-height: 1.3;
    margin: 4px 0 0 0;
}

.hero-line3 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 34px;
    font-weight: 400;
    color: rgba(255,255,255,0.85);
    line-height: 1.3;
    margin: 0;
}

/* ---- ACCENT DOTS ---- */
.dot-grid {
    position: absolute;
    right: 80px;
    top: 50%;
    transform: translateY(-50%);
    display: grid;
    grid-template-columns: repeat(5, 12px);
    gap: 14px;
    opacity: 0.25;
    z-index: 2;
}
.dot { width: 4px; height: 4px; background: #41A67E; border-radius: 50%; }

/* ---- BOTTOM FORM ---- */
.bottom-bar {
    background: #d9d9d9;
    border-top: 1px solid #aaa;
    padding: 20px 24px;
}

.bottom-bar-title {
    font-size: 11px;
    letter-spacing: 3px;
    color: #555;
    text-transform: uppercase;
    margin-bottom: 12px;
    font-weight: 500;
}

/* Input fields */
.stTextInput > div > div > input {
    background: #bfbfbf !important;
    color: black !important;
    border-radius: 10px !important;
    border: none !important;
    padding: 10px 14px !important;
    font-family: 'Jost', sans-serif !important;
}

.stTextInput > div > div > input::placeholder {
    color: #555 !important;
}

.stTextInput > label {
    color: #333 !important;
    font-size: 12px !important;
    letter-spacing: 1px !important;
    font-weight: 500 !important;
}

/* Button */
.stButton > button {
    background: #41A67E !important;
    color: black !important;
    border-radius: 17px !important;
    border: none !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    padding: 10px 28px !important;
    font-family: 'Jost', sans-serif !important;
    width: 100% !important;
    margin-top: 22px !important;
    transition: all 0.2s !important;
}

.stButton > button:hover {
    background: #35896a !important;
    transform: translateY(-1px) !important;
}

/* Success/error messages */
.success-msg {
    background: rgba(65,166,126,0.15);
    border: 1px solid #41A67E;
    border-radius: 10px;
    padding: 12px 20px;
    color: #41A67E;
    font-size: 14px;
    margin-top: 10px;
    letter-spacing: 1px;
}

.error-msg {
    background: rgba(220,80,80,0.1);
    border: 1px solid #dc5050;
    border-radius: 10px;
    padding: 12px 20px;
    color: #dc5050;
    font-size: 14px;
    margin-top: 10px;
}

/* Menu sidebar */
.menu-item {
    display: block;
    padding: 12px 20px;
    color: #333;
    font-size: 14px;
    letter-spacing: 1px;
    border-bottom: 1px solid #ddd;
    cursor: pointer;
    transition: background 0.2s;
}
.menu-item:hover { background: #e0e0e0; }
</style>
""", unsafe_allow_html=True)

# ================= DATABASE =================
DB_PATH = os.path.join(os.path.dirname(__file__), "database.json")

def load_db():
    if os.path.exists(DB_PATH):
        with open(DB_PATH, "r") as f:
            return json.load(f)
    return {"users": [], "reservations": []}

def save_db(db):
    with open(DB_PATH, "w") as f:
        json.dump(db, f, indent=4)

# ================= SESSION STATE =================
if "menu_open" not in st.session_state:
    st.session_state.menu_open = False
if "saved" not in st.session_state:
    st.session_state.saved = False
if "error" not in st.session_state:
    st.session_state.error = ""

# ================= TOP BAR =================
st.markdown("""
<div class="topbar">
    <span class="topbar-home">HOME</span>
    <span class="topbar-title">RESERVATION SYSTEM</span>
    <span class="topbar-menu">≡</span>
</div>
""", unsafe_allow_html=True)

# ================= LAYOUT =================
if st.session_state.menu_open:
    col_main, col_menu = st.columns([4, 1])
else:
    col_main = st.container()
    col_menu = None

with col_main:
    # ---- HERO ----
    dots = '<div class="dot-grid">' + '<div class="dot"></div>' * 25 + '</div>'
    st.markdown(f"""
    <div class="hero-section">
        {dots}
        <div class="hero-content">
            <p class="hero-line1">Take a journey</p>
            <p class="hero-line2">Into the world of an</p>
            <p class="hero-line3">incredible destinations.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ---- FORM ----
    st.markdown('<div class="bottom-bar">', unsafe_allow_html=True)
    st.markdown('<div class="bottom-bar-title">Sign up to get started</div>', unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns([3, 3, 3, 1.5])

    with c1:
        name = st.text_input("", placeholder="Full name", key="name", label_visibility="collapsed")
    with c2:
        phone = st.text_input("", placeholder="Phone Number", key="phone", label_visibility="collapsed")
    with c3:
        email = st.text_input("", placeholder="Email", key="email", label_visibility="collapsed")
    with c4:
        signup = st.button("SIGN UP")

    if signup:
        if not name or not phone or not email:
            st.session_state.error = "Please fill in all fields."
            st.session_state.saved = False
        else:
            db = load_db()
            db["users"].append({"name": name, "phone": phone, "email": email})
            save_db(db)
            st.session_state.saved = True
            st.session_state.error = ""
            st.rerun()

    if st.session_state.saved:
        st.markdown('<div class="success-msg">✓ &nbsp; You\'re in! Welcome aboard.</div>', unsafe_allow_html=True)
    if st.session_state.error:
        st.markdown(f'<div class="error-msg">⚠ &nbsp; {st.session_state.error}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ================= MENU TOGGLE =================
st.markdown("---")
toggle_label = "✕ Close Menu" if st.session_state.menu_open else "≡ Open Menu"
if st.button(toggle_label, key="menu_toggle"):
    st.session_state.menu_open = not st.session_state.menu_open
    st.rerun()

if col_menu and st.session_state.menu_open:
    with col_menu:
        st.markdown("""
        <div style="background:#eee; padding:10px; border-radius:10px; margin-top:10px;">
            <div class="menu-item">🏠 Home</div>
            <div class="menu-item">📅 Reservations</div>
            <div class="menu-item">⚙️ Settings</div>
        </div>
        """, unsafe_allow_html=True)
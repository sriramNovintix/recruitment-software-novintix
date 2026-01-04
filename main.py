"""
TalentMatch - AI-Powered Recruitment Platform
Main entry point with landing page, authentication, and app routing
"""
import streamlit as st

# Initialize ConfigManager FIRST before any other imports that need it
from core.config_manager import ConfigManager
# This ensures GROQ_API_KEY is loaded before llm_client module initializes

from core.auth import create_user, authenticate_user, get_user_by_id

# Page configuration
st.set_page_config(
    page_title="TalentMatch - Find the best candidates, faster",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎯"
)

def load_landing_css():
    st.markdown("""
    <style>
        /* Hide Streamlit default elements for landing page */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
        /* Remove default Streamlit padding/margin */
        .block-container {
            padding-top: 0 !important;
            padding-bottom: 0 !important;
        }
        
        /* Reset and base styles */
        .stApp {
            background: #ffffff;
        }
        
        /* Custom fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        
        * {
            font-family: 'Inter', sans-serif;
        }
        
        /* Navigation Bar - Keep it fixed */
        .navbar {
            display: grid;
            grid-template-columns: 1fr auto 1fr;
            align-items: center;
            padding: 1rem 4rem;
            background: white;
            border-bottom: 1px solid #eee;
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            z-index: 1000;
            height: 70px;
        }
        
        .nav-brand {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
        }
        
        .nav-links {
            display: flex;
            gap: 2rem;
            align-items: center;
            justify-content: center;
        }
        
        .nav-link {
            color: #666;
            text-decoration: none;
            font-weight: 500;
            font-size: 0.95rem;
            transition: color 0.2s;
            cursor: pointer;
        }
        
        .nav-link:hover {
            color: #3b82f6;
        }
        
        .nav-buttons {
            display: flex;
            gap: 1rem;
            align-items: center;
            justify-self: end;
        }
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 4rem 2rem 2rem;
            background: linear-gradient(180deg, #f0f7ff 0%, #ffffff 100%);
            margin-top: 70px;
        }
        
        .hero-title {
            font-size: 2.8rem;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 1rem;
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: 1.1rem;
            color: #666;
            max-width: 600px;
            margin: 0 auto 1.5rem;
            line-height: 1.6;
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 2rem;
        }
        
        .btn-primary {
            background: #3b82f6;
            color: white;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            transition: all 0.2s;
            text-decoration: none;
        }
        
        .btn-primary:hover {
            background: #2563eb;
            transform: translateY(-2px);
            box-shadow: 0 10px 25px rgba(59, 130, 246, 0.3);
        }
        
        .btn-secondary {
            background: white;
            color: #333;
            padding: 1rem 2rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            border: 1px solid #ddd;
            cursor: pointer;
            transition: all 0.2s;
            text-decoration: none;
        }
        
        .btn-secondary:hover {
            border-color: #3b82f6;
            color: #3b82f6;
        }
        
        /* Stats Section */
        .stats-section {
            display: flex;
            justify-content: center;
            gap: 4rem;
            padding: 2rem 2rem;
            border-top: 1px solid #eee;
            border-bottom: 1px solid #eee;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 0.3rem;
        }
        
        .stat-label {
            color: #888;
            font-size: 0.9rem;
        }
        
        /* How It Works Section */
        .hiw-section {
            padding: 3rem 2rem;
            text-align: center;
        }
        
        .hiw-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 2rem;
        }
        
        .hiw-grid {
            display: flex;
            justify-content: center;
            gap: 3rem;
            flex-wrap: wrap;
            max-width: 1000px;
            margin: 0 auto;
        }
        
        .hiw-card {
            text-align: center;
            padding: 1.5rem;
            max-width: 200px;
        }
        
        .hiw-icon {
            width: 60px;
            height: 60px;
            background: #eff6ff;
            border-radius: 15px;
            display: flex;
            align-items: center;
            justify-content: center;
            margin: 0 auto 1rem;
            font-size: 1.5rem;
            color: #3b82f6;
        }
        
        .hiw-card-title {
            font-weight: 600;
            color: #1a1a1a;
            margin-bottom: 0.5rem;
            font-size: 1.1rem;
        }
        
        .hiw-card-desc {
            color: #888;
            font-size: 0.9rem;
            line-height: 1.5;
        }
        
        /* ========================================
           AUTH PAGE STYLES - Clean Modern Design
           ======================================== */
        
        /* Auth page background */
        .auth-page-bg {
            min-height: 100vh;
            background: linear-gradient(135deg, #f5f7ff 0%, #e8f0fe 100%);
            padding: 2rem;
        }
        
        /* Auth container - white card */
        .auth-container {
            max-width: 420px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: white;
            border-radius: 16px;
            box-shadow: 0 4px 25px rgba(0,0,0,0.08);
        }
        
        .auth-brand {
            text-align: center;
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 1.5rem;
        }
        
        .auth-title {
            font-size: 1.5rem;
            font-weight: 700;
            color: #1a1a1a !important;
            text-align: center;
            margin-bottom: 0.5rem;
        }
        
        .auth-subtitle {
            color: #888 !important;
            text-align: center;
            margin-bottom: 2rem;
            font-size: 0.95rem;
        }
        
        .form-label {
            font-weight: 500;
            color: #333 !important;
            font-size: 0.9rem;
            margin-bottom: 0.5rem;
            display: block;
        }
        
        /* Force all labels and text to be dark */
        label, .stMarkdown p, .stMarkdown span {
            color: #1a1a1a !important;
        }
        
        /* Streamlit input labels */
        .stTextInput label, .stSelectbox label {
            color: #1a1a1a !important;
        }
        
        /* FIX: Input field styling - Light background */
        .stTextInput > div > div > input {
            padding: 0.75rem 1rem !important;
            padding-left: 2.5rem !important;
            border: 1.5px solid #e0e0e0 !important;
            border-radius: 10px !important;
            font-size: 0.95rem !important;
            transition: all 0.2s !important;
            background-color: #ffffff !important;
            color: #1a1a1a !important;
            caret-color: #3b82f6 !important;
        }
        
        /* Disabled input text color fix */
        .stTextInput > div > div > input:disabled {
            background-color: #f5f5f5 !important;
            color: #1a1a1a !important;
            -webkit-text-fill-color: #1a1a1a !important;
            opacity: 1 !important;
            cursor: not-allowed !important;
        }
        
        /* Force black text in disabled inputs */
        input[disabled] {
            color: #1a1a1a !important;
            -webkit-text-fill-color: #1a1a1a !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            background-color: #ffffff !important;
        }
        
        /* Input container styling */
        .stTextInput > div {
            background: transparent !important;
        }
        
        .stTextInput > div > div {
            background: transparent !important;
        }
        
        /* Password input toggle button fix */
        .stTextInput button {
            background: transparent !important;
            border: none !important;
            color: #666 !important;
        }
        
        .auth-link {
            text-align: center;
            margin-top: 1.5rem;
            color: #666 !important;
            font-size: 0.9rem;
        }
        
        .auth-link a {
            color: #3b82f6 !important;
            text-decoration: none;
            font-weight: 500;
        }
        
        .auth-link a:hover {
            text-decoration: underline;
        }
        
        /* Override Streamlit button for auth pages */
        .stButton > button {
            width: 100%;
            background: #3b82f6 !important;
            color: white !important;
            padding: 0.75rem 1.5rem;
            border-radius: 10px;
            font-weight: 600;
            font-size: 1rem;
            border: none;
            cursor: pointer;
            transition: all 0.2s;
            margin-top: 0.5rem;
        }
        
        .stButton > button:hover {
            background: #2563eb !important;
            transform: translateY(-1px);
        }
        
        /* Bottom CTA buttons styling */
        button[key="bottom_signin"] {
            padding: 0.9rem 2rem !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
        }
        
        button[key="bottom_getstarted"] {
            padding: 0.9rem 2rem !important;
            font-size: 1.05rem !important;
            font-weight: 600 !important;
            border-radius: 12px !important;
            transition: all 0.3s ease !important;
            box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3) !important;
        }
        
        button[key="bottom_getstarted"]:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.4) !important;
        }
        
        /* Secondary button style */
        .stButton > button[kind="secondary"] {
            background: white !important;
            color: #333 !important;
            border: 1.5px solid #e0e0e0 !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
            background: #f8fafc !important;
        }
        
        /* Hide sidebar on landing/auth pages */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Form styling */
        [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        /* Error/Success messages */
        .stAlert {
            border-radius: 10px !important;
        }
        
        [data-testid="stSuccess"] {
            background: #dcfce7 !important;
            color: #166534 !important;
        }
        
        [data-testid="stError"] {
            background: #fee2e2 !important;
            color: #dc2626 !important;
        }
    </style>
    """, unsafe_allow_html=True)
def show_landing_page():
    """Display the landing page"""
    
    # Top navigation bar HTML - simple without buttons
    st.markdown("""
    <!-- Navigation Bar -->
    <div class="navbar">
        <div class="nav-brand">TalentMatch</div>
        <div class="nav-links">
            <span class="nav-link">Features</span>
            <span class="nav-link">How It Works</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Hero Section and rest of the page
    st.markdown("""
    <!-- Hero Section -->
    <div class="hero-section">
        <h1 class="hero-title">Find the best candidates,<br>faster</h1>
        <p class="hero-subtitle">
            Upload resumes, match against job descriptions, and get ranked candidates with AI-powered insights.
        </p>
    </div>
    
    <!-- Stats Section -->
    <div class="stats-section">
        <div class="stat-item">
            <div class="stat-value">95%</div>
            <div class="stat-label">Accuracy Rate</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">10x</div>
            <div class="stat-label">Faster Screening</div>
        </div>
        <div class="stat-item">
            <div class="stat-value">500+</div>
            <div class="stat-label">Companies Trust Us</div>
        </div>
    </div>
    
    <!-- How It Works Section -->
    <div class="hiw-section" id="how-it-works">
        <h2 class="hiw-title">How It Works</h2>
        <div class="hiw-grid">
            <div class="hiw-card">
                <div class="hiw-icon">📝</div>
                <div class="hiw-card-title">Create Job</div>
                <div class="hiw-card-desc">Add your job description or pick a template</div>
            </div>
            <div class="hiw-card">
                <div class="hiw-icon">📤</div>
                <div class="hiw-card-title">Upload Resumes</div>
                <div class="hiw-card-desc">Bulk upload up to 20 resumes at once</div>
            </div>
            <div class="hiw-card">
                <div class="hiw-icon">⚡</div>
                <div class="hiw-card-title">AI Analysis</div>
                <div class="hiw-card-desc">Instant scoring and candidate ranking</div>
            </div>
            <div class="hiw-card">
                <div class="hiw-icon">👥</div>
                <div class="hiw-card-title">Review & Hire</div>
                <div class="hiw-card-desc">Shortlist candidates with feedback</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Call to Action Buttons Section - Below How It Works
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.5, 1.5, 2])
    
    with col2:
        if st.button("🔐 Sign In", key="bottom_signin", use_container_width=True, type="secondary"):
            st.session_state.page = "signin"
            
    
    with col4:
        if st.button("🚀 Get Started Free", key="bottom_getstarted", use_container_width=True, type="primary"):
            st.session_state.page = "signup"
            
    
    # Footer
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 2rem 2rem; background: #f8f9fa; margin-top: 2rem; border-top: 1px solid #eee;'>
        <p style='color: #888; font-size: 0.9rem; margin: 0;'>
            © 2024 TalentMatch. All rights reserved.
        </p>
        <p style='color: #aaa; font-size: 0.8rem; margin-top: 0.5rem;'>
            AI-Powered Recruitment Platform
        </p>
    </div>
    """, unsafe_allow_html=True)

def show_auth_page():
    """Display unified auth page with Login/Signup tabs"""
    
    # Initialize auth tab state based on current page
    # Always sync with page state to ensure correct tab is shown
    if st.session_state.get("page") == "signin":
        if "auth_tab" not in st.session_state or st.session_state.auth_tab != "login":
            st.session_state.auth_tab = "login"
    elif st.session_state.get("page") == "signup":
        if "auth_tab" not in st.session_state or st.session_state.auth_tab != "signup":
            st.session_state.auth_tab = "signup"
    elif "auth_tab" not in st.session_state:
        st.session_state.auth_tab = "login"
    
    # Apply purple gradient background and styling
    st.markdown("""
    <style>
        /* Purple gradient background */
        .stApp {
            background: linear-gradient(180deg, #e8dff5 0%, #d4c4e8 100%) !important;
            min-height: 100vh;
        }
        
        /* Hide sidebar */
        [data-testid="stSidebar"] {
            display: none;
        }
        
        /* Hide default header background */
        header[data-testid="stHeader"] {
            background: transparent !important;
        }
        
        /* Make all Streamlit blocks transparent to remove stray white boxes */
        [data-testid="stVerticalBlockBorderWrapper"],
        [data-testid="stHorizontalBlock"],
        .stColumn > div {
            background: transparent !important;
            box-shadow: none !important;
            border: none !important;
        }

        /* Auth box container */
        .auth-box {
            background: white;
            border-radius: 20px;
            padding: 2rem 1.8rem;
            box-shadow: 0 15px 50px rgba(0,0,0,0.12);
            margin-top: 1rem;
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            border: 1.5px solid #e5e7eb !important;
            border-radius: 10px !important;
            padding: 12px 16px !important;
            font-size: 0.95rem !important;
            background: #f9fafb !important;
            color: #333 !important;
            caret-color: #3b82f6 !important;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: #3b82f6 !important;
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1) !important;
            background: white !important;
        }
        
        .stTextInput > div > div > input::placeholder {
            color: #9ca3af !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            border-radius: 10px !important;
        }
        
        .stSelectbox [data-baseweb="select"] > div {
            border: 1.5px solid #e5e7eb !important;
            border-radius: 10px !important;
            background: #f9fafb !important;
            cursor: pointer !important;
        }
        
        /* Submit button in form */
        [data-testid="stForm"] .stButton > button {
            background: #3b82f6 !important;
            color: white !important;
            border-radius: 10px !important;
            padding: 14px 24px !important;
            font-weight: 600 !important;
            font-size: 1rem !important;
            border: none !important;
            width: 100%;
            margin-top: 1rem;
            transition: all 0.3s ease !important;
        }
        
        [data-testid="stForm"] .stButton > button:hover {
            background: #2563eb !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 6px 20px rgba(59, 130, 246, 0.35) !important;
        }
        
        /* Hide form border */
        [data-testid="stForm"] {
            background: transparent !important;
            border: none !important;
            padding: 0 !important;
        }
        
        
        /* Tab button styling - ensure colors change properly */
        div[data-testid="column"] .stButton > button {
            border-radius: 8px !important;
            transition: all 0.2s ease !important;
        }
        
        /* Primary tab button (active) */
        div[data-testid="column"] .stButton > button[kind="primary"] {
            background: #3b82f6 !important;
            color: white !important;
            border: none !important;
        }
        
        /* Secondary tab button (inactive) */
        div[data-testid="column"] .stButton > button[kind="secondary"] {
            background: white !important;
            color: #1a1a1a !important;
            border: 1.5px solid #e5e7eb !important;
        }
        
        div[data-testid="column"] .stButton > button[kind="secondary"]:hover {
            border-color: #3b82f6 !important;
            color: #3b82f6 !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Centered narrow container
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        
        # Lock icon
        st.markdown("""
        <div style="text-align: center; margin-bottom: 1rem;">
            <div style="width: 55px; height: 55px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        border-radius: 14px; display: inline-flex; align-items: center; justify-content: center;">
                <span style="font-size: 1.5rem; color: white;">🔒</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Welcome title - dynamic based on tab
        if st.session_state.auth_tab == "login":
            st.markdown("""
            <h2 style="font-size: 1.6rem; font-weight: 700; color: #1a1a1a; text-align: center; margin-bottom: 0.3rem;">Welcome Back</h2>
            <p style="color: #666; text-align: center; font-size: 0.9rem; margin-bottom: 1.2rem;">Please enter your details to sign in.</p>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <h2 style="font-size: 1.6rem; font-weight: 700; color: #1a1a1a; text-align: center; margin-bottom: 0.3rem;">Create Account</h2>
            <p style="color: #666; text-align: center; font-size: 0.9rem; margin-bottom: 1.2rem;">Please enter your details to sign up.</p>
            """, unsafe_allow_html=True)
        
        # Tab toggle buttons
        tab_col1, tab_col2 = st.columns(2)
        with tab_col1:
            login_type = "primary" if st.session_state.auth_tab == "login" else "secondary"
            login_clicked = st.button("Login", key="tab_login", type=login_type, use_container_width=True)
        with tab_col2:
            signup_type = "primary" if st.session_state.auth_tab == "signup" else "secondary"
            signup_clicked = st.button("Signup", key="tab_signup", type=signup_type, use_container_width=True)
        
        # Handle tab switching without rerun
        if login_clicked and st.session_state.auth_tab != "login":
            st.session_state.auth_tab = "login"
        if signup_clicked and st.session_state.auth_tab != "signup":
            st.session_state.auth_tab = "signup"
        
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        
        # ============ LOGIN FORM ============
        if st.session_state.auth_tab == "login":
            # Initialize session state for login fields
            if "login_email" not in st.session_state:
                st.session_state.login_email = ""
            if "login_password" not in st.session_state:
                st.session_state.login_password = ""
            
            st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem;">Email Address</p>', unsafe_allow_html=True)
            email = st.text_input("email_login", placeholder="you@example.com", label_visibility="collapsed", key="login_email_input", value=st.session_state.login_email)
            
            st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Password</p>', unsafe_allow_html=True)
            password = st.text_input("password_login", type="password", placeholder="••••••••", label_visibility="collapsed", key="login_password_input", value=st.session_state.login_password)
            
            st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
            
            if st.button("Sign in", use_container_width=True, type="primary", key="login_submit_btn"):
                # Update session state
                st.session_state.login_email = email
                st.session_state.login_password = password
                
                if not email or not password:
                    st.error("Please fill in all fields")
                else:
                    result = authenticate_user(email, password)
                    if result["success"]:
                        st.session_state.authenticated = True
                        st.session_state.user = result["user"]
                        st.session_state.page = "app"
                        # Clear login fields
                        st.session_state.login_email = ""
                        st.session_state.login_password = ""
                        st.success("Login successful!")
                        
                    else:
                        st.error(result["message"])
        
        # ============ SIGNUP FORM ============
        else:
            with st.form("signup_form", clear_on_submit=False):
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem;">Full Name</p>', unsafe_allow_html=True)
                full_name = st.text_input("full_name_signup", placeholder="John Doe", label_visibility="collapsed")
                
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Email Address</p>', unsafe_allow_html=True)
                email = st.text_input("email_signup", placeholder="you@example.com", label_visibility="collapsed")
                
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Organization</p>', unsafe_allow_html=True)
                # Disabled text input with Novintix pre-filled
                organization = st.text_input("org_signup", value="Novintix", label_visibility="collapsed", disabled=True)
                
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Password</p>', unsafe_allow_html=True)
                password = st.text_input("password_signup", type="password", placeholder="••••••••", label_visibility="collapsed")
                
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Confirm Password</p>', unsafe_allow_html=True)
                confirm_password = st.text_input("confirm_password_signup", type="password", placeholder="••••••••", label_visibility="collapsed")
                
                submitted = st.form_submit_button("Sign up", use_container_width=True)
                
                if submitted:
                    if not full_name or not email or not password or not confirm_password:
                        st.error("Please fill in all fields")
                    elif password != confirm_password:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    else:
                        result = create_user(full_name, email, password, "Novintix")
                        if result["success"]:
                            st.success("Account created successfully! Please login.")
                            st.session_state.auth_tab = "login"
                        else:
                            st.error(result["message"])
        
        # Back to home button
        st.markdown("<div style='margin-top: 1rem;'></div>", unsafe_allow_html=True)
        if st.button("← Back to Home", key="back_home_auth", use_container_width=True, type="secondary"):
            st.session_state.page = "landing"
        
        # Footer inside the card
        st.markdown("""
        <div style="text-align: center; color: #888; font-size: 0.75rem; margin-top: 1.5rem;">
            © 2024 Secure Login System. All rights reserved.
        </div>
        """, unsafe_allow_html=True)



def show_main_app():
    """Show the main application (importing from app.py logic)"""
    # Import app modules
    import uuid
    from datetime import datetime
    from core.config_manager import ConfigManager
    from core.db import (
        init_db, save_jd, save_resume, save_evaluation,
        get_jds, get_resumes_by_jd, get_evaluations_by_jd,
        get_unreviewed_resumes_by_jd, get_evaluations_by_jd_and_tier,
        mark_resume_reviewed, get_jd_by_title, get_total_resumes_count,
        get_average_match_score, get_job_stats, delete_job_and_related_data
    )
    from core.utils import extract_text
    from core.jd_parser import parse_jd
    from core.resume_parser import parse_resume
    from core.scorer import score_resume, assign_candidate_tier
    
    # Override landing page CSS to show sidebar
    st.markdown("""
    <style>
        /* Show sidebar for main app */
        [data-testid="stSidebar"] {
            display: block !important;
        }
        
        /* Ensure proper sidebar styling */
        section[data-testid="stSidebar"] {
            background-color: #f8f9fa;
        }
        
        /* Disabled input text color fix for main app */
        .stTextInput > div > div > input:disabled {
            background-color: #f5f5f5 !important;
            color: #1a1a1a !important;
            -webkit-text-fill-color: #1a1a1a !important;
            opacity: 1 !important;
            cursor: not-allowed !important;
        }
        
        /* Force black text in disabled inputs */
        input[disabled] {
            color: #1a1a1a !important;
            -webkit-text-fill-color: #1a1a1a !important;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Load custom CSS for app
    try:
        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass
    
    db = init_db()
    user = st.session_state.user
    org_id = user["user_id"]  # Using user_id as org_id
    
    # ---------------- SIDEBAR ----------------
    with st.sidebar:
        # User/Organization Info
        st.markdown(
            f"""
            <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1rem; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        border-radius: 12px; color: white;'>
                <div style='font-size: 2.5rem; margin-bottom: 0.5rem;'>🏢</div>
                <h3 style='color: white; margin: 0; font-size: 1rem;'>{user['organization']}</h3>
                <p style='color: rgba(255,255,255,0.8); font-size: 0.8rem; margin-top: 0.3rem;'>{user['email']}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        st.markdown("---")
        
        st.markdown("### 🎯 Navigation")
        
        page = st.radio(
            "Choose a page",
            ["📊 Dashboard", "➕ Create Job"],
            label_visibility="collapsed",
            key="main_nav_radio"
        )
            
        
        st.markdown("---")
        
        # Logout button
        if st.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user = None
            st.session_state.page = "landing"
            
            
        
        # Footer Info
        st.markdown(
            """
            <div style='text-align: center; padding: 1rem; margin-top: 2rem; color: #888; font-size: 0.75rem;'>
                <p style='margin: 0;'>💡 Tip: Upload JD first,<br/>then add resumes</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    
    # Clean page names for logic
    page = page.split(" ", 1)[1] if " " in page else page
    
    # ---------------- HEADER ----------------
    st.markdown(
        f"""
        <div style='text-align: center; padding: 0.5rem 0 0.8rem 0; margin-bottom: 0.5rem;'>
            <h1 style='font-size: 2rem; font-weight: 800; margin-bottom: 0.2rem; 
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;'>
                Resume Evaluation System
            </h1>
            <p style='font-size: 0.9rem; color: #666; margin: 0; font-weight: 500;'>
                🤖 AI-Powered Candidate Assessment
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # Initialize session state for navigation
    if "selected_job_id" not in st.session_state:
        st.session_state.selected_job_id = None
    if "job_view_tab" not in st.session_state:
        st.session_state.job_view_tab = "Overview"
    
    # ===================================================== 
    # DASHBOARD — LANDING PAGE WITH JOB CARDS
    # ===================================================== 
    if page == "Dashboard" and (not "selected_job_id" in st.session_state or not st.session_state.selected_job_id):
        # Get dashboard statistics
        try:
            jds_list = get_jds(org_id=org_id)
            total_jds = len(jds_list)
            total_resumes = get_total_resumes_count(org_id=org_id)
            avg_score = get_average_match_score(org_id=org_id)
            job_stats = get_job_stats(org_id=org_id)
            
        except Exception as e:
            st.error(f"Error fetching dashboard data: {str(e)}")
            total_jds = 0
            total_resumes = 0
            avg_score = 0.0
            job_stats = []
        
        # Stats Cards
        st.markdown("### 📊 Overview")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            padding: 1.2rem; border-radius: 12px; text-align: center; 
                            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
                    <div style='color: white; font-size: 0.8rem; font-weight: 600; 
                                opacity: 0.9; margin-bottom: 0.3rem;'>📄 Active Jobs</div>
                    <div style='color: white; font-size: 2rem; font-weight: 800;'>{total_jds}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col2:
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            padding: 1.2rem; border-radius: 12px; text-align: center; 
                            box-shadow: 0 4px 15px rgba(240, 147, 251, 0.3);'>
                    <div style='color: white; font-size: 0.8rem; font-weight: 600; 
                                opacity: 0.9; margin-bottom: 0.3rem;'>👥 Total Resumes</div>
                    <div style='color: white; font-size: 2rem; font-weight: 800;'>{total_resumes}</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        with col3:
            st.markdown(
                f"""
                <div style='background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                            padding: 1.2rem; border-radius: 12px; text-align: center; 
                            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);'>
                    <div style='color: white; font-size: 0.8rem; font-weight: 600; 
                                opacity: 0.9; margin-bottom: 0.3rem;'>📈 Avg Match Score</div>
                    <div style='color: white; font-size: 2rem; font-weight: 800;'>{avg_score}%</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Your Jobs Section - CLICKABLE CARDS
        st.markdown("### 💼 Your Jobs")
        
        if job_stats:
            for job in job_stats:
                # Get full job details for location and experience
                full_job = next((jd for jd in jds_list if jd["jd_id"] == job["jd_id"]), None)
                
                # Calculate days ago
                if job.get("created_at"):
                    now = datetime.utcnow()
                    created = job["created_at"]
                    days_ago = (now - created).days
                    
                    if days_ago == 0:
                        time_str = "Today"
                    elif days_ago == 1:
                        time_str = "1 day ago"
                    else:
                        time_str = f"{days_ago} days ago"
                else:
                    time_str = "N/A"
                
                # Get location and experience
                location = full_job.get("location", "Not specified") if full_job else "Not specified"
                experience_req = "Not specified"
                if full_job and "parsed_jd_json" in full_job:
                    experience_req = full_job["parsed_jd_json"].get("experience_required", "Not specified")
                
                # Clickable Job card
                col_card, col_button = st.columns([5, 1])
                
                with col_card:
                    st.markdown(
                        f"""
                        <div style='background: white; padding: 1rem 1.5rem; border-radius: 12px; 
                                    margin-bottom: 0.8rem; box-shadow: 0 2px 10px rgba(0,0,0,0.06); 
                                    border-left: 4px solid #667eea;'>
                            <div style='display: flex; justify-content: space-between; align-items: center;'>
                                <div>
                                    <h3 style='margin: 0; color: #1a1a1a; font-size: 1.1rem;'>
                                        📋 {job["role"]}
                                    </h3>
                                    <p style='margin: 0.3rem 0 0 0; color: #888; font-size: 0.85rem;'>
                                        📍 {location} • 💼 {experience_req}
                                    </p>
                                    <p style='margin: 0.2rem 0 0 0; color: #aaa; font-size: 0.8rem;'>
                                        Posted {time_str}
                                    </p>
                                </div>
                                <div style='text-align: right;'>
                                    <div style='background: #e3f2fd; padding: 0.4rem 0.8rem; 
                                                border-radius: 8px; display: inline-block;'>
                                        <span style='color: #1976d2; font-weight: 700; font-size: 1rem;'>
                                            {job["resume_count"]}
                                        </span>
                                        <span style='color: #1976d2; font-size: 0.8rem; margin-left: 0.2rem;'>
                                            Resumes
                                        </span>
                                    </div>
                                </div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                
                with col_button:
                    if st.button("View →", key=f"view_job_{job['jd_id']}", use_container_width=True):
                        st.session_state.selected_job_id = job["jd_id"]
                        st.session_state.job_view_tab = "Overview"
                        st.rerun()
                        
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem; background: #f5f5f5; 
                            border-radius: 15px; border: 2px dashed #ccc;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>📭</div>
                    <h3 style='color: #666; margin: 0;'>No Jobs Yet</h3>
                    <p style='color: #888; margin-top: 0.5rem;'>Create your first job to get started!</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    
    # ===================================================== 
    # JOB DETAILS VIEW — WHEN A JOB IS SELECTED
    # ===================================================== 
    elif page == "Dashboard" and "selected_job_id" in st.session_state and st.session_state.selected_job_id:
        # Get current job details
        jds_list = get_jds(org_id=org_id)
        current_job = next((jd for jd in jds_list if jd["jd_id"] == st.session_state.selected_job_id), None)
        
        if not current_job:
            st.error("Job not found")
            st.session_state.selected_job_id = None
            
        
        # Job title header
        st.markdown(
            f"""
            <div style='background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                        padding: 1.2rem; border-radius: 12px; margin-bottom: 1rem; 
                        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);'>
                <h2 style='color: white; margin: 0; font-size: 1.5rem; font-weight: 700;'>
                    {current_job.get('role', current_job.get('job_title', 'Job Details'))}
                </h2>
                <p style='color: rgba(255,255,255,0.9); margin-top: 0.3rem; font-size: 0.9rem;'>
                    {current_job.get('company', 'Company')} • {current_job.get('location', 'Location')}
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation tabs
        tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview & Candidates", "📤 Upload Resumes", "📈 Analytics", "⚙️ Job Settings"])
        
        # TAB 1: Overview & Candidates (Results)
        with tab1:
            st.markdown("### 📊 All Candidates")
            
            # Get evaluations for this job
            evaluations = get_evaluations_by_jd_and_tier(
                st.session_state.selected_job_id, tier=None, limit=100, org_id=org_id
            )
            
            total_candidates = len(evaluations)
            
            # Filter controls
            col_filter, col_count = st.columns([2, 1])
            
            with col_filter:
                tier_filter = st.selectbox(
                    "Filter by tier",
                    ["ALL", "TOP", "BEST", "MODERATE", "LOW", "VERY_LOW"],
                    key="candidates_tier_filter"
                )
            
            with col_count:
                st.markdown(
                    f"""
                    <div style='background: #e3f2fd; padding: 1rem; border-radius: 10px; text-align: center;'>
                        <span style='color: #1976d2; font-weight: 700; font-size: 1.2rem;'>
                            {total_candidates}
                        </span>
                        <span style='color: #1976d2; font-size: 0.9rem; margin-left: 0.3rem;'>
                            candidates total
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Filter evaluations
            if tier_filter != "ALL":
                evaluations = [ev for ev in evaluations if ev.get("candidate_tier") == tier_filter]
            
            # Display candidates as cards
            if evaluations:
                for idx, ev in enumerate(evaluations, 1):
                    # Tier colors and status
                    tier_colors = {
                        "TOP": ("#10b981", "shortlisted"),
                        "BEST": ("#3b82f6", "shortlisted"),
                        "MODERATE": ("#f59e0b", "pending"),
                        "LOW": ("#ef4444", "pending"),
                        "VERY_LOW": ("#991b1b", "rejected")
                    }
                    tier_color, status = tier_colors.get(ev.get('candidate_tier', 'MODERATE'), ("#6b7280", "pending"))
                    
                    # Get candidate email and experience from parsed resume
                    candidate_email = "N/A"
                    candidate_experience = "N/A"
                    candidate_skills = []
                    
                    # Try to get resume data
                    resume_id = ev.get("resume_id")
                    if resume_id:
                        resumes = get_resumes_by_jd(st.session_state.selected_job_id, org_id=org_id)
                        candidate_resume = next((r for r in resumes if r.get("resume_id") == resume_id), None)
                        
                        if candidate_resume and "parsed_resume_json" in candidate_resume:
                            parsed_resume = candidate_resume["parsed_resume_json"]
                            candidate_email = parsed_resume.get("email", "N/A")
                            
                            # Get experience
                            exp_years = parsed_resume.get("total_experience_years", 0)
                            if exp_years:
                                candidate_experience = f"{exp_years}yr experience"
                            
                            # Extract skills from skills_with_context
                            skills_data = parsed_resume.get("skills_with_context", [])
                            if skills_data:
                                # Get top 6 skills
                                for skill_item in skills_data[:6]:
                                    if isinstance(skill_item, dict) and "skill" in skill_item:
                                        candidate_skills.append(skill_item["skill"])
                                    elif isinstance(skill_item, str):
                                        candidate_skills.append(skill_item)
                    
                    match_percentage = int(ev.get('overall_score', 0))
                    
                    # Create a container for each candidate
                    with st.container():
                        # Use columns for layout - more compact
                        col_avatar, col_info, col_score = st.columns([0.4, 3.2, 0.7])
                        
                        with col_avatar:
                            st.markdown(
                                """
                                <div style='width: 45px; height: 45px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                                            border-radius: 50%; display: flex; align-items: center; justify-content: center;'>
                                    <span style='font-size: 1.3rem;'>👤</span>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        with col_info:
                            st.markdown(f"**{ev.get('candidate_name', 'Unknown')}**")
                            st.caption(f"{candidate_email} • {candidate_experience}")
                            
                            # Display skills as badges - more compact
                            if candidate_skills:
                                skills_html = " ".join([
                                    f"<span style='background: #f0f0f0; padding: 0.25rem 0.7rem; "
                                    f"border-radius: 15px; font-size: 0.75rem; margin-right: 0.3rem; "
                                    f"display: inline-block; margin-bottom: 0.3rem; color: #333; font-weight: 500;'>{skill}</span>"
                                    for skill in candidate_skills
                                ])
                                st.markdown(skills_html, unsafe_allow_html=True)
                        
                        with col_score:
                            st.markdown(
                                f"""
                                <div style='text-align: center; background: {tier_color}; color: white; 
                                            padding: 0.6rem 0.8rem; border-radius: 10px;'>
                                    <div style='font-size: 1.2rem; font-weight: 800;'>{match_percentage}%</div>
                                    <div style='font-size: 0.65rem; opacity: 0.9;'>Match</div>
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        
                        # Expander for detailed breakdown - more compact
                        with st.expander(f"📊 View Detailed Scores", expanded=False):
                            
                            for cat, score in ev.get("category_scores", {}).items():
                                col_cat, col_score_detail = st.columns([3, 1])
                                
                                with col_cat:
                                    st.markdown(f"**{cat}**")
                                    if "category_explanations" in ev:
                                        st.caption(ev["category_explanations"].get(cat, ""))
                                
                                with col_score_detail:
                                    score_val = score if isinstance(score, (int, float)) else 0
                                    score_color = "#10b981" if score_val >= 8 else "#3b82f6" if score_val >= 6 else "#f59e0b" if score_val >= 4 else "#ef4444"
                                    st.markdown(
                                        f"""
                                        <div style='background: {score_color}; color: white; padding: 0.4rem; 
                                                    border-radius: 6px; text-align: center; font-weight: 700; font-size: 0.9rem;'>
                                            {score_val:.1f}
                                        </div>
                                        """,
                                        unsafe_allow_html=True
                                    )
                        
                        st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
            else:
                st.markdown(
                    """
                    <div style='text-align: center; padding: 3rem; background: #f5f5f5; 
                                border-radius: 15px; border: 2px dashed #ccc;'>
                        <div style='font-size: 4rem; margin-bottom: 1rem;'>📭</div>
                        <h3 style='color: #666; margin: 0;'>No Candidates Yet</h3>
                        <p style='color: #888; margin-top: 0.5rem;'>Upload resumes to see candidates here</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
        
        # TAB 2: Upload Resumes
        with tab2:
            st.markdown("### 📤 Upload & Evaluate Resumes")
            st.markdown("Upload multiple resumes (up to 10). They will be parsed and evaluated automatically.")
            
            resume_files = st.file_uploader(
                "Upload resume files",
                type=["pdf", "docx", "txt"],
                accept_multiple_files=True,
                key="job_resume_uploader",
                help="Select one or more resume files (Max 200MB per file)"
            )
            
            if resume_files:
                st.info(f"📊 **{len(resume_files)} file(s) selected**")
                
                if st.button("🚀 Parse & Evaluate All Resumes", type="primary", use_container_width=True):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, file in enumerate(resume_files):
                        status_text.markdown(f"**Processing ({idx+1}/{len(resume_files)}):** `{file.name}`")
                        
                        # Parse resume
                        raw_text = extract_text(file)
                        parsed_resume = parse_resume(raw_text)
                        resume_id = str(uuid.uuid4())
                        candidate_name = parsed_resume.get("candidate_name", "Unknown")
                        
                        # Save resume
                        save_resume({
                            "resume_id": resume_id,
                            "candidate_name": candidate_name,
                            "jd_id": st.session_state.selected_job_id,
                            "parsed_resume_json": parsed_resume,
                            "created_at": datetime.utcnow()
                        }, org_id=org_id)
                        
                        # Evaluate immediately
                        result = score_resume(
                            current_job["parsed_jd_json"],
                            parsed_resume
                        )
                        
                        save_evaluation({
                            "jd_id": st.session_state.selected_job_id,
                            "resume_id": resume_id,
                            "candidate_name": candidate_name,
                            "category_scores": result["category_scores"],
                            "category_explanations": result["category_explanations"],
                            "overall_score": result["final_score"],
                            "candidate_tier": assign_candidate_tier(result["final_score"]),
                            "evaluated_at": datetime.utcnow()
                        }, org_id=org_id)
                        
                        progress_bar.progress((idx + 1) / len(resume_files))
                    
                    status_text.empty()
                    progress_bar.empty()
                    st.success(f"✅ Successfully processed and evaluated {len(resume_files)} resume(s)!")
                    st.toast(f"✅ {len(resume_files)} candidate(s) evaluated!", icon="🎉")
                    
                    # Refresh to show new candidates
                    st.balloons()
        
        # TAB 3: Analytics
        with tab3:
            st.markdown("### 📈 Analytics Dashboard")
            st.markdown("Comprehensive insights into candidate evaluation metrics")
            
            # Get all evaluations and resumes for this job
            evaluations = get_evaluations_by_jd_and_tier(
                st.session_state.selected_job_id, tier=None, limit=1000, org_id=org_id
            )
            
            if not evaluations or len(evaluations) == 0:
                st.info("📊 No evaluation data available yet. Upload and evaluate resumes to see analytics.")
            else:
                # Prepare data for charts
                import plotly.graph_objects as go
                import plotly.express as px
                from collections import Counter
                
                # Get JD mandatory skills
                jd_mandatory_skills = []
                if "parsed_jd_json" in current_job:
                    jd_mandatory_skills = current_job["parsed_jd_json"].get("mandatory_skills", [])
                
                # Extract data from evaluations
                score_distribution = []
                tier_counts = Counter()
                category_avg_scores = {}
                skills_match_data = []
                
                for ev in evaluations:
                    score_distribution.append(ev.get("overall_score", 0))
                    tier_counts[ev.get("candidate_tier", "UNKNOWN")] += 1
                    
                    # Aggregate category scores
                    for cat, score in ev.get("category_scores", {}).items():
                        if cat not in category_avg_scores:
                            category_avg_scores[cat] = []
                        category_avg_scores[cat].append(score)
                    
                    # Calculate skills match percentage
                    resume_id = ev.get("resume_id")
                    if resume_id and jd_mandatory_skills:
                        resumes = get_resumes_by_jd(st.session_state.selected_job_id, org_id=org_id)
                        candidate_resume = next((r for r in resumes if r.get("resume_id") == resume_id), None)
                        
                        if candidate_resume and "parsed_resume_json" in candidate_resume:
                            parsed_resume = candidate_resume["parsed_resume_json"]
                            candidate_skills = []
                            
                            # Extract all skills
                            skills_data = parsed_resume.get("skills_with_context", [])
                            for skill_item in skills_data:
                                if isinstance(skill_item, dict) and "skill" in skill_item:
                                    candidate_skills.append(skill_item["skill"].lower())
                                elif isinstance(skill_item, str):
                                    candidate_skills.append(skill_item.lower())
                            
                            # Calculate match
                            matched = sum(1 for req_skill in jd_mandatory_skills if any(req_skill.lower() in cs for cs in candidate_skills))
                            match_pct = (matched / len(jd_mandatory_skills) * 100) if jd_mandatory_skills else 0
                            skills_match_data.append({
                                "candidate": ev.get("candidate_name", "Unknown"),
                                "match_percentage": match_pct,
                                "matched": matched,
                                "total": len(jd_mandatory_skills)
                            })
                
                # Calculate averages for category scores
                category_averages = {cat: sum(scores)/len(scores) for cat, scores in category_avg_scores.items()}
                
                # Create 2x2 grid for charts
                col1, col2 = st.columns(2)
                
                # CHART 1: Score Distribution (Histogram)
                with col1:
                    st.markdown(
                        """
                        <div style='background: white; padding: 1rem; border-radius: 12px; 
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1a1a1a; font-size: 1rem;'>📊 Score Distribution</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    fig1 = go.Figure()
                    fig1.add_trace(go.Histogram(
                        x=score_distribution,
                        nbinsx=10,
                        marker_color='#667eea',
                        marker_line_color='#764ba2',
                        marker_line_width=1.5,
                        opacity=0.8,
                        name='Candidates'
                    ))
                    fig1.update_layout(
                        xaxis_title="Overall Score",
                        yaxis_title="Number of Candidates",
                        height=280,
                        margin=dict(l=40, r=20, t=20, b=40),
                        plot_bgcolor='white',
                        paper_bgcolor='white',
                        font=dict(size=11, color='#1a1a1a'),
                        showlegend=False,
                        xaxis=dict(
                            title_font=dict(color='#1a1a1a'),
                            tickfont=dict(color='#1a1a1a')
                        ),
                        yaxis=dict(
                            title_font=dict(color='#1a1a1a'),
                            tickfont=dict(color='#1a1a1a')
                        )
                    )
                    fig1.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.3)', tickcolor='#1a1a1a')
                    fig1.update_yaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.3)', tickcolor='#1a1a1a')
                    st.plotly_chart(fig1, use_container_width=True, config={'displayModeBar': False})
                
                # CHART 2: Candidate Tier Distribution (Pie Chart)
                with col2:
                    st.markdown(
                        """
                        <div style='background: white; padding: 1rem; border-radius: 12px; 
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1a1a1a; font-size: 1rem;'>🎯 Candidate Tier Distribution</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    tier_colors_map = {
                        "TOP": "#10b981",
                        "BEST": "#3b82f6",
                        "MODERATE": "#f59e0b",
                        "LOW": "#ef4444",
                        "VERY_LOW": "#991b1b"
                    }
                    
                    tier_labels = list(tier_counts.keys())
                    tier_values = list(tier_counts.values())
                    tier_colors = [tier_colors_map.get(tier, "#6b7280") for tier in tier_labels]
                    
                    fig2 = go.Figure(data=[go.Pie(
                        labels=tier_labels,
                        values=tier_values,
                        marker=dict(colors=tier_colors, line=dict(color='white', width=2)),
                        hole=0.4,
                        textinfo='label+percent',
                        textfont=dict(size=11, color='#1a1a1a'),
                        insidetextfont=dict(color='white', size=11)
                    )])
                    fig2.update_layout(
                        height=280,
                        margin=dict(l=20, r=20, t=20, b=60),
                        showlegend=True,
                        legend=dict(
                            orientation="h",
                            yanchor="bottom",
                            y=-0.3,
                            xanchor="center",
                            x=0.5,
                            font=dict(size=10, color='#1a1a1a')
                        ),
                        paper_bgcolor='white',
                        font=dict(size=11, color='#1a1a1a')
                    )
                    st.plotly_chart(fig2, use_container_width=True, config={'displayModeBar': False})
                
                col3, col4 = st.columns(2)
                
                # CHART 3: Mandatory Skills Coverage (Bar Chart)
                with col3:
                    st.markdown(
                        """
                        <div style='background: white; padding: 1rem; border-radius: 12px; 
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 1rem;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1a1a1a; font-size: 1rem;'>🎓 Mandatory Skills Coverage</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    if jd_mandatory_skills and evaluations:
                        # Count how many candidates have each mandatory skill
                        skill_counts = {skill: 0 for skill in jd_mandatory_skills}
                        
                        for ev in evaluations:
                            resume_id = ev.get("resume_id")
                            if resume_id:
                                resumes = get_resumes_by_jd(st.session_state.selected_job_id, org_id=org_id)
                                candidate_resume = next((r for r in resumes if r.get("resume_id") == resume_id), None)
                                
                                if candidate_resume and "parsed_resume_json" in candidate_resume:
                                    parsed_resume = candidate_resume["parsed_resume_json"]
                                    candidate_skills = []
                                    
                                    # Extract all skills
                                    skills_data = parsed_resume.get("skills_with_context", [])
                                    for skill_item in skills_data:
                                        if isinstance(skill_item, dict) and "skill" in skill_item:
                                            candidate_skills.append(skill_item["skill"].lower())
                                        elif isinstance(skill_item, str):
                                            candidate_skills.append(skill_item.lower())
                                    
                                    # Check which mandatory skills this candidate has
                                    for req_skill in jd_mandatory_skills:
                                        if any(req_skill.lower() in cs for cs in candidate_skills):
                                            skill_counts[req_skill] += 1
                        
                        # Sort by count
                        sorted_skills = sorted(skill_counts.items(), key=lambda x: x[1], reverse=True)[:10]
                        skills = [s[0] for s in sorted_skills]
                        counts = [s[1] for s in sorted_skills]
                        
                        # Calculate percentage for color
                        total_candidates = len(evaluations)
                        percentages = [(count / total_candidates * 100) if total_candidates > 0 else 0 for count in counts]
                        
                        fig3 = go.Figure()
                        fig3.add_trace(go.Bar(
                            x=counts,
                            y=skills,
                            orientation='h',
                            marker=dict(
                                color=percentages,
                                colorscale=[[0, '#ef4444'], [0.5, '#f59e0b'], [1, '#10b981']],
                                line=dict(color='white', width=1),
                                cmin=0,
                                cmax=100
                            ),
                            text=[f"{count}" for count in counts],
                            textposition='inside',
                            textfont=dict(color='white', size=11, family='Arial Black'),
                            hovertemplate='<b>%{y}</b><br>Candidates: %{x}<br>Coverage: %{customdata:.1f}%<extra></extra>',
                            customdata=percentages
                        ))
                        
                        fig3.update_layout(
                            xaxis_title="Number of Candidates",
                            yaxis_title="Mandatory Skills",
                            height=280,
                            margin=dict(l=120, r=20, t=20, b=40),
                            plot_bgcolor='white',
                            paper_bgcolor='white',
                            font=dict(size=11, color='#1a1a1a'),
                            showlegend=False,
                            xaxis=dict(
                                title_font=dict(color='#1a1a1a'),
                                tickfont=dict(color='#1a1a1a')
                            ),
                            yaxis=dict(
                                title_font=dict(color='#1a1a1a'),
                                tickfont=dict(color='#1a1a1a')
                            )
                        )
                        fig3.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.3)', tickcolor='#1a1a1a')
                        fig3.update_yaxes(showgrid=False, tickcolor='#1a1a1a')
                        st.plotly_chart(fig3, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("No mandatory skills data available")
                
                # CHART 4: Top Performers Leaderboard (Bar Chart)
                with col4:
                    st.markdown(
                        """
                        <div style='background: white; padding: 1rem; border-radius: 12px; 
                                    box-shadow: 0 2px 8px rgba(0,0,0,0.08); margin-bottom: 0.5rem;'>
                            <h4 style='margin: 0 0 0.5rem 0; color: #1a1a1a; font-size: 1rem;'>🏆 Top Candidates</h4>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    
                    # Number input for top N candidates
                    col_input1, col_input2 = st.columns([2, 1])
                    with col_input1:
                        st.markdown(
                            """
                            <p style='font-size: 0.85rem; color: #666; margin: 0 0 0.3rem 0;'>
                                Number of candidates to display:
                            </p>
                            """,
                            unsafe_allow_html=True
                        )
                    with col_input2:
                        top_n_candidates = st.number_input(
                            "top_n_chart",
                            min_value=1,
                            max_value=20,
                            value=5,
                            step=1,
                            label_visibility="collapsed",
                            key="top_n_candidates_chart"
                        )
                    
                    if evaluations and len(evaluations) > 0:
                        # Get top N candidates by score
                        top_candidates = sorted(evaluations, key=lambda x: x.get("overall_score", 0), reverse=True)[:top_n_candidates]
                        
                        # Prepare data
                        names = [ev.get("candidate_name", "Unknown")[:20] for ev in top_candidates]
                        scores = [ev.get("overall_score", 0) for ev in top_candidates]
                        tiers = [ev.get("candidate_tier", "UNKNOWN") for ev in top_candidates]
                        
                        # Color by tier
                        tier_colors_map = {
                            "TOP": "#10b981",
                            "BEST": "#3b82f6",
                            "MODERATE": "#f59e0b",
                            "LOW": "#ef4444",
                            "VERY_LOW": "#991b1b"
                        }
                        colors = [tier_colors_map.get(tier, "#6b7280") for tier in tiers]
                        
                        fig4 = go.Figure()
                        fig4.add_trace(go.Bar(
                            y=names,
                            x=scores,
                            orientation='h',
                            marker=dict(
                                color=colors,
                                line=dict(color='white', width=1)
                            ),
                            text=[f"{score:.1f}" for score in scores],
                            textposition='inside',
                            textfont=dict(color='white', size=10, family='Arial Black'),
                            hovertemplate='<b>%{y}</b><br>Score: %{x:.1f}<br>Tier: %{customdata}<extra></extra>',
                            customdata=tiers
                        ))
                        
                        # Adjust height based on number of candidates
                        chart_height = max(200, min(280, 40 * top_n_candidates + 80))
                        
                        fig4.update_layout(
                            xaxis_title="Overall Score",
                            yaxis_title="",
                            height=chart_height,
                            margin=dict(l=120, r=20, t=10, b=40),
                            plot_bgcolor='white',
                            paper_bgcolor='white',
                            font=dict(size=11, color='#1a1a1a'),
                            showlegend=False,
                            xaxis=dict(
                                title_font=dict(color='#1a1a1a'),
                                tickfont=dict(color='#1a1a1a'),
                                range=[0, 100]
                            ),
                            yaxis=dict(
                                tickfont=dict(color='#1a1a1a'),
                                autorange='reversed'  # Top performer at top
                            )
                        )
                        fig4.update_xaxes(showgrid=True, gridwidth=1, gridcolor='rgba(200,200,200,0.3)', tickcolor='#1a1a1a')
                        fig4.update_yaxes(showgrid=False, tickcolor='#1a1a1a')
                        st.plotly_chart(fig4, use_container_width=True, config={'displayModeBar': False})
                    else:
                        st.info("No evaluation data available")
                
                # Summary Statistics
                st.markdown("---")
                st.markdown("#### 📊 Summary Statistics")
                
                stat_col1, stat_col2, stat_col3, stat_col4 = st.columns(4)
                
                with stat_col1:
                    avg_score = sum(score_distribution) / len(score_distribution) if score_distribution else 0
                    st.metric("Average Score", f"{avg_score:.1f}", delta=None)
                
                with stat_col2:
                    max_score = max(score_distribution) if score_distribution else 0
                    st.metric("Highest Score", f"{max_score:.1f}", delta=None)
                
                with stat_col3:
                    min_score = min(score_distribution) if score_distribution else 0
                    st.metric("Lowest Score", f"{min_score:.1f}", delta=None)
                
                with stat_col4:
                    total_evaluated = len(evaluations)
                    st.metric("Total Evaluated", total_evaluated, delta=None)
        
        # TAB 4: Job Settings
        with tab4:
            st.markdown("### ⚙️ Job Settings")
            st.markdown("Manage this job posting")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Job Details Section
            st.markdown(
                """
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                            box-shadow: 0 3px 15px rgba(0,0,0,0.08); margin-bottom: 2rem;'>
                    <h3 style='color: #1a1a1a; margin: 0 0 1.5rem 0; font-size: 1.3rem;'>Job Details</h3>
                """,
                unsafe_allow_html=True
            )
            
            col_detail1, col_detail2 = st.columns(2)
            
            with col_detail1:
                st.markdown(
                    f"""
                    <div style='margin-bottom: 1rem;'>
                        <p style='color: #888; font-size: 0.85rem; margin: 0;'>Title</p>
                        <p style='color: #1a1a1a; font-size: 1.1rem; font-weight: 600; margin: 0.3rem 0 0 0;'>
                            {current_job.get('role', current_job.get('job_title', 'N/A'))}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                st.markdown(
                    f"""
                    <div style='margin-bottom: 1rem;'>
                        <p style='color: #888; font-size: 0.85rem; margin: 0;'>Location</p>
                        <p style='color: #1a1a1a; font-size: 1.1rem; font-weight: 600; margin: 0.3rem 0 0 0;'>
                            {current_job.get('location', 'Not specified')}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            with col_detail2:
                st.markdown(
                    f"""
                    <div style='margin-bottom: 1rem;'>
                        <p style='color: #888; font-size: 0.85rem; margin: 0;'>Company</p>
                        <p style='color: #1a1a1a; font-size: 1.1rem; font-weight: 600; margin: 0.3rem 0 0 0;'>
                            {current_job.get('company', user['organization'])}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Get status from parsed_jd_json if available
                experience_req = "Not specified"
                if "parsed_jd_json" in current_job:
                    experience_req = current_job["parsed_jd_json"].get("experience_required", "Not specified")
                
                st.markdown(
                    f"""
                    <div style='margin-bottom: 1rem;'>
                        <p style='color: #888; font-size: 0.85rem; margin: 0;'>Experience Required</p>
                        <p style='color: #1a1a1a; font-size: 1.1rem; font-weight: 600; margin: 0.3rem 0 0 0;'>
                            {experience_req}
                        </p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Danger Zone Section
            st.markdown(
                """
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                            box-shadow: 0 3px 15px rgba(0,0,0,0.08); border: 2px solid #fee2e2;'>
                    <h3 style='color: #dc2626; margin: 0 0 0.5rem 0; font-size: 1.3rem;'>⚠️ Danger Zone</h3>
                    <p style='color: #888; font-size: 0.9rem; margin: 0 0 1.5rem 0;'>
                        Irreversible actions
                    </p>
                """,
                unsafe_allow_html=True
            )
            
            # Delete confirmation
            if "confirm_delete" not in st.session_state:
                st.session_state.confirm_delete = False
            
            if not st.session_state.confirm_delete:
                if st.button("🗑️ Delete Job", key="delete_job_btn", type="secondary", use_container_width=False):
                    st.session_state.confirm_delete = True
                    
            else:
                st.warning("⚠️ **Are you sure?** This will permanently delete the job and all associated resumes, evaluations, and file fingerprints. This action cannot be undone.")
                
                col_confirm1, col_confirm2 = st.columns(2)
                
                with col_confirm1:
                    if st.button("✅ Yes, Delete Everything", key="confirm_delete_yes", type="primary", use_container_width=True):
                        with st.spinner("Deleting job and all related data..."):
                            result = delete_job_and_related_data(st.session_state.selected_job_id, org_id=org_id)
                            
                            if result["success"]:
                                st.success(result["message"])
                                st.toast("✅ Job deleted successfully!", icon="🗑️")
                                
                                # Reset state and go back to dashboard
                                st.session_state.confirm_delete = False
                                st.session_state.selected_job_id = None
                                
                            else:
                                st.error(result["message"])
                                st.session_state.confirm_delete = False
                
                with col_confirm2:
                    if st.button("❌ Cancel", key="confirm_delete_no", type="secondary", use_container_width=True):
                        st.session_state.confirm_delete = False
                        
            
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Back to Dashboard button at the bottom
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("← Back to Dashboard", key="back_to_dashboard", use_container_width=True, type="secondary"):
            st.session_state.selected_job_id = None
            st.rerun()
            
    
    # ===================================================== 
    # CREATE JOB — CLEAN MODERN FORM
    # ===================================================== 
    elif page == "Create Job":
        # Centered container
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            # Simple header card
            st.markdown(
                """
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                            box-shadow: 0 2px 10px rgba(0,0,0,0.05); margin-bottom: 2rem; text-align: center;'>
                    <h2 style='color: #1a1a1a; margin: 0; font-size: 1.8rem; font-weight: 700;'>Create a New Job</h2>
                    <p style='color: #666; margin-top: 0.5rem; font-size: 0.95rem;'>
                        Define the role and upload the job description
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Job Title
            st.markdown(
                """
                <label style='font-weight: 600; color: #1a1a1a; font-size: 0.9rem; 
                              display: block; margin-bottom: 0.5rem;'>
                    Job Title <span style='color: #ef4444;'>*</span>
                </label>
                """,
                unsafe_allow_html=True
            )
            job_title = st.text_input(
                "job_title",
                placeholder="e.g., Senior Software Engineer",
                label_visibility="collapsed",
                key="create_job_title"
            )
            
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Company and Location in two columns
            col_a, col_b = st.columns(2)
            
            with col_a:
                st.markdown(
                    """
                    <label style='font-weight: 600; color: #1a1a1a; font-size: 0.9rem; 
                                  display: block; margin-bottom: 0.5rem;'>
                        Company
                    </label>
                    """,
                    unsafe_allow_html=True
                )
                company = st.text_input(
                    "company",
                    value="Novintix",
                    label_visibility="collapsed",
                    key="create_job_company",
                    disabled=True
                )
            
            with col_b:
                st.markdown(
                    """
                    <label style='font-weight: 600; color: #1a1a1a; font-size: 0.9rem; 
                                  display: block; margin-bottom: 0.5rem;'>
                        Location
                    </label>
                    """,
                    unsafe_allow_html=True
                )
                location = st.text_input(
                    "location",
                    placeholder="e.g., Remote, NYC",
                    label_visibility="collapsed",
                    key="create_job_location"
                )
            
            st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
            
            # Job Description Document Upload
            st.markdown(
                """
                <label style='font-weight: 600; color: #1a1a1a; font-size: 0.9rem; 
                              display: block; margin-bottom: 0.5rem;'>
                    Job Description Document <span style='color: #ef4444;'>*</span>
                </label>
                """,
                unsafe_allow_html=True
            )
            
            jd_file = st.file_uploader(
                "Upload JD Document",
                type=["pdf", "docx", "txt"],
                label_visibility="collapsed",
                key="create_job_jd_file",
                help="Drag and drop or browse files (PDF, DOCX, TXT)"
            )
            
            st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
            
            # Submit Button - dark blue/black style
            if st.button("📋 Submit Job Post", type="primary", use_container_width=True, key="submit_create_job"):
                # Validation
                if not job_title:
                    st.error("❌ Please enter a job title")
                elif not jd_file:
                    st.error("❌ Please upload a job description document")
                else:
                    # Check for duplicate job title
                    existing_jd = get_jd_by_title(job_title, org_id=org_id)
                    
                    if existing_jd:
                        st.error(f"❌ A job with the title '{job_title}' already exists. Please use a different job title.")
                    else:
                        with st.spinner("🔄 Processing job description..."):
                            try:
                                # Extract and parse JD
                                raw_text = extract_text(jd_file)
                                parsed_jd = parse_jd(raw_text)
                                
                                # Override role with user-provided job title
                                parsed_jd["role"] = job_title
                                
                                # Set location (default to Coimbatore if not provided)
                                final_location = location.strip() if location and location.strip() else "Coimbatore"
                                parsed_jd["location"] = final_location
                                
                                # Save to database with job_title and location at top level
                                jd_id = str(uuid.uuid4())
                                save_jd({
                                    "jd_id": jd_id,
                                    "job_title": job_title,  # Top level field
                                    "role": job_title,
                                    "company": company,
                                    "location": final_location,  # Top level field
                                    "parsed_jd_json": parsed_jd,
                                    "created_at": datetime.utcnow()
                                }, org_id=org_id)
                                
                                st.success(f"✅ Job '{job_title}' created successfully!")
                                st.toast(f"✅ Job '{job_title}' created!", icon="🎉")
                                
                                # Show parsed details in expander
                                with st.expander("📄 View Parsed Job Details"):
                                    st.json(parsed_jd)
                                
                            except Exception as e:
                                st.error(f"❌ Error processing job description: {str(e)}")
            
    
    # ===================================================== 
    # LAYER 1 — JD UPLOAD (ISOLATED)
    # ===================================================== 
    elif page == "Upload JD":
        col1, col2, col3 = st.columns([1, 2.5, 1])
        
        with col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem 2rem; 
                            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                            border-radius: 20px; margin-bottom: 3rem; box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);'>
                    <div style='font-size: 5rem; margin-bottom: 1rem; animation: bounce 2s infinite;'>📝</div>
                    <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 700;'>Upload Job Description</h2>
                    <p style='color: rgba(255,255,255,0.95); margin-top: 1rem; font-size: 1.1rem;'>
                        Upload and parse your job requirements to get started
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # Upload Section
            st.markdown(
                """
                <div style='background: white; padding: 2rem; border-radius: 15px; 
                            box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
                    <h3 style='color: #333; margin: 0 0 1rem 0; font-size: 1.3rem;'>
                        📄 Select Job Description File
                    </h3>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            jd_file = st.file_uploader(
                "Upload JD file",
                type=["pdf", "docx", "txt"],
                key="jd_uploader",
                help="Supported formats: PDF, DOCX, TXT"
            )
            
            if jd_file:
                st.markdown(
                    f"""
                    <div style='background: #e8f5e9; padding: 1rem; border-radius: 10px; 
                                border-left: 4px solid #4caf50; margin: 1.5rem 0;'>
                        <span style='font-size: 1.2rem;'>✅</span>
                        <strong style='color: #2e7d32;'> File Selected:</strong> 
                        <span style='color: #1b5e20;'>{jd_file.name}</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    if st.button("🚀 Parse & Save JD", type="primary", use_container_width=True):
                        with st.spinner("🔄 Processing job description..."):
                            raw_text = extract_text(jd_file)
                            parsed_jd = parse_jd(raw_text)
                            jd_id = str(uuid.uuid4())
                            save_jd({
                                "jd_id": jd_id,
                                "role": parsed_jd.get("role", "Unknown"),
                                "parsed_jd_json": parsed_jd,
                                "created_at": datetime.utcnow()
                            }, org_id=org_id)
                            st.success("✅ Job description saved successfully!")
                            st.toast("✅ JD saved successfully!", icon="✅")
    
    # ===================================================== 
    # LAYER 2 — RESUME UPLOAD (JD-SCOPED)
    # ===================================================== 
    elif page == "Upload Resume":
        jds = get_jds(org_id=org_id)
        
        if not jds:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem; background: #fff3cd; 
                            border-radius: 15px; border: 2px solid #ffc107;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>⚠️</div>
                    <h3 style='color: #856404; margin: 0;'>No Job Descriptions Found</h3>
                    <p style='color: #856404; margin-top: 0.5rem;'>Please upload a Job Description first</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()
        
        col1, col2, col3 = st.columns([1, 2.5, 1])
        
        with col2:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem 2rem; 
                            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%); 
                            border-radius: 20px; margin-bottom: 3rem; box-shadow: 0 10px 40px rgba(240, 147, 251, 0.3);'>
                    <div style='font-size: 5rem; margin-bottom: 1rem;'>👥</div>
                    <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 700;'>Upload Candidate Resumes</h2>
                    <p style='color: rgba(255,255,255,0.95); margin-top: 1rem; font-size: 1.1rem;'>
                        Upload multiple resumes for comprehensive evaluation
                    </p>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            # JD Selection
            st.markdown(
                """
                <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                            box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
                    <h3 style='color: #333; margin: 0 0 1rem 0; font-size: 1.2rem;'>
                        🎯 Select Target Job Description
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            jd_map = {jd["jd_id"]: jd["role"] for jd in jds}
            selected_jd_id = st.selectbox(
                "Select JD for resume upload",
                options=list(jd_map.keys()),
                format_func=lambda x: f"📋 {jd_map[x]}",
                key="jd_selector"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Resume Upload
            st.markdown(
                """
                <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                            box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
                    <h3 style='color: #333; margin: 0 0 1rem 0; font-size: 1.2rem;'>
                        📎 Upload Resume Files
                    </h3>
                """,
                unsafe_allow_html=True
            )
            
            resume_files = st.file_uploader(
                "Upload resume files",
                type=["pdf", "docx", "txt"],
                accept_multiple_files=True,
                key="resume_uploader",
                help="Select one or more resume files (Max 200MB per file)"
            )
            
            st.markdown("</div>", unsafe_allow_html=True)
            
            if resume_files:
                st.markdown(
                    f"""
                    <div style='background: #e3f2fd; padding: 1rem; border-radius: 10px; 
                                border-left: 4px solid #2196f3; margin: 1.5rem 0;'>
                        <span style='font-size: 1.2rem;'>📊</span>
                        <strong style='color: #1565c0;'> Files Selected:</strong> 
                        <span style='color: #0d47a1; font-weight: 600;'>{len(resume_files)} file(s)</span>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                col_a, col_b, col_c = st.columns([1, 2, 1])
                with col_b:
                    if st.button("🚀 Parse & Save All Resumes", type="primary", use_container_width=True):
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        for idx, file in enumerate(resume_files):
                            status_text.markdown(f"**Processing:** `{file.name}`")
                            raw_text = extract_text(file)
                            parsed_resume = parse_resume(raw_text)
                            resume_id = str(uuid.uuid4())
                            candidate_name = parsed_resume.get("candidate_name", "Unknown")
                            save_resume({
                                "resume_id": resume_id,
                                "candidate_name": candidate_name,
                                "jd_id": selected_jd_id,
                                "parsed_resume_json": parsed_resume,
                                "created_at": datetime.utcnow()
                            }, org_id=org_id)
                            progress_bar.progress((idx + 1) / len(resume_files))
                        
                        status_text.empty()
                        progress_bar.empty()
                        st.success(f"✅ Successfully saved {len(resume_files)} resume(s)!")
                        st.toast(f"✅ {len(resume_files)} resume(s) saved successfully!", icon="✅")
    
    # ===================================================== 
    # LAYER 3 — RESULTS & SCORING
    # ===================================================== 
    elif page == "Results":
        jds = get_jds(org_id=org_id)
        
        if not jds:
            st.markdown(
                """
                <div style='text-align: center; padding: 3rem; background: #fff3cd; 
                            border-radius: 15px; border: 2px solid #ffc107;'>
                    <div style='font-size: 4rem; margin-bottom: 1rem;'>⚠️</div>
                    <h3 style='color: #856404; margin: 0;'>No Job Descriptions Found</h3>
                    <p style='color: #856404; margin-top: 0.5rem;'>Please upload a Job Description first</p>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.stop()
        
        # Header Section
        st.markdown(
            """
            <div style='text-align: center; padding: 3rem 2rem; 
                        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); 
                        border-radius: 20px; margin-bottom: 3rem; box-shadow: 0 10px 40px rgba(79, 172, 254, 0.3);'>
                <div style='font-size: 5rem; margin-bottom: 1rem;'>📊</div>
                <h2 style='color: white; margin: 0; font-size: 2rem; font-weight: 700;'>Results & Evaluation</h2>
                <p style='color: rgba(255,255,255,0.95); margin-top: 1rem; font-size: 1.1rem;'>
                    Analyze and rank candidates based on AI assessment
                </p>
            </div>
            """,
            unsafe_allow_html=True
        )
        
        # Controls Section
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(
                """
                <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                            box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
                    <h3 style='color: #333; margin: 0 0 1rem 0; font-size: 1.2rem;'>🎯 Select Job Description</h3>
                """,
                unsafe_allow_html=True
            )
            jd_map = {jd["jd_id"]: jd["role"] for jd in jds}
            selected_jd_id = st.selectbox(
                "Select JD for evaluation",
                options=list(jd_map.keys()),
                format_func=lambda x: f"📋 {jd_map[x]}",
                key="results_jd_selector"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        with col2:
            st.markdown(
                """
                <div style='background: white; padding: 1.5rem; border-radius: 15px; 
                            box-shadow: 0 5px 20px rgba(0,0,0,0.08); margin-bottom: 1.5rem;'>
                    <h3 style='color: #333; margin: 0 0 1rem 0; font-size: 1.2rem;'>🔢 Number of Candidates</h3>
                """,
                unsafe_allow_html=True
            )
            top_n = st.number_input(
                "Number of top candidates to display",
                min_value=1,
                max_value=50,
                value=5,
                key="top_n_input"
            )
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Run Evaluation Button
        col_a, col_b, col_c = st.columns([1, 2, 1])
        with col_b:
            if st.button("▶️ Run AI Evaluation", type="primary", use_container_width=True, 
                         help="Click to evaluate all unreviewed resumes"):
                jd = next(jd for jd in jds if jd["jd_id"] == selected_jd_id)
                resumes = get_unreviewed_resumes_by_jd(selected_jd_id, org_id=org_id)
                
                if not resumes:
                    st.toast("ℹ️ No unreviewed resumes for this JD.", icon="ℹ️")
                else:
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    for idx, resume in enumerate(resumes):
                        status_text.markdown(f"**Evaluating:** `{resume['candidate_name']}`")
                        result = score_resume(
                            jd["parsed_jd_json"],
                            resume["parsed_resume_json"]
                        )
                        save_evaluation({
                            "jd_id": selected_jd_id,
                            "resume_id": str(resume["_id"]),
                            "candidate_name": resume["candidate_name"],
                            "category_scores": result["category_scores"],
                            "category_explanations": result["category_explanations"],
                            "overall_score": result["final_score"],
                            "candidate_tier": assign_candidate_tier(result["final_score"]),
                            "evaluated_at": datetime.utcnow()
                        }, org_id=org_id)
                        mark_resume_reviewed(resume["_id"])
                        progress_bar.progress((idx + 1) / len(resumes))
                    
                    status_text.empty()
                    progress_bar.empty()
                    st.success("✅ Evaluation completed successfully!")
                    st.toast("✅ Evaluation completed!", icon="🎯")
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("---")
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Results Section
        st.markdown("### 🏆 Ranked Candidates")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            tier_filter = st.selectbox(
                "Filter candidates by tier",
                ["ALL", "TOP", "BEST", "MODERATE", "LOW", "VERY_LOW"],
                format_func=lambda x: f"🎯 {x}",
                key="tier_filter"
            )
        
        evaluations = get_evaluations_by_jd_and_tier(
            selected_jd_id, tier_filter, limit=top_n, org_id=org_id
        )
        
        if evaluations:
            for idx, ev in enumerate(evaluations, 1):
                # Tier color coding
                tier_colors = {
                    "TOP": "#10b981",
                    "BEST": "#3b82f6",
                    "MODERATE": "#f59e0b",
                    "LOW": "#ef4444",
                    "VERY_LOW": "#991b1b"
                }
                tier_color = tier_colors.get(ev['candidate_tier'], "#6b7280")
                
                # Expander for detailed breakdown - starts collapsed
                with st.expander(f"**#{idx}** {ev['candidate_name']}", expanded=False):
                    # Score and tier info
                    col_score, col_tier = st.columns(2)
                    
                    with col_score:
                        st.markdown(
                            f"""
                            <div style='text-align: center; padding: 1.5rem; background: {tier_color}; 
                                        color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                <div style='font-size: 2.5rem; font-weight: 800; margin-bottom: 0.3rem;'>
                                    {ev['overall_score']:.1f}
                                </div>
                                <div style='font-size: 0.9rem; opacity: 0.95; font-weight: 600;'>
                                    OVERALL SCORE
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    with col_tier:
                        st.markdown(
                            f"""
                            <div style='text-align: center; padding: 1.5rem; background: {tier_color}; 
                                        color: white; border-radius: 12px; box-shadow: 0 4px 15px rgba(0,0,0,0.1);'>
                                <div style='font-size: 1.8rem; font-weight: 800; margin-bottom: 0.3rem;'>
                                    {ev['candidate_tier']}
                                </div>
                                <div style='font-size: 0.9rem; opacity: 0.95; font-weight: 600;'>
                                    CANDIDATE TIER
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    # Category Scores
                    st.markdown("### 📊 Category Analysis")
                    
                    for cat, score in ev["category_scores"].items():
                        # Score color based on value
                        if score >= 8:
                            score_color = "#10b981"
                            score_icon = "🟢"
                        elif score >= 6:
                            score_color = "#3b82f6"
                            score_icon = "🔵"
                        elif score >= 4:
                            score_color = "#f59e0b"
                            score_icon = "🟡"
                        else:
                            score_color = "#ef4444"
                            score_icon = "🔴"
                        
                        col1, col2 = st.columns([3, 1])
                        with col1:
                            st.markdown(f"**{score_icon} {cat}**")
                            st.caption(ev["category_explanations"][cat])
                        with col2:
                            st.markdown(
                                f"""
                                <div style='text-align: center; padding: 0.8rem; background: {score_color}; 
                                            color: white; border-radius: 10px; font-size: 1.5rem; 
                                            font-weight: 800; box-shadow: 0 2px 8px rgba(0,0,0,0.1);'>
                                    {score:.1f}
                                </div>
                                """,
                                unsafe_allow_html=True
                            )
                        st.markdown("---")
        else:
            st.markdown(
                """
                <div style='text-align: center; padding: 2rem; background: #e3f2fd; 
                            border-radius: 15px; border: 2px dashed #2196f3;'>
                    <div style='font-size: 3rem; margin-bottom: 1rem;'>📭</div>
                    <h3 style='color: #1565c0; margin: 0;'>No Evaluations Found</h3>
                    <p style='color: #1976d2; margin-top: 0.5rem;'>Try adjusting your filter or run an evaluation first</p>
                </div>
                """,
                unsafe_allow_html=True
            )


# ========================
# MAIN APP LOGIC
# ========================
def main():
    # Initialize session state
    if "page" not in st.session_state:
        st.session_state.page = "landing"
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    if "user" not in st.session_state:
        st.session_state.user = None
    
    # Load CSS
    load_landing_css()
    
    # Route to appropriate page
    if st.session_state.authenticated and st.session_state.user:
        # User is authenticated, show the main app
        show_main_app()
    elif st.session_state.page in ["signin", "signup"]:
        # Show auth page for signin/signup
        show_auth_page()
    elif st.session_state.page == "app":
        # If trying to access app without auth, redirect to signin
        if not st.session_state.authenticated:
            st.session_state.page = "signin"
            show_auth_page()
        else:
            show_main_app()
    elif st.session_state.page == "landing":
        show_landing_page()
    else:
        show_landing_page()


if __name__ == "__main__":
    main()

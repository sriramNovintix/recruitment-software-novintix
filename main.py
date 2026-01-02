"""
TalentMatch - AI-Powered Recruitment Platform
Main entry point with landing page, authentication, and app routing
"""
import streamlit as st
from core.auth import create_user, authenticate_user, get_user_by_id

# Page configuration
st.set_page_config(
    page_title="TalentMatch - Find the best candidates, faster",
    layout="wide",
    initial_sidebar_state="collapsed",
    page_icon="🎯"
)

def load_landing_css():
    st.markdown("""
    <style>
        /* Hide Streamlit default elements for landing page */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        
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
        
        /* Remove fixed positioning for top buttons - they're now at bottom */
        
        /* Hero Section */
        .hero-section {
            text-align: center;
            padding: 8rem 2rem 4rem;
            background: linear-gradient(180deg, #f0f7ff 0%, #ffffff 100%);
            margin-top: 70px;
        }
        
        .hero-title {
            font-size: 3.5rem;
            font-weight: 800;
            color: #1a1a1a;
            margin-bottom: 1.5rem;
            line-height: 1.2;
        }
        
        .hero-subtitle {
            font-size: 1.25rem;
            color: #666;
            max-width: 600px;
            margin: 0 auto 2.5rem;
            line-height: 1.6;
        }
        
        .hero-buttons {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 3rem;
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
            gap: 6rem;
            padding: 3rem 2rem;
            border-top: 1px solid #eee;
            border-bottom: 1px solid #eee;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-value {
            font-size: 2.5rem;
            font-weight: 700;
            color: #3b82f6;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            color: #888;
            font-size: 0.95rem;
        }
        
        /* How It Works Section */
        .hiw-section {
            padding: 5rem 2rem;
            text-align: center;
        }
        
        .hiw-title {
            font-size: 2rem;
            font-weight: 700;
            color: #1a1a1a;
            margin-bottom: 3rem;
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
            <a href="#features" class="nav-link">Features</a>
            <a href="#how-it-works" class="nav-link">How It Works</a>
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
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns([2, 1.5, 0.5, 1.5, 2])
    
    with col2:
        if st.button("🔐 Sign In", key="bottom_signin", use_container_width=True, type="secondary"):
            st.session_state.page = "signin"
            st.rerun()
    
    with col4:
        if st.button("🚀 Get Started Free", key="bottom_getstarted", use_container_width=True, type="primary"):
            st.session_state.page = "signup"
            st.rerun()
    
    # Footer
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align: center; padding: 3rem 2rem; background: #f8f9fa; margin-top: 4rem; border-top: 1px solid #eee;'>
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
            with st.form("login_form", clear_on_submit=False):
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem;">Email Address</p>', unsafe_allow_html=True)
                email = st.text_input("email_login", placeholder="you@example.com", label_visibility="collapsed")
                
                st.markdown('<p style="font-weight: 600; color: #333; font-size: 0.85rem; margin-bottom: 0.3rem; margin-top: 0.8rem;">Password</p>', unsafe_allow_html=True)
                password = st.text_input("password_login", type="password", placeholder="••••••••", label_visibility="collapsed")
                
                submitted = st.form_submit_button("Sign in", use_container_width=True)
                
                if submitted:
                    if not email or not password:
                        st.error("Please fill in all fields")
                    else:
                        result = authenticate_user(email, password)
                        if result["success"]:
                            st.session_state.authenticated = True
                            st.session_state.user = result["user"]
                            st.session_state.page = "app"
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
                # Regular text input with Novintix pre-filled
                organization = st.text_input("org_signup", value="Novintix", label_visibility="collapsed")
                
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
        mark_resume_reviewed
    )
    from core.utils import extract_text
    from core.jd_parser import parse_jd
    from core.resume_parser import parse_resume
    from core.scorer import score_resume, assign_candidate_tier
    
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
            ["📝 Upload JD", "👤 Upload Resume", "📊 Results"],
            label_visibility="collapsed"
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
        <div style='text-align: center; padding: 2rem 0 3rem 0; margin-bottom: 2rem;'>
            <h1 style='font-size: 3rem; font-weight: 800; margin-bottom: 0.5rem; 
                       background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                       -webkit-background-clip: text; -webkit-text-fill-color: transparent;
                       background-clip: text;'>
                Resume Evaluation System
            </h1>
            <p style='font-size: 1.2rem; color: #666; margin: 0; font-weight: 500;'>
                🤖 AI-Powered Candidate Assessment & Intelligent Ranking
            </p>
            <p style='font-size: 0.9rem; color: #888; margin-top: 0.5rem;'>
                Organization: <strong>{user['organization']}</strong>
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    # ===================================================== 
    # LAYER 1 — JD UPLOAD (ISOLATED)
    # ===================================================== 
    if page == "Upload JD":
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

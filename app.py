import streamlit as st
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

# ---------------- CONFIG ----------------
st.set_page_config(
    page_title="Resume–JD Evaluation",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Load custom CSS
def load_css():
    try:
        with open('assets/style.css') as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except FileNotFoundError:
        pass

load_css()

db = init_db()

# ---------------- SIDEBAR ----------------
with st.sidebar:
    # Logo/Brand Section
    st.markdown(
        """
        <div style='text-align: center; padding: 1.5rem 0; margin-bottom: 1.5rem;'>
            <div style='font-size: 3rem; margin-bottom: 0.5rem;'>📊</div>
            <h2 style='color: #667eea; margin: 0; font-size: 1.3rem;'>Resume Evaluator</h2>
            <p style='color: #888; font-size: 0.85rem; margin-top: 0.3rem;'>AI-Powered Assessment</p>
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
    """
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
                        })
                        st.success("✅ Job description saved successfully!")
                        st.toast("✅ JD saved successfully!", icon="✅")

# ===================================================== 
# LAYER 2 — RESUME UPLOAD (JD-SCOPED)
# ===================================================== 
elif page == "Upload Resume":
    jds = get_jds()
    
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
                        })
                        progress_bar.progress((idx + 1) / len(resume_files))
                    
                    status_text.empty()
                    progress_bar.empty()
                    st.success(f"✅ Successfully saved {len(resume_files)} resume(s)!")
                    st.toast(f"✅ {len(resume_files)} resume(s) saved successfully!", icon="✅")

# ===================================================== 
# LAYER 3 — RESULTS & SCORING
# ===================================================== 
elif page == "Results":
    jds = get_jds()
    
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
            resumes = get_unreviewed_resumes_by_jd(selected_jd_id)
            
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
                    })
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
        selected_jd_id, tier_filter, limit=top_n
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
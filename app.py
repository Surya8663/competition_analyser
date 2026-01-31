# app.py - COMPLETE FIXED WITH PROPER EXPERIENCE-AWARE SCORING
import streamlit as st
import os
import json
from datetime import datetime
import sys
import re
import time
from typing import Dict, List, Optional

# Set page config MUST be first
st.set_page_config(
    page_title="GitHub Repo Evaluator",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

# Import the GitHub Analyzer Agent
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
try:
    from github_analyzer_agent import GitHubAnalyzerAgent
    from evaluation_logic import RealScoringEngine
    ANALYZER_AVAILABLE = True
except ImportError as e:
    st.error(f"Failed to import analyzer: {str(e)}")
    ANALYZER_AVAILABLE = False

# Custom CSS - FIXED WITH ALL ISSUES RESOLVED
st.markdown("""
<style>
    /* Reset default colors */
    .stApp {
        background-color: #ffffff;
    }
    
    /* Fix all text colors */
    .stMarkdown, .stText, p, h1, h2, h3, h4, h5, h6, div, span {
        color: #1f2937 !important;
    }
    
    /* Fix input text color - VERY IMPORTANT */
    .stTextInput input {
        color: #1f2937 !important;
        background-color: white !important;
    }
    
    .stTextInput input::placeholder {
        color: #6b7280 !important;
    }
    
    /* Main Container */
    .main-header {
        text-align: center;
        padding: 25px 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white !important;
        border-radius: 10px;
        margin-bottom: 25px;
    }
    
    .main-header h2, .main-header p {
        color: white !important;
    }
    
    /* Challenge Cards - FIXED LARGER TITLES */
    .challenge-card {
        background: #ffffff;
        padding: 15px;
        border-radius: 8px;
        border: 1px solid #e0e0e0;
        margin: 5px 0;
        transition: all 0.2s ease;
        cursor: pointer;
        height: 160px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .challenge-card:hover {
        border-color: #4a90e2;
        transform: translateY(-2px);
        box-shadow: 0 3px 10px rgba(74, 144, 226, 0.15);
    }
    
    .challenge-card.selected {
        border-color: #10b981;
        background: #f0fdf4;
        box-shadow: 0 3px 10px rgba(16, 185, 129, 0.15);
    }
    
    /* Tech Tags - HORIZONTAL & COMPACT - FIXED */
    .tech-container {
        display: flex;
        flex-wrap: wrap;
        gap: 4px;
        margin: 6px 0;
    }
    
    .tech-tag {
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        color: white !important;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 10px;
        font-weight: 500;
        white-space: nowrap;
    }
    
    /* Score Cards */
    .score-card {
        background: #ffffff;
        padding: 20px;
        border-radius: 10px;
        margin: 15px 0;
        border-left: 4px solid;
        box-shadow: 0 2px 6px rgba(0,0,0,0.05);
    }
    
    .score-excellent { 
        border-left-color: #10b981;
        background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    }
    .score-good { 
        border-left-color: #3b82f6;
        background: linear-gradient(135deg, #ffffff 0%, #eff6ff 100%);
    }
    .score-fair { 
        border-left-color: #f59e0b;
        background: linear-gradient(135deg, #ffffff 0%, #fffbeb 100%);
    }
    .score-poor { 
        border-left-color: #ef4444;
        background: linear-gradient(135deg, #ffffff 0%, #fef2f2 100%);
    }
    
    /* Analysis Boxes */
    .analysis-box {
        background: #f8fafc;
        padding: 15px;
        border-radius: 8px;
        margin: 10px 0;
        border-left: 3px solid #6366f1;
    }
    
    .analysis-box strong {
        color: #1f2937 !important;
        font-size: 14px;
        display: block;
        margin-bottom: 6px;
    }
    
    .analysis-box p {
        color: #4b5563 !important;
        margin: 0;
        font-size: 13px;
        line-height: 1.4;
    }
    
    /* Section Titles */
    .section-title {
        color: #1f2937 !important;
        border-bottom: 2px solid #6366f1;
        padding-bottom: 8px;
        margin: 20px 0 15px 0;
        font-size: 1.3rem;
        font-weight: 600;
    }
    
    /* Status Boxes */
    .status-box {
        padding: 10px 12px;
        border-radius: 8px;
        margin: 8px 0;
        font-size: 13px;
        font-weight: 500;
        border-left: 3px solid;
    }
    
    .status-success {
        background: #d1fae5;
        color: #065f46 !important;
        border-left-color: #10b981;
    }
    
    .status-warning {
        background: #fef3c7;
        color: #92400e !important;
        border-left-color: #f59e0b;
    }
    
    .status-error {
        background: #fee2e2;
        color: #991b1b !important;
        border-left-color: #ef4444;
    }
    
    /* Compact Button Styling - REMOVED ICON PARAMETER */
    .stButton > button {
        border-radius: 6px;
        font-weight: 500;
        font-size: 14px;
        padding: 6px 12px;
        margin: 2px 0;
    }
    
    /* Fix success/error/warning message colors */
    .stAlert > div {
        color: inherit !important;
    }
    
    .stSuccess > div {
        color: #065f46 !important;
    }
    
    .stError > div {
        color: #991b1b !important;
    }
    
    .stWarning > div {
        color: #92400e !important;
    }
    
    .stInfo > div {
        color: #1e40af !important;
    }
    
    /* Fix metric colors */
    [data-testid="stMetricValue"] {
        color: #1f2937 !important;
        font-weight: 600;
    }
    
    [data-testid="stMetricLabel"] {
        color: #6b7280 !important;
    }
    
    [data-testid="stMetricDelta"] {
        color: #059669 !important;
    }
    
    /* Fix table colors */
    .stDataFrame, .stTable {
        color: #1f2937 !important;
    }
    
    /* Reduce spacing in expanders */
    .streamlit-expanderHeader {
        padding: 10px;
        font-size: 14px;
        color: #1f2937 !important;
        background: #f8fafc;
    }
    
    /* Fix code blocks */
    .stCodeBlock {
        background: #f8fafc !important;
        color: #1f2937 !important;
        border: 1px solid #e5e7eb !important;
    }
    
    /* Fix hr */
    hr {
        border-color: #e5e7eb !important;
        margin: 20px 0;
    }
    
    /* Compact form elements */
    .stTextInput > div > div > input {
        padding: 8px 12px;
        font-size: 14px;
        border: 1px solid #d1d5db !important;
        border-radius: 6px;
        color: #1f2937 !important;
        background: white !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 2px rgba(99, 102, 241, 0.1);
    }
</style>
""", unsafe_allow_html=True)

class GitHubRepoEvaluator:
    def __init__(self):
        self.init_session_state()
        self.challenges = self.load_challenges()
        self.analyzer_agent = None
        
        if not ANALYZER_AVAILABLE:
            st.warning("⚠️ Analyzer module not available. Please check dependencies.")
    
    def init_session_state(self):
        """Initialize session state variables"""
        defaults = {
            'selected_challenge': None,
            'repo_url': '',
            'analysis_results': None,
            'evaluation_report': None,
            'is_analyzing': False,
            'error_message': None,
            'show_detailed_report': False,
            'experience_level': 'fresher',
            'experience_adjusted_score': None
        }
        
        for key, value in defaults.items():
            if key not in st.session_state:
                st.session_state[key] = value
    
    def load_challenges(self):
        """Load challenges from your JSON data"""
        return [
            {
                "id": "challenge_023",
                "title": "AI Agents Builder System",
                "short_description": "Build AI agent system combining CV and LLMs for document understanding",
                "full_description": "QuickPlans AI is looking for exceptional builders who can create production-ready AI agent systems that combine computer vision and language models for document understanding.",
                "eval_criteria": """**A. Multi-Modal Implementation (60 points)**
• Computer Vision Quality (20 pts): Object detection accuracy, OCR integration, layout analysis, CV error handling
• Multi-Agent System (20 pts): Specialized agents for different modalities, effective coordination, multi-modal reasoning, state management
• System Engineering (20 pts): Clean integration of CV and NLP, code organization, performance optimization, testing coverage

**B. Functionality & Results (25 points)**
• Multi-Modal Accuracy (15 pts): Extraction precision, fusion quality, validation effectiveness
• Confidence & Demo (10 pts): Multi-modal confidence scoring, demo video clarity, documentation quality

**C. Innovation & Practicality (15 points)**
• Creative Multi-Modal Solutions (8 pts): Novel CV+LLM integration, innovative fusion strategies, smart optimization
• Production Readiness (7 pts): Deployment considerations, scalability, cost optimization

**Bonus Points (Up to +15 Extra)**""",
                "skills": "Python, Computer Vision, LLMs, OCR, LangGraph, CrewAI, FastAPI, Qdrant, YOLO, Tesseract, Multi-modal AI",
                "technologies": ["Python", "Computer Vision", "OpenCV", "LLMs", "OCR", "LangGraph", "CrewAI", "FastAPI", "Qdrant", "YOLO", "Tesseract", "Multi-modal AI"],
                "difficulty": "advanced",
                "prize": "Direct Interview with QuickPlans AI + Certificate"
            },
            {
                "id": "challenge_024",
                "title": "AI Healthcare Agent System",
                "short_description": "Build GenAI apps with RAG and agents for healthcare",
                "full_description": "Midoc AI is looking for talented AI Engineers who can build production-ready Generative AI applications with RAG pipelines, AI agents, and robust evaluation frameworks.",
                "eval_criteria": """**A. Technical Implementation (60 points)**
• RAG Pipeline Quality (20 pts): Vector DB integration, retrieval accuracy, chunking strategy
• AI Agent Development (20 pts): Agent architecture, workflow design, tool integration
• Evaluation Framework (10 pts): Metrics design, automation, comprehensiveness
• Deployment & Infrastructure (10 pts): Cloud deployment, containerization, scalability

**B. Functionality & Results (25 points)**
• System Performance (15 pts): Response time, accuracy, reliability
• Demo & Documentation (10 pts): Video clarity, code documentation, setup instructions

**C. Innovation & Best Practices (15 points)**
• Creative Solutions (8 pts): Novel approaches, optimization strategies
• Production Readiness (7 pts): Error handling, monitoring, cost optimization

**Bonus Points (Up to +15 Extra)**""",
                "skills": "Python, GenAI, RAG, AI Agents, LangChain, LangGraph, CrewAI, Vector Databases, AWS, Docker, FastAPI",
                "technologies": ["Python", "GenAI", "RAG", "AI Agents", "LangChain", "LangGraph", "CrewAI", "Vector Databases", "AWS", "Docker", "FastAPI"],
                "difficulty": "advanced",
                "prize": "Direct Interview with Midoc AI + Certificate"
            },
            {
                "id": "challenge_025",
                "title": "Healthcare Analytics",
                "short_description": "Build ETL pipelines for healthcare data processing",
                "full_description": "Build comprehensive data engineering solution for healthcare supply chain management with ETL pipelines, database design, and cloud deployment.",
                "eval_criteria": """**A. Technical Implementation (60 points)**
• ETL Pipeline Quality (20 pts): Data extraction, transformation, loading efficiency
• Database Design (15 pts): Schema design, optimization, relationships
• Data Pipeline Architecture (15 pts): Scalability, reliability, error handling
• Cloud Deployment (10 pts): AWS integration, containerization, monitoring

**B. Functionality & Results (25 points)**
• Data Processing Accuracy (15 pts): Data quality, validation, completeness
• Demo & Documentation (10 pts): Video clarity, documentation quality, setup instructions

**C. Innovation & Best Practices (15 points)**
• Creative Solutions (8 pts): Novel approaches, optimization strategies
• Production Readiness (7 pts): Error handling, monitoring, scalability

**Bonus Points (Up to +15 Extra)**""",
                "skills": "Python, ETL, PostgreSQL, Airflow, AWS, Docker, Data Engineering",
                "technologies": ["Python", "ETL", "PostgreSQL", "MongoDB", "AWS", "Apache Airflow", "Docker", "Pandas", "PySpark"],
                "difficulty": "intermediate",
                "prize": "Direct Interview with bebliss.in + Certificate"
            },
            {
                "id": "challenge_026",
                "title": "AI Healthcare Platform",
                "short_description": "Build full-stack app with AI integration for healthcare",
                "full_description": "Build full-stack healthcare supply chain management platform with AI/ML integration, automation, and modern web technologies.",
                "eval_criteria": """**A. Technical Implementation (60 points)**
• Frontend Development (20 pts): UI/UX quality, responsiveness, interactivity
• Backend Development (15 pts): API design, security, performance
• AI/ML Integration (15 pts): Model integration, automation workflows, intelligence
• Deployment & Infrastructure (10 pts): Cloud deployment, containerization, scalability

**B. Functionality & Results (25 points)**
• System Performance (15 pts): Response time, reliability, user experience
• Demo & Documentation (10 pts): Video clarity, documentation quality, setup instructions

**C. Innovation & Best Practices (15 points)**
• Creative Solutions (8 pts): Novel features, optimization strategies
• Production Readiness (7 pts): Error handling, security, monitoring

**Bonus Points (Up to +15 Extra)**""",
                "skills": "React, Django, Node.js, AI/ML, PostgreSQL, Docker, Full Stack Development",
                "technologies": ["Next.js", "React.js", "Python Django", "Node.js", "PostgreSQL", "MongoDB", "AI/ML", "Automation", "AWS", "Docker", "Celery", "Redis"],
                "difficulty": "intermediate",
                "prize": "Direct Interview with bebliss.in + Certificate"
            },
            {
                "id": "challenge_027",
                "title": "Enterprise Platform",
                "short_description": "Build production app with task queues and monitoring",
                "full_description": "Build production-ready full-stack web application with Next.js/React.js, Python Django/Node.js, task queues, and monitoring systems.",
                "eval_criteria": """**A. Technical Implementation (60 points)**
• Frontend Development (20 pts): UI/UX quality, responsiveness, code organization
• Backend Development (15 pts): API design, security, performance
• Database Design (10 pts): Schema design, optimization, relationships
• Task Queue Implementation (10 pts): Queue integration, job processing, reliability
• Deployment & Infrastructure (5 pts): Cloud deployment, containerization

**B. Functionality & Results (25 points)**
• System Performance (15 pts): Response time, reliability, user experience
• Demo & Documentation (10 pts): Video clarity, documentation quality, setup instructions

**C. Innovation & Best Practices (15 points)**
• Creative Solutions (8 pts): Novel features, optimization strategies
• Production Readiness (7 pts): Error handling, security, monitoring, testing

**Bonus Points (Up to +15 Extra)**""",
                "skills": "React, Django, Celery, Redis, Monitoring, Docker, System Design",
                "technologies": ["Next.js", "React.js", "Python Django", "Node.js", "PostgreSQL", "MongoDB", "Celery", "Bull Queue", "Redis", "AWS", "Docker"],
                "difficulty": "intermediate",
                "prize": "Direct Interview with Midoc AI + Certificate"
            }
        ]
    
    def initialize_analyzer_agent(self):
        """Initialize the GitHub Analyzer Agent"""
        try:
            gemini_api_key = os.environ.get("GEMINI_API_KEY")
            github_token = os.environ.get("GITHUB_TOKEN")
            
            if not gemini_api_key:
                st.error("❌ Missing GEMINI_API_KEY in .env file")
                return False
            if not github_token:
                st.error("❌ Missing GITHUB_TOKEN in .env file")
                return False
            
            self.analyzer_agent = GitHubAnalyzerAgent(
                gemini_api_key=gemini_api_key,
                github_token=github_token
            )
            return True
        except Exception as e:
            st.error(f"❌ Failed to initialize analyzer agent: {str(e)}")
            return False
    
    def validate_github_url(self, url: str) -> bool:
        """Validate GitHub repository URL"""
        if not url:
            return False
        
        url = url.strip().rstrip('/')
        pattern = r'^https://github\.com/[a-zA-Z0-9_.-]+/[a-zA-Z0-9_.-]+/?$'
        return bool(re.match(pattern, url))
    
    def extract_repo_info(self, url: str) -> tuple:
        """Extract owner and repo from GitHub URL"""
        url = url.rstrip('/')
        parts = url.split('/')
        if len(parts) >= 5:
            return parts[-2], parts[-1]
        return None, None
    
    def display_header(self):
        """Display application header"""
        st.markdown("""
        <div class="main-header">
            <h2 style="margin: 0; font-size: 2rem;">🏆 GitHub Repository Evaluator</h2>
            <p style="margin: 8px 0; font-size: 1rem; opacity: 0.95;">AI-Powered Technical Assessment Platform</p>
            <div style="display: flex; justify-content: center; gap: 10px; margin-top: 10px; font-size: 0.8rem;">
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 15px;">Real GitHub Analysis</span>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 15px;">Gemini AI Powered</span>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 15px;">Experience-Aware</span>
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 15px;">Challenge Specific</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def display_experience_selector(self):
        """Display experience level selector"""
        st.markdown('<p class="section-title">👤 Select Experience Level</p>', unsafe_allow_html=True)
        
        experience_levels = [
            "1st_year", "2nd_year", "3rd_year", "4th_year",
            "fresher", "experienced_0_2", "senior"
        ]
        
        experience_names = {
            "1st_year": "1st Year Student",
            "2nd_year": "2nd Year Student",
            "3rd_year": "3rd Year Student",
            "4th_year": "4th Year Student",
            "fresher": "Recent Graduate",
            "experienced_0_2": "1-2 Years Experience",
            "senior": "3+ Years Experience"
        }
        
        # Create 7 columns for the 7 experience levels
        cols = st.columns(7)
        
        for idx, level in enumerate(experience_levels):
            with cols[idx]:
                is_selected = st.session_state.experience_level == level
                
                button_text = "✓" if is_selected else experience_names[level]
                
                if st.button(
                    button_text,
                    key=f"exp_{level}",
                    type="primary" if is_selected else "secondary",
                    use_container_width=True,
                    help=f"{experience_names[level]}"
                ):
                    st.session_state.experience_level = level
                    st.rerun()
        
        # Show selected level
        selected_name = experience_names.get(st.session_state.experience_level, "Unknown")
        st.info(f"**Selected Experience Level:** {selected_name}")
    
    def display_challenge_selector(self):
        """Display challenge selection with horizontal tech tags"""
        st.markdown('<p class="section-title">🎯 Select Challenge</p>', unsafe_allow_html=True)
        
        cols = st.columns(5)
        
        for idx, challenge in enumerate(self.challenges):
            with cols[idx]:
                is_selected = st.session_state.selected_challenge and st.session_state.selected_challenge['id'] == challenge['id']
                
                # Card container
                with st.container():
                    st.markdown(f"""
                    <div style="margin-bottom: 5px;">
                        <div style="font-size: 14px; font-weight: 600; color: #1f2937; margin-bottom: 5px;">
                            {challenge['title']}
                        </div>
                        <div style="font-size: 10px; color: {'#ef4444' if challenge['difficulty'] == 'advanced' else '#f59e0b'}; 
                                 margin: 3px 0; font-weight: 500;">
                            {challenge['difficulty'].upper()}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.markdown(f'<div style="font-size: 10px; color: #6b7280; margin: 5px 0; height: 40px;">{challenge["short_description"][:70]}...</div>', unsafe_allow_html=True)
                    
                    tech_html = '<div class="tech-container">'
                    for tech in challenge['technologies'][:4]:
                        tech_html += f'<span class="tech-tag">{tech}</span>'
                    if len(challenge['technologies']) > 4:
                        tech_html += f'<span class="tech-tag">+{len(challenge["technologies"])-4}</span>'
                    tech_html += '</div>'
                    st.markdown(tech_html, unsafe_allow_html=True)
                    
                    if st.button(
                        "✓ Selected" if is_selected else "Select",
                        key=f"challenge_{challenge['id']}",
                        type="primary" if is_selected else "secondary",
                        use_container_width=True,
                        help=f"Select {challenge['title']}"
                    ):
                        st.session_state.selected_challenge = challenge
                        st.session_state.analysis_results = None
                        st.session_state.evaluation_report = None
                        st.rerun()
    
    def display_selected_challenge_info(self):
        """Display information about selected challenge"""
        if not st.session_state.selected_challenge:
            return
        
        challenge = st.session_state.selected_challenge
        
        with st.expander(f"📋 {challenge['title']} - Challenge Details", expanded=False):
            st.markdown(f"**Full Description:**")
            st.info(challenge['full_description'])
            
            st.markdown("**Evaluation Criteria:**")
            st.markdown(challenge['eval_criteria'])
            
            st.markdown("**Required Skills:**")
            st.markdown(challenge['skills'])
            
            st.markdown("**Technologies:**")
            tech_html = '<div class="tech-container">'
            for tech in challenge['technologies']:
                tech_html += f'<span class="tech-tag">{tech}</span>'
            tech_html += '</div>'
            st.markdown(tech_html, unsafe_allow_html=True)
            
            st.markdown(f"**Prize:** {challenge['prize']}")
            st.markdown(f"**Difficulty:** {challenge['difficulty'].upper()}")
    
    def display_repository_input(self):
        """Display repository URL input"""
        st.markdown('<p class="section-title">📂 Analyze Repository</p>', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([3, 1, 1])
        
        with col1:
            st.markdown("""
            <style>
            div[data-testid="stTextInput"] input {
                color: #1f2937 !important;
                background: white !important;
            }
            </style>
            """, unsafe_allow_html=True)
            
            repo_url = st.text_input(
                "GitHub Repository URL",
                value=st.session_state.repo_url,
                placeholder="https://github.com/username/repository",
                label_visibility="collapsed",
                help="Enter a public GitHub repository URL"
            )
            
            if repo_url != st.session_state.repo_url:
                st.session_state.repo_url = repo_url
            
            if repo_url:
                if self.validate_github_url(repo_url):
                    st.success("✅ Valid GitHub URL")
                    st.markdown(f"**Repository to analyze:** `{repo_url}`")
                else:
                    st.error("❌ Invalid GitHub URL format")
        
        with col2:
            exp_level = st.session_state.experience_level
            exp_display = exp_level.replace("_", " ").title()
            st.metric("Experience", exp_display, delta=None)
        
        with col3:
            analyze_disabled = not (
                st.session_state.selected_challenge and 
                repo_url and 
                self.validate_github_url(repo_url) and
                not st.session_state.is_analyzing and
                ANALYZER_AVAILABLE
            )
            
            analyze_text = "🚀 Analyzing..." if st.session_state.is_analyzing else "🚀 Start Analysis"
            
            if st.button(
                analyze_text,
                type="primary",
                disabled=analyze_disabled,
                use_container_width=True,
                key="start_analysis",
                help="Start repository analysis"
            ):
                st.session_state.is_analyzing = True
                st.session_state.error_message = None
                
                try:
                    self.run_analysis(repo_url)
                except Exception as e:
                    st.session_state.error_message = str(e)
                    st.session_state.is_analyzing = False
                    st.rerun()
    
    def run_analysis(self, repo_url: str):
        """Run analysis using the GitHub Analyzer Agent"""
        try:
            if not self.analyzer_agent:
                if not self.initialize_analyzer_agent():
                    st.session_state.is_analyzing = False
                    return
            
            owner, repo = self.extract_repo_info(repo_url)
            if not owner or not repo:
                st.error("❌ Could not extract repository information from URL")
                st.session_state.is_analyzing = False
                return
            
            challenge = st.session_state.selected_challenge
            experience_level = st.session_state.experience_level
            
            with st.status("🔄 Running Analysis...", expanded=True) as status:
                status.write("1. 📥 Extracting repository content...")
                time.sleep(1)
                
                status.write("2. 🔍 AI analyzing codebase...")
                
                analysis_result = self.analyzer_agent.analyze_repository(
                    github_repo=repo_url,
                    github_project_name=challenge['title'],
                    eval_criteria=challenge['eval_criteria'],
                    skills=challenge['skills']
                )
                
                if analysis_result.get("status") == "error":
                    raise Exception(f"Analysis failed: {analysis_result.get('message')}")
                
                st.session_state.analysis_results = analysis_result
                
                status.write("3. 🔬 Performing deep code analysis...")
                time.sleep(1)
                
                try:
                    from real_analyzer import RealRepositoryAnalyzer
                    
                    import tempfile
                    import subprocess
                    with tempfile.TemporaryDirectory() as temp_dir:
                        status.write("   📂 Downloading full repository...")
                        download_success = False
                        try:
                            clone_cmd = f"git clone {repo_url} {temp_dir}/repo --depth 1"
                            result = subprocess.run(clone_cmd, shell=True, capture_output=True, text=True, timeout=60)
                            if result.returncode == 0:
                                download_success = True
                                status.write("   ✅ Repository downloaded successfully")
                            else:
                                status.write("   ⚠️ Git clone failed, using API analysis only")
                        except:
                            status.write("   ⚠️ Could not download repository, using API analysis only")
                        
                        if download_success:
                            deep_analyzer = RealRepositoryAnalyzer(f"{temp_dir}/repo")
                            deep_analysis = deep_analyzer.analyze_deep()
                            
                            repo_content = self._extract_full_repo_content(f"{temp_dir}/repo")
                            
                            status.write("4. 🎯 Applying experience-aware evaluation...")
                            time.sleep(0.5)
                            
                            # Calculate experience-adjusted score
                            exp_evaluator = ExperienceScoringEngine()
                            raw_score = analysis_result.get("data", {}).get("final_report", {}).get("report", {}).get("hidevs_score", {}).get("score", 70)
                            
                            experience_adjusted_score = exp_evaluator.adjust_score_for_experience(
                                raw_score=raw_score,
                                experience_level=experience_level,
                                code_analysis=deep_analysis,
                                challenge_id=challenge['id']
                            )
                            
                            st.session_state.experience_adjusted_score = experience_adjusted_score
                            
                            if analysis_result.get("status") == "success":
                                report_data = analysis_result.get("data", {}).get("final_report", {})
                                if report_data:
                                    report_data['experience_evaluation'] = {
                                        'experience_level': experience_level,
                                        'raw_score': raw_score,
                                        'adjusted_score': experience_adjusted_score['final_score'],
                                        'score_breakdown': experience_adjusted_score['breakdown'],
                                        'industry_benchmark': experience_adjusted_score['industry_benchmark'],
                                        'feedback': experience_adjusted_score['feedback']
                                    }
                                    st.session_state.evaluation_report = report_data
                                    status.write("   ✅ Experience evaluation complete")
                        else:
                            if analysis_result.get("status") == "success":
                                report_data = analysis_result.get("data", {}).get("final_report", {})
                                if report_data:
                                    st.session_state.evaluation_report = report_data
                
                except Exception as e:
                    status.write(f"⚠️ Deep analysis skipped: {str(e)}")
                    if analysis_result.get("status") == "success":
                        report_data = analysis_result.get("data", {}).get("final_report", {})
                        if report_data:
                            st.session_state.evaluation_report = report_data
                
                status.write("5. ✅ Finalizing analysis...")
                time.sleep(0.5)
            
            st.session_state.is_analyzing = False
            st.success("✅ Analysis complete!")
            st.rerun()
            
        except Exception as e:
            st.session_state.is_analyzing = False
            st.error(f"❌ Analysis failed: {str(e)}")
    
    def _extract_full_repo_content(self, repo_path: str) -> str:
        """Extract full repository content as text"""
        import os
        from pathlib import Path
        
        content_parts = []
        repo_path_obj = Path(repo_path)
        
        text_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.java', '.cpp', '.c', '.go', 
                          '.rs', '.rb', '.php', '.html', '.css', '.scss', '.less', '.md', 
                          '.txt', '.json', '.yaml', '.yml', '.toml', '.ini', '.cfg'}
        
        for file_path in repo_path_obj.rglob('*'):
            if file_path.is_file() and file_path.suffix in text_extensions:
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(5000)
                        content_parts.append(f"\n{'='*80}\nFile: {file_path.relative_to(repo_path_obj)}\n{'='*80}\n{content}")
                except:
                    continue
        
        return "\n".join(content_parts[:50])
    
    def display_results(self):
        """Display analysis results"""
        if not st.session_state.evaluation_report:
            return
        
        report = st.session_state.evaluation_report
        challenge = st.session_state.selected_challenge
        
        st.markdown("## 📈 Evaluation Results")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.markdown(f"**Repository:**")
            st.code(st.session_state.repo_url, language="text")
        with col2:
            st.markdown(f"**Challenge:** {challenge['title']}")
        with col3:
            exp_level = st.session_state.experience_level
            exp_display = exp_level.replace('_', ' ').title()
            st.markdown(f"**Experience:** {exp_display}")
        with col4:
            st.markdown(f"**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # 1. TOTAL SCORE CALCULATION
        self._display_total_score(report)
        
        st.markdown("---")
        
        # 2. MARKS DISTRIBUTION
        self._display_marks_distribution(report)
        
        st.markdown("---")
        
        # 3. WHAT IS GOOD
        self._display_whats_good(report)
        
        st.markdown("---")
        
        # 4. WHAT IS NOT GOOD
        self._display_whats_not_good(report)
        
        st.markdown("---")
        
        # 5. INDUSTRY EXPECTATIONS
        self._display_industry_expectations(report)
        
        st.markdown("---")
        
        # 6. RECOMMENDATION
        self._display_recommendation(report)
        
        st.markdown("---")
        
        # Action buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📥 Download Full Report", use_container_width=True):
                self.download_report(report)
        
        with col2:
            if st.button("📋 Copy Summary", use_container_width=True):
                self.copy_summary(report)
        
        with col3:
            if st.button("🔄 New Analysis", type="primary", use_container_width=True):
                self.reset_analysis()
    
    def _display_total_score(self, report: Dict):
        """Display total score calculation"""
        st.markdown('<p class="section-title">1. 📊 TOTAL SCORE CALCULATION</p>', unsafe_allow_html=True)
        
        if 'experience_evaluation' in report:
            exp_eval = report['experience_evaluation']
            raw_score = exp_eval.get('raw_score', 0)
            adjusted_score = exp_eval.get('adjusted_score', 0)
            breakdown = exp_eval.get('score_breakdown', {})
            
            # Display calculation steps
            st.markdown("### 🔢 How Your Score Was Calculated:")
            
            if breakdown:
                # Show calculation steps
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Score Breakdown:**")
                    for category, details in breakdown.items():
                        if isinstance(details, dict):
                            score = details.get('score', 0)
                            explanation = details.get('explanation', '')
                            st.markdown(f"- **{category}:** {score:.1f}/100")
                            if explanation:
                                with st.expander(f"ℹ️ {category} details"):
                                    st.info(explanation)
                
                with col2:
                    st.markdown("**Experience Adjustment:**")
                    exp_level = st.session_state.experience_level
                    exp_display = exp_level.replace('_', ' ').title()
                    
                    # Show raw vs adjusted
                    st.metric("Raw Technical Score", f"{raw_score:.1f}/100")
                    st.metric("Experience Level", exp_display)
                    
                    adjustment = adjusted_score - raw_score
                    st.metric("Experience Adjustment", f"{adjustment:+.1f} points")
                    st.metric("Final Adjusted Score", f"{adjusted_score:.1f}/100", 
                             delta=f"{adjustment:+.1f}" if adjustment != 0 else "0")
            
            # Visual score comparison
            exp_level = st.session_state.experience_level
            benchmark_scores = {
                "1st_year": 60, "2nd_year": 65, "3rd_year": 70, 
                "4th_year": 75, "fresher": 68, "experienced_0_2": 78, "senior": 85
            }
            
            benchmark = benchmark_scores.get(exp_level, 70)
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: #f0f9ff; border-radius: 10px; border: 2px solid #3b82f6;">
                    <div style="font-size: 0.9rem; color: #1e40af; margin-bottom: 5px;">Your Score</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #1e40af;">{adjusted_score:.1f}</div>
                    <div style="font-size: 0.8rem; color: #6b7280;">/100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: #f0fdf4; border-radius: 10px; border: 2px solid #10b981;">
                    <div style="font-size: 0.9rem; color: #065f46; margin-bottom: 5px">Industry Benchmark</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: #065f46;">{benchmark}</div>
                    <div style="font-size: 0.8rem; color: #6b7280;">/100</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col3:
                gap = adjusted_score - benchmark
                gap_color = "#10b981" if gap >= 0 else "#ef4444"
                gap_icon = "📈" if gap >= 0 else "📉"
                
                st.markdown(f"""
                <div style="text-align: center; padding: 15px; background: #fef3f2; border-radius: 10px; border: 2px solid {gap_color};">
                    <div style="font-size: 0.9rem; color: {gap_color}; margin-bottom: 5px">Performance Gap</div>
                    <div style="font-size: 2.5rem; font-weight: 700; color: {gap_color};">{gap_icon} {gap:+.1f}</div>
                    <div style="font-size: 0.8rem; color: #6b7280;">points vs benchmark</div>
                </div>
                """, unsafe_allow_html=True)
    
    def _display_marks_distribution(self, report: Dict):
        """Display marks distribution"""
        st.markdown('<p class="section-title">2. 📈 MARKS DISTRIBUTION</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'evaluation_criteria' in report['report']:
            import pandas as pd
            criteria_data = []
            total_score = 0
            criteria_count = 0
            
            for criterion in report['report']['evaluation_criteria']:
                criteria_name = criterion.get('criterion_name', 'Unknown')
                score = criterion.get('score', 0)
                assessment = criterion.get('score_guide', 'No assessment')
                
                criteria_data.append({
                    'Criteria': criteria_name,
                    'Score': f"{score}/100",
                    'Assessment': assessment[:80] + "..." if len(assessment) > 80 else assessment
                })
                
                total_score += score
                criteria_count += 1
            
            if criteria_data:
                df = pd.DataFrame(criteria_data)
                st.dataframe(df, use_container_width=True, hide_index=True)
                
                if criteria_count > 0:
                    avg_score = total_score / criteria_count
                    st.metric("Average Score", f"{avg_score:.1f}/100")
        
        # Also show experience-specific breakdown if available
        if 'experience_evaluation' in report:
            exp_eval = report['experience_evaluation']
            if 'score_breakdown' in exp_eval:
                st.markdown("#### 🎓 Experience-Specific Breakdown:")
                
                breakdown = exp_eval['score_breakdown']
                for category, details in breakdown.items():
                    if isinstance(details, dict):
                        score = details.get('score', 0)
                        max_score = details.get('max_score', 100)
                        
                        # Create a progress bar
                        progress = score / max_score if max_score > 0 else 0
                        color = "#10b981" if progress >= 0.8 else "#f59e0b" if progress >= 0.6 else "#ef4444"
                        
                        st.markdown(f"""
                        <div style="margin: 10px 0;">
                            <div style="display: flex; justify-content: space-between; margin-bottom: 5px;">
                                <span style="font-weight: 600; font-size: 14px;">{category.replace('_', ' ').title()}</span>
                                <span style="font-weight: 600; font-size: 14px; color: {color};">{score:.1f}/{max_score}</span>
                            </div>
                            <div style="height: 8px; background: #e5e7eb; border-radius: 4px; overflow: hidden;">
                                <div style="height: 100%; width: {progress*100}%; background: {color}; border-radius: 4px;"></div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)
    
    def _display_whats_good(self, report: Dict):
        """Display what is good"""
        st.markdown('<p class="section-title">3. ✅ WHAT IS GOOD</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'final_deliverables' in report['report']:
            strengths = report['report']['final_deliverables'].get('key_strengths', [])
            if strengths:
                for idx, strength in enumerate(strengths[:5], 1):
                    st.markdown(f"""
                    <div class="analysis-box">
                        <strong>Strength #{idx}</strong>
                        <p>{strength}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No specific strengths identified in analysis")
        
        # Add experience-specific strengths
        exp_level = st.session_state.experience_level
        exp_strengths = {
            "1st_year": [
                "Good foundational understanding for a first-year student",
                "Shows enthusiasm and willingness to learn",
                "Basic implementation demonstrates comprehension"
            ],
            "2nd_year": [
                "Improved code structure compared to first year",
                "Shows understanding of basic design patterns",
                "Good progress in technical skills"
            ],
            "3rd_year": [
                "Good architectural decisions",
                "Proper error handling implementation",
                "Shows understanding of software engineering principles"
            ],
            "4th_year": [
                "Near-production quality code",
                "Good consideration of scalability",
                "Professional approach to problem-solving"
            ],
            "fresher": [
                "Solid foundation for entry-level position",
                "Good practical implementation",
                "Shows potential for growth"
            ],
            "experienced_0_2": [
                "Industry-standard practices",
                "Good consideration of real-world constraints",
                "Professional code quality"
            ],
            "senior": [
                "Enterprise-level architecture",
                "Excellent consideration of scalability and maintainability",
                "Leadership-level technical decisions"
            ]
        }
        
        strengths_list = exp_strengths.get(exp_level, [])
        if strengths_list:
            st.markdown(f"#### 🎓 Strengths for {exp_level.replace('_', ' ').title()}:")
            for strength in strengths_list:
                st.markdown(f"✅ {strength}")
    
    def _display_whats_not_good(self, report: Dict):
        """Display what is not good"""
        st.markdown('<p class="section-title">4. ⚠️ WHAT IS NOT GOOD</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'final_deliverables' in report['report']:
            improvements = report['report']['final_deliverables'].get('key_areas_for_improvement', [])
            if improvements:
                for idx, improvement in enumerate(improvements[:5], 1):
                    st.markdown(f"""
                    <div class="analysis-box">
                        <strong>Improvement Needed #{idx}</strong>
                        <p>{improvement}</p>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.info("No specific areas for improvement identified")
        
        # Add experience-specific improvements
        exp_level = st.session_state.experience_level
        exp_improvements = {
            "1st_year": [
                "Needs more comments and documentation",
                "Basic error handling could be improved",
                "Code organization needs work"
            ],
            "2nd_year": [
                "Should implement more testing",
                "Could use better design patterns",
                "Needs more modular code structure"
            ],
            "3rd_year": [
                "Should consider scalability more",
                "Needs better documentation",
                "Could implement more advanced features"
            ],
            "4th_year": [
                "Production deployment considerations",
                "Monitoring and observability",
                "Security aspects need attention"
            ],
            "fresher": [
                "Industry best practices implementation",
                "Production readiness",
                "Advanced testing strategies"
            ],
            "experienced_0_2": [
                "Enterprise architecture patterns",
                "Advanced security considerations",
                "System design at scale"
            ],
            "senior": [
                "Strategic technical leadership",
                "Complex system architecture",
                "Advanced performance optimization"
            ]
        }
        
        improvements_list = exp_improvements.get(exp_level, [])
        if improvements_list:
            st.markdown(f"#### 🎓 Areas to Improve for {exp_level.replace('_', ' ').title()}:")
            for improvement in improvements_list:
                st.markdown(f"⚠️ {improvement}")
    
    def _display_industry_expectations(self, report: Dict):
        """Display industry expectations"""
        st.markdown('<p class="section-title">5. 🏢 INDUSTRY EXPECTATIONS</p>', unsafe_allow_html=True)
        
        exp_level = st.session_state.experience_level
        exp_display = exp_level.replace('_', ' ').title()
        
        # Industry benchmarks for each level
        benchmarks = {
            "1st_year": {
                "score_range": "95-100",
                "expectations": [
                    "Basic understanding of programming concepts",
                    "Ability to write simple working code",
                    "Familiarity with version control",
                    "Understanding of basic algorithms"
                ]
            },
            "2nd_year": {
                "score_range": "90-95", 
                "expectations": [
                    "Good grasp of data structures",
                    "Ability to work with APIs",
                    "Basic understanding of databases",
                    "Simple project implementation"
                ]
            },
            "3rd_year": {
                "score_range": "80-85",
                "expectations": [
                    "Good software design principles",
                    "Ability to work in teams",
                    "Understanding of testing",
                    "Moderate complexity projects"
                ]
            },
            "4th_year": {
                "score_range": "75-80",
                "expectations": [
                    "Production-ready code quality",
                    "Good architecture decisions",
                    "Understanding of deployment",
                    "Complex project implementation"
                ]
            },
            "fresher": {
                "score_range": "70-75",
                "expectations": [
                    "Industry-standard coding practices",
                    "Ability to work independently",
                    "Good problem-solving skills",
                    "Ready for entry-level position"
                ]
            },
            "experienced_0_2": {
                "score_range": "65-70",
                "expectations": [
                    "Professional code quality",
                    "Good system design",
                    "Understanding of scalability",
                    "Team collaboration skills"
                ]
            },
            "senior": {
                "score_range": "60-65",
                "expectations": [
                    "Enterprise architecture",
                    "Leadership in technical decisions",
                    "Advanced system design",
                    "Mentorship capabilities"
                ]
            }
        }
        
        benchmark = benchmarks.get(exp_level, benchmarks["fresher"])
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
            <div style="background: #f8fafc; padding: 15px; border-radius: 10px; border: 2px solid #6366f1;">
                <div style="font-size: 1.2rem; font-weight: 600; color: #6366f1; margin-bottom: 10px;">
                    Industry Standards for {exp_display}
                </div>
                <div style="font-size: 2rem; font-weight: 700; color: #1f2937; margin-bottom: 15px;">
                    Expected Score: {benchmark['score_range']}
                </div>
                <div style="font-size: 0.9rem; color: #6b7280;">
                    This is the typical score range expected for developers at this experience level
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background: #f0f9ff; padding: 15px; border-radius: 10px; border: 2px solid #3b82f6;">
                <div style="font-size: 1.1rem; font-weight: 600; color: #1e40af; margin-bottom: 10px;">
                    Key Expectations:
                </div>
                <ul style="margin: 0; padding-left: 20px;">
            """, unsafe_allow_html=True)
            
            for expectation in benchmark['expectations'][:4]:
                st.markdown(f"<li style='margin-bottom: 5px; color: #4b5563;'>{expectation}</li>", unsafe_allow_html=True)
            
            st.markdown("</ul>", unsafe_allow_html=True)
        
        # Show how they compare
        if 'experience_evaluation' in report:
            exp_eval = report['experience_evaluation']
            adjusted_score = exp_eval.get('adjusted_score', 0)
            
            expected_range = benchmark['score_range']
            low, high = map(int, expected_range.split('-'))
            
            if low <= adjusted_score <= high:
                status = "✅ MEETS EXPECTATIONS"
                color = "#10b981"
                icon = "🎯"
            elif adjusted_score > high:
                status = "🎖️ EXCEEDS EXPECTATIONS"
                color = "#8b5cf6"
                icon = "🏆"
            else:
                status = "⚠️ BELOW EXPECTATIONS"
                color = "#ef4444"
                icon = "📉"
            
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #ffffff 0%, {color}15 100%); 
                      padding: 15px; border-radius: 10px; border: 2px solid {color}; 
                      margin-top: 15px;">
                <div style="display: flex; align-items: center; gap: 10px;">
                    <div style="font-size: 2rem;">{icon}</div>
                    <div>
                        <div style="font-size: 1.2rem; font-weight: 600; color: {color};">
                            {status}
                        </div>
                        <div style="font-size: 0.9rem; color: #6b7280; margin-top: 5px;">
                            Your score of {adjusted_score:.1f}/100 compares to the expected range of {expected_range} for {exp_display}
                        </div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    def _display_recommendation(self, report: Dict):
        """Display hiring recommendation"""
        st.markdown('<p class="section-title">6. 🤝 HIRING RECOMMENDATION</p>', unsafe_allow_html=True)
        
        if 'experience_evaluation' in report:
            exp_eval = report['experience_evaluation']
            adjusted_score = exp_eval.get('adjusted_score', 0)
            exp_level = st.session_state.experience_level
            
            # Determine recommendation based on score and experience
            recommendations = {
                "1st_year": [
                    (90, "✅ Excellent potential! Consider for internship with mentorship"),
                    (80, "👍 Good foundation. Suitable for learning internship"),
                    (70, "🤔 Shows potential but needs guidance. Consider for supervised projects"),
                    (0, "📚 Needs more learning. Recommend additional coursework")
                ],
                "2nd_year": [
                    (88, "✅ Strong candidate for summer internship"),
                    (78, "👍 Good progress. Suitable for project-based internship"),
                    (68, "🤔 Developing skills. Consider for structured internship program"),
                    (0, "📚 Needs focused improvement in core concepts")
                ],
                "3rd_year": [
                    (85, "✅ Ready for technical internship with responsibilities"),
                    (75, "👍 Good candidate for entry-level internship"),
                    (65, "🤔 Borderline. Consider for internship with close supervision"),
                    (0, "📚 Needs to strengthen technical fundamentals")
                ],
                "4th_year": [
                    (82, "✅ Strong hire for entry-level position"),
                    (72, "👍 Suitable for junior developer role"),
                    (62, "🤔 Consider for internship-to-hire program"),
                    (0, "📚 Needs portfolio projects to demonstrate skills")
                ],
                "fresher": [
                    (80, "✅ Strong hire for entry-level position"),
                    (70, "👍 Good candidate for junior developer role"),
                    (60, "🤔 Consider for probationary position with training"),
                    (0, "📚 Needs more practical experience before hiring")
                ],
                "experienced_0_2": [
                    (85, "✅ Excellent hire for mid-level position"),
                    (75, "👍 Good fit for experienced junior role"),
                    (65, "🤔 Consider for position with growth opportunities"),
                    (0, "📚 Needs to demonstrate more practical experience")
                ],
                "senior": [
                    (90, "✅ Exceptional candidate for senior/lead position"),
                    (80, "👍 Strong senior developer candidate"),
                    (70, "🤔 Consider for senior role with specific domain expertise"),
                    (0, "📚 Needs to demonstrate leadership and architecture skills")
                ]
            }
            
            rec_rules = recommendations.get(exp_level, recommendations["fresher"])
            recommendation = ""
            
            for threshold, rec_text in rec_rules:
                if adjusted_score >= threshold:
                    recommendation = rec_text
                    break
            
            # Get icon and color based on score
            if adjusted_score >= 85:
                icon = "🏆"
                color = "#10b981"
                bg_color = "#d1fae5"
            elif adjusted_score >= 75:
                icon = "👍"
                color = "#3b82f6"
                bg_color = "#dbeafe"
            elif adjusted_score >= 65:
                icon = "🤔"
                color = "#f59e0b"
                bg_color = "#fef3c7"
            else:
                icon = "📚"
                color = "#ef4444"
                bg_color = "#fee2e2"
            
            # Display recommendation
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: {bg_color}; 
                          border-radius: 10px; border: 2px solid {color};">
                    <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: {color};">
                        {recommendation.split(' ')[0]}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div style="background: #f8fafc; padding: 20px; border-radius: 10px; border-left: 4px solid {color};">
                    <div style="font-size: 1.3rem; font-weight: 600; color: {color}; margin-bottom: 10px;">
                        Recommendation Details
                    </div>
                    <div style="color: #4b5563; line-height: 1.6;">
                        {recommendation}
                    </div>
                    <div style="margin-top: 15px; padding: 10px; background: white; border-radius: 6px;">
                        <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px;">Score Analysis:</div>
                        <div style="font-size: 1.1rem; color: #1f2937;">
                            <strong>{adjusted_score:.1f}/100</strong> for a {exp_level.replace('_', ' ').title()}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Next steps
            st.markdown("#### 📝 Next Steps:")
            
            next_steps = []
            if adjusted_score >= 80:
                next_steps.extend([
                    "Proceed to technical interview",
                    "Schedule system design discussion",
                    "Prepare for coding assessment"
                ])
            elif adjusted_score >= 70:
                next_steps.extend([
                    "Conduct technical screening",
                    "Review specific technical skills",
                    "Consider practical assignment"
                ])
            else:
                next_steps.extend([
                    "Provide constructive feedback",
                    "Suggest specific learning resources",
                    "Consider re-evaluation after improvement"
                ])
            
            for step in next_steps:
                st.markdown(f"• {step}")
    
    def download_report(self, report: Dict):
        """Download evaluation report"""
        try:
            full_report = {
                'repository': st.session_state.repo_url,
                'challenge': st.session_state.selected_challenge['title'],
                'experience_level': st.session_state.experience_level,
                'analysis_date': datetime.now().isoformat(),
                'overall_score': report['report']['hidevs_score']['score'] if 'report' in report and 'hidevs_score' in report['report'] else 0,
                'evaluation_results': report
            }
            
            report_json = json.dumps(full_report, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="⬇️ Download JSON Report",
                data=report_json,
                file_name=f"repo_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        except Exception as e:
            st.error(f"Failed to generate report: {str(e)}")
    
    def copy_summary(self, report: Dict):
        """Copy summary to clipboard"""
        try:
            score = report['report']['hidevs_score']['score'] if 'report' in report and 'hidevs_score' in report['report'] else 0
            challenge = st.session_state.selected_challenge['title']
            repo_url = st.session_state.repo_url
            exp_level = st.session_state.experience_level
            
            summary = f"""
GitHub Repository Evaluation Summary
====================================
Repository: {repo_url}
Challenge: {challenge}
Experience Level: {exp_level.replace('_', ' ').title()}
Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

OVERALL SCORE: {score}/100
"""
            
            if 'experience_evaluation' in report:
                exp_eval = report['experience_evaluation']
                exp_score = exp_eval.get('adjusted_score', 0)
                exp_benchmark = exp_eval.get('industry_benchmark', 0)
                
                summary += f"""
EXPERIENCE-AWARE EVALUATION:
----------------------------
Raw Technical Score: {exp_eval.get('raw_score', 0):.1f}/100
Adjusted Score: {exp_score:.1f}/100
Industry Benchmark: {exp_benchmark}/100
Performance Gap: {exp_score - exp_benchmark:+.1f}

"""
            
            summary += f"""
RECOMMENDATION: {'Strong Hire' if score >= 85 else 'Hire' if score >= 70 else 'Consider' if score >= 60 else 'Do Not Hire'}
            """
            
            st.code(summary, language="text")
            st.success("📋 Summary displayed above. Select and copy manually.")
            
        except Exception as e:
            st.error(f"Failed to generate summary: {str(e)}")
    
    def reset_analysis(self):
        """Reset analysis state"""
        st.session_state.analysis_results = None
        st.session_state.evaluation_report = None
        st.session_state.repo_url = ''
        st.session_state.is_analyzing = False
        st.session_state.error_message = None
        st.session_state.experience_adjusted_score = None
        st.rerun()
    
    def display_error(self):
        """Display error message if any"""
        if st.session_state.error_message:
            st.error(f"❌ Error: {st.session_state.error_message}")
        
        if not ANALYZER_AVAILABLE:
            st.error("❌ Analyzer module not available. Please check that all dependencies are installed.")
    
    def run(self):
        """Main application runner"""
        self.display_header()
        
        if not ANALYZER_AVAILABLE:
            st.error("""
            ⚠️ **Setup Required:**
            1. Install dependencies: `pip install streamlit google-generativeai pygithub python-dotenv requests pydantic PyYAML gitpython`
            2. Create `.env` file with:
               - GEMINI_API_KEY=your_key_here
               - GITHUB_TOKEN=your_token_here
            3. Restart the application
            """)
            return
        
        if not os.environ.get("GEMINI_API_KEY") or not os.environ.get("GITHUB_TOKEN"):
            st.error("""
            ⚠️ **API Keys Missing:**
            Please create a `.env` file in the project root with:
            ```
            GEMINI_API_KEY=your_gemini_api_key_here
            GITHUB_TOKEN=your_github_token_here
            ```
            """)
        
        self.display_challenge_selector()
        self.display_experience_selector()
        self.display_selected_challenge_info()
        self.display_repository_input()
        self.display_error()
        
        if st.session_state.is_analyzing:
            st.info("🔄 Analysis in progress... This may take 1-2 minutes.")
        
        if st.session_state.evaluation_report:
            self.display_results()
        
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6b7280; font-size: 11px; padding: 15px;'>
            <div style="font-size: 12px; font-weight: 600; color: #4f46e5; margin-bottom: 5px;">
                GitHub Repository Evaluator v2.0
            </div>
            <div>AI-Powered Technical Assessment • Real GitHub Analysis • Experience-Aware Evaluation</div>
            <div style="margin-top: 5px; font-size: 10px;">Powered by Gemini AI • Secure & Confidential</div>
        </div>
        """, unsafe_allow_html=True)

class ExperienceScoringEngine:
    """Engine to adjust scores based on experience level"""
    
    def __init__(self):
        self.experience_multipliers = {
            "1st_year": 1.0,    # No penalty
            "2nd_year": 0.95,   # Slight penalty
            "3rd_year": 0.90,   # More penalty
            "4th_year": 0.85,   # Significant penalty
            "fresher": 0.92,    # Recent grad penalty
            "experienced_0_2": 0.80,  # Experienced penalty
            "senior": 0.75      # Senior penalty (strictest)
        }
        
        self.industry_benchmarks = {
            "1st_year": 60,
            "2nd_year": 65,
            "3rd_year": 70,
            "4th_year": 75,
            "fresher": 68,
            "experienced_0_2": 78,
            "senior": 85
        }
    
    def adjust_score_for_experience(self, raw_score: float, experience_level: str, 
                                   code_analysis: Dict, challenge_id: str) -> Dict:
        """
        Adjust score based on experience level with proper calculations
        
        Higher experience = stricter grading = lower scores for same quality
        """
        
        # Base adjustment
        multiplier = self.experience_multipliers.get(experience_level, 0.85)
        industry_benchmark = self.industry_benchmarks.get(experience_level, 70)
        
        # Calculate experience penalties based on code analysis
        penalties = self._calculate_penalties(code_analysis, experience_level, challenge_id)
        
        # Calculate experience rewards based on exceeding expectations
        rewards = self._calculate_rewards(code_analysis, experience_level, challenge_id)
        
        # Apply adjustments
        adjusted_score = raw_score * multiplier
        adjusted_score = max(0, min(100, adjusted_score - penalties + rewards))
        
        # Generate breakdown
        breakdown = self._generate_score_breakdown(
            raw_score, adjusted_score, multiplier, penalties, rewards,
            experience_level, code_analysis
        )
        
        # Generate feedback
        feedback = self._generate_feedback(
            raw_score, adjusted_score, industry_benchmark,
            experience_level, penalties, rewards
        )
        
        return {
            'raw_score': raw_score,
            'final_score': adjusted_score,
            'industry_benchmark': industry_benchmark,
            'experience_level': experience_level,
            'multiplier_applied': multiplier,
            'penalties_applied': penalties,
            'rewards_applied': rewards,
            'breakdown': breakdown,
            'feedback': feedback
        }
    
    def _calculate_penalties(self, code_analysis: Dict, experience_level: str, challenge_id: str) -> float:
        """Calculate penalties based on missing expectations for experience level"""
        penalties = 0
        
        # Higher experience = higher expectations
        if experience_level in ["senior", "experienced_0_2"]:
            # Enterprise expectations
            if not code_analysis.get("docker", {}).get("has_dockerfile", False):
                penalties += 5
            if not code_analysis.get("testing", {}).get("has_tests", False):
                penalties += 8
            if not code_analysis.get("ci_cd", {}).get("has_ci", False):
                penalties += 3
            if code_analysis.get("documentation", {}).get("readme", {}).get("quality_score", 0) < 7:
                penalties += 4
        
        elif experience_level in ["3rd_year", "4th_year"]:
            # Intermediate expectations
            if not code_analysis.get("testing", {}).get("has_tests", False):
                penalties += 5
            if not code_analysis.get("docker", {}).get("has_dockerfile", False):
                penalties += 3
            if code_analysis.get("documentation", {}).get("readme", {}).get("quality_score", 0) < 5:
                penalties += 3
        
        elif experience_level in ["1st_year", "2nd_year", "fresher"]:
            # Junior expectations (minimal penalties)
            if not code_analysis.get("documentation", {}).get("readme", {}).get("exists", False):
                penalties += 2
        
        # Challenge-specific penalties
        penalties += self._calculate_challenge_penalties(code_analysis, challenge_id, experience_level)
        
        return penalties
    
    def _calculate_challenge_penalties(self, code_analysis: Dict, challenge_id: str, experience_level: str) -> float:
        """Calculate challenge-specific penalties"""
        penalties = 0
        
        challenge_specific = code_analysis.get("challenge_specific", {})
        
        if challenge_id == "challenge_023":  # AI Agents
            if not challenge_specific.get("ai_ml_indicators", {}).get("has_ai_ml", False):
                if experience_level in ["senior", "experienced_0_2"]:
                    penalties += 10
                elif experience_level in ["3rd_year", "4th_year"]:
                    penalties += 7
                else:
                    penalties += 3
        
        elif challenge_id == "challenge_024":  # Healthcare AI
            if not challenge_specific.get("ai_ml_indicators", {}).get("has_ai_ml", False):
                if experience_level in ["senior", "experienced_0_2"]:
                    penalties += 8
                elif experience_level in ["3rd_year", "4th_year"]:
                    penalties += 5
        
        return penalties
    
    def _calculate_rewards(self, code_analysis: Dict, experience_level: str, challenge_id: str) -> float:
        """Calculate rewards for exceeding expectations"""
        rewards = 0
        
        # Higher experience = fewer rewards (already expected)
        if experience_level in ["1st_year", "2nd_year"]:
            # Junior developers get rewarded for good work
            if code_analysis.get("testing", {}).get("has_tests", False):
                rewards += 3
            if code_analysis.get("docker", {}).get("has_dockerfile", False):
                rewards += 2
            if code_analysis.get("ci_cd", {}).get("has_ci", False):
                rewards += 2
        
        # Excellent documentation for any level
        if code_analysis.get("documentation", {}).get("readme", {}).get("quality_score", 0) >= 8:
            rewards += 2
        
        return rewards
    
    def _generate_score_breakdown(self, raw_score: float, adjusted_score: float, 
                                 multiplier: float, penalties: float, rewards: float,
                                 experience_level: str, code_analysis: Dict) -> Dict:
        """Generate detailed score breakdown"""
        
        breakdown = {
            "raw_technical_score": {
                "score": raw_score,
                "max_score": 100,
                "explanation": "Score from AI analysis of repository"
            },
            "experience_adjustment": {
                "score": -(1 - multiplier) * raw_score,
                "max_score": 0,
                "explanation": f"Adjustment for {experience_level.replace('_', ' ')} expectations"
            },
            "penalties": {
                "score": -penalties,
                "max_score": 0,
                "explanation": "Penalties for missing features expected at this level"
            },
            "rewards": {
                "score": rewards,
                "max_score": 10,
                "explanation": "Rewards for exceeding expectations"
            },
            "final_score": {
                "score": adjusted_score,
                "max_score": 100,
                "explanation": "Final experience-adjusted score"
            }
        }
        
        # Add specific penalty/reward details
        penalty_details = []
        reward_details = []
        
        if penalties > 0:
            if not code_analysis.get("testing", {}).get("has_tests", False):
                penalty_details.append("Missing tests")
            if not code_analysis.get("docker", {}).get("has_dockerfile", False):
                penalty_details.append("Missing Docker configuration")
            if code_analysis.get("documentation", {}).get("readme", {}).get("quality_score", 0) < 5:
                penalty_details.append("Poor documentation")
        
        if rewards > 0:
            if code_analysis.get("documentation", {}).get("readme", {}).get("quality_score", 0) >= 8:
                reward_details.append("Excellent documentation")
            if code_analysis.get("ci_cd", {}).get("has_ci", False):
                reward_details.append("CI/CD pipeline present")
        
        breakdown["penalty_details"] = penalty_details
        breakdown["reward_details"] = reward_details
        
        return breakdown
    
    def _generate_feedback(self, raw_score: float, adjusted_score: float, 
                          benchmark: float, experience_level: str,
                          penalties: float, rewards: float) -> str:
        """Generate feedback based on score and experience"""
        
        feedback_parts = []
        
        # Overall assessment
        if adjusted_score >= benchmark + 10:
            feedback_parts.append(f"✅ **EXCELLENT PERFORMANCE:** Your score of {adjusted_score:.1f} significantly exceeds the {experience_level.replace('_', ' ')} benchmark of {benchmark}.")
        elif adjusted_score >= benchmark:
            feedback_parts.append(f"👍 **GOOD PERFORMANCE:** Your score of {adjusted_score:.1f} meets the {experience_level.replace('_', ' ')} benchmark of {benchmark}.")
        elif adjusted_score >= benchmark - 10:
            feedback_parts.append(f"⚠️ **AVERAGE PERFORMANCE:** Your score of {adjusted_score:.1f} is below the {experience_level.replace('_', ' ')} benchmark of {benchmark}.")
        else:
            feedback_parts.append(f"❌ **BELOW EXPECTATIONS:** Your score of {adjusted_score:.1f} is significantly below the {experience_level.replace('_', ' ')} benchmark of {benchmark}.")
        
        # Explanation of adjustments
        if penalties > 0:
            feedback_parts.append(f"\n**Penalties Applied:** -{penalties:.1f} points for missing features expected at {experience_level.replace('_', ' ')} level.")
        
        if rewards > 0:
            feedback_parts.append(f"\n**Rewards Applied:** +{rewards:.1f} points for exceeding expectations.")
        
        # Experience-specific advice
        if experience_level in ["1st_year", "2nd_year"]:
            feedback_parts.append("\n**For Junior Developers:** Focus on building a strong foundation. Work on clean code, basic testing, and good documentation.")
        elif experience_level in ["3rd_year", "4th_year"]:
            feedback_parts.append("\n**For Intermediate Developers:** Focus on architecture, testing strategies, and production considerations.")
        elif experience_level in ["experienced_0_2", "senior"]:
            feedback_parts.append("\n**For Experienced Developers:** Focus on enterprise patterns, scalability, security, and technical leadership.")
        
        return "\n".join(feedback_parts)

def main():
    """Main application entry point"""
    evaluator = GitHubRepoEvaluator()
    evaluator.run()

if __name__ == "__main__":
    main()
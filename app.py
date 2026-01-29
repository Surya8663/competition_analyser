# app.py - COMPLETE FIXED APPLICATION
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
    from evaluation_logic import RealScoringEngine  # Added import
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
            'show_detailed_report': False
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
                <span style="background: rgba(255,255,255,0.2); padding: 4px 10px; border-radius: 15px;">Challenge Specific</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    def display_challenge_selector(self):
        """Display challenge selection with horizontal tech tags - FIXED LARGER TITLES"""
        st.markdown('<p class="section-title">🎯 Select Challenge</p>', unsafe_allow_html=True)
        
        cols = st.columns(5)
        
        for idx, challenge in enumerate(self.challenges):
            with cols[idx]:
                is_selected = st.session_state.selected_challenge and st.session_state.selected_challenge['id'] == challenge['id']
                
                # Card container
                with st.container():
                    # Title and difficulty - LARGER TITLE FIXED
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
                    
                    # Short description
                    st.markdown(f'<div style="font-size: 10px; color: #6b7280; margin: 5px 0; height: 40px;">{challenge["short_description"][:70]}...</div>', unsafe_allow_html=True)
                    
                    # HORIZONTAL TECH TAGS - FIXED HORIZONTAL DISPLAY
                    tech_html = '<div class="tech-container">'
                    for tech in challenge['technologies'][:4]:  # Show first 4 techs
                        tech_html += f'<span class="tech-tag">{tech}</span>'
                    if len(challenge['technologies']) > 4:
                        tech_html += f'<span class="tech-tag">+{len(challenge["technologies"])-4}</span>'
                    tech_html += '</div>'
                    st.markdown(tech_html, unsafe_allow_html=True)
                    
                    # Select button
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
        """Display repository URL input - FIXED TEXT COLOR"""
        st.markdown('<p class="section-title">📂 Analyze Repository</p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            # Add custom CSS to ensure input text is visible
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
                    # Show the URL entered
                    st.markdown(f"**Repository to analyze:** `{repo_url}`")
                else:
                    st.error("❌ Invalid GitHub URL format")
        
        with col2:
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
            # Initialize analyzer agent
            if not self.analyzer_agent:
                if not self.initialize_analyzer_agent():
                    st.session_state.is_analyzing = False
                    return
            
            # Extract repo info
            owner, repo = self.extract_repo_info(repo_url)
            if not owner or not repo:
                st.error("❌ Could not extract repository information from URL")
                st.session_state.is_analyzing = False
                return
            
            # Get challenge details
            challenge = st.session_state.selected_challenge
            
            # Show progress steps
            with st.status("🔄 Running Analysis...", expanded=True) as status:
                # Step 1: Extract repository content
                status.write("1. 📥 Extracting repository content...")
                time.sleep(1)
                
                # Step 2: Analyze with Gemini AI
                status.write("2. 🔍 AI analyzing codebase...")
                
                # Call the analyzer agent
                analysis_result = self.analyzer_agent.analyze_repository(
                    github_repo=repo_url,
                    github_project_name=challenge['title'],
                    eval_criteria=challenge['eval_criteria'],
                    skills=challenge['skills']
                )
                
                # Debug: Show raw scores
                if analysis_result.get("status") == "success":
                    report_data = analysis_result.get("data", {}).get("final_report", {})
                    if report_data and 'report' in report_data and 'scoring_details' in report_data['report']:
                        scores = report_data['report']['scoring_details']
                        st.info(f"📊 Raw Scores: Code Quality: {scores.get('code_quality', 0)}, Total: {scores.get('total', 0)}")
                
                if analysis_result.get("status") == "error":
                    raise Exception(f"Analysis failed: {analysis_result.get('message')}")
                
                st.session_state.analysis_results = analysis_result
                
                # Step 3: Generate evaluation report
                status.write("3. 📊 Generating evaluation report...")
                time.sleep(1)
                
                # Extract and structure the report
                if analysis_result.get("status") == "success":
                    report_data = analysis_result.get("data", {}).get("final_report", {})
                    if report_data:
                        st.session_state.evaluation_report = report_data
                
                # Step 4: Complete
                status.write("4. ✅ Finalizing analysis...")
                time.sleep(0.5)
            
            st.session_state.is_analyzing = False
            st.success("✅ Analysis complete!")
            st.rerun()
            
        except Exception as e:
            st.session_state.is_analyzing = False
            st.error(f"❌ Analysis failed: {str(e)}")
    
    def display_results(self):
        """Display analysis results"""
        if not st.session_state.evaluation_report:
            return
        
        report = st.session_state.evaluation_report
        challenge = st.session_state.selected_challenge
        
        st.markdown("## 📈 Evaluation Results")
        
        # Header info
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"**Repository:**")
            st.code(st.session_state.repo_url, language="text")
        with col2:
            st.markdown(f"**Challenge:** {challenge['title']}")
        with col3:
            st.markdown(f"**Analyzed:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
        
        st.markdown("---")
        
        # Overall Score
        if 'report' in report and 'hidevs_score' in report['report']:
            score_data = report['report']['hidevs_score']
            score = score_data.get('score', 0)
            
            # Determine score category
            if score >= 90:
                score_class = "score-excellent"
                score_label = "🏅 Excellent"
                score_color = "#10b981"
            elif score >= 75:
                score_class = "score-good"
                score_label = "👍 Good"
                score_color = "#3b82f6"
            elif score >= 60:
                score_class = "score-fair"
                score_label = "⚠️ Fair"
                score_color = "#f59e0b"
            else:
                score_class = "score-poor"
                score_label = "❌ Poor"
                score_color = "#ef4444"
            
            st.markdown(f"""
            <div class="score-card {score_class}">
                <div style="display: flex; align-items: center; justify-content: space-between;">
                    <div>
                        <div style="font-size: 3rem; font-weight: 700; color: {score_color}; line-height: 1;">
                            {score}<span style="font-size: 1.2rem; color: #6b7280;">/100</span>
                        </div>
                        <div style="font-size: 1.1rem; font-weight: 600; color: {score_color}; margin-top: 5px;">
                            {score_label}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        <div style="font-size: 0.9rem; color: #6b7280; margin-bottom: 5px;">Overall Score</div>
                        <div style="font-size: 0.8rem; color: #6b7280;">Based on comprehensive evaluation</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
        
        # Marks Distribution Table
        st.markdown('<p class="section-title">📊 Marks Distribution</p>', unsafe_allow_html=True)
        
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
                
                # Calculate average
                if criteria_count > 0:
                    avg_score = total_score / criteria_count
                    st.metric("Average Score", f"{avg_score:.1f}/100")
        
        # Tech Stack Used - HORIZONTAL
        st.markdown('<p class="section-title">🛠️ Tech Stack Detected</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'project_summary' in report['report']:
            tech_stack = report['report']['project_summary'].get('tech_stack', [])
            if tech_stack:
                # Ensure tech stack is displayed horizontally
                tech_html = '<div class="tech-container">'
                for tech in tech_stack[:20]:  # Limit to 20 technologies
                    tech_html += f'<span class="tech-tag">{tech}</span>'
                if len(tech_stack) > 20:
                    tech_html += f'<span class="tech-tag" style="background: #9ca3af;">+{len(tech_stack)-20} more</span>'
                tech_html += '</div>'
                st.markdown(tech_html, unsafe_allow_html=True)
            else:
                st.info("No specific tech stack detected in analysis")
        
        # What is Good (Strengths)
        st.markdown('<p class="section-title">✅ What is Good</p>', unsafe_allow_html=True)
        
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
        
        # What is Not Good (Areas for Improvement)
        st.markdown('<p class="section-title">⚠️ What is Not Good</p>', unsafe_allow_html=True)
        
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
        
        # Skill Ratings
        st.markdown('<p class="section-title">🎯 Skill Ratings</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'skill_ratings' in report['report']:
            skills = report['report']['skill_ratings']
            if skills and isinstance(skills, dict):
                cols = st.columns(3)
                skill_items = list(skills.items())
                
                for idx, (skill_name, skill_data) in enumerate(skill_items[:6]):  # Show up to 6 skills
                    with cols[idx % 3]:
                        rating = skill_data.get('rating', 0) if isinstance(skill_data, dict) else 0
                        justification = skill_data.get('justification', 'No justification') if isinstance(skill_data, dict) else str(skill_data)
                        
                        if rating >= 80:
                            delta = "↑ Strong"
                        elif rating >= 60:
                            delta = "→ Average"
                        else:
                            delta = "↓ Weak"
                        
                        st.metric(
                            label=skill_name[:20],  # Truncate long names
                            value=f"{rating}/100",
                            delta=delta
                        )
        
        # Hiring Recommendation
        st.markdown('<p class="section-title">🤝 Hiring Recommendation</p>', unsafe_allow_html=True)
        
        if 'report' in report and 'hidevs_score' in report['report']:
            score = report['report']['hidevs_score'].get('score', 0)
            
            if score >= 85:
                recommendation = "✅ **Strong Hire** - Ready for full-time position"
                justification = "Excellent technical skills and project implementation. Demonstrates strong understanding of requirements and industry best practices."
                icon = "🏆"
            elif score >= 70:
                recommendation = "👍 **Hire as Intern** - Good potential with mentorship"
                justification = "Solid technical foundation suitable for internship. Shows good understanding of core concepts with room for growth under guidance."
                icon = "👨‍🎓"
            elif score >= 60:
                recommendation = "🤔 **Consider for Internship** - Needs improvement but has potential"
                justification = "Basic understanding shown but requires significant guidance. Could benefit from internship program with structured mentorship."
                icon = "📚"
            else:
                recommendation = "❌ **Do Not Hire** - Below minimum standards"
                justification = "Insufficient technical skills demonstrated. Does not meet the minimum requirements for consideration."
                icon = "⚠️"
            
            col1, col2 = st.columns([1, 2])
            with col1:
                st.markdown(f"""
                <div style="text-align: center; padding: 20px; background: #f8fafc; border-radius: 10px; border: 2px solid {'#10b981' if score >= 85 else '#3b82f6' if score >= 70 else '#f59e0b' if score >= 60 else '#ef4444'};">
                    <div style="font-size: 3rem; margin-bottom: 10px;">{icon}</div>
                    <div style="font-size: 1.2rem; font-weight: 600; color: {'#10b981' if score >= 85 else '#3b82f6' if score >= 70 else '#f59e0b' if score >= 60 else '#ef4444'};">{recommendation.split(' - ')[0]}</div>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                <div class="analysis-box">
                    <strong>Recommendation</strong>
                    <p>{recommendation}</p>
                </div>
                <div class="analysis-box">
                    <strong>Justification</strong>
                    <p>{justification}</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Action Buttons - FIXED ICON PARAMETER ISSUE
        st.markdown("---")
        
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
    
    def download_report(self, report: Dict):
        """Download evaluation report"""
        try:
            # Create a comprehensive report
            full_report = {
                'repository': st.session_state.repo_url,
                'challenge': st.session_state.selected_challenge['title'],
                'analysis_date': datetime.now().isoformat(),
                'overall_score': report['report']['hidevs_score']['score'] if 'report' in report and 'hidevs_score' in report['report'] else 0,
                'evaluation_results': report
            }
            
            report_json = json.dumps(full_report, indent=2, ensure_ascii=False)
            
            # Create download button
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
            
            summary = f"""
GitHub Repository Evaluation Summary
====================================
Repository: {repo_url}
Challenge: {challenge}
Evaluation Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}

OVERALL SCORE: {score}/100

SCORE BREAKDOWN:
{'-' * 50}
"""
            if 'report' in report and 'evaluation_criteria' in report['report']:
                for criterion in report['report']['evaluation_criteria']:
                    summary += f"{criterion.get('criterion_name', 'Unknown')}: {criterion.get('score', 0)}/100\n"
            
            summary += f"""
{'-' * 50}

TECH STACK:
{', '.join(report['report']['project_summary'].get('tech_stack', [])[:10]) if 'report' in report and 'project_summary' in report['report'] else 'Not specified'}

KEY STRENGTHS:
{chr(10).join([f"• {s}" for s in report['report']['final_deliverables'].get('key_strengths', [])[:3]]) if 'report' in report and 'final_deliverables' in report['report'] else 'None specified'}

AREAS FOR IMPROVEMENT:
{chr(10).join([f"• {i}" for i in report['report']['final_deliverables'].get('key_areas_for_improvement', [])[:3]]) if 'report' in report and 'final_deliverables' in report['report'] else 'None specified'}

RECOMMENDATION: {'Strong Hire' if score >= 85 else 'Hire as Intern' if score >= 70 else 'Consider for Internship' if score >= 60 else 'Do Not Hire'}
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
        
        # Display status
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
        
        # API key check
        if not os.environ.get("GEMINI_API_KEY") or not os.environ.get("GITHUB_TOKEN"):
            st.error("""
            ⚠️ **API Keys Missing:**
            Please create a `.env` file in the project root with:
            ```
            GEMINI_API_KEY=your_gemini_api_key_here
            GITHUB_TOKEN=your_github_token_here
            ```
            """)
        
        # Challenge selector
        self.display_challenge_selector()
        
        # Selected challenge info
        self.display_selected_challenge_info()
        
        # Repository input
        self.display_repository_input()
        
        # Display error if any
        self.display_error()
        
        # Show analysis progress
        if st.session_state.is_analyzing:
            st.info("🔄 Analysis in progress... This may take 1-2 minutes.")
        
        # Display evaluation results
        if st.session_state.evaluation_report:
            self.display_results()
        
        # Footer
        st.markdown("---")
        st.markdown("""
        <div style='text-align: center; color: #6b7280; font-size: 11px; padding: 15px;'>
            <div style="font-size: 12px; font-weight: 600; color: #4f46e5; margin-bottom: 5px;">
                GitHub Repository Evaluator v2.0
            </div>
            <div>AI-Powered Technical Assessment • Real GitHub Analysis • Challenge-Specific Evaluation</div>
            <div style="margin-top: 5px; font-size: 10px;">Powered by Gemini AI • Secure & Confidential</div>
        </div>
        """, unsafe_allow_html=True)

def main():
    """Main application entry point"""
    evaluator = GitHubRepoEvaluator()
    evaluator.run()

if __name__ == "__main__":
    main()
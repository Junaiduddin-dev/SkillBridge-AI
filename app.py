import streamlit as st
import google.generativeai as genai
try:
    import PyPDF2 as pdf
except ImportError:
    st.error("🚨 Library missing! Please run: pip install PyPDF2")
    st.stop()

# --- 1. CONFIGURATION & AI SETUP ---
# Using your verified Metal Mariner Key (...fLQQ)
API_KEY = "AIzaSyCq1JW3oSAYXDP47p9TvN_AYnxlkHIfLQQ"
genai.configure(api_key=API_KEY)

# Initialize Session State variables if they don't exist
if 'analysis_ready' not in st.session_state:
    st.session_state['analysis_ready'] = False
if 'report_text' not in st.session_state:
    st.session_state['report_text'] = ""
if 'active_model' not in st.session_state:
    st.session_state['active_model'] = ""

def extract_text_from_pdf(uploaded_file):
    try:
        reader = pdf.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
        return text
    except Exception as e:
        return f"Error reading PDF: {e}"

# --- 2. ADVANCED UI DESIGN (CSS) ---
st.set_page_config(page_title="SkillBridge AI | June", page_icon="🎯", layout="wide")

st.markdown("""
    <style>
    .stApp { background: linear-gradient(135deg, #f3f4f6 0%, #ffffff 100%); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .main-title { color: #1E3A8A; text-align: center; font-size: 3rem; font-weight: 800; margin-bottom: 0px; letter-spacing: -1px; }
    .sub-title { text-align: center; color: #64748b; font-size: 1.2rem; margin-bottom: 2rem; }
    .report-card { background-color: #ffffff; padding: 2rem; border-radius: 16px; border-top: 5px solid #3b82f6; box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1); margin-top: 1.5rem; }
    .stButton>button { background: linear-gradient(90deg, #1E3A8A 0%, #3b82f6 100%); color: white; border: none; padding: 0.75rem 2rem; font-size: 1.1rem; font-weight: 600; border-radius: 12px; width: 100%; transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(59, 130, 246, 0.4); color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. SIDEBAR & HEADER ---
with st.sidebar:
    st.title("SkillBridge Details")
    st.markdown("**Developer:** Juneduddin")
    st.info("Agentic AI powered by Gemini 1.5 Flash.")
    if st.button("Clear App Data"):
        st.session_state['analysis_ready'] = False
        st.rerun()

st.markdown("<h1 class='main-title'>🎯 SkillBridge AI</h1>", unsafe_allow_html=True)
st.markdown("<p class='sub-title'>Advanced Career Pathing & Talent Gap Analysis Agent</p>", unsafe_allow_html=True)

# --- 4. MAIN INPUTS ---
col1, col2 = st.columns(2, gap="large")
with col1:
    st.markdown("### 📋 Job Requirements")
    jd_text = st.text_area("Paste the Job Description here...", height=250)
with col2:
    st.markdown("### 📄 Candidate Resume")
    uploaded_file = st.file_uploader("Upload Resume (PDF)", type="pdf")

st.divider()

# --- 5. CORE AGENT EXECUTION ---
if st.button("🚀 EXECUTE FULL SKILL ANALYSIS"):
    if not jd_text or not uploaded_file:
        st.warning("Please provide both a Job Description and a Resume.")
    else:
        with st.spinner("🧠 Agent is analyzing..."):
            resume_content = extract_text_from_pdf(uploaded_file)
            try:
                # Discovery and Generation
                available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
                selected_model = next((m for m in available_models if "1.5-flash" in m), available_models[0])
                
                model = genai.GenerativeModel(selected_model)
                prompt = f"""
                You are an elite Career Coach. Analyze the following for June:
                JD: {jd_text}
                RESUME: {resume_content}
                
                Structure:
                1. **Skill Gap Matrix**: Table of Match/Gap.
                2. **Adjacent Skills Logic**: Why current skills make learning gaps easier.
                3. **3-Day Learning Plan**: Focused on the biggest gap.
                4. **Technical Interview Challenge**: Provide one complex technical question.
                """
                
                response = model.generate_content(prompt)
                
                # Save to State Memory
                st.session_state['report_text'] = response.text
                st.session_state['active_model'] = selected_model
                st.session_state['analysis_ready'] = True
                st.balloons()
                
            except Exception as e:
                st.error(f"Critical System Error: {e}")

# --- 6. DISPLAY RESULTS AND INTERVIEWER ---
if st.session_state['analysis_ready']:
    # Show the Analysis Report
    st.success(f"Analysis Complete! Using {st.session_state['active_model']}")
    st.markdown(f'<div class="report-card">{st.session_state["report_text"]}</div>', unsafe_allow_html=True)
    
    st.divider()
    st.markdown("### 💬 Live Interview Practice")
    st.write("The Agent has proposed a challenge above. Submit your response below for evaluation:")
    
    # Text area for the interview answer
    user_answer = st.text_area("Your Response:", placeholder="Type your answer here...", key="interview_box")
    
    if st.button("Submit to Agent"):
        if user_answer:
            with st.spinner("Agent is grading..."):
                try:
                    model = genai.GenerativeModel(st.session_state['active_model'])
                    eval_prompt = f"Grade this answer: '{user_answer}' based on this report: '{st.session_state['report_text']}'."
                    eval_res = model.generate_content(eval_prompt)
                    st.markdown(f'<div class="report-card" style="border-left: 10px solid #10b981;">{eval_res.text}</div>', unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Feedback Error: {e}")
        else:
            st.warning("Please type an answer first!")

st.markdown("<br><hr>", unsafe_allow_html=True)
st.caption("Developed for Catalyst Hackathon 2026 | Hyderabad | Developed by Junaiduddin")
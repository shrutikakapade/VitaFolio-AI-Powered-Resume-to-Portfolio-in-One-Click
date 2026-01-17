import streamlit as st
import os
from PyPDF2 import PdfReader
from dotenv import load_dotenv
import zipfile
from io import BytesIO
import re
import time

load_dotenv()
st.set_page_config(page_title="VitaFolio", layout="wide")

# Simple clean CSS
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
* { font-family: 'Inter', sans-serif; }
body { background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f0f23 100%); color: white; }
.card { 
    background: rgba(255,255,255,0.1); 
    border-radius: 16px; 
    padding: 2rem; 
    border: 1px solid rgba(255,255,255,0.1);
    margin: 1rem 0;
}
.btn-main { 
    background: linear-gradient(135deg, #7c3aed, #9333ea) !important; 
    border-radius: 12px !important; 
    height: 50px !important; 
    font-weight: 600 !important;
}
input, textarea, select { 
    background: rgba(255,255,255,0.1) !important; 
    border: 1px solid rgba(255,255,255,0.2) !important; 
    border-radius: 12px !important; 
    color: white !important; 
}
</style>
""", unsafe_allow_html=True)

st.title("✨ VitaFolio")
st.markdown("*Resume → Portfolio Website*")

# Simple 2-column layout
col1, col2 = st.columns([1, 1.2])

with col1:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("🎨 Design")
    
    style = st.selectbox("Style", ["Modern", "Clean", "Professional"])
    title = st.text_input("Title", "My Portfolio")
    prompt = st.text_area("Instructions", 
        "Clean portfolio with projects and skills", height=150)
    
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    #st.markdown('<div class="card">', unsafe_allow_html=True)
    st.subheader("📁 Upload & Generate")
    
    # API check
    api_key = os.getenv("gemini")
    if not api_key:
        st.error("❌ Add `GOOGLE_API_KEY=your_key` to `.env`")
        st.stop()
    
    # Upload
    uploaded = st.file_uploader("PDF Resume", type="pdf")
    if uploaded:
        reader = PdfReader(uploaded)
        text = ""
        for page in reader.pages:
            text += page.extract_text() or ""
        st.session_state.resume_text = text.strip()
        st.success("✅ Resume loaded")
    
    # Generate
    if st.button("✨ Generate Portfolio", type="primary") and 'resume_text' in st.session_state:
        with st.spinner("Creating..."):
            try:
                from langchain_google_genai import ChatGoogleGenerativeAI
                llm = ChatGoogleGenerativeAI(
                    model="gemini-1.5-flash",
                    api_key=api_key
                )
                
                response = llm.invoke(f"""
Resume: {st.session_state.resume_text[:3000]}
Title: {title}
Style: {style}

Generate portfolio website. Return ONLY:
--HTML--[html]--HTML--
--CSS--[css]--CSS--
--JS--[js]--JS--
                """)
                
                # Parse
                parts = re.split(r'--(?:HTML|CSS|JS)--', response.content)
                html = parts[1].strip() if len(parts) > 1 else "<h1>Portfolio</h1>"
                css = parts[3].strip() if len(parts) > 3 else ""
                js = parts[5].strip() if len(parts) > 5 else ""
                
                # ZIP
                buffer = BytesIO()
                with zipfile.ZipFile(buffer, 'w') as zf:
                    zf.writestr('index.html', html)
                    zf.writestr('style.css', css)
                    zf.writestr('script.js', js)
                
                st.session_state.zip_file = buffer.getvalue()
                st.success("✅ Portfolio ready!")
                
            except Exception as e:
                st.error(f"Error: {e}")
    
    if 'zip_file' in st.session_state:
        st.download_button(
            "📥 Download Website", 
            st.session_state.zip_file, 
            "portfolio.zip", 
            "application/zip"
        )
    
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown("""
<div style='text-align: center; padding: 2rem; color: #94a3b8;'>
    Simple. Clean. Professional.
</div>
""", unsafe_allow_html=True)

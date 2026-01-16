import streamlit as st

import dotenv
from dotenv import load_dotenv
load_dotenv()

from PyPDF2 import PdfReader #Used to read and extract text from PDF files
import zipfile

import langchain
from langchain_google_genai import ChatGoogleGenerativeAI

import os
os.environ["GOOGLE_API_KEY"] = os.getenv("gemini")

st.set_page_config(page_title = "VitaFolio" ,page_icon= "🪽")
st.title("Your Resume, Reimagined as a Living Website") #Displays a main heading at the top of the Streamlit app

#Note: st.file_uploader() = This allows users to upload files from their local system.

uploaded_pdf = st.file_uploader(
    "Choose a PDF file",
    type=["pdf"]
)
#Allows only PDF files (type="pdf")

if uploaded_pdf is not None:
    st.success("PDF uploaded successfully!")
    
    reader = PdfReader(uploaded_pdf) #Loads the uploaded PDF into memory

    resume_text = "" #Prepares a variable to store extracted text

    for page in reader.pages:
        text = page.extract_text()
        if text:  # avoids None concatenation
            resume_text += text
# Loops through each page in the PDF
# extract_text() extracts readable text from that page
# Appends text to resume_text
#     st.subheader("Extracted Resume Text")
#     st.text_area("", resume_text, height=350)

website_prompt = st.text_area(
    "Describe your website",
    height=160,
    placeholder="Tell us what kind of website you want — purpose, style, sections, and features.")

if st.button("generate portfolio"):
        message = [("system", f"""{resume_text} You are a senior frontend engineer and UI/UX expert. 
Goal: Generate a complete, production-ready static website based ONLY on the user description and resume_text. 
Requirements: - Use modern, semantic HTML5 structure (header, main, section, footer, etc.).
- Add clear sections: hero, features/benefits, call-to-action, and any additional sections explicitly requested. 
- Ensure the layout is responsive and mobile-friendly (flexbox or CSS grid, no frameworks). 
- Use clean, readable class names and consistent indentation. 
- Do NOT include inline CSS or inline JavaScript inside the HTML. Styling: 
- Provide all styling in a separate CSS file. 
- Use a modern look with good spacing, hierarchy, and accessible color contrast. 
- Use a simple Google Font (e.g., Inter, Poppins, or similar) imported in CSS. 
- Include hover states for buttons and links. 
- Respect any colors, branding, or style instructions from the user description. 
Behavior (JavaScript): - Only write vanilla JavaScript. 
- Add smooth scroll for internal navigation links if there is a navbar. 
- Add small, useful interactions if relevant (e.g., mobile nav toggle, simple animations, FAQ accordion). 
- Do NOT use external JS libraries or frameworks. Output format (strict):
Return your answer in EXACTLY this structure with no extra text, comments, or explanations:

--html--
HTML
--html--

--css--
CSS
--css--

--js--
JS
--js--
""" )]
        message.append(("user", website_prompt))
        
        model = ChatGoogleGenerativeAI(model = "gemini-2.5-flash-lite")
        
        response = model.invoke(message)
    
        with open("index.html","w", encoding="utf-8")as file:
            file.write(response.content.split("--html--")[1])
            
        with open("style.css","w", encoding="utf-8") as file:
            file.write(response.content.split("--css--")[1])
        
        with open("script.js","w", encoding="utf-8") as file:
            file.write(response.content.split("--js--")[1])
        
        #zip the above 3 files (html,css,js)
        with zipfile.ZipFile("website.zip","w")as zip:
            zip.write("index.html")
            zip.write("style.css")
            zip.write("script.js")
        st.download_button("click to download",data= open("website.zip","rb"),file_name ="website.zip")  #read binary file
    
        st.write("success")

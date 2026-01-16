<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
   
<div>   
    <h1> AI-Powered Resume to Portfolio in One Click </h1>
<div>
    <h2>Project Overview</h2>
    <p>VitaFolio is an AI-driven application that converts resumes or project descriptions into fully functional, responsive portfolio websites. Users can instantly download their website as a ZIP file containing HTML, CSS, and JavaScript files.</p>
<div>
    <h2>Features</h2>
    <ul>
        <li>AI-generated websites based on user input</li>
        <li>Modern, semantic HTML5 structure</li>
        <li>Responsive design using CSS Flexbox/Grid</li>
        <li>Separate HTML, CSS, and JS files for clean structure</li>
        <li>Automated ZIP download for instant deployment</li>
        <li>Designed for students, professionals, and job seekers</li>
    </ul>
<div>
    <h2>Project Structure</h2>
    <pre>
RESUME PORTFOLIO GENERATOR/
│
├─ portfolio/
│   ├─ files/
│   │   ├─ .env           # Stores Google API key
│   │   ├─ app.py         # Streamlit app
│   │   ├─ index.html     # Generated HTML
│   │   ├─ style.css      # Generated CSS
│   │   ├─ script.js      # Generated JS
│   │   ├─ req.txt        # Python dependencies
│   │   └─ website.zip    # Downloadable ZIP
│
└─ pyvenv.cfg             # Virtual environment config
    </pre>
<div>
    <h2>Setup & Usage</h2>
    <ol>
        <li>Create and activate a virtual environment:</li>
        <pre>python -m venv venv
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate</pre>
        <li>Install dependencies: <code>pip install -r files/req.txt</code></li>
        <li>Add your Google API key in <code>files/.env</code>:</li>
        <pre>gemini=YOUR_GOOGLE_API_KEY</pre>
        <li>Run the Streamlit app: <code>streamlit run files/app.py</code></li>
        <li>Enter your website description and click <strong>Generate</strong> to create your portfolio.</li>
    </ol>

</html>

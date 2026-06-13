# AI-Powered Resume Screening System

An intelligent, end-to-end resume screening and analysis tool. The application parses resume documents (PDF, DOCX, TXT), extracts text and metadata, classifies candidate roles using a custom TensorFlow model, evaluates skill alignment against job descriptions, and provides structured recommendation reports.

## Features

- **Interactive Dashboard**: A responsive, visually premium user interface with drag-and-drop file uploads.
- **Resume Parser**: Robust text extraction supporting PDF, DOCX, and TXT files.
- **NLP Feature Extraction**: Automatically extracts emails, phone numbers, social handles (GitHub, LinkedIn), skills, and highlights education/experience.
- **TensorFlow Classification**: Classifies resumes into industry roles (e.g., Software Engineering, Data Science & AI, Human Resources, Finance, Marketing, Product Management).
- **Match Analysis**: Compares candidate profile against job descriptions to score overall fit, skills matches, and semantic similarity.

---

## Project Structure

```text
├── backend/                  # FastAPI Web Server & ML Modules
│   ├── classifier.py         # TensorFlow Keras resume classification model
│   ├── main.py               # REST API endpoints & static serving
│   ├── nlp_processor.py      # Rule-based NLP parser (emails, skills, etc.)
│   ├── parser.py             # Document text extractor (pypdf, python-docx)
│   ├── similarity.py         # Cosine-similarity calculation & recommendation engine
│   └── model_files/          # Directory where trained .keras models are stored
├── frontend/                 # Static Assets Served by FastAPI
│   ├── index.html            # Main structure
│   ├── style.css             # Premium custom styling & animations
│   └── app.js                # Frontend routing, upload handlers, & render logic
├── Dockerfile                # Deployment container configuration
├── requirements.txt          # Python dependencies
└── sample_resume_swe.txt     # Sample data for testing
```

---

## Getting Started (Local Development)

### Prerequisites
- Python 3.10+
- Git

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Abhisheknath25/AI-Powered-Resume-Screening-System-.git
   cd AI-Powered-Resume-Screening-System-
   ```

2. **Create and activate a virtual environment:**
   ```bash
   python -m venv .venv
   # On Windows (cmd):
   .venv\Scripts\activate
   # On Windows (PowerShell):
   .venv\Scripts\Activate.ps1
   # On macOS/Linux:
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   uvicorn backend.main:app --reload
   ```

5. Open your browser and navigate to `http://127.0.0.1:8000` to interact with the system.

---

## Deployment Instructions

### Option A: Hugging Face Spaces (Recommended for Machine Learning)
Since this project uses TensorFlow, deploying it on a free tier platform with limited RAM (e.g., 512MB on Render) might result in Out of Memory (OOM) crashes. Hugging Face Spaces provides **16 GB RAM** for free.

1. Create a free account at [Hugging Face](https://huggingface.co/).
2. Click **New Space** and configure:
   - **Space Name**: `ai-resume-screening`
   - **SDK**: **Docker** (Select the *Blank* template).
   - **Public/Private**: As preferred.
3. Once the Space is created, copy the Git remote URL from Hugging Face.
4. Add the Hugging Face remote to your local repository:
   ```bash
   git remote add hf https://huggingface.co/spaces/Abhisheknath25/ai-resume-screening
   ```
5. Push your code:
   ```bash
   git push hf main
   ```

### Option B: Render (Standard Web Hosting)
1. Go to [Render](https://render.com/) and log in.
2. Click **New** -> **Web Service**.
3. Connect your GitHub repository: `AI-Powered-Resume-Screening-System-`.
4. Configure the service:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
5. Select the Instance Type and click **Deploy Web Service**.

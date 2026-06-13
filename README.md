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


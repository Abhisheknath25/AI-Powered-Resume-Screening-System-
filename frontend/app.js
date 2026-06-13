// Configuration & State
let selectedFile = null;

const JD_TEMPLATES = {
    datascience: `We are looking for a Data Scientist to join our AI engineering team. The ideal candidate will have strong experience in Python programming and SQL databases. You will develop machine learning and deep learning models using TensorFlow, Keras, or PyTorch.

Key Requirements:
- Hands-on experience with Pandas, NumPy, and Scikit-learn for data analysis.
- Experience with Natural Language Processing (NLP) or Computer Vision (CV) is a plus.
- Solid understanding of statistics and mathematical concepts.
- Experience building data visualizations using Tableau or Power BI.`,

    software: `We are seeking a Full Stack Software Engineer to build scalable web applications.
Qualifications:
- Proficient in JavaScript, TypeScript, HTML, and CSS.
- Experience with React, Node.js, and Express framework.
- Strong knowledge of databases, specifically PostgreSQL or MongoDB.
- Experience with Docker containers and deploying on AWS or GCP.
- Understanding of Git version control, CI/CD pipelines, and writing automated unit tests.
- Experience working in an Agile/Scrum team.`,

    hr: `We are hiring a Human Resources Manager to lead our talent acquisition and onboarding.
Responsibilities:
- Manage the full-cycle recruiting and sourcing process.
- Conduct candidate screening and structure behavioral interviewing.
- Administer payroll, performance management reviews, and employee relations programs.
- Experience working with ATS (Applicant Tracking Systems) to track candidate workflows.
- Assist in developing hr policies, employee handbook, and benefits administration.`,

    finance: `We are looking for a Financial Analyst to join our corporate finance team. The candidate will perform financial modeling, analysis, and forecasting.

Requirements:
- Strong experience with corporate finance, general ledger, QuickBooks, and Excel.
- Ability to conduct cash flow forecasting, budget analysis, and ledger reconciliation.
- Prepare detailed financial reporting, cost reduction plans, and risk assessments.
- Bachelor's degree in Finance, Accounting, or Economics.`,

    marketing: `We are seeking a Digital Marketing & Sales Specialist to drive lead generation and brand awareness.

Key Responsibilities:
- Execute digital marketing campaigns across social media, email channels, and SEO.
- Optimize search engine optimization (SEO) and manage Google Ads budgets.
- Manage the sales pipeline, customer relationships via CRM (e.g., Salesforce).
- Experience in content creation, copywriting, and growth hacking metrics.`,

    product: `We are looking for a Product Manager to guide the lifecycle of our software products from inception to launch.

Qualifications:
- Experience writing business requirements, user stories, and managing product roadmaps.
- Proficient with Agile/Scrum methodologies, JIRA, and Confluence.
- Strong stakeholder management and feature prioritization skills.
- Define product metrics, KPIs, and perform user testing and UX research.`
};


// DOM Elements
const apiStatusEl = document.getElementById('apiStatus');
const jdInput = document.getElementById('jdInput');
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
const fileIndicator = document.getElementById('fileIndicator');
const fileNameEl = document.getElementById('fileName');
const removeFileBtn = document.getElementById('removeFile');
const screenBtn = document.getElementById('screenBtn');

// Dashboard States
const statePlaceholder = document.getElementById('statePlaceholder');
const stateLoading = document.getElementById('stateLoading');
const stateResults = document.getElementById('stateResults');

// Loading state details
const loaderTitle = document.getElementById('loaderTitle');
const loaderSubtitle = document.getElementById('loaderSubtitle');
const loaderProgress = document.getElementById('loaderProgress');

// Results elements
const scoreRing = document.getElementById('scoreRing');
const scoreNumber = document.getElementById('scoreNumber');
const matchBadge = document.getElementById('matchBadge');
const predictedRole = document.getElementById('predictedRole');
const predictedConfidence = document.getElementById('predictedConfidence');
const roleConfidenceBar = document.getElementById('roleConfidenceBar');
const probabilitiesList = document.getElementById('probabilitiesList');
const skillMatchPercent = document.getElementById('skillMatchPercent');
const skillMatchBar = document.getElementById('skillMatchBar');
const semanticMatchPercent = document.getElementById('semanticMatchPercent');
const semanticMatchBar = document.getElementById('semanticMatchBar');

// Contact elements
const contactEmail = document.getElementById('contactEmail');
const contactPhone = document.getElementById('contactPhone');
const contactLinkedin = document.getElementById('contactLinkedin');
const contactGithub = document.getElementById('contactGithub');

// Skills split lists
const foundSkillsEl = document.getElementById('foundSkills');
const missingSkillsEl = document.getElementById('missingSkills');

// Experience and Education lists
const experienceHighlights = document.getElementById('experienceHighlights');
const educationHighlights = document.getElementById('educationHighlights');
const recommendationsList = document.getElementById('recommendationsList');

// INITIALIZATION
document.addEventListener('DOMContentLoaded', () => {
    checkBackendStatus();
    setupEventListeners();
});

// Check API & TensorFlow Status
async function checkBackendStatus() {
    try {
        const res = await fetch('/api/status');
        if (res.ok) {
            const data = await res.json();
            if (data.model_loaded) {
                setApiStatus('ready', 'TF Model Ready');
            } else {
                setApiStatus('pulsing', 'Training Classifier...');
                // Retry check in 3 seconds
                setTimeout(checkBackendStatus, 3000);
            }
        } else {
            setApiStatus('error', 'API Error');
        }
    } catch (err) {
        setApiStatus('error', 'Server Offline');
    }
}

function setApiStatus(statusClass, text) {
    const dot = apiStatusEl.querySelector('.status-dot');
    const label = apiStatusEl.querySelector('.status-text');
    
    dot.className = 'status-dot';
    dot.classList.add(statusClass);
    label.innerText = text;
}

// Setup Event Listeners
function setupEventListeners() {
    // JD Templates
    document.querySelectorAll('.template-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            const type = btn.getAttribute('data-type');
            if (JD_TEMPLATES[type]) {
                jdInput.value = JD_TEMPLATES[type];
                validateInputs();
            }
        });
    });

    jdInput.addEventListener('input', validateInputs);

    // Drag and Drop
    dropZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        dropZone.classList.add('dragover');
    });

    dropZone.addEventListener('dragleave', () => {
        dropZone.classList.remove('dragover');
    });

    dropZone.addEventListener('drop', (e) => {
        e.preventDefault();
        dropZone.classList.remove('dragover');
        if (e.dataTransfer.files.length > 0) {
            handleFileSelection(e.dataTransfer.files[0]);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files.length > 0) {
            handleFileSelection(fileInput.files[0]);
        }
    });

    removeFileBtn.addEventListener('click', (e) => {
        e.stopPropagation(); // Prevent opening file chooser
        clearFileSelection();
    });

    screenBtn.addEventListener('click', runScreeningProcess);
}

function handleFileSelection(file) {
    const allowedExtensions = ['.pdf', '.docx', '.txt'];
    const extension = file.name.substring(file.name.lastIndexOf('.')).toLowerCase();
    
    if (!allowedExtensions.includes(extension)) {
        alert('Unsupported file type. Please select a PDF, DOCX, or TXT file.');
        return;
    }
    
    selectedFile = file;
    fileNameEl.innerText = file.name;
    fileIndicator.style.display = 'flex';
    validateInputs();
}

function clearFileSelection() {
    selectedFile = null;
    fileInput.value = '';
    fileIndicator.style.display = 'none';
    validateInputs();
}

function validateInputs() {
    const hasJd = jdInput.value.trim().length > 20;
    const hasFile = selectedFile !== null;
    screenBtn.disabled = !(hasJd && hasFile);
}

// RUN SCREENING PROCESS
async function runScreeningProcess() {
    if (!selectedFile || !jdInput.value.trim()) return;

    // Show Loading Panel
    statePlaceholder.style.display = 'none';
    stateResults.style.display = 'none';
    stateLoading.style.display = 'flex';
    
    // Simulate multi-step loader
    updateLoader("Reading Document...", "Parsing file structure and extracting raw text", "15%");

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('jd', jdInput.value.trim());

    // Slow down updates to make them readable and visually satisfying
    setTimeout(() => updateLoader("Analyzing NLP Features...", "Extracting skills, contact detail cards, and educational credentials", "45%"), 1000);
    setTimeout(() => updateLoader("Invoking TensorFlow Model...", "Evaluating resume vocabulary against professional category classifier", "75%"), 2200);

    try {
        const startTime = Date.now();
        const response = await fetch('/api/screen', {
            method: 'POST',
            body: formData
        });

        // Ensure we show step 3 for at least some visual duration
        const elapsed = Date.now() - startTime;
        const delay = Math.max(3000 - elapsed, 0);

        setTimeout(async () => {
            if (response.ok) {
                const report = await response.json();
                updateLoader("Finishing Analysis...", "Compiling scores and visual report...", "100%");
                setTimeout(() => renderReport(report), 800);
            } else {
                const errData = await response.json();
                showErrorState("Screening Failed", errData.detail || "Server error occurred");
            }
        }, delay);

    } catch (err) {
        showErrorState("Network Error", "Unable to connect to the backend server. Please verify FastAPI is running.");
    }
}

function updateLoader(title, subtitle, progressWidth) {
    loaderTitle.innerText = title;
    loaderSubtitle.innerText = subtitle;
    loaderProgress.style.width = progressWidth;
}

function showErrorState(title, message) {
    stateLoading.style.display = 'none';
    stateResults.style.display = 'none';
    statePlaceholder.style.display = 'flex';
    
    const icon = statePlaceholder.querySelector('.placeholder-icon');
    const header = statePlaceholder.querySelector('h2');
    const desc = statePlaceholder.querySelector('p');
    
    icon.className = 'bx bx-error-alt placeholder-icon';
    icon.style.color = 'var(--accent-red)';
    header.innerText = title;
    desc.innerText = message;
}

// RENDER REPORT IN DASHBOARD
function renderReport(report) {
    stateLoading.style.display = 'none';
    stateResults.style.display = 'flex';

    // 1. Overall Score Ring animation
    const score = report.matching.overall_score;
    scoreNumber.innerText = `${score}%`;
    
    // SVG ring circumference is ~440 (r=70, 2 * pi * 70)
    const offset = 440 - (440 * score) / 100;
    scoreRing.style.strokeDashoffset = offset;
    
    // Classify overall rating
    matchBadge.className = 'match-badge';
    if (score >= 80) {
        matchBadge.classList.add('high');
        matchBadge.innerText = 'Strong Candidate Match';
    } else if (score >= 60) {
        matchBadge.classList.add('mid');
        matchBadge.innerText = 'Moderate Match';
    } else {
        matchBadge.classList.add('low');
        matchBadge.innerText = 'Low Match Rating';
    }

    // 2. Indicators (Skills and Semantic Match)
    skillMatchPercent.innerText = `${report.matching.skill_score}%`;
    skillMatchBar.style.width = `${report.matching.skill_score}%`;
    
    semanticMatchPercent.innerText = `${report.matching.text_similarity}%`;
    semanticMatchBar.style.width = `${report.matching.text_similarity}%`;

    // 3. TensorFlow Role Prediction
    const predicted = report.classification;
    predictedRole.innerText = predicted.predicted_role;
    predictedConfidence.innerText = `Confidence: ${predicted.confidence}%`;
    roleConfidenceBar.style.setProperty('--progress', `${predicted.confidence}%`);

    // Render individual probabilities
    probabilitiesList.innerHTML = '';
    const sortedProbabilities = Object.entries(predicted.probabilities)
        .sort((a, b) => b[1] - a[1]); // Sort by highest percentage
        
    sortedProbabilities.forEach(([cat, val]) => {
        const item = document.createElement('div');
        item.className = 'probability-item';
        
        // Shorten category names if too long
        const catShort = cat.replace("Finance & Accounting", "Finance")
                            .replace("Marketing & Sales", "Marketing")
                            .replace("Software Engineering", "Software Eng.");
                            
        item.innerHTML = `
            <span class="prob-name">${catShort}</span>
            <span class="prob-val">${val}%</span>
        `;
        probabilitiesList.appendChild(item);
    });

    // 4. Contact Details
    contactEmail.innerText = report.contact_info.email;
    contactPhone.innerText = report.contact_info.phone;
    
    if (report.contact_info.linkedin !== 'Not Found') {
        contactLinkedin.innerText = 'LinkedIn Profile';
        contactLinkedin.href = report.contact_info.linkedin;
        contactLinkedin.classList.remove('disabled');
    } else {
        contactLinkedin.innerText = 'Not Found';
        contactLinkedin.removeAttribute('href');
        contactLinkedin.classList.add('disabled');
    }

    if (report.contact_info.github !== 'Not Found') {
        contactGithub.innerText = 'GitHub Profile';
        contactGithub.href = report.contact_info.github;
        contactGithub.classList.remove('disabled');
    } else {
        contactGithub.innerText = 'Not Found';
        contactGithub.removeAttribute('href');
        contactGithub.classList.add('disabled');
    }

    // 5. Skills Cloud split
    foundSkillsEl.innerHTML = '';
    if (report.matching.matching_skills.length > 0) {
        report.matching.matching_skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'skill-tag found';
            span.innerText = skill;
            foundSkillsEl.appendChild(span);
        });
    } else {
        foundSkillsEl.innerHTML = '<span class="no-skills-msg">No matching keywords found.</span>';
    }

    missingSkillsEl.innerHTML = '';
    if (report.matching.missing_skills.length > 0) {
        report.matching.missing_skills.forEach(skill => {
            const span = document.createElement('span');
            span.className = 'skill-tag missing';
            span.innerText = skill;
            missingSkillsEl.appendChild(span);
        });
    } else {
        missingSkillsEl.innerHTML = '<span class="no-skills-msg">No missing skills detected!</span>';
    }

    // 6. Highlights & Education lists
    renderList(experienceHighlights, report.experience_highlights, "No explicit work experience lines detected.");
    renderList(educationHighlights, report.education_highlights, "No explicit academic qualifications detected.");

    // 7. Recommendations
    renderList(recommendationsList, report.matching.recommendations, "No specific recommendations needed.");
}

function renderList(targetEl, items, emptyText) {
    targetEl.innerHTML = '';
    if (items && items.length > 0) {
        items.forEach(item => {
            const li = document.createElement('li');
            li.innerText = item;
            targetEl.appendChild(li);
        });
    } else {
        const li = document.createElement('li');
        li.className = 'empty-item';
        li.innerText = emptyText;
        targetEl.appendChild(li);
    }
}

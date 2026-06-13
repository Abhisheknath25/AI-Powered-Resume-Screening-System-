import re
from typing import Dict, List, Set, Tuple

# Comprehensive skills dictionary categorized by domain
SKILLS_DB = {
    # Software Engineering
    "python": ["python", "py"],
    "javascript": ["javascript", "js"],
    "typescript": ["typescript", "ts"],
    "java": ["java"],
    "c++": ["c\\+\\+"],
    "c#": ["c#", "c-sharp"],
    "ruby": ["ruby"],
    "go": ["go", "golang"],
    "php": ["php"],
    "rust": ["rust"],
    "swift": ["swift"],
    "kotlin": ["kotlin"],
    "html": ["html", "html5"],
    "css": ["css", "css3", "sass", "less"],
    "react": ["react", "reactjs", "react.js"],
    "angular": ["angular", "angularjs"],
    "vue": ["vue", "vuejs", "vue.js"],
    "node.js": ["node", "nodejs", "node.js"],
    "express": ["express", "expressjs"],
    "django": ["django"],
    "flask": ["flask"],
    "fastapi": ["fastapi"],
    "spring boot": ["spring boot", "spring"],
    "docker": ["docker"],
    "kubernetes": ["kubernetes", "k8s"],
    "aws": ["aws", "amazon web services"],
    "gcp": ["gcp", "google cloud"],
    "azure": ["azure", "microsoft azure"],
    "git": ["git", "github", "gitlab", "bitbucket"],
    "ci/cd": ["ci/cd", "jenkins", "github actions", "circleci"],
    "postgresql": ["postgresql", "postgres"],
    "mysql": ["mysql"],
    "mongodb": ["mongodb", "mongo"],
    "redis": ["redis"],
    "graphql": ["graphql"],
    
    # Data Science & AI
    "machine learning": ["machine learning", "ml"],
    "deep learning": ["deep learning", "dl"],
    "tensorflow": ["tensorflow", "tf"],
    "pytorch": ["pytorch"],
    "keras": ["keras"],
    "natural language processing": ["natural language processing", "nlp"],
    "computer vision": ["computer vision", "cv"],
    "pandas": ["pandas"],
    "numpy": ["numpy"],
    "scikit-learn": ["scikit-learn", "sklearn"],
    "scipy": ["scipy"],
    "matplotlib": ["matplotlib"],
    "seaborn": ["seaborn"],
    "spark": ["spark", "pyspark", "apache spark"],
    "hadoop": ["hadoop"],
    "sql": ["sql", "mysql", "sqlite", "oracle"],
    "nosql": ["nosql"],
    "tableau": ["tableau"],
    "power bi": ["power bi", "powerbi"],
    "data analysis": ["data analysis", "analytics"],
    "data visualization": ["data visualization"],
    "statistics": ["statistics", "statistical analysis"],
    
    # Human Resources
    "recruiting": ["recruiting", "recruitment", "talent acquisition"],
    "sourcing": ["sourcing"],
    "interviewing": ["interviewing", "interviews"],
    "onboarding": ["onboarding"],
    "employee relations": ["employee relations"],
    "payroll": ["payroll"],
    "performance management": ["performance management"],
    "hr policies": ["hr policies", "human resources policies"],
    "ats": ["ats", "applicant tracking system"],
    
    # Finance & Accounting
    "accounting": ["accounting"],
    "financial modeling": ["financial modeling", "financial analysis"],
    "valuation": ["valuation"],
    "forecasting": ["forecasting", "financial forecasting"],
    "auditing": ["auditing", "audit"],
    "tax": ["tax", "taxation"],
    "quickbooks": ["quickbooks"],
    "excel": ["excel", "microsoft excel", "spreadsheets"],
    "budgeting": ["budgeting"],
    
    # Product Management & Business
    "agile": ["agile"],
    "scrum": ["scrum"],
    "product roadmap": ["product roadmap", "roadmapping"],
    "jira": ["jira"],
    "confluence": ["confluence"],
    "market research": ["market research"],
    "competitor analysis": ["competitor analysis"],
    "product lifecycle": ["product lifecycle", "product development"],
    "project management": ["project management", "pmp"],
    "crm": ["crm", "salesforce", "hubspot"],
    "customer success": ["customer success"],
    "sales": ["sales", "selling"],
    "digital marketing": ["digital marketing", "marketing"],
    "seo": ["seo", "sem"],
}

# Regular expressions for contact info extraction
EMAIL_REGEX = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_REGEX = re.compile(r'(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}')
LINKEDIN_REGEX = re.compile(r'linkedin\.com/in/[\w\-]+')
GITHUB_REGEX = re.compile(r'github\.com/[\w\-]+')

def extract_contact_info(text: str) -> Dict[str, str]:
    """Extracts email, phone, LinkedIn, and GitHub links from the text."""
    email_match = EMAIL_REGEX.search(text)
    phone_match = PHONE_REGEX.search(text)
    linkedin_match = LINKEDIN_REGEX.search(text)
    github_match = GITHUB_REGEX.search(text)
    
    return {
        "email": email_match.group(0) if email_match else "Not Found",
        "phone": phone_match.group(0) if phone_match else "Not Found",
        "linkedin": f"https://{linkedin_match.group(0)}" if linkedin_match else "Not Found",
        "github": f"https://{github_match.group(0)}" if github_match else "Not Found"
    }

def extract_skills(text: str) -> List[str]:
    """Matches text against the skill dictionary and extracts found skills."""
    text_lower = text.lower()
    found_skills = []
    
    for skill, patterns in SKILLS_DB.items():
        for pattern in patterns:
            # Handle special characters in skills like C++ or C# safely in regex
            # Use word boundaries for alphabetic strings, and raw search for symbolic/mix strings
            if re.search(r'^[a-zA-Z0-9]+$', pattern):
                regex_pattern = rf"\b{pattern}\b"
            else:
                regex_pattern = re.escape(pattern)
                
            if re.search(regex_pattern, text_lower):
                found_skills.append(skill)
                break  # If one pattern matches, the skill is found
                
    return sorted(list(set(found_skills)))

def analyze_experience_and_education(text: str) -> Dict[str, List[str]]:
    """Simple rule-based parser to extract education and experience highlights from text."""
    lines = text.split('\n')
    education_keywords = ['bachelor', 'master', 'phd', 'degree', 'university', 'college', 'bs', 'ms', 'b.tech', 'm.tech', 'bca', 'mca', 'b.sc', 'm.sc', 'mba']
    experience_keywords = ['experience', 'work history', 'professional background', 'employment', 'worked as', 'years of experience']
    
    education_lines = []
    experience_lines = []
    
    for line in lines:
        line_stripped = line.strip()
        if len(line_stripped) < 5 or len(line_stripped) > 150:
            continue
            
        line_lower = line_stripped.lower()
        
        # Check for education indicators
        if any(rf"\b{kw}\b" in line_lower or kw in line_lower for kw in education_keywords):
            if len(education_lines) < 5:  # Cap at 5 lines
                education_lines.append(line_stripped)
                
        # Check for experience indicators
        if any(rf"\b{kw}\b" in line_lower or kw in line_lower for kw in experience_keywords):
            if len(experience_lines) < 5:  # Cap at 5 lines
                experience_lines.append(line_stripped)
                
    return {
        "education": education_lines,
        "experience": experience_lines
    }

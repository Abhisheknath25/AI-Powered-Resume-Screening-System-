import os
import numpy as np
import tensorflow as tf

CATEGORIES = [
    "Software Engineering",
    "Data Science & AI",
    "Human Resources (HR)",
    "Finance & Accounting",
    "Marketing & Sales",
    "Product Management"
]

class ResumeClassifier:
    def __init__(self, model_dir="backend/model_files"):
        self.model_dir = model_dir
        self.model_path = os.path.join(model_dir, "resume_classifier.keras")
        self.model = None
        
    def _generate_synthetic_data(self):
        """Generates synthetic resumes and phrases for training."""
        vocab_software = [
            "python javascript typescript react node java developer software engineer backend frontend fullstack html css git docker k8s aws",
            "building scalable web applications API design databases sql postgresql mongodb systems design backend architecture code testing deployment",
            "software development lifecycle agile scrum spring boot django flask microservices code reviews unit testing cicd pipeline debugging code base"
        ]
        vocab_datascience = [
            "machine learning deep learning python data science artificial intelligence tensorflow pytorch keras scikit-learn pandas numpy visualization",
            "predictive modeling statistics r programming sql database data analysis neural networks computer vision natural language processing nlp spark",
            "big data engineering data pipeline models validation feature engineering mathematical analysis algorithms tabular data graphs regression trees classification"
        ]
        vocab_hr = [
            "human resources recruiting talent acquisition ats applicant tracking screening interviews recruitment hiring employee relations onboarding",
            "performance management payroll hr policies regulations training development labor laws retention programs diversity inclusion hr generalist benefits",
            "conducting candidate screening phone screen behavioral interview sourcing platforms linkedin recruiter job description matching culture fit"
        ]
        vocab_finance = [
            "accounting general ledger QuickBooks financial reporting tax preparation auditing spreadsheets bookkeeping payroll management budget analysis",
            "financial modeling valuation cash flow forecasting audit balance sheet p&l ledger reconciliation corporate finance investment planning stocks excel",
            "cost reduction strategies accounts payable accounts receivable finance compliance risk assessment cash management transactions billing invoices"
        ]
        vocab_marketing = [
            "digital marketing seo search engine optimization social media manager advertising google ads analytics campaign brand management copywriting",
            "sales pipeline b2b conversion optimization crm salesforce lead generation client relationships marketing strategy market research promotion",
            "content creation email campaigns influencer marketing affiliate marketing sales rep account manager customer success growth hacking metrics"
        ]
        vocab_product = [
            "product management roadmap agile scrum user stories backlog grooming jira confluence product lifecycle market research product design",
            "feature prioritization product specifications stakeholder management user testing analytics product metrics kpi launch strategy ux research",
            "business requirements document product owner strategy mapping user journey prototyping mockups wireframes customer discovery validation"
        ]
        
        corpus = []
        labels = []
        
        # Generate 100 samples per category by mixing and matching phrases
        np.random.seed(42)
        for cat_idx, vocab in enumerate([vocab_software, vocab_datascience, vocab_hr, vocab_finance, vocab_marketing, vocab_product]):
            for _ in range(60):
                # Sample random components and mix them up
                n_sentences = np.random.randint(2, 5)
                mix = []
                for _ in range(n_sentences):
                    # Pick a base phrase
                    base = np.random.choice(vocab)
                    # Add some random filler words
                    words = base.split()
                    np.random.shuffle(words)
                    mix.extend(words[:np.random.randint(5, 12)])
                
                # Combine words to build a dummy resume text snippet
                text = " ".join(mix)
                corpus.append(text)
                labels.append(cat_idx)
                
        return np.array(corpus), np.array(labels)

    def train(self):
        """Builds, trains, and saves the resume classification model."""
        print("Tensorflow: Generating synthetic training data...")
        X, y = self._generate_synthetic_data()
        
        # Shuffling dataset
        indices = np.arange(len(X))
        np.random.shuffle(indices)
        X = X[indices]
        y = y[indices]
        
        # Define TextVectorization layer
        print("Tensorflow: Setting up TextVectorization...")
        max_tokens = 1000
        seq_length = 100
        
        vectorizer = tf.keras.layers.TextVectorization(
            max_tokens=max_tokens,
            output_mode='int',
            output_sequence_length=seq_length
        )
        vectorizer.adapt(X)
        
        # Build Keras model
        print("Tensorflow: Initializing Sequential model...")
        model = tf.keras.Sequential([
            vectorizer,
            tf.keras.layers.Embedding(input_dim=max_tokens, output_dim=32, mask_zero=True),
            tf.keras.layers.GlobalAveragePooling1D(),
            tf.keras.layers.Dense(32, activation='relu'),
            tf.keras.layers.Dropout(0.2),
            tf.keras.layers.Dense(len(CATEGORIES), activation='softmax')
        ])
        
        model.compile(
            loss='sparse_categorical_crossentropy',
            optimizer='adam',
            metrics=['accuracy']
        )
        
        print("Tensorflow: Starting training...")
        # Small epochs since dataset is small & simple
        model.fit(tf.constant(X), tf.constant(y), epochs=15, batch_size=16, verbose=0)
        
        # Create output dir and save
        os.makedirs(self.model_dir, exist_ok=True)
        model.save(self.model_path)
        self.model = model
        print(f"Tensorflow: Model successfully trained and saved to {self.model_path}")

    def load_or_train(self):
        """Loads model if it exists, otherwise trains a new one."""
        if os.path.exists(self.model_path):
            try:
                print(f"Tensorflow: Loading existing model from {self.model_path}...")
                # Custom objects/safe loading if needed
                self.model = tf.keras.models.load_model(self.model_path)
                print("Tensorflow: Model loaded successfully.")
                return
            except Exception as e:
                print(f"Tensorflow: Failed to load model ({e}), retraining...")
                
        self.train()

    def predict(self, text: str):
        """Predicts the category of a given resume text.
        
        Returns:
            best_category (str): The predicted role category
            confidence (float): Confidence score between 0.0 and 1.0
            probabilities (dict): Dictionary mapping categories to confidence scores
        """
        if self.model is None:
            self.load_or_train()
            
        # Format input (model expects a list/batch of strings)
        predictions = self.model.predict(tf.constant([text]), verbose=0)[0]
        
        probabilities = {}
        for idx, score in enumerate(predictions):
            probabilities[CATEGORIES[idx]] = float(score)
            
        best_idx = int(np.argmax(predictions))
        best_category = CATEGORIES[best_idx]
        confidence = float(predictions[best_idx])
        
        return {
            "category": best_category,
            "confidence": confidence,
            "probabilities": probabilities
        }

# Global instance for easier reuse
classifier = ResumeClassifier()

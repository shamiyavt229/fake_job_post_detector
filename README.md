# 🔍 Fake Job Post Detector

A full-stack machine learning application that analyzes job descriptions and identifies whether a job posting is **genuine or potentially fraudulent**.

The application combines **Natural Language Processing (NLP), TF-IDF feature extraction, a trained machine learning classifier, and company email checks** to provide a prediction, confidence score, and warning information to the user.

---

## 📌 Overview

Online job scams can imitate legitimate job advertisements and may use misleading descriptions or suspicious recruiter contact information.

This project aims to provide an additional layer of screening by allowing a user to submit:

* A job description
* A company/recruiter email address

The system processes the submitted information and returns:

* **Genuine job** or **Fraudulent job**
* Prediction confidence
* Email-related warnings, when applicable

The project is implemented as a **React frontend + Django REST-style backend + machine learning inference pipeline**.

---

## ✨ Features

### 🤖 Machine Learning Prediction

Uses a trained machine learning model to classify job descriptions as:

* Genuine
* Fraudulent

The trained model and TF-IDF vectorizer are stored as serialized `.pkl` files and loaded by the Django backend during inference.

### 📝 Job Description Validation

The backend validates the submitted job description before running the model.

It checks that:

* A description is provided
* The input is textual
* The description contains at least 5 words
* The description contains at least 30 characters
* The description does not exceed 10,000 characters

This prevents obviously invalid input from reaching the prediction pipeline.

### 🔤 NLP & TF-IDF

The submitted description is normalized before prediction.

The current preprocessing pipeline:

1. Convert text to lowercase
2. Remove non-word/non-space characters
3. Normalize whitespace
4. Transform the processed text using the previously trained TF-IDF vectorizer

The vectorizer is loaded from `tfidf_vectorizer.pkl` and used with `transform()` during inference.

### 📧 Company Email Check

The application performs a rule-based check on the supplied company/recruiter email.

It checks:

* Whether the email has a valid basic structure
* Whether the domain belongs to a free email provider

For example, free providers such as Gmail, Yahoo, Hotmail, and Outlook can generate a warning because they are not company-owned domains.

> **Note:** This is an email-domain warning system, not an external verification of whether the company itself is legitimate.

### 📊 Confidence Score

The backend obtains the class probabilities from the trained classifier and returns the probability associated with the predicted class as the confidence percentage.

### 🌐 Full-Stack Architecture

The application separates the user interface from the prediction backend:

**React → Django API → ML Pipeline → Django Response → React UI**

---

# 🏗️ System Architecture

```text
                         ┌─────────────────────────┐
                         │         USER            │
                         │                         │
                         │ Job Description         │
                         │ Company Email           │
                         └────────────┬────────────┘
                                      │
                                      ▼
                         ┌─────────────────────────┐
                         │     REACT FRONTEND      │
                         │                         │
                         │ JobInput                │
                         │ CompanyEmail             │
                         │ PredictButton            │
                         │ PredictionCard           │
                         │ WarningList              │
                         └────────────┬────────────┘
                                      │
                              HTTP POST /api/predict/
                                      │
                                      ▼
                    ┌──────────────────────────────────┐
                    │         DJANGO BACKEND            │
                    │                                  │
                    │       prediction/views.py        │
                    └───────────────┬──────────────────┘
                                    │
                     ┌──────────────┴──────────────┐
                     │                             │
                     ▼                             ▼
          ┌────────────────────┐       ┌────────────────────┐
          │   Input Validation │       │  Email Rule Engine │
          │                    │       │                    │
          │ Length             │       │ Format             │
          │ Word count         │       │ Domain type        │
          └─────────┬──────────┘       └─────────┬──────────┘
                    │                            │
                    ▼                            │
          ┌────────────────────┐                 │
          │   Text Cleaning    │                 │
          │                    │                 │
          │ Lowercase          │                 │
          │ Remove characters  │                 │
          │ Normalize spaces   │                 │
          └─────────┬──────────┘                 │
                    │                            │
                    ▼                            │
          ┌────────────────────┐                 │
          │   TF-IDF Vectorizer│                 │
          │                    │                 │
          │ tfidf_vectorizer   │                 │
          │       .pkl         │                 │
          └─────────┬──────────┘                 │
                    │                            │
                    ▼                            │
          ┌────────────────────┐                 │
          │  ML Classifier     │                 │
          │                    │                 │
          │ fake_job_model.pkl │                 │
          └─────────┬──────────┘                 │
                    │                            │
                    │ Prediction + Probability  │
                    └──────────────┬─────────────┘
                                   │
                                   ▼
                         ┌───────────────────────┐
                         │    JSON RESPONSE      │
                         │                       │
                         │ prediction             │
                         │ probability            │
                         │ warnings               │
                         └───────────┬───────────┘
                                     │
                                     ▼
                         ┌─────────────────────────┐
                         │     REACT FRONTEND      │
                         │                         │
                         │ Display Prediction      │
                         │ Confidence              │
                         │ Warnings                │
                         └─────────────────────────┘
```

---

# 🔄 Prediction Workflow

The application follows this workflow:

```text
User enters job description + email
              │
              ▼
       React captures input
              │
              ▼
      POST request to Django
              │
              ▼
       Validate the input
              │
        ┌─────┴─────┐
        │           │
        ▼           ▼
 Description     Company Email
 Validation       Rule Check
        │           │
        ▼           │
   Clean text      │
        │           │
        ▼           │
      TF-IDF       │
      transform    │
        │           │
        ▼           │
   ML prediction   │
        │           │
        └─────┬─────┘
              ▼
       Build JSON response
              │
              ▼
       React receives response
              │
              ▼
      Display prediction,
      confidence & warnings
```

---

# 🧠 Machine Learning Pipeline

The machine learning component uses a pre-trained classifier and TF-IDF vectorizer.

During application development, the job-posting dataset was used to train the model.

The trained artifacts are:

```text
fake_job_model.pkl
tfidf_vectorizer.pkl
```

During prediction, the backend does **not retrain the model**.

Instead:

```python
vector = vectorizer.transform([cleaned_description])
prediction = model.predict(vector)
prediction_prob = model.predict_proba(vector)
```

This means the production/inference side of the application only performs feature transformation and prediction using the artifacts that were already trained.

---

# 🔤 NLP Pipeline

The submitted job description passes through the following processing stages:

```text
Raw Job Description
        │
        ▼
   Convert to lowercase
        │
        ▼
 Remove non-word characters
        │
        ▼
 Normalize whitespace
        │
        ▼
 TF-IDF transformation
        │
        ▼
 Numerical feature vector
        │
        ▼
 Machine Learning Model
```

TF-IDF converts textual information into numerical features that can be processed by the machine learning classifier.

---

# 📧 Rule-Based Email Analysis

The email analysis is implemented separately from the machine learning prediction.

The rule engine checks the supplied email for:

### 1. Basic email format

An invalid email format produces a warning.

### 2. Free email provider

The current implementation identifies domains such as:

```text
gmail.com
yahoo.com
hotmail.com
outlook.com
```

and produces a warning indicating that the recruiter is using a free email provider instead of a company domain.

This information is returned separately from the ML prediction.

Therefore, the application has two complementary analysis components:

```text
                 Job Description
                       │
                       ▼
                ML Classification
                       │
                       ├── Genuine
                       └── Fraudulent

                 Company Email
                       │
                       ▼
                Rule-Based Check
                       │
                       └── Warning(s)
```

---

# 🖥️ Frontend Architecture

The frontend is built using **React**.

The main application component maintains the state for:

* Company email
* Job description
* Prediction
* Confidence
* Warnings
* Errors

The UI is divided into reusable components.

```text
fake_job_post_frontend/
│
├── src/
│   ├── App.jsx
│   ├── App.css
│   ├── index.css
│   │
│   └── components/
│       ├── navbar.jsx
│       ├── JobInput.jsx
│       ├── companyEmail.jsx
│       ├── PredictButton.jsx
│       ├── PredictionCard.jsx
│       └── Warninglist.jsx
│
├── public/
├── package.json
├── package-lock.json
└── vite.config.js
```

`App.jsx` coordinates the components and sends the prediction request to the Django backend.

The current frontend API endpoint is:

```text
POST http://127.0.0.1:8000/api/predict/
```

The request contains:

```json
{
  "company_email": "recruiter@example.com",
  "description": "Job description..."
}
```

The backend responds with information such as:

```json
{
  "prediction": "Genuine job",
  "label": 0,
  "probability": 94.25,
  "warnings": []
}
```

---

# ⚙️ Backend Architecture

The backend is implemented using **Django**.

```text
fake_job_post_backend/
│
├── manage.py
│
├── fake_job_post_backend/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
└── prediction/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py
    ├── urls.py
    ├── views.py
    ├── tests.py
    ├── fraud_rules.py
    │
    └── migrations/
        └── __init__.py
```

### `views.py`

Acts as the main prediction controller.

It:

1. Receives the POST request
2. Reads the JSON body
3. Validates the input
4. Checks the company email
5. Cleans the job description
6. Transforms the text using TF-IDF
7. Runs the ML model
8. Calculates prediction confidence
9. Returns a JSON response

### `fraud_rules.py`

Contains the rule-based email checking logic.

### `models.py`

Contains Django model definitions for the application.

### `urls.py`

Connects the API endpoint to the prediction view.

---

# 🐳 Docker Support

The repository includes separate Dockerfiles for the backend and frontend:

```text
Dockerfile.backend
Dockerfile.frontend
```

This allows the two application layers to be containerized independently.

Conceptually:

```text
                 Application
                     │
          ┌──────────┴──────────┐
          │                     │
          ▼                     ▼
   Backend Container     Frontend Container
          │                     │
       Django                  React
          │
     ML Inference
```

---

# 📁 Project Structure

```text
fake_job_post_detector/
│
├── data/
│   └── fake_job_postings.csv
│
├── fake_job_post_backend/
│   ├── manage.py
│   │
│   ├── fake_job_post_backend/
│   │   ├── settings.py
│   │   ├── urls.py
│   │   ├── asgi.py
│   │   └── wsgi.py
│   │
│   └── prediction/
│       ├── views.py
│       ├── fraud_rules.py
│       ├── models.py
│       ├── urls.py
│       └── migrations/
│
├── fake_job_post_frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   └── components/
│   │       ├── JobInput.jsx
│   │       ├── PredictButton.jsx
│   │       ├── PredictionCard.jsx
│   │       ├── Warninglist.jsx
│   │       ├── companyEmail.jsx
│   │       └── navbar.jsx
│   │
│   ├── public/
│   ├── package.json
│   └── vite.config.js
│
├── fake_job_model.pkl
├── tfidf_vectorizer.pkl
├── requirements.txt
├── Dockerfile.backend
├── Dockerfile.frontend
├── .dockerignore
├── .gitignore
├── main.py
└── README.md
```

---

# 🛠️ Technology Stack

| Layer               | Technology            |
| ------------------- | --------------------- |
| Frontend            | React                 |
| Frontend tooling    | Vite                  |
| Backend             | Django                |
| API communication   | HTTP / JSON           |
| Machine Learning    | Python / scikit-learn |
| NLP                 | TF-IDF                |
| Model serialization | Pickle                |
| Dataset             | CSV                   |
| Containerization    | Docker                |
| Version control     | Git / GitHub          |

---

# 🚀 Getting Started

## 1. Clone the repository

```bash
git clone https://github.com/shamiyavt229/fake_job_post_detector.git
cd fake_job_post_detector
```

## 2. Backend setup

Create and activate a Python virtual environment:

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

Install the Python dependencies:

```bash
pip install -r requirements.txt
```

Move into the Django backend:

```bash
cd fake_job_post_backend
```

Run migrations:

```bash
python manage.py migrate
```

Start the Django development server:

```bash
python manage.py runserver
```

The backend will be available at:

```text
http://127.0.0.1:8000/
```

---

## 3. Frontend setup

Open another terminal and navigate to:

```bash
cd fake_job_post_frontend
```

Install dependencies:

```bash
npm install
```

Start the Vite development server:

```bash
npm run dev
```

Open the URL displayed by Vite in your browser.

---

# 🔐 Environment Variables

Sensitive configuration such as the Django secret key should be stored outside the source code using environment variables.

The `.env` file should **not** be committed to Git.

A typical setup can use:

```text
DJANGO_SECRET_KEY=your-secret-key
```

Make sure your `.gitignore` excludes:

```text
.env
.venv/
__pycache__/
```

---

# 🔒 Security Considerations

The application includes basic input validation and keeps the Django secret key outside the source code.

However, this project should be considered a **screening tool rather than a definitive fraud verification service**.

A machine learning prediction should not be treated as proof that a job posting is legitimate or fraudulent.

---

# 📈 Future Improvements

Possible improvements include:

* Add stronger company verification using external company/domain data
* Expand the rule engine beyond email-domain checks
* Preserve and analyze additional suspicious textual signals
* Add explainability for ML predictions
* Add model evaluation metrics to the application
* Improve handling of class imbalance
* Add automated backend and frontend tests
* Move API URLs into environment variables
* Add production-ready CORS configuration
* Add authentication and rate limiting
* Deploy frontend and backend independently
* Add CI/CD using GitHub Actions
* Improve Docker deployment with a multi-container setup

---

# 🎯 Learning Objectives

This project demonstrates practical experience with:

* Full-stack application development
* React component architecture
* React state management
* Django backend development
* REST-style API communication
* Natural Language Processing
* TF-IDF feature extraction
* Machine learning inference
* Rule-based fraud detection
* Input validation
* JSON-based frontend/backend communication
* Docker containerization
* Environment variable management
* Git and GitHub version control

---

# 👩‍💻 Author

**Shamiya VT**

B.Tech  Information Technology Graduate

---

## 📄 License

This project is intended for educational and portfolio purposes.

from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from pathlib import Path
import pickle
import re
from .fraud_rules import check_company_email


def clean_text(text):
  text = text.lower()
  text = re.sub(r"[^\w\s]", "", text)
  text = re.sub(r"\s+", " ", text)
  return text.strip() 



#------input validation----------------#
MIN_DESCRIPTION_LENGTH = 30
MAX_DESCRIPTION_LENGTH = 10000


def validate_job_input(description,company_email):
    errors = {}

    # Description checks
    if not isinstance(description, str):
        errors["description"] = "Description must be text."

    elif not description.strip():
        errors["description"] = "Description is required."

    else:
        text = description.strip()
        word_count = len(text.split())

        if len(text) < MIN_DESCRIPTION_LENGTH or word_count < 5:
            errors["description"] = (
                "Please enter a meaningful job description "
                "(at least 5 words and 30 characters)."
            )

        elif len(text) > MAX_DESCRIPTION_LENGTH:
            errors["description"] = (
                "Description must be 10,000 characters or fewer."
            )

    if company_email is not None and not isinstance(company_email, str):
      errors["company_email"] = "Company email must be text."
    return errors
  
  
#------------------------------------------------------------------------#

BASE_DIR=Path(__file__).resolve().parent.parent.parent
model=pickle.load(open(BASE_DIR/"fake_job_model.pkl","rb"))
vectorizer=pickle.load(open(BASE_DIR/"tfidf_vectorizer.pkl","rb"))

@csrf_exempt
def predict_job(request):
  
  if request.method == "POST":
    
    
    data=json.loads(request.body)
    description=data.get("description")
    company_email=data.get("company_email")
    errors = validate_job_input(description, company_email)

    
    print("DESCRIPTION:", description)
    print("COMPANY EMAIL:", company_email)
    print("ERRORS:", errors)
    
    
    if errors:
      return JsonResponse(
        {
            "error": "Invalid input.",
            "details": errors,
        },
        status=400,
    )
    email_warnings = check_company_email(company_email)
    cleaned_description = clean_text(description)
    vector = vectorizer.transform([cleaned_description])
    
    if vector.nnz == 0:
      return JsonResponse(
        {
            "error": (
                "Please enter a real job description. "
                "We could not find any recognizable job-related words."
            )
        },
        status=422,
    )
    
    prediction=model.predict(vector)
    prediction_prob=model.predict_proba(vector)
    confidence=float(prediction_prob[0][prediction[0]])*100
    #print("Prediction:", prediction)
    #print("Probability:", prediction_prob)
    if prediction[0]==0:
      result="Genuine job"
    else:
      result="Fraudulent job"
    
    return JsonResponse({
      "prediction":result,
      "label":int(prediction[0]),
      "probability":round(confidence,2),
      "warnings": email_warnings
      
   
    })
  
    
  return JsonResponse({
    "message":"Please send a post request"
  })
#print(BASE_DIR)
#print(BASE_DIR / "fake_job_model.pkl")
#print(BASE_DIR / "tfidf_vectorizer.pkl")
import re

FREE_EMAIL_PROVIDERS = {
    "gmail.com",
    "yahoo.com",
    "hotmail.com",
    "outlook.com",
}

def check_company_email(company_email):
    if not company_email:
        return []

    email = company_email.strip().lower()

    if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", email):
        return ["Company email look suspicious.Be Cautious"]

    domain = email.split("@")[1]

    if domain in FREE_EMAIL_PROVIDERS:
        return [
            "Recruiter uses a free email provider, not a company email domain."
        ]

    return ["hooray!!!!!No warnings#######"]
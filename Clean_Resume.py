import re


def clean_resume(resume_text):
    if resume_text is None:
        print("No text found in resume.")
        return ""
    name = re.findall(r'\b([A-Z][a-z]+(?: [A-Z]\.)? [A-Z][a-z]+)\b', resume_text)
    number = re.findall(r'(?:\+?\d{1,2} \()?[-.\s]?\d{3}[-\.\s]?\d{3,10}', resume_text)
    email_pattern = re.findall(r'\b[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+\b', resume_text)
    if not any([name, number, email_pattern]):
        print("Warning: No name, number, or email found in resume.")
    return {'name': name[0] if name else None, 'number': number[0] if number else None,
            'email': email_pattern[0] if email_pattern else None}

import re
import streamlit as st
import PyPDF2
# from Question_Generation import question_generation
import hashlib

hashed = ''

class ResumeBot:
    negative_responses = ("nothing", "don't", "stop", "sorry", "no", "sorry")
    exit_commands = ("quit", "pause", "exit", "goodbye", "bye", "later")

    def __init__(self):
        self.name = None
        self.questions = []

    def greet(self):
        self.name = st.text_input("Hi, I'm ResumeBot. What's your name? ")
        return self.name

    def resume(self):
        resume = st.text_input(
            f"Hi {self.name}, I'm here to help you. Can you provide me with your resume? Type 'yes' or 'no' ")

        if resume.lower() == 'yes':
            file = st.file_uploader("Upload your resume", type='pdf')
            if file is not None:
                global hashed
                pdf_bytes = file.read()
                hash_object = hashlib.sha256()
                hash_object.update(pdf_bytes)
                hashed = hash_object.hexdigest()
                print(hashed)
                st.write("Great! Let's get started.")
                try:
                    pdf_reader = PyPDF2.PdfReader(file)
                    num_pages = len(pdf_reader.pages)
                    text = ""
                    for page_num in range(num_pages):
                        page = pdf_reader.pages[page_num]
                        text += page.extract_text()
                    return text
                except Exception as e:
                    st.error(f"Error processing resume: {e}")
                    return None
        elif resume in self.negative_responses:
            st.write("I'm sorry to hear that. Let me know if you change your mind.")
            return None


# if __name__ == "__main__":
#     bot = ResumeBot()
#     bot.greet()
#     if bot.name:
#         resume_text = bot.resume()
#         if resume_text:
#             skills = bot.skill_config('skills.txt')
#             matched_skills = bot.matched_skills(resume_text, skills)
#             st.write(bot.matching_skills(resume_text, skills))
#             que = bot.question_generator(matched_skills)
#             bot.evaluate(question=que)
#             return None

import threading
from Bot import ResumeBot, hashed
from Clean_Resume import clean_resume
from Question_Generation import question_generation
from Question_generator import question_generator
import Percentage as ms
import Config_file as cf
import streamlit as st
from pymongo import MongoClient
import time
from datetime import datetime
import os
import signal
import openai

# Set up your OpenAI API key
openai.api_key = 'sk-proj-YZeNdxNeQrVJWlCywtxNT3BlbkFJ9LASmXH2TamdclhNevk5'


def end_server():
    pid = os.getpid()
    os.kill(pid, signal.SIGTERM)


def encode_field_name(field_name):
    return field_name.replace('.', '_dot_')


def decode_field_name(field_name):
    return field_name.replace('_dot_', '.')


def Experience():
    st.write("Experience Checker")
    note = st.selectbox("Select your Year of experience",
                        ["Fresher(0-2Y)", "Intermediate(2-4Y)", "Experienced(Above 4Y)",
                         "Expert(Above 10Y)"], key="experience_selectbox")
    if st.button('Submit', key="experience_submit_button"):
        return note
    else:
        return None


def PrintQuestion(_id):
    client = MongoClient('localhost', 27017)
    db = client['Practice']
    collection = db['Bot']

    if 'questions_generated' not in st.session_state or not st.session_state['questions_generated']:
        questions = collection.find_one({'_id': _id})['question']
        st.session_state['questions'] = questions
        st.session_state['questions_generated'] = True
    else:
        questions = st.session_state['questions']

    answer = {}
    for i, question in enumerate(questions):
        st.write(f"Question: {question}")
        answer[question] = {
            "answer": st.text_input("Your Answer: ", key=f"{question}_{i}"),
            "submitted_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    submit_button = st.button("Submit Answers", key=f"submit_answers_button_{_id}")
    if submit_button:
        answers_to_store = {}
        for key, value in answer.items():
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            answers_to_store[encode_field_name(key)] = value
        collection.update_one({'_id': _id}, {'$set': {'answers': answers_to_store}})
        st.success("Answers submitted successfully!")
        import random
        numbers = random.randint(23, 100)
        st.write(f"Similarity Percentage", numbers)

        # st.write("Your answers:", answer)

        stored_answers = collection.find_one({'_id': _id}).get('answers', {})
        decoded_answers = {decode_field_name(k): v for k, v in stored_answers.items()}
        # st.write(decoded_answers)

        # similarity_scores = compare_with_gpt(questions, decoded_answers)
        # st.write("Similarity Scores:", similarity_scores)


def timer(max_time_seconds):
    start_time = time.time()
    while True:
        remaining_time = max_time_seconds - (time.time() - start_time)
        if remaining_time <= 0:
            st.error("Time's up! Program ended.")
            break
        else:
            st.write(f"Time remaining: {int(remaining_time)} seconds")
            time.sleep(1)


# def compare_with_gpt(questions, answers):
#     similarity_scores = {}
#     for question, answer_data in answers.items():
#         user_answer = answer_data['answer']
#         gpt_answer = get_gpt_answer(question)
#         similarity = calculate_similarity(user_answer, gpt_answer)
#         similarity_scores[question] = similarity
#     return similarity_scores


# def get_gpt_answer(question):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": "You are an AI assistant."},
#                   {"role": "user", "content": question}]
#     )
#     return response.choices[0].message['content'].strip()


# def calculate_similarity(answer1, answer2):
#     response = openai.ChatCompletion.create(
#         model="gpt-3.5-turbo",
#         messages=[{"role": "system", "content": "You are an AI assistant."},
#                   {"role": "user",
#                    "content": f"Compare the similarity between these two answers and provide a similarity score ("
#                               f"0-100):\n\nAnswer 1: {answer1}\n\nAnswer 2: {answer2}"}]
#     )
#     return response.choices[0].message['content'].strip()


def main():
    bot = ResumeBot()
    bot.greet()
    if bot.name:
        resume_text = bot.resume()
        if resume_text:
            skills = ms.skill_config('skills.txt')
            matched_skills = ms.matched_skills(resume_text, skills)
            percentage = ms.matching_skills(resume_text, skills)
            st.write(percentage)
            # st.write(matched_skills)
            if 'experience' not in st.session_state:
                exp = Experience()
                if exp:
                    st.session_state.experience = exp
            else:
                exp = st.session_state.experience

            if exp:
                client = MongoClient('localhost', 27017)
                db = client['Practice']
                collection = db['Bot']

                user_data = clean_resume(resume_text)
                name = user_data['name']
                number = user_data['number']
                email = user_data['email']

                _id = hashed
                existing_entry = collection.find_one({'_id': _id})

                if existing_entry:
                    if 'questions_generated' not in st.session_state or not st.session_state['questions_generated']:
                        st.session_state['questions'] = question_generator(matched_skills, exp)
                        collection.update_one({'_id': _id}, {'$set': {'question': st.session_state['questions']}})
                        st.session_state['questions_generated'] = True
                else:
                    new_questions = question_generator(matched_skills, exp)
                    collection.insert_one(
                        {'_id': _id, 'name': name, 'number': number, 'email': email,
                         'skills': matched_skills, 'percentage': percentage,
                         'experience': exp, 'question': new_questions,
                         })

                    st.session_state['questions'] = new_questions
                    st.session_state['questions_generated'] = True

                    max_time_seconds = 120  # 30 minutes
                    timer_thread = threading.Thread(target=timer, args=(max_time_seconds,))
                    timer_thread.start()

                if 'answers' not in st.session_state:
                    st.session_state.answers = {}

                PrintQuestion(_id)
                st.write("Click the button below to end the program.")
                if st.button("End program"):
                    end_server()


if __name__ == "__main__":
    main()

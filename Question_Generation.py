import os
import openai
import streamlit as st

# api_key = st.secrets["openai"]["api_key"]
# if api_key:
#     openai.api_key = api_key
# else:
#     st.error("API key not found in Streamlit secrets.")


def question_generation(questions, experience):
    if experience == 'Fresher(0-2Y)':
        experience = 'Easy'
    elif experience == 'Intermediate(2-4Y)':
        experience = 'Medium'
    elif experience == 'Experienced(Above 4Y)' or experience == 'Expert(Above 10Y)':
        experience = 'Hard'

    client = openai.OpenAI(api_key='sk-proj-YZeNdxNeQrVJWlCywtxNT3BlbkFJ9LASmXH2TamdclhNevk5')
    t = (f'{questions}interview Questions for each programming languages with {experience} level  and dont mention '
         f'the language name in the'
         f'question')

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": t,
            }
        ],
        model="gpt-3.5-turbo",
    )
    question_answer = chat_completion.choices[0].message.content.splitlines()
    total = []
    for i in range(len(question_answer)):
        if question_answer[i].strip() == '':
            continue
        else:
            total.append(question_answer[i])
    question_answer = total
    question = []
    for i in range(len(question_answer)):
        question.append(question_answer[i])

    return question


# def answer_generation(questions):
#     client = OpenAI(
#         api_key='sk-proj-q90Vk8IpUcY9bn66odEtT3BlbkFJ4VYEjBHbxCDuy5oYuaGU',
#     )
#     t = f'{questions} give me answer for this question based on the language seperately in single line and give me title as language and  answer in next line'
#
#     chat_completion = client.chat.completions.create(
#         messages=[
#             {
#                 "role": "user",
#                 "content": t,
#             }
#         ],
#         model="gpt-3.5-turbo",
#     )
#
#     question_answer = chat_completion.choices[0].message.content.splitlines()
#     total = []
#     for i in range(len(question_answer)):
#         if question_answer[i].strip() == '':
#             continue
#         else:
#             total.append(question_answer[i])
#     return total


if __name__ == "__main__":
    question = question_generation(['C++', 'Python'])
    print(question)
    # answer = answer_generation(question)
    # print(answer)

# import streamlit as st
# from pymongo import MongoClient
# import Clean_Resume as cr
#
#
# #
# #
# # def evaluate(question):
# #     print('question', question)
# #     st.write(question)
# #
# #     answers = {}  # Initialize an empty dictionary to store answers
# #     index = 0
# #
# #
# #     for i in question:
# #         st.write(f"Question {index + 1}: {i}")
# #
# #         text_area_key = f"text_area_{i}"
# #
# #         answer_text_area = st.text_area("Your Answers (Separate with commas):", key=text_area_key)
# #
# #         submit_button = st.button("Submit All Answers", key=f"submit_{i}")
# #
# #         if submit_button:
# #             try:
# #                 user_answers = answer_text_area.strip().split(',')
# #                 answers[i] = [answer.strip() for answer in user_answers]  # Clean up whitespace
# #             except ValueError:
# #                 st.error("Please enter answers separated by commas.")
# #                 continue
# #
# #             answer_text_area.value = ""
# #
# #             index += 1
# #
# #     print(f"Collected answers: {answers}")
#
#
# def evaluate(self, question):
#     st.write(question)
#     answers = {}
#     index = 0
#     for i in question:
#         st.write(f"Question {index + 1}: {i}")
#         text_area_key = f"text_area_{i}"
#         answer_text_area = st.text_area("Your Answers (Separate with commas):", key=text_area_key)
#         submit_button = st.button("Submit All Answers", key=f"submit_{i}")
#         if submit_button:
#             try:
#                 user_answers = answer_text_area.strip().split(',')
#                 answers[i] = [answer.strip() for answer in user_answers]
#             except ValueError:
#                 st.error("Please enter answers separated by commas.")
#                 continue
#             answer_text_area.value = ""
#             index += 1

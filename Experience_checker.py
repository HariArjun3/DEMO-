import streamlit as st


def Experience():
    st.write("Experience Checker")
    note = st.selectbox("Select your Year of experience",
                        ["Fresher(0-2Y)", "Intermediate(2-4Y)", "Experienced(Above 4Y)",
                         "Expert(Above 10Y)"])
    if st.button('Submit',  key="experience_submit_button"):
        return note
    else:
        return None


if __name__ == '__main__':
    Experience()

#front end interface on mom's website for agent
import streamlit as st
from main import process_submission

st.title("Submit your ChatGPT Research")
url = st.text_input("Paste your ChatGPT Shareable Link:")
student_email = st.text_input("Your Email: ")
assignment_name = st.text_input("Assignment Name: ")

if st.button("Submit"):
    result = process_submission(url, student_email,assignment_name)
    st.write(result["student_message"])


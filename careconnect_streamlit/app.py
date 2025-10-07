import streamlit as st

st.title("CareConnect Streamlit App")
st.write("Welcome! This app lets you manage your health records and more.")

# Example input
user_name = st.text_input("What's your name?")
if user_name:
    st.success(f"Hello, {user_name}!")

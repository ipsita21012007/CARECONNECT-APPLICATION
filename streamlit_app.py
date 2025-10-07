import streamlit as st
from backend import add_user, get_users

st.title('Simple Streamlit + SQLite Backend')

name = st.text_input('Name:')
email = st.text_input('Email:')

if st.button('Add User'):
    add_user(name, email)
    st.success('User added!')

if st.button('Show Users'):
    users = get_users()
    st.write(users)

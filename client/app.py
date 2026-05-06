import streamlit as st

# Define pages
home = st.Page("pages/homepage.py", title="Homepage", icon="🏠")
login = st.Page('pages/login.py',title='Login To Vantaguard',icon='🔐')
signup = st.Page('pages/signup.py',title='Signup To Vantaguard',icon='🔐')

# Navigation setup
pg = st.navigation([home,login,signup])

# Run selected page
pg.run()
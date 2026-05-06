import streamlit as st
from pages.style import css
st.set_page_config(page_title='Vantaguard - Architectural Intelligence , Autonomous Assurance.' , page_icon='🔐')

st.markdown(css, unsafe_allow_html=True)

# Creating Header container
Header_Container = st.container(horizontal_alignment='center',vertical_alignment='center',height='stretch',width='stretch')

# Page header Title
Header_Container.markdown('<h1 class="text-align:center;">Login to Vantaguard</h1>',unsafe_allow_html=True)
    
# Page subheader 
Header_Container.subheader('Architectural Intelligence . Autonomous Assurance')



# Creating Login form component    
login_form = st.form(clear_on_submit=True,enter_to_submit=True,border=True,width='stretch',height='stretch',key='loginForm')

login_form.info('Please provide your credentials for logging to your account')

# Taking email from user
email = login_form.text_input('Email', placeholder='Ex - johndoe@gmail.com')
# Taking Password from user
password = login_form.text_input('Password', placeholder='Enter your registered Password', type='password') 
# Form Submit button
submit = login_form.form_submit_button(label='Submit Login Details')

# Validating form inputs
if submit:
    if not email or not password:
        st.error("⚠️ Please fill in all fields.")
    elif "@" not in email or "." not in email:
        st.error("⚠️ Enter a valid email address.")
    elif len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters.")
    else:
        st.success("✅ Login successful!")
        st.session_state["user"] = email
        st.switch_page('pages/homepage.py') 


# Setting navigation to signup page
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("<h6 class='font-weight:400'>Don’t have an account? Sign up to Vantaguard</h6>",unsafe_allow_html=True)

with col2:
    if st.button("Sign up"):
        st.switch_page('pages/signup.py')
    





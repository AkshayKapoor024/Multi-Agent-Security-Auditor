import streamlit as st
from pages.style import css
from api_client import signup_user
st.set_page_config(page_title='Vantaguard - Architectural Intelligence , Autonomous Assurance.' , page_icon='🔐')

st.markdown(css, unsafe_allow_html=True)

# Creating Header container
Header_Container = st.container(horizontal_alignment='center',vertical_alignment='center',height='stretch',width='stretch')

# Page header Title
Header_Container.markdown('<h1 class="text-align:center;">Sign Up to Vantaguard</h1>',unsafe_allow_html=True)
    
# Page subheader 
Header_Container.subheader('Architectural Intelligence . Autonomous Assurance')



# Creating Login form component    
login_form = st.form(clear_on_submit=True,enter_to_submit=True,border=True,width='stretch',height='stretch',key='loginForm')

login_form.info('Please provide your credentials for signing up to new account')

# Taking Name of user
name = login_form.text_input('Name',placeholder='John Doe')
# Taking Username from user
username = login_form.text_input('Username',placeholder='Enter your new username')
# Taking email from user
email = login_form.text_input('Email', placeholder='Ex - johndoe@gmail.com')
# Taking Password from user
password = login_form.text_input('Password', placeholder='Enter your Password', type='password') 
# Form Submit button
submit = login_form.form_submit_button(label='Create New Account')

# Validating form inputs
if submit:
    if not name or not username or not email or not password:
        st.error("⚠️ Please fill in all fields.")
    elif "@" not in email or "." not in email:
        st.error("⚠️ Enter a valid email address.")
    elif len(password) < 6:
        st.error("⚠️ Password must be at least 6 characters.")
    else:
        with st.spinner(text='Signing user up',show_time=True):  
            # Create user dict
            user_dict = dict(name=name,username=username,password=password,email=email)
            # Getting response from signup
            response = signup_user(user=user_dict)
            
            # Fetching response body
            body = response.json()
            
            # Successful signup and auto login
            if response.status_code==200:
                st.toast(body.get('message'), icon='✅',duration='long')
                st.balloons()
                # Getting user from response and storing in session object
                st.session_state.user = body.get('user')
                st.switch_page('pages/homepage.py') 
            else: 
                st.toast(f"Error while signing up user: {body.get('error')}", icon='☠️',duration='long')


# Setting navigation to signup page
col1, col2 = st.columns([1,1])

with col1:
    st.markdown("<h6 class='font-weight:400'>Already have an account ? Login to Vantaguard</h6>",unsafe_allow_html=True)

with col2:
    if st.button("Log in"):
        st.switch_page('pages/login.py')
    





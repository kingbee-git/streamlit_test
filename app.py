# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu
import bcrypt

import utils
import home
import orderlist

import time
import warnings
warnings.filterwarnings("ignore")

def load_users_data():
    users_data = utils.load_users_data()
    users = {}
    for index, row in users_data.iterrows():
        username = row['employeeName']
        password = row['password']
        try:
            hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
            users[username] = hashed_password
        except Exception as e:
            print(f"Error hashing password for user {username}: {e}")
    return users

def login(username, password):
    users = load_users_data()
    if username in users:
        stored_password = users[username]
        try:
            if bcrypt.checkpw(password.encode(), stored_password):
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                return True
        except Exception as e:
            print(f"Error checking password for user {username}: {e}")
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None
    st.session_state['jobTitle'] = None

def main():
    st.set_page_config(page_title="Mido_Plus",
                       page_icon=None,
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['jobTitle'] = None

    if st.session_state['logged_in']:
        st.write(f"Hello, {st.session_state['username']} ({st.session_state['jobTitle']})!")
        if st.button("Logout"):
            logout()
            st.experimental_rerun()  # 로그아웃 후 페이지 새로고침

        with st.sidebar:
            selected = option_menu("Main Menu", ["HOME", "DB", "test"],
                                   icons=["house", "gear", "gear"],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical",
                                   key='main_option',
                                   styles={
                                       "container": {"padding": "5!important", "background-color": "#fafafa"},
                                       "icon": {"color": "orange", "font-size": "25px"},
                                       "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#eee"},
                                       "nav-link-selected": {"background-color": "#02ab21"},
                                   })

        if selected == "HOME":
            home.home()
        elif selected == "DB":
            orderlist.orderlist()
    else:
        st.write("Please login to continue.")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            if login(username, password):
                st.success("Logged in successfully!")
                st.experimental_rerun()  # 로그인 후 페이지 새로고침
            else:
                st.error("Invalid username or password")

if __name__ == "__main__":
    main()
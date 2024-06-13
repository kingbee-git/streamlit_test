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

# 유저 데이터 저장을 위한 임시 저장소
users = {
    "범모": bcrypt.hashpw("1234".encode(), bcrypt.gensalt()),
    "형관": bcrypt.hashpw("1234".encode(), bcrypt.gensalt()),
}

def login(username, password):
    if username in users and bcrypt.checkpw(password.encode(), users[username]):
        st.session_state['logged_in'] = True
        st.session_state['username'] = username
        return True
    return False

def logout():
    st.session_state['logged_in'] = False
    st.session_state['username'] = None

def main():
    st.set_page_config(page_title="Mido_Plus",
                       page_icon=None,
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None

    if st.session_state['logged_in']:
        st.write(f"Hello, {st.session_state['username']}!")
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

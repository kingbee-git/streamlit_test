# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu

import utils
import home_app
import orderlist_app
import orderlist_realtime_app
import orderlist_updated_app
import stat_app

import time
import warnings
warnings.filterwarnings("ignore")


def load_users_data():
    users_data = utils.load_users_data()
    return users_data


def login(username, password):
    users_data = load_users_data()
    users = {row['employeeName']: {'jobTitle': row['jobTitle'], 'password': row['password']} for _, row in users_data.iterrows()}

    if username in users:
        stored_password_plain = users[username]['password']
        if password == stored_password_plain:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['jobTitle'] = users[username]['jobTitle']
            return True
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

    st.markdown("""
        <style>
        .username-jobTitle {
            font-size: 22px;
            font-weight: bold;
        }
        </style>
        """, unsafe_allow_html=True)

    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
        st.session_state['username'] = None
        st.session_state['jobTitle'] = None

    if st.session_state['logged_in']:
        with st.sidebar:

            col1, col2 = st.columns([1, 1])
            with col1:
                st.markdown(
                    f"""
                    <span class='username-jobTitle'>{st.session_state['username']} {st.session_state['jobTitle']}</span>님
                    """,
                    unsafe_allow_html=True
                )

            with col2:
                if st.button("로그아웃", key="logout_button"):
                    logout()
                    st.experimental_rerun()

            styles = {
                "container": {"padding": "5!important", "background-color": "#fafafa"},
                "icon": {"color": "orange", "font-size": "25px"},
                "nav-link": {
                    "font-size": "16px",
                    "text-align": "left",
                    "margin": "0px",
                    "--hover-color": "#eee",
                    "color": "#000",
                },
                "nav-link-selected": {"background-color": "#02ab21", "color": "#fff"},
            }

            selected = option_menu("Mido Plus", ["HOME", "orderlist", "orderlist_realtime", "orderlist_updated", "STAT"],
                                   icons=["house", "gear", "gear", "gear", "gear"],
                                   menu_icon="cast",
                                   default_index=0,
                                   orientation="vertical",
                                   key='main_option',
                                   styles=styles,
                                   )

        if selected == "HOME":
            home_app.home_app()
        elif selected == "orderlist":
            orderlist_app.orderlist_app()
        elif selected == "orderlist_realtime":
            orderlist_realtime_app.orderlist_realtime_app()
        elif selected == "orderlist_updated":
            orderlist_updated_app.orderlist_updated_app()
        elif selected == "STAT":
            stat_app.stat_app()

    else:
        st.write("계속하시려면 로그인하세요.")
        username = st.text_input("이름")
        password = st.text_input("비밀번호", type="password")
        if st.button("로그인"):
            if login(username, password):
                st.success("로그인에 성공하였습니다.")
                st.experimental_rerun()  # Reload page after login
            else:
                st.error("이름 또는 비밀번호를 확인해주세요.")


if __name__ == "__main__":
    main()
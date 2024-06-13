# -*- coding: utf-8 -*-
import streamlit as st
from streamlit_option_menu import option_menu

import utils

import time
import warnings
warnings.filterwarnings("ignore")

def main():
    st.set_page_config(page_title="Mido_Plus",
                       page_icon=None,
                       layout="wide",
                       initial_sidebar_state="auto",
                       menu_items=None)

    # Streamlit 앱 실행
    with st.sidebar:
        selected = option_menu("Main Menu", ["HOME", "DB", "test"],
                               icons=["house", "gear", "gear"],
                               menu_icon="cast",
                               default_index=0,
                               orientation="vertical",
                               key = 'main_option',
                               styles = {
                                   "container": {"padding": "5!important", "background-color": "#fafafa"},
                                   "icon": {"color": "orange", "font-size": "25px"},
                                   "nav-link": {"font-size": "16px", "text-align":"left", "margin":"0px", "--hover-color": "#eee"},
                                   "nav-link-selected": {"background-color": "#02ab21"},
                               })

if __name__ == "__main__":
    main()
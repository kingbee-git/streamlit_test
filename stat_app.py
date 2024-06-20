# -*- coding: utf-8 -*-
import streamlit as st

import utils

def stat_app():
    col1, col2 = st.columns([3, 1])

    with col1:
        st.header("왼쪽 컬럼")
        st.write("이곳에 다양한 내용을 추가할 수 있습니다.")

    with col2:
        st.header("오른쪽 컬럼")
        st.write("여기도 다양한 내용을 추가할 수 있습니다.")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.subheader("첫 번째 칼럼")
        st.write("이곳에 그래프나 데이터를 표시할 수 있습니다.")

    with col4:
        st.subheader("두 번째 칼럼")
        st.write("이곳에 다른 형태의 데이터를 표시할 수 있습니다.")

    with col5:
        st.subheader("세 번째 칼럼")
        st.write("이곳에 추가적인 정보를 표시할 수 있습니다.")
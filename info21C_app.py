# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils


def info21C_app():
    bir_ser_df_yesterday, bir_ser_df_today = utils.load_bid_ser_data()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader("첫 번째 칼럼")
        st.write("이곳에 그래프나 데이터를 표시할 수 있습니다.")

    with col2:

        bir_ser_key_column = '용역명'

        bir_ser_new = bir_ser_df_today[
            ~bir_ser_df_today[bir_ser_key_column].isin(bir_ser_df_yesterday[bir_ser_key_column])]

        st.subheader("인포21C (용역입찰)")
        st.markdown("<h5>새로운 용역입찰 건 입니다.</h5>", unsafe_allow_html=True)
        st.write(f"{len(bir_ser_new)} 건")
        st.dataframe(bir_ser_new, hide_index=True)

        st.markdown("<h5>키워드 내 인포21C 용역입찰 입니다.</h5>", unsafe_allow_html=True)
        bir_ser_column_index = bir_ser_df_today.columns.get_loc(bir_ser_key_column)
        bir_ser_column = st.selectbox('필터링할 열 선택', bir_ser_df_today.columns, index=bir_ser_column_index)
        bir_ser_search_term = st.text_input(f'{bir_ser_column}에서 검색할 내용 입력')

        if bir_ser_search_term:
            bir_ser_filtered_df = bir_ser_df_today[
                bir_ser_df_today[bir_ser_column].str.contains(bir_ser_search_term, case=False, na=False)]
            st.write(f"{len(bir_ser_filtered_df)} 건")
            st.dataframe(bir_ser_filtered_df, hide_index=True)
        else:
            bir_ser_filtered_df = bir_ser_df_today
            st.write(f"{len(bir_ser_filtered_df)} 건")
            st.dataframe(bir_ser_filtered_df, hide_index=True)

    with col3:
        st.subheader("세 번째 칼럼")
        st.write("이곳에 추가적인 정보를 표시할 수 있습니다.")
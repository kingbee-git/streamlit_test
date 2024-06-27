# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils


def news_app():
    news_df_yesterday, news_df_today = utils.load_news_data()


    news_key_column = '용역명'

    news_new = news_df_today[
        ~news_df_today[news_key_column].isin(news_df_yesterday[news_key_column])]

    st.subheader("인포21C (용역입찰)")
    st.markdown("<h5>새로운 용역입찰 건 입니다.</h5>", unsafe_allow_html=True)
    st.dataframe(news_new)

    st.markdown("<h5>키워드 내 인포21C 용역입찰 입니다.</h5>", unsafe_allow_html=True)
    news_column_index = news_df_today.columns.get_loc(news_key_column)
    news_column = st.selectbox('필터링할 열 선택', news_df_today.columns, index=news_column_index)
    news_search_term = st.text_input(f'{news_column}에서 검색할 내용 입력')

    if news_search_term:
        news_filtered_df = news_df_today[
            news_df_today[news_column].str.contains(news_search_term, case=False, na=False)]
        st.dataframe(news_filtered_df)
    else:
        news_filtered_df = news_df_today
        st.dataframe(news_filtered_df)
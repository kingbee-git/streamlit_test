# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils


def make_clickable(val):
    return f'<a target="_blank" href="{val}">{val}</a>'

def news_app():
    news_df_yesterday, news_df_today = utils.load_news_data()


    news_key_column = '내용'

    news_new = news_df_today[
        ~news_df_today[news_key_column].isin(news_df_yesterday[news_key_column])]

    st.subheader("키워드 내 뉴스 입니다.")
    st.markdown("<h5>새로운 뉴스 입니다.</h5>", unsafe_allow_html=True)
    st.data_editor(
        news_new[['기사날짜', '제목', 'URL', '내용']],
        column_config={
            "URL": st.column_config.LinkColumn(
                "URL",
                display_text="기사 보기",
                help="기사의 원본 링크",
                validate="^https?://",
                max_chars=100
            )
        },
        hide_index=True,
    )

    st.markdown("<h5>키워드 내 뉴스 입니다.</h5>", unsafe_allow_html=True)
    news_column_index = news_df_today.columns.get_loc(news_key_column)
    news_column = st.selectbox('필터링할 열 선택', news_df_today.columns, index=news_column_index)
    news_search_term = st.text_input(f'{news_column}에서 검색할 내용 입력')

    if news_search_term:
        news_filtered_df = news_df_today[
            news_df_today[news_column].str.contains(news_search_term, case=False, na=False)]

        st.data_editor(
            news_filtered_df[['기사날짜', '제목', 'URL', '내용']],
            column_config={
                "URL": st.column_config.LinkColumn(
                    "기사 URL",
                    display_text="기사 보기",
                    help="기사의 원본 링크",
                    validate="^https?://",
                    max_chars=100
                )
            },
            hide_index=True,
        )
    else:
        news_filtered_df = news_df_today

        st.data_editor(
            news_filtered_df[['기사날짜', '제목', 'URL', '내용']],
            column_config={
                "URL": st.column_config.LinkColumn(
                    "URL",
                    display_text="기사 보기",
                    help="기사의 원본 링크",
                    validate="^https?://",
                    max_chars=100
                )
            },
            hide_index=True,
        )

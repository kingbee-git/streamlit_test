# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils

def listup_app():
    QWGJK_df_yesterday, QWGJK_df_today = utils.load_QWGJK_data()
    dep_edu_df = utils.load_dep_edu_data()
    nara_df = utils.load_nara_data()

    st.subheader("지자체 예산 MAPPING TEST")

    QWGJK_key_column = '세부사업명'
    numeric_columns = ['예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']

    st.markdown("<h5>키워드 내 지자체 예산 입니다.</h5>", unsafe_allow_html=True)
    QWGJK_column_index = QWGJK_df_today.columns.get_loc(QWGJK_key_column)
    QWGJK_column = st.selectbox('필터링할 열 선택', QWGJK_df_today.columns, index=QWGJK_column_index, key='QWGJK_column')

    if QWGJK_column in numeric_columns:
        min_value = float(QWGJK_df_today[QWGJK_column].min())
        max_value = float(QWGJK_df_today[QWGJK_column].max())
        QWGJK_range = st.slider(f'{QWGJK_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                value=(min_value, max_value), key='QWGJK_range')
        QWGJK_filtered_df = QWGJK_df_today[
            (QWGJK_df_today[QWGJK_column] >= QWGJK_range[0]) & (QWGJK_df_today[QWGJK_column] <= QWGJK_range[1])]
    else:
        QWGJK_search_term = st.text_input(f'{QWGJK_column}에서 검색할 내용 입력', key='QWGJK_search_term')
        if QWGJK_search_term:
            QWGJK_filtered_df = QWGJK_df_today[
                QWGJK_df_today[QWGJK_column].str.contains(QWGJK_search_term, case=False, na=False)]
        else:
            QWGJK_filtered_df = QWGJK_df_today

    st.write(f"{len(QWGJK_filtered_df)} 건")
    st.dataframe(QWGJK_filtered_df, hide_index=True)

    st.markdown("<h5>키워드 내 교육청 예산 입니다.</h5>", unsafe_allow_html=True)
    st.write(f"{len(dep_edu_df)} 건")
    st.dataframe(dep_edu_df, hide_index=True)

    st.markdown("<h5>키워드 내 종합쇼핑몰 납품상세내역 입니다.</h5>", unsafe_allow_html=True)
    st.write(f"{len(nara_df)} 건")
    st.dataframe(nara_df, hide_index=True)
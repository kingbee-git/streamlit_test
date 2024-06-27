# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils

def QWGJK_app():
    QWGJK_df_yesterday, QWGJK_df_today = utils.load_QWGJK_data()

    st.subheader("지자체 예산")

    QWGJK_key_column = '세부사업명'
    numeric_columns = ['예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']

    QWGJK_end = QWGJK_df_yesterday[~QWGJK_df_yesterday[QWGJK_key_column].isin(QWGJK_df_today[QWGJK_key_column])]
    QWGJK_new = QWGJK_df_today[~QWGJK_df_today[QWGJK_key_column].isin(QWGJK_df_yesterday[QWGJK_key_column])]

    st.markdown("<h5>지자체 예산 금일 지출결의 된 건 입니다.</h5>", unsafe_allow_html=True)
    QWGJK_new_column_index = QWGJK_new.columns.get_loc(QWGJK_key_column)
    QWGJK_new_column = st.selectbox('필터링할 열 선택', QWGJK_new.columns, index=QWGJK_new_column_index,
                                    key='QWGJK_new_column')

    if QWGJK_new_column in numeric_columns:
        min_value = float(QWGJK_new[QWGJK_new_column].min())
        max_value = float(QWGJK_new[QWGJK_new_column].max())
        QWGJK_new_range = st.slider(f'{QWGJK_new_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='QWGJK_new_range')
        QWGJK_new_filtered_df = QWGJK_new[
            (QWGJK_new[QWGJK_new_column] >= QWGJK_new_range[0]) & (QWGJK_new[QWGJK_new_column] <= QWGJK_new_range[1])]
    else:
        QWGJK_new_search_term = st.text_input(f'{QWGJK_new_column}에서 검색할 내용 입력', key='QWGJK_new_search_term')
        if QWGJK_new_search_term:
            QWGJK_new_filtered_df = QWGJK_new[
                QWGJK_new[QWGJK_new_column].str.contains(QWGJK_new_search_term, case=False, na=False)]
        else:
            QWGJK_new_filtered_df = QWGJK_new

    st.write(f"{len(QWGJK_new_filtered_df)} 건")
    st.dataframe(QWGJK_new_filtered_df, hide_index=True)

    st.markdown("<h5>지자체 예산 금일 지출결의 종료 된 건 입니다.</h5>", unsafe_allow_html=True)
    QWGJK_end_column_index = QWGJK_end.columns.get_loc(QWGJK_key_column)
    QWGJK_end_column = st.selectbox('필터링할 열 선택', QWGJK_end.columns, index=QWGJK_end_column_index,
                                    key='QWGJK_end_column')

    if QWGJK_end_column in numeric_columns:
        min_value = float(QWGJK_end[QWGJK_end_column].min())
        max_value = float(QWGJK_end[QWGJK_end_column].max())
        QWGJK_end_range = st.slider(f'{QWGJK_end_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='QWGJK_end_range')
        QWGJK_end_filtered_df = QWGJK_end[
            (QWGJK_end[QWGJK_end_column] >= QWGJK_end_range[0]) & (QWGJK_end[QWGJK_end_column] <= QWGJK_end_range[1])]
    else:
        QWGJK_end_search_term = st.text_input(f'{QWGJK_end_column}에서 검색할 내용 입력', key='QWGJK_end_search_term')
        if QWGJK_end_search_term:
            QWGJK_end_filtered_df = QWGJK_end[
                QWGJK_end[QWGJK_end_column].str.contains(QWGJK_end_search_term, case=False, na=False)]
        else:
            QWGJK_end_filtered_df = QWGJK_end

    st.write(f"{len(QWGJK_end_filtered_df)} 건")
    st.dataframe(QWGJK_end_filtered_df, hide_index=True)

    st.markdown("<h5>키워드 내 지자체 예산 전체 입니다.</h5>", unsafe_allow_html=True)
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
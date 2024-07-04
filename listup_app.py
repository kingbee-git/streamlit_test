# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils

def listup_app():
    cross_dep_edu_df, cross_QWGJK_df, remain_dep_edu_df, remain_QWGJK_df = utils.load_listup_data()

    st.subheader("지자체 예산 MAPPING TEST")

    col1, col2 = st.columns(2)

    with col1:

        QWGJK_key_column = '세부사업명'
        numeric_columns = ['예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']

        st.markdown("<h5>키워드 내 지자체 예산 입니다.</h5>", unsafe_allow_html=True)
        QWGJK_column_index = remain_QWGJK_df.columns.get_loc(QWGJK_key_column)
        QWGJK_column = st.selectbox('필터링할 열 선택', remain_QWGJK_df.columns, index=QWGJK_column_index, key='QWGJK_column')

        if QWGJK_column in numeric_columns:
            min_value = float(remain_QWGJK_df[QWGJK_column].min())
            max_value = float(remain_QWGJK_df[QWGJK_column].max())
            QWGJK_range = st.slider(f'{QWGJK_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='QWGJK_range')
            QWGJK_filtered_df = remain_QWGJK_df[
                (remain_QWGJK_df[QWGJK_column] >= QWGJK_range[0]) & (remain_QWGJK_df[QWGJK_column] <= QWGJK_range[1])]
        else:
            QWGJK_search_term = st.text_input(f'{QWGJK_column}에서 검색할 내용 입력', key='QWGJK_search_term')
            if QWGJK_search_term:
                QWGJK_filtered_df = remain_QWGJK_df[
                    remain_QWGJK_df[QWGJK_column].str.contains(QWGJK_search_term, case=False, na=False)]
            else:
                QWGJK_filtered_df = remain_QWGJK_df

        st.write(f"{len(QWGJK_filtered_df)} 건")
        st.dataframe(QWGJK_filtered_df, hide_index=True)

        st.markdown("<h5>키워드 내 지자체 예산 제외 된 건 입니다.</h5>", unsafe_allow_html=True)
        st.dataframe(cross_QWGJK_df, hide_index=True)


    with col2:

        dep_edu_key_column = '과업명'
        numeric_columns = ['금액', '면적']

        st.markdown("<h5>키워드 내 교육청 예산 입니다.</h5>", unsafe_allow_html=True)
        dep_edu_column_index = remain_dep_edu_df.columns.get_loc(QWGJK_key_column)
        dep_edu_column = st.selectbox('필터링할 열 선택', remain_dep_edu_df.columns, index=dep_edu_column_index, key='QWGJK_column')

        if dep_edu_column in numeric_columns:
            min_value = float(remain_dep_edu_df[dep_edu_column].min())
            max_value = float(remain_dep_edu_df[dep_edu_column].max())
            dep_edu_range = st.slider(f'{dep_edu_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='dep_edu_range')
            dep_edu_filtered_df = remain_dep_edu_df[
                (remain_dep_edu_df[dep_edu_column] >= dep_edu_range[0]) & (remain_dep_edu_df[dep_edu_column] <= dep_edu_range[1])]
        else:
            dep_edu_search_term = st.text_input(f'{dep_edu_column}에서 검색할 내용 입력', key='QWGJK_search_term')
            if dep_edu_search_term:
                dep_edu_filtered_df = remain_dep_edu_df[
                    remain_dep_edu_df[dep_edu_column].str.contains(dep_edu_search_term, case=False, na=False)]
            else:
                dep_edu_filtered_df = remain_dep_edu_df

        st.write(f"{len(dep_edu_filtered_df)} 건")
        st.dataframe(dep_edu_filtered_df, hide_index=True)

        st.markdown("<h5>키워드 내 교육청 예산 제외 된 건 입니다.</h5>", unsafe_allow_html=True)
        st.dataframe(cross_dep_edu_df, hide_index=True)
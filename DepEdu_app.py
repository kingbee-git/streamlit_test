# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils

def DepEdu_app():
    dep_edu_df = utils.load_dep_edu_data()

    st.subheader("교육청 예산")

    dep_edu_key_column = '과업명'
    numeric_columns = ['금액']

    for column in numeric_columns:
        if column in dep_edu_df.columns:
            dep_edu_df[column] = dep_edu_df[column].str.replace(',', '').astype(float)


    dep_edu_column_index = dep_edu_df.columns.get_loc(dep_edu_key_column)
    dep_edu_column = st.selectbox('필터링할 열 선택', dep_edu_df.columns, index=dep_edu_column_index,
                                    key='dep_edu_key_column')

    if dep_edu_column in numeric_columns:
        min_value = float(dep_edu_df[dep_edu_column].min())
        max_value = float(dep_edu_df[dep_edu_column].max())
        dep_edu_range = st.slider(f'{dep_edu_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='dep_edu_range')
        dep_edu_filtered_df = dep_edu_df[
            (dep_edu_df[dep_edu_column] >= dep_edu_range[0]) & (dep_edu_df[dep_edu_column] <= dep_edu_range[1])]
    else:
        dep_edu_search_term = st.text_input(f'{dep_edu_column}에서 검색할 내용 입력', key='dep_edu_search_term')
        if dep_edu_search_term:
            dep_edu_filtered_df = dep_edu_df[
                dep_edu_df[dep_edu_column].str.contains(dep_edu_search_term, case=False, na=False)]
        else:
            dep_edu_filtered_df = dep_edu_df

    st.write(f"{len(dep_edu_filtered_df)} 건")
    st.dataframe(dep_edu_filtered_df, hide_index=True)
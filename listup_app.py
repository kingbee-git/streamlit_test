# -*- coding: utf-8 -*-
import streamlit as st

import numpy as np
import pandas as pd

import utils

def listup_app():
    remain_dep_edu_df, remain_QWGJK_df = utils.load_listup_data()

    st.header("예산 사업 현황")
    st.markdown("---")

    tab1, tab2 = st.tabs(["**지자체 예산 현황**", "**교육청 예산 현황**"])

    with tab1:
        st.header("**지자체 예산 현황**")
        st.markdown("---")

        numeric_columns = ['예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']
        remain_QWGJK_df['삭제'] = False  # 삭제 여부 컬럼 추가

        for column in numeric_columns:
            if column in remain_QWGJK_df.columns:
                remain_QWGJK_df[column] = remain_QWGJK_df[column].astype(str).str.replace(',', '').astype(float)

        st.markdown("---")
        QWGJK_key_column = st.selectbox('필터링할 열 선택', remain_QWGJK_df.columns,
                                        index=remain_QWGJK_df.columns.get_loc('세부사업명'))

        if QWGJK_key_column in numeric_columns:
            min_value = float(remain_QWGJK_df[QWGJK_key_column].min())
            max_value = float(remain_QWGJK_df[QWGJK_key_column].max())
            QWGJK_range = st.slider(f'{QWGJK_key_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                    value=(min_value, max_value), key='QWGJK_range')
            QWGJK_filtered_df = remain_QWGJK_df[
                (remain_QWGJK_df[QWGJK_key_column] >= QWGJK_range[0]) & (
                            remain_QWGJK_df[QWGJK_key_column] <= QWGJK_range[1])]
        else:
            QWGJK_search_term = st.text_input(f'{QWGJK_key_column}에서 검색할 내용 입력', key='QWGJK_search_term')
            if QWGJK_search_term:
                QWGJK_filtered_df = remain_QWGJK_df[
                    remain_QWGJK_df[QWGJK_key_column].str.contains(QWGJK_search_term, case=False, na=False)]
            else:
                QWGJK_filtered_df = remain_QWGJK_df

        st.markdown("---")
        st.write(f"{len(QWGJK_filtered_df)} 건")
        QWGJK_editable_df = st.data_editor(
            QWGJK_filtered_df,
            hide_index=True,
        )

        if st.button('지자체 저장'):
            utils.save_dataframe_to_bigquery(QWGJK_editable_df, 'mido_test', 'remain_QWGJK_df')
            utils.save_dataframe_to_bigquery(QWGJK_editable_df, 'mido_test', 'remain_QWGJK_df_save')

    with tab2:
        st.header("**교육청 예산 현황**")
        st.markdown("---")

        numeric_columns = ['금액', '면적']
        remain_dep_edu_df['삭제'] = False  # 삭제 여부 컬럼 추가

        for column in numeric_columns:
            if column in remain_dep_edu_df.columns:
                remain_dep_edu_df[column] = remain_dep_edu_df[column].replace('', np.nan).astype(str).str.replace(',',
                                                                                                                  '').astype(
                    float)

        st.markdown("---")
        dep_edu_key_column = st.selectbox('필터링할 열 선택', remain_dep_edu_df.columns,
                                          index=remain_dep_edu_df.columns.get_loc('과업명'))

        if dep_edu_key_column in numeric_columns:
            min_value = float(remain_dep_edu_df[dep_edu_key_column].min())
            max_value = float(remain_dep_edu_df[dep_edu_key_column].max())
            dep_edu_range = st.slider(f'{dep_edu_key_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
                                      value=(min_value, max_value), key='dep_edu_range')
            dep_edu_filtered_df = remain_dep_edu_df[
                (remain_dep_edu_df[dep_edu_key_column] >= dep_edu_range[0]) & (
                            remain_dep_edu_df[dep_edu_key_column] <= dep_edu_range[1])]
        else:
            dep_edu_search_term = st.text_input(f'{dep_edu_key_column}에서 검색할 내용 입력', key='dep_edu_search_term')
            if dep_edu_search_term:
                dep_edu_filtered_df = remain_dep_edu_df[
                    remain_dep_edu_df[dep_edu_key_column].str.contains(dep_edu_search_term, case=False, na=False)]
            else:
                dep_edu_filtered_df = remain_dep_edu_df

        st.markdown("---")
        st.write(f"{len(dep_edu_filtered_df)} 건")
        dep_edu_editable_df = st.data_editor(
            dep_edu_filtered_df,
            hide_index=True,
        )

        if st.button('교육청 저장'):
            utils.save_dataframe_to_bigquery(dep_edu_editable_df, 'mido_test', 'remain_dep_edu_df')
            utils.save_dataframe_to_bigquery(dep_edu_editable_df, 'mido_test', 'remain_dep_edu_df_save')


    # remain_dep_edu_df, remain_QWGJK_df = utils.load_listup_data()
    #
    # st.header("예산 사업 현황")
    # st.markdown("---")
    #
    # tab1, tab2 = st.tabs(["**지자체 예산 현황**", "**교육청 예산 현황**"])
    #
    # with tab1:
    #
    #     QWGJK_key_column = '세부사업명'
    #     numeric_columns = ['예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']
    #
    #     for column in numeric_columns:
    #         if column in remain_QWGJK_df.columns:
    #             remain_QWGJK_df[column] = remain_QWGJK_df[column].astype(str).str.replace(',', '').astype(float)
    #
    #     st.markdown("---")
    #     QWGJK_column_index = remain_QWGJK_df.columns.get_loc(QWGJK_key_column)
    #     QWGJK_column = st.selectbox('필터링할 열 선택', remain_QWGJK_df.columns, index=QWGJK_column_index, key='QWGJK_column')
    #
    #     if QWGJK_column in numeric_columns:
    #         min_value = float(remain_QWGJK_df[QWGJK_column].min())
    #         max_value = float(remain_QWGJK_df[QWGJK_column].max())
    #         QWGJK_range = st.slider(f'{QWGJK_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
    #                                 value=(min_value, max_value), key='QWGJK_range')
    #         QWGJK_filtered_df = remain_QWGJK_df[
    #             (remain_QWGJK_df[QWGJK_column] >= QWGJK_range[0]) & (remain_QWGJK_df[QWGJK_column] <= QWGJK_range[1])]
    #     else:
    #         QWGJK_search_term = st.text_input(f'{QWGJK_column}에서 검색할 내용 입력', key='QWGJK_search_term')
    #         if QWGJK_search_term:
    #             QWGJK_filtered_df = remain_QWGJK_df[
    #                 remain_QWGJK_df[QWGJK_column].str.contains(QWGJK_search_term, case=False, na=False)]
    #         else:
    #             QWGJK_filtered_df = remain_QWGJK_df
    #
    #     st.markdown("---")
    #     st.write(f"{len(QWGJK_filtered_df)} 건")
    #     st.data_editor(
    #         QWGJK_filtered_df,
    #         hide_index=True,
    #     )
    #
    # with tab2:
    #
    #     dep_edu_key_column = '과업명'
    #     numeric_columns = ['금액', '면적']
    #
    #     for column in numeric_columns:
    #         if column in remain_dep_edu_df.columns:
    #             remain_dep_edu_df[column] = remain_dep_edu_df[column].replace('', np.nan).astype(str).str.replace(',', '').astype(float)
    #
    #     st.markdown("---")
    #     dep_edu_column_index = remain_dep_edu_df.columns.get_loc(dep_edu_key_column)
    #     dep_edu_column = st.selectbox('필터링할 열 선택', remain_dep_edu_df.columns, index=dep_edu_column_index, key='dep_edu_column')
    #
    #     if dep_edu_column in numeric_columns:
    #         min_value = float(remain_dep_edu_df[dep_edu_column].min())
    #         max_value = float(remain_dep_edu_df[dep_edu_column].max())
    #         dep_edu_range = st.slider(f'{dep_edu_column}에서 검색할 범위 선택', min_value=min_value, max_value=max_value,
    #                                 value=(min_value, max_value), key='dep_edu_range')
    #         dep_edu_filtered_df = remain_dep_edu_df[
    #             (remain_dep_edu_df[dep_edu_column] >= dep_edu_range[0]) & (remain_dep_edu_df[dep_edu_column] <= dep_edu_range[1])]
    #     else:
    #         dep_edu_search_term = st.text_input(f'{dep_edu_column}에서 검색할 내용 입력', key='dep_edu_search_term')
    #         if dep_edu_search_term:
    #             dep_edu_filtered_df = remain_dep_edu_df[
    #                 remain_dep_edu_df[dep_edu_column].str.contains(dep_edu_search_term, case=False, na=False)]
    #         else:
    #             dep_edu_filtered_df = remain_dep_edu_df
    #
    #     st.markdown("---")
    #     st.write(f"{len(dep_edu_filtered_df)} 건")
    #     st.data_editor(
    #         dep_edu_filtered_df,
    #         hide_index=True,
    #     )
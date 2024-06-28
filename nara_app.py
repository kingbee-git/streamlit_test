# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import utils

def nara_app():
    try:
        nara_df = utils.load_nara_data()

        nara_df_key_column = '납품요구건명'

        st.markdown("<h5>종합쇼핑몰 납품상세내역 입니다.</h5>", unsafe_allow_html=True)
        nara_column_index = nara_df.columns.get_loc(nara_df_key_column)
        nara_column = st.selectbox('필터링할 열 선택', nara_df.columns, index=nara_column_index)
        nara_search_term = st.text_input(f'{nara_column}에서 검색할 내용 입력', key='bid_con_search')

        if nara_column in ['단가', '수량', '금액', '납품요구금액']:
            nara_df[nara_column] = nara_df[nara_column].replace(',', '', regex=True).astype(float)
            min_value = float(nara_df[nara_column].min())
            max_value = float(nara_df[nara_column].max())
            range_values = st.slider(f'{nara_column} 범위 선택', min_value, max_value, (min_value, max_value))

        if nara_search_term:
            if nara_df[nara_column].dtype == 'object':
                nara_filtered_df = nara_df[
                    nara_df[nara_column].str.contains(nara_search_term, case=False, na=False)]
            elif pd.api.types.is_numeric_dtype(nara_df[nara_column]):
                search_term_cleaned = nara_search_term.replace(',', '')
                nara_filtered_df = nara_df[nara_df[nara_column] == int(nara_search_term)]
            else:
                nara_filtered_df = nara_df
        else:
            nara_filtered_df = nara_df

        if nara_column in ['단가', '수량', '금액', '납품요구금액']:
            nara_filtered_df = nara_filtered_df[
                (nara_filtered_df[nara_column] >= range_values[0]) & (nara_filtered_df[nara_column] <= range_values[1])
            ]

        st.write(f"{len(nara_filtered_df)} 건")
        st.dataframe(nara_filtered_df, hide_index=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
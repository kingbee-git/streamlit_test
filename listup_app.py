# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd

import utils

def listup_app():
    QWGJK_df_yesterday, QWGJK_df_today = utils.load_QWGJK_data()
    nara_df = utils.load_nara_data()

    try:
        bid_con_key_column = '공고명'
        bid_con_new = bid_con_df_today[
            ~bid_con_df_today[bid_con_key_column].isin(bid_con_df_yesterday[bid_con_key_column])]

        st.subheader("인포21C (공사입찰)")
        st.markdown("<h5>새로운 공사입찰 건 입니다.</h5>", unsafe_allow_html=True)
        st.write(f"{len(bid_con_new)} 건")
        st.dataframe(bid_con_new, hide_index=True)

        st.markdown("<h5>키워드 내 인포21C 공사입찰 입니다.</h5>", unsafe_allow_html=True)
        bid_con_column_index = bid_con_df_today.columns.get_loc(bid_con_key_column)
        bid_con_column = st.selectbox('필터링할 열 선택', bid_con_df_today.columns, index=bid_con_column_index)
        bid_con_search_term = st.text_input(f'{bid_con_column}에서 검색할 내용 입력', key='bid_con_search')

        if bid_con_search_term:
            if bid_con_df_today[bid_con_column].dtype == 'object':
                bid_con_filtered_df = bid_con_df_today[
                    bid_con_df_today[bid_con_column].str.contains(bid_con_search_term, case=False, na=False)]
            elif pd.api.types.is_numeric_dtype(bid_con_df_today[bid_con_column]):
                bid_con_filtered_df = bid_con_df_today[bid_con_df_today[bid_con_column] == int(bid_con_search_term)]
            else:
                bid_con_filtered_df = bid_con_df_today
            st.write(f"{len(bid_con_filtered_df)} 건")
            st.dataframe(bid_con_filtered_df, hide_index=True)
        else:
            bid_con_filtered_df = bid_con_df_today
            st.write(f"{len(bid_con_filtered_df)} 건")
            st.dataframe(bid_con_filtered_df, hide_index=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
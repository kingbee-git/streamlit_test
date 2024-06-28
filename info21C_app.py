# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import utils

def info21C_app():
    try:
        bid_con_df_yesterday, bid_con_df_today = utils.load_bid_con_data()
        bid_ser_df_yesterday, bid_ser_df_today = utils.load_bid_ser_data()
        bid_pur_df_yesterday,  bid_pur_df_today = utils.load_bid_pur_data()

        col1, col2, col3 = st.columns(3)

        with col1:
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

        with col2:
            bid_ser_key_column = '공고명'
            bid_ser_new = bid_ser_df_today[
                ~bid_ser_df_today[bid_ser_key_column].isin(bid_ser_df_yesterday[bid_ser_key_column])]

            st.subheader("인포21C (용역입찰)")
            st.markdown("<h5>새로운 용역입찰 건 입니다.</h5>", unsafe_allow_html=True)
            st.write(f"{len(bid_ser_new)} 건")
            st.dataframe(bid_ser_new, hide_index=True)

            st.markdown("<h5>키워드 내 인포21C 용역입찰 입니다.</h5>", unsafe_allow_html=True)
            bid_ser_column_index = bid_ser_df_today.columns.get_loc(bid_ser_key_column)
            bid_ser_column = st.selectbox('필터링할 열 선택', bid_ser_df_today.columns, index=bid_ser_column_index)
            bid_ser_search_term = st.text_input(f'{bid_ser_column}에서 검색할 내용 입력', key='bid_ser_search')

            if bid_ser_search_term:
                if bid_ser_df_today[bid_ser_column].dtype == 'object':
                    bid_ser_filtered_df = bid_ser_df_today[
                        bid_ser_df_today[bid_ser_column].str.contains(bid_ser_search_term, case=False, na=False)]
                elif pd.api.types.is_numeric_dtype(bid_ser_df_today[bid_ser_column]):
                    bid_ser_filtered_df = bid_ser_df_today[bid_ser_df_today[bid_ser_column] == int(bid_ser_search_term)]
                else:
                    bid_ser_filtered_df = bid_ser_df_today
                st.write(f"{len(bid_ser_filtered_df)} 건")
                st.dataframe(bid_ser_filtered_df, hide_index=True)
            else:
                bid_ser_filtered_df = bid_ser_df_today
                st.write(f"{len(bid_ser_filtered_df)} 건")
                st.dataframe(bid_ser_filtered_df, hide_index=True)

        with col3:
            bid_pur_key_column = '공고명'
            bid_pur_new = bid_pur_df_today[
                ~bid_pur_df_today[bid_pur_key_column].isin(bid_pur_df_yesterday[bid_pur_key_column])]

            st.subheader("인포21C (구매입찰)")
            st.markdown("<h5>새로운 구매입찰 건 입니다.</h5>", unsafe_allow_html=True)
            st.write(f"{len(bid_pur_new)} 건")
            st.dataframe(bid_pur_new, hide_index=True)

            st.markdown("<h5>키워드 내 인포21C 구매입찰 입니다.</h5>", unsafe_allow_html=True)
            bid_pur_column_index = bid_pur_df_today.columns.get_loc(bid_pur_key_column)
            bid_pur_column = st.selectbox('필터링할 열 선택', bid_pur_df_today.columns, index=bid_pur_column_index)
            bid_pur_search_term = st.text_input(f'{bid_pur_column}에서 검색할 내용 입력', key='bid_pur_search')

            if bid_pur_search_term:
                if bid_pur_df_today[bid_pur_column].dtype == 'object':
                    bid_pur_filtered_df = bid_pur_df_today[
                        bid_pur_df_today[bid_pur_column].str.contains(bid_pur_search_term, case=False, na=False)]
                elif pd.api.types.is_numeric_dtype(bid_pur_df_today[bid_pur_column]):
                    bid_pur_filtered_df = bid_pur_df_today[bid_pur_df_today[bid_pur_column] == int(bid_pur_search_term)]
                else:
                    bid_pur_filtered_df = bid_pur_df_today
                st.write(f"{len(bid_pur_filtered_df)} 건")
                st.dataframe(bid_pur_filtered_df, hide_index=True)
            else:
                bid_pur_filtered_df = bid_pur_df_today
                st.write(f"{len(bid_pur_filtered_df)} 건")
                st.dataframe(bid_pur_filtered_df, hide_index=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()
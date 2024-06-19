# -*- coding: utf-8 -*-
import streamlit as st

import utils


def orderlist():
    orderlist = utils.load_orderlist_data()

    st.title("Orderlist")

    column = st.selectbox('필터링할 열 선택', orderlist.columns)
    search_term = st.text_input(f'{column}에서 검색할 내용 입력')

    if search_term:
        filtered_df = orderlist[orderlist[column].str.contains(search_term, case=False, na=False)]
        st.data_editor(filtered_df, num_rows="dynamic")
    else:
        filtered_df = orderlist  # 검색어가 없으면 전체 데이터프레임을 출력
        st.data_editor(filtered_df, num_rows="dynamic")

    col1, col2 = st.columns([3, 1])
    with col1:
        st.write("")
    with col2:
        if st.button('수정'):
            st.write("")






    # if '삭제' not in orderlist.columns:
    #     orderlist['삭제'] = False
    #
    # st.write("Streamlit 편집기")
    # edited_df = st.data_editor(orderlist, num_rows="dynamic")
    #
    # if '삭제' in edited_df.columns:
    #     if st.button('선택된 행 삭제'):
    #         edited_df = edited_df[edited_df['삭제'] == False]
    #         edited_df = edited_df.drop(columns=['삭제'])
    #
    # st.write("Streamlit 편집 후 데이터프레임")
    # st.dataframe(edited_df)





    # st.write("Streamlit 테이블")
    # st.table(orderlist)
    #
    # # st.write("Streamlit에서 대용량 데이터 프레임 처리하기")
    # container = st.container()
    # for i in range(0, len(orderlist), 50):
    #     container.dataframe(orderlist[i:i + 50])
    #
    # st.write("Streamlit에서 데이터프레임 스타일링1")
    # st.markdown("""
    # <style>
    # table {background-color: #f0f0f0;}
    # </style>
    # """, unsafe_allow_html=True)
    # st.dataframe(orderlist)
    #
    # st.write("Streamlit에서 데이터프레임 스타일링2")
    # st.dataframe(orderlist.style.background_gradient(cmap='Blues'))
    #
    # st.write("Streamlit 데이터프레임 필터링")
    # column = st.selectbox('필터링할 열 선택', orderlist.columns)
    # min_val, max_val = st.slider('값의 범위 선택', min(orderlist[column]), max(orderlist[column]), (min(orderlist[column]), max(orderlist[column])))
    # filtered_df = orderlist[(orderlist[column] >= min_val) & (orderlist[column] <= max_val)]
    # st.dataframe(filtered_df)

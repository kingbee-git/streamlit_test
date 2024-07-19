# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import pydeck as pdk
import os

import utils

def font_set():
    font_dirs = [os.getcwd() + '/nanum']

    font_files = fm.findSystemFonts(fontpaths=font_dirs)

    for font_file in font_files:
        fm.fontManager.addfont(font_file)

    plt.rcParams['font.family'] = fm.FontProperties(fname=font_files[0]).get_name()


def plot_company_data(nara_df, company_keywords, total_amount_total=None):

    company_data = {}
    for keyword in company_keywords:
        filtered_df = nara_df[nara_df['업체명'].str.contains(keyword)]
        total_amount = filtered_df['금액'].sum()
        total_count = filtered_df.shape[0]
        company_data[keyword] = {'금액': total_amount, '건수': total_count}

    if total_amount_total is None:
        total_amount_total = nara_df['금액'].sum()

    total_amount_ratios = [data['금액'] / total_amount_total * 100 for data in company_data.values()]
    total_counts = [data['건수'] for data in company_data.values()]
    total_amounts = [data['금액'] for data in company_data.values()]
    companies = list(company_data.keys())

    fig = go.Figure()

    fig.add_trace(go.Bar(
        x=companies,
        y=total_amounts,
        name='Total Amount',
        marker_color='blue',
        opacity=0.6,
        text=[f'금액: {amount:,}\n\n비율: {ratio:.2f}%' for amount, ratio in zip(total_amounts, total_amount_ratios)],
        textposition='auto'
    ))

    fig.add_trace(go.Scatter(
        x=companies,
        y=total_counts,
        name='Total Count',
        yaxis='y2',
        marker=dict(color='red', size=10),
        line=dict(color='red', width=2),
        text=[f'건수: {count}\n\n비율: {count / nara_df.shape[0] * 100:.2f}%' for count in total_counts],
        textposition='top center'
    ))

    fig.update_layout(
        title='Company Performance Comparison',
        xaxis_title='Company',
        yaxis_title='Total Amount',
        yaxis2=dict(
            title='Total Count',
            overlaying='y',
            side='right',
            range=[0, nara_df.shape[0] * 1.1]
        ),
        legend=dict(x=1.1, y=1.0),
        yaxis=dict(
            range=[0, total_amount_total * 1.1],
            showgrid = False
        )
    )

    st.plotly_chart(fig)

    return company_data


def home_app():
    nara_df = utils.load_nara_data()

    nara_select_df = nara_df[nara_df['업체명'].str.contains('미도플러스|에코그라운드')]

    try:
        nara_df_key_column = '납품요구건명'
        nara_veiw_column = [
            '납품요구접수일자', '수요기관명', '납품요구건명', '업체명', '금액', '수량', '단위', '단가', '품목'
        ]

        st.markdown("<h4>종합쇼핑몰 납품상세내역 현황</h4>", unsafe_allow_html=True)
        nara_column_index = nara_select_df.columns.get_loc(nara_df_key_column)
        nara_column = st.selectbox('필터링할 열 선택', nara_veiw_column, index=nara_column_index)
        nara_search_term = st.text_input(f'{nara_column}에서 검색할 내용 입력', key='nara_search_term')

        if nara_column in ['단가', '수량', '금액', '납품요구금액']:
            nara_select_df[nara_column] = nara_select_df[nara_column].replace(',', '', regex=True).astype(float)
            min_value = float(nara_select_df[nara_column].min())
            max_value = float(nara_select_df[nara_column].max())
            range_values = st.slider(f'{nara_column} 범위 선택', min_value, max_value, (min_value, max_value))

        if nara_search_term:
            if nara_select_df[nara_column].dtype == 'object':
                nara_filtered_df = nara_select_df[
                    nara_select_df[nara_column].str.contains(nara_search_term, case=False, na=False)]
            elif pd.api.types.is_numeric_dtype(nara_select_df[nara_column]):
                search_term_cleaned = nara_search_term.replace(',', '')
                nara_filtered_df = nara_select_df[nara_select_df[nara_column] == int(nara_search_term)]
            else:
                nara_filtered_df = nara_select_df
        else:
            nara_filtered_df = nara_select_df

        if nara_column in ['단가', '수량', '금액', '납품요구금액']:
            nara_filtered_df = nara_filtered_df[
                (nara_filtered_df[nara_column] >= range_values[0]) & (nara_filtered_df[nara_column] <= range_values[1])
            ]

        st.write(f"{len(nara_filtered_df)} 건")
        st.dataframe(nara_filtered_df[nara_veiw_column], hide_index=True)

    except Exception as e:
        st.error(f"An error occurred: {e}")
        st.stop()


    col1, space, col2 = st.columns([5, 0.1, 5])

    with col1:
        nara_df['금액'] = nara_df['금액'].str.replace(',', '').astype(int)

        company_keywords = ["미도플러스", "에코그라운드"]

        company_data = plot_company_data(nara_df, company_keywords)

    with col2:
        st.write("")

        # # NaN 값을 가진 행을 제거
        # nara_df = nara_df.dropna(subset=['위도', '경도'])
        #
        # # 위도와 경도를 숫자로 변환 (문자열을 숫자로 변환할 수 없는 경우 NaN으로 처리)
        # nara_df['위도'] = pd.to_numeric(nara_df['위도'], errors='coerce')
        # nara_df['경도'] = pd.to_numeric(nara_df['경도'], errors='coerce')
        #
        # # NaN 값을 가진 행 제거
        # nara_df = nara_df.dropna(subset=['위도', '경도'])
        #
        # # 데이터 타입 변환
        # nara_df[size_col] = pd.to_numeric(nara_df[size_col], errors='coerce')
        #
        # # Pydeck 지도 생성
        # layer = pdk.Layer(
        #     'ScatterplotLayer',
        #     data=nara_df,
        #     get_position='[경도, 위도]',
        #     get_color='[200, 30, 0, 160]',
        #     get_radius=size_col,
        #     pickable=True
        # )
        #
        # view_state = pdk.ViewState(
        #     latitude=nara_df['위도'].mean(),
        #     longitude=nara_df['경도'].mean(),
        #     zoom=5,
        #     pitch=50
        # )
        #
        # r = pdk.Deck(layers=[layer], initial_view_state=view_state,
        #              tooltip={"text": "{업체명}\n" + size_col + ": {" + size_col + "}"})
        # st.pydeck_chart(r)
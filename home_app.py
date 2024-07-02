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
    # 데이터 전처리
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
    companies = list(company_data.keys())

    # Plotly 그래프 생성
    fig = go.Figure()

    # Total Amount Ratio Bar
    fig.add_trace(go.Bar(
        x=companies,
        y=total_amount_ratios,
        name='Total Amount Ratio (%)',
        marker_color='blue',
        opacity=0.6,
        text=[f'Total Amount: {ratio:.2f}%' for ratio in total_amount_ratios],
        textposition='auto'
    ))

    # Total Count Line
    fig.add_trace(go.Scatter(
        x=companies,
        y=total_counts,
        name='Total Count',
        marker=dict(color='red', size=10),
        line=dict(color='red', width=2),
        text=[f'Total Count: {count / nara_df.shape[0] * 100:.2f}%' for count in total_counts],
        textposition='top center'
    ))

    # 레이아웃 설정
    fig.update_layout(
        title='Company Performance Comparison',
        xaxis_title='Company',
        yaxis_title='Total Amount Ratio (%)',
        yaxis2=dict(
            title='Total Count',
            overlaying='y',
            side='right'
        ),
        legend=dict(x=0.1, y=1.1),
        xaxis_tickangle=-45
    )

    # Streamlit에 그래프 표시
    st.plotly_chart(fig)

    return company_data


def home_app():
    nara_df = utils.load_nara_data()
    nara_select_df = nara_df[nara_df['업체명'].str.contains('미도플러스|에코그라운드')]

    col1, col2 = st.columns([1, 1])

    with col1:
        try:
            nara_df_key_column = '납품요구건명'

            st.markdown("<h5>종합쇼핑몰 납품상세내역 현황 입니다.</h5>", unsafe_allow_html=True)
            nara_column_index = nara_select_df.columns.get_loc(nara_df_key_column)
            nara_column = st.selectbox('필터링할 열 선택', nara_select_df.columns, index=nara_column_index)
            nara_search_term = st.text_input(f'{nara_column}에서 검색할 내용 입력', key='bid_con_search')

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
            st.dataframe(nara_filtered_df, hide_index=True)

        except Exception as e:
            st.error(f"An error occurred: {e}")
            st.stop()

        # # folium 지도 생성
        # map = folium.Map(location=[36.34, 127.77], zoom_start=6)
        #
        # # 색상 매핑 사전 정의
        # color_mapping = {
        #     '남기영': 'rgba(0, 0, 255, 0.9)',  # 반투명 파랑
        #     '야동원': 'rgba(255, 0, 0, 0.9)',  # 반투명 빨강
        #     '서인상': 'rgba(0, 255, 0, 0.9)',  # 반투명 초록
        # }
        #
        # # GeoJson 레이어 추가
        # folium.GeoJson(
        #     region_geodata,
        #     style_function=lambda feature: {
        #         'fillColor': color_mapping.get(feature['properties']['지역담당자'], 'gray'),
        #         'color': 'black',
        #         'weight': 2,
        #         'dashArray': '5, 5'
        #     },
        #     tooltip=folium.features.GeoJsonTooltip(fields=['지역담당자'], labels=False)
        # ).add_to(map)
        #
        # # 지도 출력
        # st_folium(map, width=400, height=500)

    with col2:
        nara_df['금액'] = nara_df['금액'].str.replace(',', '').astype(int)

        st.title("납품 데이터 분석")
        company_keywords = ["미도플러스", "에코그라운드"]

        company_data = plot_company_data(nara_df, company_keywords)

        st.markdown("### 세부 내역")
        for company, data in company_data.items():
            st.write(f"{company}:")
            st.write(f"총 금액: {data['금액']}원")
            st.write(f"총 건수: {data['건수']}건")

            
        # # EPSG:4326 좌표계로 변환
        # region_geodata = region_geodata.to_crs(epsg=4326)
        #
        # # 중심점 계산
        # region_geodata['centroid'] = region_geodata.geometry.centroid
        #
        # # 중심점을 데이터프레임으로 변환
        # df = pd.DataFrame({
        #     'name': region_geodata['지역담당자'],
        #     'lon': region_geodata['centroid'].x,
        #     'lat': region_geodata['centroid'].y
        # })
        #
        # # 결과 데이터프레임 출력
        # st.dataframe(df)
        #
        # # Pydeck 시각화 (멀티폴리곤 포함)
        # geojson = region_geodata.__geo_interface__
        # layer = pdk.Layer(
        #     'GeoJsonLayer',
        #     geojson,
        #     pickable=True,
        #     stroked=True,
        #     filled=True,
        #     extruded=False,
        #     get_fill_color='[200, 30, 0, 160]',
        #     get_line_color=[0, 0, 0],
        #     get_line_width=2,
        # )
        #
        # view_state = pdk.ViewState(
        #     latitude=df['lat'].mean(),
        #     longitude=df['lon'].mean(),
        #     zoom=6,
        #     pitch=0,
        # )
        #
        # deck = pdk.Deck(layers=[layer], initial_view_state=view_state)
        # st.pydeck_chart(deck)

    col3, col4, col5 = st.columns(3)

    with col3:
        st.write(" ")

    with col4:
        st.write(" ")

    with col5:
        st.write(" ")
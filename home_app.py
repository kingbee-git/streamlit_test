# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import pydeck as pdk

import utils

def home_app():
    # region_geodata = utils.load_region_geodata()
    # region_geodata.crs = "EPSG:5179"

    QWGJK_df_yesterday, QWGJK_df_today = utils.load_QWGJK_data()
    bir_ser_df_yesterday, bir_ser_df_today = utils.load_bid_ser_data()
    news_df_yesterday, news_df_today = utils.load_news_data()

    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("지자체 예산")
        st.write("키워드 내 지자체 예산 전체 입니다.")
        st.dataframe(QWGJK_df_today)


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
        QWGJK_key_column = '세부사업명'

        QWGJK_end = QWGJK_df_yesterday[~QWGJK_df_yesterday[QWGJK_key_column].isin(QWGJK_df_today[QWGJK_key_column])]
        QWGJK_new = QWGJK_df_today[~QWGJK_df_today[QWGJK_key_column].isin(QWGJK_df_yesterday[QWGJK_key_column])]

        st.write("금일 추가된 지자체 예산 사업 입니다.")
        st.dataframe(QWGJK_new)

        st.write("금일 집행 종료 된 지자체 예산 사업 입니다.")
        st.dataframe(QWGJK_end)


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
        st.subheader("인포 21C (용역입찰)")
        st.write("키워드 내 용역입찰 건 입니다.")
        st.dataframe(bir_ser_df_today)

    with col4:
        bir_ser_key_column = '용역명'

        bir_ser_new = bir_ser_df_today[
            ~bir_ser_df_today[bir_ser_key_column].isin(bir_ser_df_yesterday[bir_ser_key_column])]

        st.write("새로운 용역입찰 건 입니다.")
        st.dataframe(bir_ser_new)

    with col5:
        news_key_column = '제목'

        news_new = news_df_today[~news_df_today[news_key_column].isin(news_df_yesterday[news_key_column])]

        st.subheader("뉴스")
        st.write("키워드 내 뉴스 입니다.")
        st.dataframe(news_new)
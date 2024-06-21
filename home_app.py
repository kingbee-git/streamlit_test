# -*- coding: utf-8 -*-
import streamlit as st

import folium
from streamlit_folium import st_folium

import utils

def home_app():
    region_geodata = utils.load_region_geodata()
    region_geodata.crs = "EPSG:5179"

    col1, col2 = st.columns([3, 1])

    with col1:
        # folium 지도 생성
        map = folium.Map(location=[36.34, 127.77], zoom_start=6)

        # 색상 매핑 사전 정의
        color_mapping = {
            '남기영': 'rgba(0, 0, 255, 0.9)',  # 반투명 파랑
            '야동원': 'rgba(255, 0, 0, 0.9)',  # 반투명 빨강
            '서인상': 'rgba(0, 255, 0, 0.9)',  # 반투명 초록
        }

        # GeoJson 레이어 추가
        folium.GeoJson(
            region_geodata,
            style_function=lambda feature: {
                'fillColor': color_mapping.get(feature['properties']['지역담당자'], 'gray'),
                'color': 'black',
                'weight': 2,
                'dashArray': '5, 5'
            },
            tooltip=folium.features.GeoJsonTooltip(fields=['지역담당자'], labels=False)
        ).add_to(map)

        # 지도 출력
        st_folium(map, width=400, height=500)

    with col2:
        st.header("오른쪽 컬럼")
        st.write("여기도 다양한 내용을 추가할 수 있습니다.")

    col3, col4, col5 = st.columns(3)

    with col3:
        st.subheader("첫 번째 칼럼")
        st.write("이곳에 그래프나 데이터를 표시할 수 있습니다.")

    with col4:
        st.subheader("두 번째 칼럼")
        st.write("이곳에 다른 형태의 데이터를 표시할 수 있습니다.")

    with col5:
        st.subheader("세 번째 칼럼")
        st.write("이곳에 추가적인 정보를 표시할 수 있습니다.")
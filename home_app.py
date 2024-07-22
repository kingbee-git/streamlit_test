# -*- coding: utf-8 -*-
import streamlit as st

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.font_manager as fm
import plotly.graph_objects as go
import pydeck as pdk
import datetime
import time
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


def pydeck_company_data(nara_df, company_keywords, date_filter=None):
    # Filter by company keywords and date
    pattern = '|'.join(company_keywords)
    if date_filter:
        if isinstance(date_filter, datetime.date):
            date_filter = date_filter.strftime('%Y-%m-%d')
        filtered_df = nara_df[nara_df['업체명'].str.contains(pattern, na=False) & (nara_df['납품요구접수일자'] == date_filter)]
    else:
        filtered_df = nara_df[nara_df['업체명'].str.contains(pattern, na=False)]

    # 위도, 경도 데이터 정리
    filtered_df = filtered_df.dropna(subset=['위도', '경도'])
    filtered_df['위도'] = pd.to_numeric(filtered_df['위도'], errors='coerce')
    filtered_df['경도'] = pd.to_numeric(filtered_df['경도'], errors='coerce')
    filtered_df = filtered_df.dropna(subset=['위도', '경도'])

    # 지도 중심 설정
    midpoint = (filtered_df['위도'].mean(), filtered_df['경도'].mean())

    # Color mapping
    color_map = {
        "주식회사 미도플러스 (MIDOPLUS Inc.)": [180, 0, 0, 160],
        "(주)에코그라운드": [0, 0, 180, 160]
    }

    filtered_df['color'] = filtered_df['업체명'].map(color_map)

    default_color = [0, 255, 0, 160]
    filtered_df['color'] = filtered_df['color'].apply(lambda x: x if isinstance(x, list) else default_color)

    # 레이어 설정
    layer = pdk.Layer(
        'ScatterplotLayer',
        data=filtered_df,
        opacity=0.3,
        stroked=True,
        filled=True,
        radius_scale=10,
        radius_min_pixels=5,
        radius_max_pixels=60,
        line_width_min_pixels=1,
        get_position='[경도, 위도]',
        get_fill_color='color',
        get_line_color=[255,255,255],
        get_radius='금액 / 100000',
        pickable=True,
        extruded=True,
    )

    # Deck 설정
    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(
            latitude=midpoint[0],
            longitude=midpoint[1],
            zoom=6,
            pitch=45,
        ),

        map_style="mapbox://styles/mapbox/light-v10",
        tooltip={"text": "{업체명}\n{납품요구건명}\n금액: {금액}원"}
    )

    return deck


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

        company_data_1 = plot_company_data(nara_df, company_keywords)

    with col2:
        # subheading = st.subheader("")
        #
        # # Initial date
        # date = datetime.datetime.strptime(nara_df['납품요구접수일자'].min(), '%Y-%m-%d').date()

        # Set company keywords
        company_keywords = ["미도플러스", "에코그라운드"]

        # Render the initial map
        company_data_2 = pydeck_company_data(nara_df, company_keywords)
        st.pydeck_chart(company_data_2)

        # # Update the map and subheading each day for 120 days
        # for i in range(120):
        #     # Increment day by 1
        #     date += datetime.timedelta(days=1)
        #     current_date_str = date.strftime("%Y-%m-%d")
        #
        #     # Update data in map layers
        #     company_data_2 = pydeck_company_data(nara_df, company_keywords, current_date_str)
        #
        #     # Render the map
        #     st.pydeck_chart(company_data_2)
        #
        #     # Update the heading with current date
        #     subheading.subheader(f"{current_date_str}")
        #
        #     time.sleep(1)
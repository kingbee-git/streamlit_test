# -*- coding: utf-8 -*-
import streamlit as st

import time
import numpy as np
import pandas as pd
import plotly.express as px

import utils

def stat_app():
    g2b_data = utils.load_g2b_data()

    # CSS 스타일링
    st.markdown("""
        <style>
            .stMultiSelect {
                height: 65px;
                overflow-y: auto;
            }
            .stMultiSelect div {
                font-size: 6px;
            }
        </style>
    """, unsafe_allow_html=True)

    st.header("종합쇼핑몰 납품요구 상세내역")
    st.markdown("---")

    # 체크박스: 우수제품여부
    excellent_products = st.checkbox("우수제품여부", value=False)

    if excellent_products:
        filtered_data = g2b_data[g2b_data['우수제품여부'] == 'Y']
    else:
        filtered_data = g2b_data

    col1, space, col2 = st.columns([5, 0.1, 1])

    with col1:
        # 멀티셀렉트: 업체명
        unique_companies = sorted(filtered_data['업체명'].unique())
        selected_companies = st.multiselect("업체명 선택:", unique_companies, default=unique_companies)

        if selected_companies:
            filtered_data = filtered_data[filtered_data['업체명'].isin(selected_companies)]

        else:
            filtered_data = filtered_data

        # 멀티셀렉트: 지역명
        unique_regions = sorted(filtered_data['도광역시'].unique())
        selected_regions = st.multiselect("지역 선택:", unique_regions, default=unique_regions)

        if selected_companies:
            filtered_data = filtered_data[filtered_data['도광역시'].isin(selected_regions)]

        else:
            filtered_data = filtered_data

        date_col1, date_col2, date_col3 = st.columns([5, 1, 1])

        with date_col1:
            # 멀티셀렉트: 연도
            unique_years = pd.to_datetime(filtered_data['납품요구접수일자']).dt.year.unique()
            selected_years = st.multiselect("연도 선택:", unique_years, default=unique_years)

            if selected_years:
                filtered_data = filtered_data[pd.to_datetime(filtered_data['납품요구접수일자']).dt.year.isin(selected_years)]

            else:
                filtered_data = filtered_data

            # 캘린더: 세부 기간
            min_date = pd.to_datetime(filtered_data['납품요구접수일자'].min())
            max_date = pd.to_datetime(filtered_data['납품요구접수일자'].max())


        if selected_years:
            with date_col2:
                start_date = st.date_input("시작 날짜:", value=pd.to_datetime(f"{min(selected_years)}-01-01"))
            with date_col3:
                end_date = st.date_input("종료 날짜:", value=pd.to_datetime(f"{max(selected_years)}-12-31"))
        else:
            with date_col2:
                start_date = st.date_input("시작 날짜:", value=min_date)
            with date_col3:
                end_date = st.date_input("종료 날짜:", value=max_date)

        # 기간 유효성 체크
        if start_date > end_date:
            st.error("시작 날짜는 종료 날짜보다 이전이어야 합니다.")

        filtered_data = filtered_data[
            (filtered_data['납품요구접수일자'] >= pd.to_datetime(start_date)) &
            (filtered_data['납품요구접수일자'] <= pd.to_datetime(end_date))
            ]
    with space:
        st.write("")

    with col2:
        # 슬라이더 추가: 단가, 수량, 금액
        min_price = float(filtered_data['단가'].min())
        max_price = float(filtered_data['단가'].max())
        price_range = (min_price, max_price) if min_price < max_price else (0.0, max_price)

        min_quantity = float(filtered_data['수량'].min())
        max_quantity = float(filtered_data['수량'].max())
        quantity_range = (min_quantity, max_quantity) if min_quantity < max_quantity else (0.0, max_quantity)

        min_amount = float(filtered_data['금액'].min())
        max_amount = float(filtered_data['금액'].max())
        amount_range = (min_amount, max_amount) if min_amount < max_amount else (0.0, max_amount)

        min_price, max_price = st.slider("단가 범위 선택:", min_price, max_price, price_range)
        min_quantity, max_quantity = st.slider("수량 범위 선택:", min_quantity, max_quantity, quantity_range)
        min_amount, max_amount = st.slider("금액 범위 선택:", min_amount, max_amount, amount_range)

        filtered_data = filtered_data[
            (filtered_data['단가'] >= min_price) & (filtered_data['단가'] <= max_price) &
            (filtered_data['수량'] >= min_quantity) & (filtered_data['수량'] <= max_quantity) &
            (filtered_data['금액'] >= min_amount) & (filtered_data['금액'] <= max_amount)
        ]

        # st.markdown("---")
        # st.markdown(
        #     f"<h3 style='text-align: center;'><span style='color: red; font-size: 38px;'>{len(filtered_data)}</span> "
        #     f"/<span style='color: black; font-size: 36px;'>{len(g2b_data)}</span></h3>",
        #     unsafe_allow_html=True
        # )
    st.markdown("---")

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        label="단가 평균",
        value=f"₩{round(filtered_data['단가'].mean(), 2):,}",
        delta=f"₩{round(g2b_data['단가'].mean(), 2):,}",
        delta_color="inverse" if round(filtered_data['단가'].mean(), 2) < round(g2b_data['단가'].mean(), 2) else "normal"
    )

    kpi2.metric(
        label="수량 평균(m²)",
        value=f"{round(filtered_data['수량'].mean()):,}",
        delta=f"{round(g2b_data['수량'].mean()):,}",
        delta_color="inverse" if round(filtered_data['수량'].mean(), 2) < round(g2b_data['수량'].mean(), 2) else "normal"
    )

    kpi3.metric(
        label="금액 평균",
        value=f"₩{round(filtered_data['금액'].mean(), 2):,}",
        delta=f"₩{round(g2b_data['금액'].mean(), 2):,}",
        delta_color="inverse" if round(filtered_data['금액'].mean(), 2) < round(g2b_data['금액'].mean(), 2) else "normal"
    )

    kpi4, kpi5, kpi6 = st.columns(3)

    kpi4.metric(
        label="거래 건",
        value=f"{filtered_data['단가'].count():,}",  # 거래 건 수는 금액 표시 없이 간단히 표시
        delta=f"{g2b_data['단가'].count():,}",
        delta_color="inverse" if filtered_data['단가'].count() < g2b_data['단가'].count() else "normal"
    )

    kpi5.metric(
        label="수량 합 (m²)",
        value=f"{round(filtered_data['수량'].sum()):,}",
        delta=f"{round(g2b_data['수량'].sum()):,}",
        delta_color="inverse" if round(filtered_data['수량'].sum(), 2) < round(g2b_data['수량'].sum(), 2) else "normal"
    )

    kpi6.metric(
        label="금액 합",
        value=f"₩{round(filtered_data['금액'].sum(), 2):,}",
        delta=f"₩{round(g2b_data['금액'].sum(), 2):,}",
        delta_color="inverse" if round(filtered_data['금액'].sum(), 2) < round(g2b_data['금액'].sum(), 2) else "normal"
    )

    st.markdown("---")

    # 라디오 버튼 추가
    metric_to_plot = st.radio("차트에 표시할 항목을 선택하세요:", ("단가", "수량", "금액"))

    # 차트 표시
    fig_col1, fig_col2 = st.columns(2)

    with fig_col1:
        st.markdown("### 차트")

        if metric_to_plot == "단가":
            # 평균 단가 계산
            avg_price = filtered_data.groupby("업체명")["단가"].mean().reset_index()
            fig = px.bar(avg_price, x="업체명", y="단가", title="업체별 평균 단가 차트")
            fig.update_layout(yaxis_title="단가 (원)")  # 원화 단위 추가
        elif metric_to_plot == "수량":
            # 수량 합계 계산
            total_quantity = filtered_data.groupby("업체명")["수량"].sum().reset_index()
            fig = px.bar(total_quantity, x="업체명", y="수량", title="업체별 수량 차트")
            fig.update_layout(yaxis_title="수량")  # 수량 단위 추가
        else:
            # 금액 합계 계산
            total_amount = filtered_data.groupby("업체명")["금액"].sum().reset_index()
            fig = px.bar(total_amount, x="업체명", y="금액", title="업체별 금액 차트")
            fig.update_layout(yaxis_title="금액 (원)")  # 원화 단위 추가

        # 모든 값 표시
        fig.update_traces(texttemplate='%{y:.0f}', textposition='outside')  # 소수점 없이 모든 값 표시

        st.write(fig)

    with fig_col2:
        st.markdown("### 지도")

        # NaN 값을 가진 행을 제거
        valid_data = filtered_data.dropna(subset=['위도', '경도'])

        # 위도와 경도를 숫자로 변환 (문자열을 숫자로 변환할 수 없는 경우 NaN으로 처리)
        valid_data['위도'] = pd.to_numeric(valid_data['위도'], errors='coerce')
        valid_data['경도'] = pd.to_numeric(valid_data['경도'], errors='coerce')

        # NaN 값을 가진 행 제거
        valid_data = valid_data.dropna(subset=['위도', '경도'])

        if '위도' in valid_data.columns and '경도' in valid_data.columns:
            if metric_to_plot == "단가":
                size_col = '단가'
            elif metric_to_plot == "수량":
                size_col = '수량'
            else:
                size_col = '금액'

            # 데이터 타입 변환
            valid_data[size_col] = pd.to_numeric(valid_data[size_col], errors='coerce')

            fig2 = px.scatter_mapbox(
                valid_data,
                lat="위도",
                lon="경도",
                size=size_col,
                color="업체명",
                hover_name="업체명",
                hover_data={size_col: True},
                zoom=5,
                mapbox_style="open-street-map"  # 필요시 API 키를 사용하여 변경
            )
            st.write(fig2)
        else:
            st.error("위도와 경도 데이터가 필요합니다. 데이터를 확인하세요.")


    st.markdown("---")
    st.dataframe(filtered_data)
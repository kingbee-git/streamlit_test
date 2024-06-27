# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import geopandas as gpd
import pandas_gbq
from datetime import datetime, timedelta
import json
from shapely import wkt
from google.cloud import bigquery
from google.oauth2 import service_account

import warnings
warnings.filterwarnings("ignore")

credentials = service_account.Credentials.from_service_account_info(st.secrets["gcp_service_account"])

def save_dataframe_to_bigquery(df, dataset_id, table_id):

    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials)

    # 테이블 레퍼런스 생성
    table_ref = client.dataset(dataset_id).table(table_id)

    # 데이터프레임을 BigQuery 테이블에 적재
    job_config = bigquery.LoadJobConfig()
    job_config.write_disposition = "WRITE_TRUNCATE"  # 기존 테이블 내용 삭제 후 삽입

    job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
    job.result()  # 작업 완료 대기

    print(f"Data inserted into table {table_id} successfully.")
def get_dataframe_from_bigquery(dataset_id, table_id):

    # BigQuery 클라이언트 생성
    client = bigquery.Client(credentials=credentials, project=credentials.project_id)

    # 테이블 레퍼런스 생성
    table_ref = client.dataset(dataset_id).table(table_id)

    # 테이블 데이터를 DataFrame으로 변환
    df = client.list_rows(table_ref).to_dataframe()

    return df

def get_geodataframe_from_bigquery(dataset_id, table_id):

    # 빅쿼리 클라이언트 객체 생성
    client = bigquery.Client(credentials=credentials)

    # 쿼리 작성
    query = f"SELECT * FROM `{dataset_id}.{table_id}`"

    # 쿼리 실행
    df = client.query(query).to_dataframe()

    # 'geometry' 열의 문자열을 다각형 객체로 변환
    df['geometry'] = df['geometry'].apply(wkt.loads)

    # GeoDataFrame으로 변환
    gdf = gpd.GeoDataFrame(df, geometry='geometry')
    gdf.crs = "EPSG:5179"

    return gdf


@st.cache_data
def load_users_data():
    users = get_dataframe_from_bigquery('mido_test', 'users').sort_values(by='employeeNumber').reset_index(drop=True)
    users = users[['employeeName', 'jobTitle', 'password']]

    return users

@st.cache_data
def load_QWGJK_data():
    QWGJK_df_yesterday = get_dataframe_from_bigquery('mido_test', 'QWGJK_df_yesterday')
    QWGJK_df_today = get_dataframe_from_bigquery('mido_test', 'QWGJK_df_today')

    QWGJK_df_yesterday['회계연도'] = pd.to_datetime(QWGJK_df_yesterday['회계연도'], format='%Y').dt.strftime('%Y')
    QWGJK_df_yesterday['집행일자'] = pd.to_datetime(QWGJK_df_yesterday['집행일자'], format='%Y%m%d').dt.strftime('%Y%m%d')
    QWGJK_df_today['회계연도'] = pd.to_datetime(QWGJK_df_today['회계연도'], format='%Y').dt.strftime('%Y')
    QWGJK_df_today['집행일자'] = pd.to_datetime(QWGJK_df_today['집행일자'], format='%Y%m%d').dt.strftime('%Y%m%d')

    # 키워드 중요도 리스트
    keywords = ['인조잔디', '조성사업']
    keyword_importance = {keyword: i for i, keyword in enumerate(keywords)}

    def get_importance(name):
        for keyword, importance in keyword_importance.items():
            if keyword in name:
                return importance
        return float('inf')  # 키워드가 없는 경우 맨 뒤로 정렬

    # 키워드 중요도 점수 컬럼 추가
    QWGJK_df_yesterday['중요도'] = QWGJK_df_yesterday['세부사업명'].apply(get_importance)
    QWGJK_df_today['중요도'] = QWGJK_df_today['세부사업명'].apply(get_importance)

    # 중요도 순서로 정렬
    QWGJK_df_yesterday = QWGJK_df_yesterday.sort_values(by='중요도')
    QWGJK_df_today = QWGJK_df_today.sort_values(by='중요도')

    # 중요도 컬럼 제거 (원하지 않으면)
    QWGJK_df_yesterday = QWGJK_df_yesterday.drop(columns=['중요도'])
    QWGJK_df_today = QWGJK_df_today.drop(columns=['중요도'])


    return QWGJK_df_yesterday, QWGJK_df_today

@st.cache_data
def load_bid_ser_data():
    bir_ser_df_yesterday = get_dataframe_from_bigquery('mido_test', 'bir_ser_df_yesterday').sort_values('공고일', ascending=False)
    bir_ser_df_today = get_dataframe_from_bigquery('mido_test', 'bir_ser_df_today').sort_values('공고일', ascending=False)

    return bir_ser_df_yesterday, bir_ser_df_today

@st.cache_data
def load_news_data():
    news_df_yesterday = get_dataframe_from_bigquery('mido_test', 'news_df_yesterday').sort_values('기사날짜', ascending=False)
    news_df_today = get_dataframe_from_bigquery('mido_test', 'news_df_today').sort_values('기사날짜', ascending=False)

    # 키워드 중요도 리스트
    keywords = ['인조잔디']
    keyword_importance = {keyword: i for i, keyword in enumerate(keywords)}

    def get_importance(name):
        for keyword, importance in keyword_importance.items():
            if keyword in name:
                return importance
        return float('inf')  # 키워드가 없는 경우 맨 뒤로 정렬

    # 키워드 중요도 점수 컬럼 추가
    news_df_yesterday['중요도'] = news_df_yesterday['내용'].apply(get_importance)
    news_df_today['중요도'] = news_df_today['내용'].apply(get_importance)

    # 중요도 순서로 정렬
    news_df_yesterday = news_df_yesterday.sort_values(by='중요도')
    news_df_today = news_df_today.sort_values(by='중요도')

    # 중요도 컬럼 제거 (원하지 않으면)
    news_df_yesterday = news_df_yesterday.drop(columns=['중요도'])
    news_df_today = news_df_today.drop(columns=['중요도'])

    return news_df_yesterday, news_df_today

@st.cache_data
def load_orderlist_data():
    orderlist = get_dataframe_from_bigquery('mido_test', 'order_test')

    return orderlist

# @st.cache_data
# def load_region_geodata():
#     region_geodata = get_geodataframe_from_bigquery('mido_test', 'region_df')
#
#     return region_geodata
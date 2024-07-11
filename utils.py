# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import geopandas as gpd
import pandas_gbq
from datetime import datetime, timedelta
import pytz
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

def process_dataframe(df, columns_to_keep, columns_order, sort_by, ascending=True):
    # Drop columns not in the columns_to_keep list
    df = df[columns_to_keep]

    # Reorder the columns
    df = df[columns_order]

    # Sort the dataframe
    df = df.sort_values(by=sort_by, ascending=ascending)

    return df

def log_user_action(username, action, dataset_id, table_id):

    client = bigquery.Client(credentials=credentials)

    table_ref = f"{client.project}.{dataset_id}.{table_id}"

    # 현재 시각을 한국 시간으로 설정
    kst = pytz.timezone('Asia/Seoul')
    timestamp_now = datetime.now(kst).strftime('%Y-%m-%d %H:%M:%S')

    rows_to_insert = [
        {
            "username": username,
            "timestamp": timestamp_now,  # 문자열로 변환된 시각
            "action": action
        }
    ]

    errors = client.insert_rows_json(table_ref, rows_to_insert)
    if errors == []:
        print("New rows have been added.")
    else:
        print("Encountered errors while inserting rows: {}".format(errors))



@st.cache_data
def load_users_data():
    users = get_dataframe_from_bigquery('mido_test', 'users').sort_values(by='employeeNumber').reset_index(drop=True)
    users = users[['employeeName', 'jobTitle', 'password']]

    return users

@st.cache_data(ttl=3600)
def load_QWGJK_data():
    QWGJK_df_yesterday = get_dataframe_from_bigquery('mido_test', 'QWGJK_df_yesterday')
    QWGJK_df_today = get_dataframe_from_bigquery('mido_test', 'QWGJK_df_today')
    QWGJK_df_new = get_dataframe_from_bigquery('mido_test', 'QWGJK_df_new')

    QWGJK_df_yesterday['회계연도'] = pd.to_datetime(QWGJK_df_yesterday['회계연도'], format='%Y').dt.strftime('%Y')
    QWGJK_df_yesterday['집행일자'] = pd.to_datetime(QWGJK_df_yesterday['집행일자'], format='%Y%m%d').dt.strftime('%Y%m%d')
    QWGJK_df_today['회계연도'] = pd.to_datetime(QWGJK_df_today['회계연도'], format='%Y').dt.strftime('%Y')
    QWGJK_df_today['집행일자'] = pd.to_datetime(QWGJK_df_today['집행일자'], format='%Y%m%d').dt.strftime('%Y%m%d')
    QWGJK_df_new['회계연도'] = pd.to_datetime(QWGJK_df_new['회계연도'], format='%Y').dt.strftime('%Y')
    QWGJK_df_new['집행일자'] = pd.to_datetime(QWGJK_df_new['집행일자'], format='%Y%m%d').dt.strftime('%Y%m%d')

    columns_to_keep = ['집행일자', '지역명', '자치단체명', '세부사업명', '예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']
    columns_order = ['집행일자', '지역명', '자치단체명', '세부사업명', '예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']
    sort_by = ['세부사업명']

    QWGJK_df_yesterday = process_dataframe(QWGJK_df_yesterday, columns_to_keep, columns_order, sort_by)
    QWGJK_df_today = process_dataframe(QWGJK_df_today, columns_to_keep, columns_order, sort_by)

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
    QWGJK_df_new = QWGJK_df_new.sort_values(by='집행일자')


    # 중요도 컬럼 제거 (원하지 않으면)
    QWGJK_df_yesterday = QWGJK_df_yesterday.drop(columns=['중요도'])
    QWGJK_df_today = QWGJK_df_today.drop(columns=['중요도'])

    return QWGJK_df_yesterday, QWGJK_df_today, QWGJK_df_new

@st.cache_data(ttl=3600)
def load_dep_edu_data():
    dep_edu_df = get_dataframe_from_bigquery('mido_test', 'dep_edu_df')

    columns_to_keep = ['도광역시', '시군구', '구분', '과업명', '금액', '면적', '예산집행']
    columns_order = ['도광역시', '시군구', '구분', '과업명', '금액', '면적', '예산집행']
    sort_by = ['도광역시', '시군구']

    dep_edu_df = process_dataframe(dep_edu_df, columns_to_keep, columns_order, sort_by)

    return dep_edu_df

@st.cache_data(ttl=3600)
def load_bid_con_data():
    bir_con_df_yesterday = get_dataframe_from_bigquery('mido_test', 'bir_con_df_yesterday')
    bir_con_df_today = get_dataframe_from_bigquery('mido_test', 'bir_con_df_today')

    columns_to_keep = ['공고일', '지역', '발주처', '구분', '공고명', '업종', '분류']
    columns_order = ['공고일', '지역', '발주처', '구분', '공고명', '업종', '분류']
    sort_by = ['공고일']

    bir_con_df_yesterday = process_dataframe(bir_con_df_yesterday, columns_to_keep, columns_order, sort_by, False)
    bir_con_df_today = process_dataframe(bir_con_df_today, columns_to_keep, columns_order, sort_by, False)


    return bir_con_df_yesterday, bir_con_df_today

@st.cache_data(ttl=3600)
def load_bid_ser_data():
    bir_ser_df_yesterday = get_dataframe_from_bigquery('mido_test', 'bir_ser_df_yesterday')
    bir_ser_df_today = get_dataframe_from_bigquery('mido_test', 'bir_ser_df_today')

    columns_to_keep = ['공고일', '지역', '발주처', '구분', '공고명']
    columns_order = ['공고일', '지역', '발주처', '구분', '공고명']
    sort_by = ['공고일']

    bir_ser_df_yesterday = process_dataframe(bir_ser_df_yesterday, columns_to_keep, columns_order, sort_by, False)
    bir_ser_df_today = process_dataframe(bir_ser_df_today, columns_to_keep, columns_order, sort_by, False)

    return bir_ser_df_yesterday, bir_ser_df_today

@st.cache_data(ttl=3600)
def load_bid_pur_data():
    bir_pur_df_yesterday = get_dataframe_from_bigquery('mido_test', 'bir_pur_df_yesterday')
    bir_pur_df_today = get_dataframe_from_bigquery('mido_test', 'bir_pur_df_today')

    columns_to_keep = ['공고명', '업종', '분류']
    columns_order = ['공고명', '업종', '분류']
    sort_by = ['공고명']

    bir_pur_df_yesterday = process_dataframe(bir_pur_df_yesterday, columns_to_keep, columns_order, sort_by, False)
    bir_pur_df_today = process_dataframe(bir_pur_df_today, columns_to_keep, columns_order, sort_by, False)

    return bir_pur_df_yesterday, bir_pur_df_today

@st.cache_data(ttl=3600)
def load_nara_data():
    nara_df = get_dataframe_from_bigquery('mido_test', 'nara_df')

    # columns_to_keep = [
    #     '납품요구접수일자', '수요기관명', '납품요구건명', '업체명', '품목', '단가', '단위', '수량', '금액', '납품기한일자',
    #     '계약구분', '계약번호', '계약변경차수', '다수공급자계약여부', '우수제품여부', '최종납품요구여부', '최초납품요구접수일자',
    #     '납품요구수량', '납품요구금액', '수요기관지역명', '납품요구지청명'
    # ]
    # columns_order = [
    #     '납품요구접수일자', '수요기관명', '납품요구건명', '업체명', '품목', '단가', '단위', '수량', '금액', '납품기한일자',
    #     '계약구분', '계약번호', '계약변경차수', '다수공급자계약여부', '우수제품여부', '최종납품요구여부', '최초납품요구접수일자',
    #     '납품요구수량', '납품요구금액', '수요기관지역명', '납품요구지청명'
    # ]

    columns_to_keep = [
        '납품요구접수일자', '수요기관명', '납품요구건명', '업체명', '금액', '수량', '단위', '단가', '품목'
    ]
    columns_order = [
        '납품요구접수일자', '수요기관명', '납품요구건명', '업체명', '금액', '수량', '단위', '단가', '품목'
    ]
    sort_by = ['납품요구접수일자']

    nara_df = process_dataframe(nara_df, columns_to_keep, columns_order, sort_by, False)

    return nara_df

@st.cache_data(ttl=3600)
def load_news_data():
    news_df_yesterday = get_dataframe_from_bigquery('mido_test', 'news_df_yesterday').sort_values('기사날짜', ascending=False)
    news_df_today = get_dataframe_from_bigquery('mido_test', 'news_df_today').sort_values('기사날짜', ascending=False)

    # 키워드 중요도 리스트
    keywords = ['인조잔디','예산', '추경']
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


@st.cache_data(ttl=600)
def load_listup_data():
    remain_dep_edu_df = get_dataframe_from_bigquery('mido_test', 'remain_dep_edu_df')
    remain_QWGJK_df = get_dataframe_from_bigquery('mido_test', 'remain_QWGJK_df')

    remain_dep_edu_df = remain_dep_edu_df[['도광역시', '시군구', '구분', '과업명', '삭제', '금액', '면적', '예산집행']]
    remain_QWGJK_df = remain_QWGJK_df[['지역명', '자치단체명', '세부사업명', '삭제', '예산현액', '국비', '시도비', '시군구비', '기타', '지출액', '편성액']]

    remain_dep_edu_df = remain_dep_edu_df.sort_values(by=['도광역시', '시군구'])
    remain_QWGJK_df = remain_QWGJK_df.sort_values(by=['지역명', '자치단체명'])

    return remain_dep_edu_df, remain_QWGJK_df

# @st.cache_data
# def load_region_geodata():
#     region_geodata = get_geodataframe_from_bigquery('mido_test', 'region_df')
#
#     return region_geodata
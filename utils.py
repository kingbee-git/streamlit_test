# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import json
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

def load_data():
    orderlist = get_dataframe_from_bigquery('mido_test', 'order_test')

    return orderlist
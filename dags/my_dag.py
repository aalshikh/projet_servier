from airflow import DAG
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator

from random import randint
from datetime import datetime
import pandas as pd
import numpy as np



def _clean_drugs():
	df_drugs = pd.read_csv("drugs.csv", header=0, index_col=None, sep=',', encoding="utf-8")
	df_drugs.drop(5 , inplace=True)
	df_drugs.reset_index(inplace=True, drop=True)
	return randint(1, 10)
	
def _clean_clinical():
	df_clinical = pd.read_csv("clinical_trials.csv", header=0, index_col=None, sep=',',  encoding="utf-8")
	df_clinical['date'] = pd.to_datetime(df_clinical['date'].str.strip('"')).dt.strftime('%d/%m/%Y')
	df_clinical.drop(2 , inplace=True)
	df_clinical.reset_index(inplace=True, drop=True)
	df_clinical = df_clinical[df_clinical['id'].notna()]
	df_clinical.iloc[4, df_clinical.columns.get_loc('journal')] = 'Journal of emergency nursing'
	df_clinical.iloc[5, df_clinical.columns.get_loc('journal')] = 'Journal of emergency nursing'
	df_clinical.reset_index(inplace=True, drop=True)
	
	return randint(1, 10)
	
def _clean_pubmed():
	df_pubmed = pd.read_csv("pubmed.csv", header=0, index_col=None, sep=',')
	df_pubmed['date'] = pd.to_datetime(df_pubmed['date'].str.strip('"')).dt.strftime('%d/%m/%Y')
	return randint(1, 10)

def _create_graph_json():
	csv_cleaned = ti.xcom_pull(task_ids=[
		'first_csv',
		'second_csv',
		'third_csv'
	])
	return 'ok'



with DAG("my_dag", start_date=datetime(2021, 1, 1), schedule_interval="@daily", catchup=False) as dag:
	first_csv = PythonOperator(
		task_id="first_csv",
		python_callable=_clean_drugs
	)
	
	second_csv = PythonOperator(
		task_id="second_csv",
		python_callable=_clean_clinical
	)
	
	third_csv = PythonOperator(
		task_id="third_csv",
		python_callable=_clean_pubmed
	)
	
	create_graph_json = BranchPythonOperator(
		task_id="create_graph_json",
		python_callable=_create_graph_json
	)
	
	[first_csv, second_csv, third_csv] >> create_graph_json


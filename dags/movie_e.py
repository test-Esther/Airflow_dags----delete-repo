from datetime import datetime, timedelta
from textwrap import dedent
from pprint import pprint

# The DAG object; we'll need this to instantiate a DAG
from airflow import DAG

# Operators; we need this to operate!
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import (
    ExternalPythonOperator,
    PythonOperator,
    PythonVirtualenvOperator,
    is_venv_installed,
    BranchPythonOperator
)
import os

with DAG(
    'movie',
    # These args will get passed on to each operator
    # You can override them on a per-task basis during operator initialization
    default_args={
        'depends_on_past': False,
        'retries': 1,
        'retry_delay': timedelta(seconds=3)
    },
    max_active_runs=1,
    max_active_tasks=3,
    description='movie_db',
   # schedule_interval=timedelta(days=1),
    schedule="10 2 * * *",
    start_date=datetime(2024, 7, 24),
    catchup=True,
    tags=['movie', 'movie_db'],
) as dag:

    def branch():
        print(branch)


    def get():
        print(get)

    def fun_divide():
        print(divide)

    def save():
        print(save)

    branch_op = BranchPythonOperator(
	    task_id="branch.op",
    	python_callable=branch
    ) 


    get_data = PythonVirtualenvOperator(
        task_id="get.data",
        python_callable=get,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #venv_cache_path="/home/young12/tmp2/air_venv/get_data"
    )
    

    save_data = PythonVirtualenvOperator(
        task_id="save.data",
        python_callable=save,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #venv_cache_path="/home/young12/tmp2/air_venv/get_data"
    )


    multi_y = PythonVirtualenvOperator(
        task_id="multi_y",
        python_callable=fun_divide,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #op_kwargs={ 'url_param': {"multiMovieYn": "Y"}}
    )

    
    multi_n = PythonVirtualenvOperator(
        #task_id='multi.n',
        python_callable=fun_divide,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #op_kwargs={ 'url_param': {"multiMovieYn": "N"}}
    )

    nation_k = PythonVirtualenvOperator(
        task_id='nation.k',
        python_callable=fun_divide,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #op_kwargs={ 'url_param': {"repNationCd": "K"}}
    )

    nation_f = PythonVirtualenvOperator(
        task_id='nation.f',
        python_callable=fun_divide,
        system_site_packages=False,
        #requirements=["git+https://github.com/Nicou11/@/"],
        #op_kwargs={ 'url_param': {"repNationCd": "F"}}
    )


    rm_dir = BashOperator(
	    task_id='rm.dir',
        bash_command="echo rm_dir"
	    #bash_command='rm -rf ~/tmp/test_parquet/load_dt={{ ds_nodash }}'
    )


    echo_task = BashOperator(
            task_id='echo.task',
            bash_command="echo 'task'"
    )


    end  = EmptyOperator(task_id='end', trigger_rule="all_done")
    start  = EmptyOperator(task_id='start')

    throw_err  = BashOperator(
            task_id='throw.err',
            bash_command="exit 1",
            trigger_rule="all_done")
    
    get_start = EmptyOperator(task_id='get.start', trigger_rule="all_done")
    get_end = EmptyOperator(task_id='get.end')


    start >> branch_op
    start >> throw_err >> save_data

    branch_op >> echo_task
    branch_op >> rm_dir >> get_start
    branch_op >> get_start
    get_start >> [get_data, multi_y, multi_n, nation_k, nation_f] >> get_end
    
    get_end >> save_data >> end
    

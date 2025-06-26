from airflow.sdk import dag, task, Context
from typing import Dict, Any

@dag
def xcom_dog():

    @task
    def t1() -> Dict[str, Any]:
        my_val=42
        my_sentence="Hello, World"
        return {
            "my_sentence": my_sentence,
            "my_val": my_val
            }
        

    @task
    def t2(data: Dict[str, Any]):
        print(data['my_sentence'])
        print(+data['my_val'])

    val = t1() 
    t2(val)
xcom_dog()    
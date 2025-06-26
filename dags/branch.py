from airflow.sdk import dag, task

@dag
def branch():

    @task
    def a():
        return 1
    
    @task.branch
    def b(val: int):
        if val == 2:
            return "equal_1"
        return "not_equal_one"
        
    @task
    def equal_1(val: int):
        print(f"equal to {val}")

    @task
    def not_equal_one(val: int):
        print(f'not equal {val}')

    val = a()
    b(val) >> [equal_1(val), not_equal_one(val)]   

branch()
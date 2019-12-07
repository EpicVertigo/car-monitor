from carmonitor.celery import app


@app.task()
def monitor_query():
    print('It works!')

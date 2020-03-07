broker_url = 'redis://127.0.0.1:6379/5'
broker_poor_limit = 10

timezone = 'Asia/Shanghai'
accept_content = ['pickle', 'json']
task_serializer = 'pickle'

result_backend = 'redis://127.0.0.1:6379/5'
result_serializer = 'pickle'
result_chche_max = 10000
result_expires = 3600

worker_redirect_stdouts_level = 'INFO'

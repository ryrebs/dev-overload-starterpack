# Change this part <>
# bind = '127.0.0.1:8000'
bind = "unix:/yourpath/run/gunicorn.sock"
workers = 5
user = "web"
group = "users"

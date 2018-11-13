# from flask import Flask
# app = Flask(__name__)
#
# @app.route('/')
# def hello_world():
#     return 'Hello World!'
#
# if __name__ == '__main__':
#     app.run()


import psycopg2

conn = psycopg2.connect(database="postgres", user="scheduler", password="jerryyin", host="127.0.0.1", port="5432")

print(conn)
print("Opened database successfully")

# psql -U scheduler -d postgres -h 127.0.0.1 -W



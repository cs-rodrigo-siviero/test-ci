# from ddtrace import patch_all
# patch_all()
import time
import os
from flask import Flask
# from ddtrace import tracer
# from datadog import initialize, api
from random import randint
import logging
import mysql.connector

app = Flask(__name__)

FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger(__name__)
log.level = logging.INFO

options = {
    'api_key': os.environ['DD_API_KEY'],
}

# initialize(**options)

#Tagging

tags_blue = ["app:hello-python","route:blue"]
tags_green = ["app:hello-python","route:green"]

#@tracer.wrap()
def random_num():
    log.info('Def random')
    return randint(0, 10)

#@tracer.wrap()
def query_cloudsql(query):
    log.info('Querying cloudsql')
    cnx = mysql.connector.connect(user='root', password=os.environ['DB_PASS'],
                                host=os.environ['DB_HOST'],
                                database=os.environ['DB_SCHEMA'])
    cursor = cnx.cursor()
    cursor.execute(query)
    content = cursor.fetchall()
    cursor.close()
    cnx.close()
    return content

@app.route("/schema")
def cloudsql():
    query = ("show schemas;")
    return str(query_cloudsql(query))

@app.route("/loja_sp")
def loja_sp():
    query = ("select (CASE WHEN post_status = 'pla-active' THEN 1 ELSE 2 END)as post_status from facily_wp.wp_posts WHERE ID = '173538'")
    return str(query_cloudsql(query))

@app.route("/")
def hello():
    num = random_num()
    log.info('Rota Default')
    return str(random_num())


@app.route("/blue")
def blue():
    # response = api.Metric.send(
    #                             metric='hello-python-blue.datadog.metric',
    #                             points=[(int(time.time()), float(1))],
    #                             tags=tags_blue,
    #                             type='count'
    #                         )
    log.info('Rota Blue')
    return str(random_num())


@app.route("/green")
def green():
    # response = api.Metric.send(
    #                             metric='hello-python-green.datadog.metric',
    #                             points=[(int(time.time()), float(1))],
    #                             tags=tags_green,
    #                             type='count'
    #                         )
    log.info('Rota Green')
    return str(random_num())

if __name__ == "__main__":
    app.run(host='0.0.0.0')

from flask import Flask
import requests, random, os
from opencensus.ext.flask.flask_middleware import FlaskMiddleware
from opencensus.ext.stackdriver.trace_exporter import StackdriverExporter
from opencensus.trace import execution_context
from opencensus.trace.propagation import google_cloud_format
from opencensus.trace.samplers import AlwaysOnSampler

_url_productservice = os.environ.get("URL_PRODUCTSERVICE", default='http://localhost:8080/')

app = Flask(__name__)
propagator = google_cloud_format.GoogleCloudFormatPropagator()
def createMiddleWare(exporter):
    middleware = FlaskMiddleware(
        app,
        exporter=exporter,
        propagator=propagator,
        sampler=AlwaysOnSampler())
    return middleware

createMiddleWare(StackdriverExporter())

@app.route("/api/recommends", methods=['GET'])
def recommend():
  # make trace header
  trace_context_header = propagator.to_header(execution_context.get_opencensus_tracer().span_context)
  # 상품 목록을 조회한다.
  response = requests.get(_url_productservice + "/api/products")
  products = response.json()
  # 랜덤한 4개의 상품을 추천한다.
  recommendations = { 'recommendations': random.sample(products['products'], 4)}
  print("recommendations : {}".format(recommendations))
  return recommendations
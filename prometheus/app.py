import os

import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import PlainTextResponse
from prometheus_client import multiprocess, CollectorRegistry, CONTENT_TYPE_LATEST, generate_latest
from starlette.responses import Response

from prometheus.exceptions import exception_handler
from prometheus.models import RequestMetric, MethodMetric
from prometheus.src import build_request_history, build_method_metric, PrometheusExporter

os.environ["PROMETHEUS_MULTIPROC_DIR"] = "data"
os.makedirs("data", exist_ok=True)

app = FastAPI()

app.exception_handler(exception_handler)


@app.post("/track_request_metric", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def track_request_metric(metric: RequestMetric):
    build_request_history(metric)
    return


@app.post("/track_methods_metric", status_code=status.HTTP_200_OK, response_class=PlainTextResponse)
async def track_method_metric(metric: MethodMetric):
    build_method_metric(metric)
    return


@app.get("/metrics", status_code=status.HTTP_200_OK)
def metrics() -> Response:
    registry = CollectorRegistry()
    registry.register(PrometheusExporter())
    multiprocess.MultiProcessCollector(CollectorRegistry())
    return Response(generate_latest(registry), headers={"Content-Type": CONTENT_TYPE_LATEST})


if __name__ == '__main__':
    uvicorn.run("app:app", host="localhost", port=5555, reload=True, log_level="debug")

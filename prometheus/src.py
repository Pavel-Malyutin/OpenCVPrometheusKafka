import copy

from prometheus_client.core import CounterMetricFamily, HistogramMetricFamily

from prometheus.models import RequestMetric, MethodMetric


class PrometheusExporter:
    requests_count = {}
    requests_latency = {}
    methods_latency = {}
    buckets = {
        "0.1": 0,
        "0.5": 0,
        "1.5": 0,
        "2.5": 0,
        "5": 0,
        "10": 0,
        "20": 0,
    }

    def collect(self):
        requests_total = CounterMetricFamily(
            name="http_service_requests_total",
            documentation="Count of requests to endpoint",
            labels=["status"]
        )

        requests_latency = HistogramMetricFamily(
            name="http_service_latency",
            documentation="Service endpoints duration",
            labels=["status"]
        )

        methods_latency = HistogramMetricFamily(
            name="service_method_latency",
            documentation="Service methods duration",
            labels=["method"]
        )

        for status, count in self.requests_count.items():
            requests_total.add_metric([status], count)
        yield requests_total

        for endpoint, storage in self.requests_latency.items():
            requests_latency.add_metric([endpoint], list(storage["buckets"].items()), storage["sum"])
        yield requests_latency

        for method, storage in self.methods_latency.items():
            methods_latency.add_metric([method], list(storage["buckets"].items()), storage["sum"])
        yield methods_latency


def build_request_history(metric: RequestMetric):
    PrometheusExporter.requests_count[str(metric.status)] \
        = PrometheusExporter.requests_count.get(metric.status, 0) + 1
    endpoint_storage = PrometheusExporter.requests_latency.setdefault(metric.endpoint, {})
    buckets_storage = endpoint_storage.setdefault("buckets", copy.deepcopy(PrometheusExporter.buckets))
    for bucket in buckets_storage.keys():
        if metric.duration <= float(bucket):
            buckets_storage[bucket] += 1
    endpoint_storage["sum"] = endpoint_storage.get("sum", 0) + metric.duration
    print(metric)


def build_method_metric(metric: MethodMetric):
    methods_storage = PrometheusExporter.requests_latency.setdefault(metric.method, {})
    buckets_storage = methods_storage.setdefault("buckets", copy.deepcopy(PrometheusExporter.buckets))
    for bucket in buckets_storage.keys():
        if metric.duration <= float(bucket):
            buckets_storage[bucket] += 1
    methods_storage["sum"] = methods_storage.get("sum", 0) + metric.duration
    print(metric)

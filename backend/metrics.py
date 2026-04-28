from prometheus_client import Counter, Gauge

REQUESTS = Counter("requests_total", "Total API requests")
ERRORS = Counter("errors_total", "Total errors")
BIAS = Gauge("bias_score", "Bias score")


"""hello-api — the smallest honest production-shaped service.

Three endpoints, each existing for an operational reason:
  /         identity + version + hostname (rolling/canary demos read this)
  /healthz  liveness/readiness probe target (no auth, no dependencies)
  /metrics  Prometheus exposition (scraped via PodMonitor)
"""

import os
import socket

from fastapi import FastAPI
from prometheus_client import Counter, make_asgi_app

APP_VERSION = os.getenv("APP_VERSION", "dev")

app = FastAPI(title="hello-api", version=APP_VERSION)

REQUESTS = Counter("hello_requests_total", "Requests to /", ["path"])

# Prometheus exposition mounted as a sub-app: keeps /metrics out of
# FastAPI's routing/docs and uses the client library's own ASGI handler.
app.mount("/metrics", make_asgi_app())


@app.get("/")
def root() -> dict:
    REQUESTS.labels(path="/").inc()
    return {
        "service": "hello-api",
        "version": APP_VERSION,
        "host": socket.gethostname(),
    }


@app.get("/healthz")
def healthz() -> dict:
    # Deliberately dependency-free: a probe must answer even when
    # everything downstream is on fire, or restarts make outages worse.
    return {"status": "ok"}

# ============================================================================
# Multi-stage build — the two-stage split is THE Docker lesson here:
#   builder: has pip, compilers, caches — big, throwaway
#   runtime: only the installed packages + source — small, shippable
# Layer-order lesson: requirements.txt copied BEFORE app/ so code changes
# don't invalidate the (slow) dependency layer.
# ============================================================================
FROM python:3.12-slim AS builder
WORKDIR /build
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

FROM python:3.12-slim
# Non-root from the start (PSA `restricted` will demand this at Phase 9).
RUN useradd --uid 10001 --no-create-home appuser
COPY --from=builder /install /usr/local
WORKDIR /srv
COPY app/ app/
# Baked at build time by CI (--build-arg APP_VERSION=<git sha>); the /
# endpoint reports it — that's how rolling/canary demos are OBSERVED.
ARG APP_VERSION=dev
ENV APP_VERSION=${APP_VERSION}
USER 10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]

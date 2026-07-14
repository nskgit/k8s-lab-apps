# k8s-lab-apps — application monorepo

Application source for the k8s-lab cluster. **Public repo by design**
(locked decision D7): public repos get GitHub's free native
`ubuntu-24.04-arm` runners — real ARM builds for our ARM cluster, no QEMU.
No secrets ever live here; CI credentials are GitHub Actions secrets.

## The 3-repo boundary (who holds what power)

| Repo | Holds | Can touch |
|---|---|---|
| **k8s-lab-apps** (this, public) | service code, Dockerfiles, per-service CI | OCIR (push images), gitops repo (PR a tag bump) — never the cloud, never the cluster |
| k8s-lab-gitops (private) | desired state Argo reconciles | the cluster, via Argo pull |
| k8s-lab-infra (private) | Terraform + Ansible | the cloud + cluster substrate |

## Layout (monorepo, path-filtered CI)

```
services/<name>/        one service = one folder = one Dockerfile = one CI workflow
  app/                  source
  tests/                pytest
  Dockerfile            multi-stage, non-root, arm64
.github/workflows/      <name>-ci.yml, triggered only on paths: services/<name>/**
```

## Pipeline 2 (per service)

PR → ruff · pytest · gitleaks · docker build (NO push)
merge to main → buildx arm64 · tag = git SHA (immutable) · Trivy scan ·
push OCIR → bump `workloads/` image tag in k8s-lab-gitops via PR → Argo
deploys dev. Promotion/prod & rollback happen in the gitops repo only.

## Services

- `hello-api` — FastAPI demo service: `/` (identity+version — the canary
  demo readout), `/healthz` (probes), `/metrics` (Prometheus).

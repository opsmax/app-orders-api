# orders-api — IDP Reference Application

> A demo REST API that showcases the full Internal Developer Platform (IDP)
> workflow, from intent declaration to production deployment.

This repository follows the **"Option A: Monorepo"** pattern from the IDP
design — application source code and infrastructure intent live together in a
single repository.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Language | Python 3.12 |
| Framework | FastAPI |
| Database | PostgreSQL (optional — falls back to in-memory mock data) |
| Container | Docker multi-stage build |
| Tests | pytest + httpx |
| CI | GitHub Actions |

## Running Locally

```bash
# Install dependencies
pip install -r src/requirements.txt

# Start the server
uvicorn src.app.main:app --host 0.0.0.0 --port 8080 --reload

# Or run with Docker
docker build -t orders-api .
docker run -p 8080:8080 orders-api
```

The app starts immediately with mock data — no database required.
To connect to PostgreSQL, set `DATABASE_URL`:

```bash
export DATABASE_URL="postgresql://user:pass@localhost:5432/orders"
```

## API Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | App info and available endpoints |
| GET | `/health` | Health check with database status |
| GET | `/api/orders` | List all orders |
| GET | `/api/orders/{id}` | Get a single order |
| GET | `/api/stats` | Order statistics (revenue, top products) |
| GET | `/docs` | Interactive OpenAPI documentation |

## Running Tests

```bash
pip install pytest httpx
pytest tests/ -v
```

## How It Works

The IDP workflow is driven by a single file: **`infra/deploy.yaml`** (the
*intent contract*). Developers describe *what* the application needs; the
platform figures out *how* to deliver it.

```
┌─────────────────────────────────────────────────────────────────┐
│  Developer edits infra/deploy.yaml                              │
│       ↓                                                         │
│  Platform validates & resolves intent                           │
│       ↓                                                         │
│  Terragrunt configs generated → Azure resources provisioned     │
│       ↓                                                         │
│  Kustomize overlays generated → ArgoCD deploys to AKS           │
└─────────────────────────────────────────────────────────────────┘
```

### 1. Declare Intent

Edit `infra/deploy.yaml` to declare compute, data, networking, security, and
reliability requirements:

```yaml
apiVersion: idp.platform/v1
kind: ApplicationIntent
metadata:
  name: orders-api
  ownerTeam: commerce

spec:
  compute:
    platform: aks
    workloadType: web-api
  data:
    postgres:
      enabled: true
      tier: general-purpose-small
  security:
    complianceTier: standard
  reliability:
    slo: "99.9"
```

The contract is the **only** file a developer needs to touch. Everything
downstream is automated by the platform.

### 2. Platform Resolves Intent

On push / PR, the platform:

1. **Validates** the contract against a JSON Schema.
2. **Resolves** each field through a resolution table — mapping abstract
   intents (e.g. `tier: general-purpose-small`) to concrete Terraform
   variable values.
3. **Generates** Terragrunt live configs and Kustomize overlays.

### 3. Infrastructure Provisioning

Generated Terragrunt configurations are applied to provision Azure resources
(AKS namespaces, PostgreSQL Flexible Server, Key Vault secrets, etc.) using
Azure Verified Modules (AVM).

### 4. GitOps Deployment

Generated Kustomize overlays are committed and picked up by ArgoCD, which
deploys the application to the target AKS cluster.

## Repository Structure

```
app-orders-api/
├── src/
│   ├── app/
│   │   ├── main.py          # FastAPI application and routes
│   │   ├── models.py        # Pydantic response models
│   │   ├── database.py      # PostgreSQL connection (with fallback)
│   │   └── mock_data.py     # Mock order data
│   └── requirements.txt     # Python dependencies
├── tests/
│   ├── conftest.py          # Test fixtures
│   └── test_api.py          # API endpoint tests
├── infra/
│   ├── deploy.yaml          # Intent contract (the key interface)
│   ├── base/                # Kustomize base manifests
│   └── overlays/            # Per-environment overrides
├── Dockerfile               # Multi-stage production build
├── .github/workflows/       # CI/CD workflows
├── LICENSE
└── README.md
```

## License

[MIT](LICENSE) — Copyright 2025 opsmax

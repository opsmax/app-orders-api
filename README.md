# orders-api — IDP Reference Application

> A demo REST API that showcases the full Internal Developer Platform (IDP)
> workflow, from intent declaration to production deployment.

This repository follows the **"Option A: Monorepo"** pattern from the IDP
design — application source code and infrastructure intent live together in a
single repository.

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
├── infra/
│   ├── deploy.yaml              # Intent contract (the key interface)
│   ├── base/                    # Kustomize base manifests
│   └── overlays/
│       ├── dev/                 # Dev environment overrides
│       ├── uat/                 # UAT environment overrides
│       └── prod/                # Production environment overrides
├── src/                         # Application source code
├── tests/                       # Tests
├── .github/workflows/           # CI/CD workflows
├── LICENSE
└── README.md
```

### Kustomize Layout

The `infra/` directory uses the standard Kustomize pattern:

- **`base/`** — shared Kubernetes manifests (Deployment, Service, ConfigMap)
  that apply to every environment.
- **`overlays/{env}/`** — per-environment patches (replica counts, resource
  limits, environment variables, ingress rules).

ArgoCD points at each overlay directory to deploy the corresponding
environment.

## Getting Started

1. Clone this repository.
2. Edit `infra/deploy.yaml` to describe your application's requirements.
3. Open a PR — the platform will validate the contract and preview changes.
4. Merge — infrastructure is provisioned and the app is deployed automatically.

## License

[MIT](LICENSE) — Copyright 2025 opsmax

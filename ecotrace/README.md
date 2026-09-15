# EcoTrace
## AI-Powered E-Waste & Device Lifecycle Passport System

EcoTrace is a Django + SQLite sustainability prototype for the 1M1B – IBM SkillsBuild AI for Sustainability Virtual Internship. It is aligned with **UN SDG 12: Responsible Consumption and Production**.

### What it demonstrates

- Digital lifecycle passports for campus electronics
- Searchable/filterable hardware inventory
- IBM BOB-style AI orchestration layer
- Optional IBM Granite foundation-model inference through watsonx.ai
- Explainable repair / maintain / continue / recycle recommendations
- Predictive maintenance priority
- Sustainability impact logging
- Responsible AI governance: Fairness, Transparency, Privacy and Ethics
- Impact dashboard for carbon saved and e-waste diverted

### Architecture

`Django UI → Lifecycle View → IBMBOBAIEngine → IBM Granite / deterministic fallback → structured recommendation → ElectronicAsset + SustainabilityLog`

The local fallback is intentionally deterministic. It allows the project to run without IBM credentials while making it explicit in the UI that a real Granite deployment is an optional configured path.

### Quick start

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS/Linux:
# source .venv/bin/activate

pip install -r requirements.txt

copy .env.example .env
# macOS/Linux: cp .env.example .env

python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open http://127.0.0.1:8000/

Admin: http://127.0.0.1:8000/admin/

### IBM Granite setup

1. Create/configure a watsonx.ai project.
2. Obtain an IBM Cloud API key and project ID.
3. Put them in `.env`.
4. Set an available Granite model in `IBM_GRANITE_MODEL_ID`.
5. Restart Django.

If credentials are missing or the SDK/inference call fails, EcoTrace falls back to its local deterministic rules engine instead of claiming that a model was used.

### Important prototype note

The sustainability figures in this educational prototype are **illustrative impact estimates**, not measured lifecycle LCAs. For a production deployment, replace the fixed estimation values with campus-specific lifecycle/carbon datasets and validated e-waste weights.

### Production hardening checklist

- Use PostgreSQL instead of SQLite for multi-user production workloads.
- Put Django behind HTTPS and a production WSGI/ASGI server.
- Store secrets in a proper secret manager.
- Add authentication/authorization and audit trails.
- Add human approval before physical retirement/recycling.
- Add validated carbon/LCA factors.
- Add tests, CI, rate limiting and structured logging.
- Pin and regularly review dependency versions.

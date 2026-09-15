# EcoTrace 🌱

## AI-Powered E-Waste & Device Lifecycle Passport System

EcoTrace is a Django-based prototype for responsible electronic-device lifecycle management. It creates a digital lifecycle passport for each registered device and provides AI-assisted decision support for whether a device should be **continued, maintained, repaired, or recycled**.

The project is aligned with **UN Sustainable Development Goal 12 (SDG 12): Responsible Consumption and Production** and was developed as part of the **1M1B – IBM SkillsBuild AI for Sustainability Virtual Internship**.

---

## 🎯 Problem Statement

Organizations often manage large numbers of electronic devices without a structured and transparent way to decide what should happen to aging equipment.

This can lead to:

- Premature replacement of usable devices
- Unnecessary electronic waste
- Poor visibility into device lifecycle history
- Inconsistent maintenance and repair decisions
- Limited traceability of end-of-life decisions

EcoTrace addresses this by creating a traceable lifecycle record for every device and using AI-assisted analysis to support more informed lifecycle decisions.

---

## 💡 Solution

EcoTrace provides a **Digital Lifecycle Passport** for each electronic asset.

Users can register a device with information such as:

- Device name
- Device type
- Purchase date
- Condition score
- Operational status

The system then generates a lifecycle assessment with:

- Lifecycle recommendation
- Diagnosis
- Maintenance priority
- Rationale
- Confidence information
- AI model/source information

Supported lifecycle recommendations are:

**CONTINUE → MAINTAIN → REPAIR → RECYCLE**

The recommendation is presented as **decision support, not an autonomous decision**. A human remains responsible for the final operational decision.

---

## 🤖 AI & IBM Integration

### IBM BOB

**IBM BOB** was incorporated during the development of EcoTrace.

BOB was used to:

- Support project ideation and planning
- Analyze the actual EcoTrace codebase
- Assist with implementation of the Lifecycle Passport
- Support human-oversight and audit-trail improvements
- Assist with development and testing

### IBM Granite & watsonx.ai

The application architecture provides an optional pathway for **IBM Granite foundation-model inference through IBM watsonx.ai** when live credentials are configured.

For the current prototype demonstration, the default recommendation pathway uses the **EcoTrace deterministic local fallback / Rules Engine** when live model credentials are not configured.

This distinction is intentionally documented so that the prototype does not overclaim live foundation-model inference.

---

## 🧠 How EcoTrace Works

```text
Register Electronic Device
          ↓
Collect Lifecycle Information
          ↓
AI-Assisted Lifecycle Assessment
          ↓
Continue / Maintain / Repair / Recycle
          ↓
Explain Recommendation
          ↓
Human Review & Decision
          ↓
Audit Trail
          ↓
Sustainability Tracking
```

---

## 📋 Digital Lifecycle Passport

Each device has a dedicated lifecycle passport containing:

- Device identity
- Device type
- Purchase date
- Condition score
- Operational status
- AI recommendation
- Recommendation rationale
- AI source/model information
- Sustainability information
- Lifecycle/audit history

This creates a single traceable record for lifecycle management.

---

## 👤 Human-in-the-Loop

EcoTrace is designed around human oversight.

The system does **not** make autonomous operational decisions.

Instead:

> **AI recommends. Humans remain accountable.**

Users can review an AI recommendation and update the operational status of an asset when real-world circumstances require a different decision.

Human status changes are recorded in the lifecycle log, providing an audit trail.

---

## 🛡️ Responsible AI

Responsible AI principles are integrated into the prototype through:

### Fairness
Recommendations are based on defined device lifecycle inputs rather than arbitrary user characteristics.

### Transparency
The system shows the recommendation, rationale, confidence information, and AI source/model information. The prototype also clearly distinguishes its local fallback from optional live Granite inference.

### Privacy
Secrets and API credentials are kept outside the public source code through environment variables. `.env` files are excluded from version control.

### Ethics
AI is used as decision support rather than replacing human accountability. Users can review and override operational decisions.

---

## 🌱 SDG 12 Alignment

EcoTrace supports **UN SDG 12: Responsible Consumption and Production** by encouraging:

- Longer useful lifetimes for electronic devices
- Maintenance before unnecessary replacement
- Repair and reuse where appropriate
- Responsible recycling at end of life
- Better lifecycle traceability
- More transparent sustainability decisions

---

## 📊 Sustainability Metrics

The dashboard includes prototype indicators such as:

- Carbon savings from device life extension
- Electronic waste diverted from disposal

**Important:** The current prototype uses illustrative estimates for demonstration purposes. These figures are not presented as measured lifecycle-assessment results.

A production implementation could replace these estimates with organization-specific lifecycle-assessment data and verified environmental factors.

---

## 🖥️ Technology Stack

- **Python 3.11+**
- **Django 5.2**
- **SQLite**
- **HTML5**
- **CSS / Tailwind CSS**
- **JavaScript**
- **Django ORM**
- **IBM BOB**
- **IBM watsonx.ai SDK**
- **IBM Granite Models** — optional live inference pathway
- **Prompt Engineering**
- **AI Decision-Support Workflow**
- **Human-in-the-Loop**
- **Responsible AI**

---

## 📁 Project Structure

```text
ecotrace/
├── manage.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── TESTING.md
│
├── ecotrace/
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── ...
│
└── lifecycle/
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    ├── tests.py
    ├── ai_engine.py
    ├── templates/
    └── ...
```

---

## ⚙️ Setup

### 1. Clone the repository

```bash
git clone https://github.com/ashutosh-sahoo-dev/EcoTrace.git
cd EcoTrace/ecotrace
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

macOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure environment variables

Copy `.env.example` to `.env`.

Windows:

```powershell
Copy-Item .env.example .env
```

macOS/Linux:

```bash
cp .env.example .env
```

Add IBM watsonx.ai credentials only if you want to configure the optional live Granite pathway.

**Never commit `.env` or API credentials to GitHub.**

### 5. Apply migrations

```bash
python manage.py migrate
```

### 6. Start the development server

```bash
python manage.py runserver
```

Then open:

```text
http://127.0.0.1:8000/
```

---

## 🧪 Testing

Run the Django test suite with:

```bash
python manage.py test
```

The project includes tests covering the lifecycle passport, AI recommendation display, human oversight, operational-status updates, audit logging, and invalid status handling.

See **[TESTING.md](TESTING.md)** for testing details.

---

## 🔐 Security Notes

This repository is intended to contain source code and project documentation, not secrets.

- `.env` is excluded from Git
- API credentials should be stored in environment variables
- `.env.example` contains placeholders only
- Virtual environments and Python cache files are excluded
- Do not place passwords, API keys, or access tokens in source files or comments

---

## 🚀 Future Improvements

Potential future development includes:

- Live IBM Granite inference through watsonx.ai
- More detailed device health and maintenance history
- Evidence-based sustainability factors
- Organization-level analytics
- Device import and bulk asset management
- Role-based access control
- Production database deployment
- Cloud hosting for the Django application
- More comprehensive lifecycle prediction models

---

## 👥 Target Users

EcoTrace is designed for:

- IT asset managers
- Sustainability officers
- Educational institutions
- Operations teams
- Procurement teams
- Auditors and compliance teams

---

## 🎓 Internship Context

**Program:** 1M1B – IBM SkillsBuild AI for Sustainability Virtual Internship

**Project:** EcoTrace

**SDG:** UN SDG 12 — Responsible Consumption and Production

The project demonstrates how AI-assisted decision support can be combined with lifecycle tracking, human oversight, auditability, and sustainability metrics to encourage responsible electronic-device management.

---

## 📌 Prototype Disclaimer

EcoTrace is an educational internship prototype.

AI recommendations are intended as **decision support** and should be reviewed by an appropriate human decision-maker. The sustainability metrics shown in the prototype are illustrative estimates and should not be interpreted as independently verified environmental measurements.

---

## 🌍 Project Goal

**Every device has a lifecycle. Make it count.**

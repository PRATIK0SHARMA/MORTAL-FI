# 💳 MORTAL-FI

### AI-Powered Financial Reconciliation & Exception Resolution System

> **Reconcile transactions. Detect financial exceptions. Reason safely. Resolve low-risk cases autonomously. Escalate risky cases. Verify every autonomous action.**

---

## 📌 Overview

Financial reconciliation systems must compare large volumes of orders, payments, and settlement records to determine whether money has moved correctly.

Traditional reconciliation workflows are often heavily rule-based and require manual investigation whenever records do not match exactly.

**MORTAL-FI** is an AI-assisted financial reconciliation and exception-resolution system designed to automate this workflow safely.

The system:

- ingests and normalizes financial transaction data,
- reconciles orders, payments, and settlements,
- detects financial exceptions,
- performs deterministic financial reasoning,
- uses AI to assist exception analysis,
- evaluates financial risk and guardrails,
- autonomously resolves only validated low-risk cases,
- escalates high-risk cases for human review,
- independently verifies autonomous executions,
- and maintains an end-to-end audit trail.

The key principle behind MORTAL-FI is simple:

> **AI may assist financial reasoning, but it should never receive unrestricted authority to execute financial operations.**

---

# 🏗️ System Architecture

MORTAL-FI combines deterministic financial reconciliation, AI-assisted reasoning, risk-based guardrails, controlled execution, and independent post-execution verification.

![MORTAL-FI System Architecture](docs/images/mortal_fi_architecture.png)

---

# 🎯 Problem Statement

Payment systems process transactions across multiple stages:

```text
Customer
   ↓
Order
   ↓
Payment
   ↓
Settlement
   ↓
Merchant
```

Records generated at these stages may not always match perfectly.

Common reconciliation problems include:

- duplicate payments,
- missing orders,
- missing settlements,
- incorrect transaction amounts,
- mismatched reference IDs,
- delayed or incomplete settlement records.

Traditional systems can detect many of these problems using rules, but exception investigation and resolution often require significant manual effort.

Using an LLM alone for this process creates another problem:

> **AI-generated reasoning is probabilistic and should not directly control financial actions.**

MORTAL-FI therefore combines:

**deterministic reconciliation + AI reasoning + financial guardrails + controlled execution + independent verification.**

---

# 💡 Our Solution

MORTAL-FI implements an end-to-end financial exception-management pipeline.

```text
Orders + Payments + Settlements
              │
              ▼
      ETL & Data Validation
              │
              ▼
      Reconciliation Engine
              │
              ▼
       Exception Detection
              │
              ▼
 Deterministic Financial Reasoning
              │
              ▼
        AI Reasoning Agent
              │
              ▼
      Risk + Guardrail Layer
              │
              ▼
       Resolution Decision
          ┌────┴────┐
          │         │
          ▼         ▼
    AUTO_RESOLVE  ESCALATE
          │         │
          ▼         ▼
 Controlled       Human
 Execution        Review
          │
          ▼
 Post-Execution Verification
          │
          ▼
 Audit + Metrics + Dashboard
```

This architecture allows AI to contribute useful reasoning without making it the sole authority over financial operations.

---

# 🛡️ Safety-First AI Architecture

The most important design decision in MORTAL-FI is the separation between:

1. **AI reasoning**
2. **financial decision authority**
3. **financial execution**

An AI response alone can never authorize an autonomous resolution.

A transaction can reach autonomous resolution only when multiple conditions agree:

```text
Valid AI Response
        +
Deterministic Financial Validation
        +
LOW Financial Risk
        +
No Blocking Guardrail
        ↓
   AUTO_RESOLVE
```

If these conditions are not satisfied:

```text
Unsafe / Uncertain Condition
            ↓
       DO NOT EXECUTE
            ↓
 Human Review / Escalation
```

This creates a safety boundary between probabilistic AI reasoning and deterministic financial operations.

> **MORTAL-FI does not give an LLM unrestricted control over financial operations. AI assists with reasoning, while deterministic financial validation and guardrails determine whether an action is safe to execute. Every autonomous execution is independently verified afterward.**

---

# ⚙️ System Architecture

MORTAL-FI consists of several specialized layers.

## 1. Data Layer

The system works with three primary financial datasets:

```text
Orders
Payments
Settlements
```

Raw records pass through an ETL pipeline before reconciliation.

The ETL layer handles:

- schema normalization,
- datatype conversion,
- missing-value validation,
- transaction-field validation,
- standardized processed datasets,
- ETL audit reporting.

---

## 2. Reconciliation Engine

The reconciliation engine compares payment activity against order and settlement records.

The pipeline performs:

```text
Payment
   ↓
Order Validation
   ↓
Duplicate Detection
   ↓
Exact Settlement Matching
   ↓
Reference Recovery
   ↓
Amount Validation
   ↓
Final Reconciliation Status
```

The reconciliation engine is deterministic.

AI is **not required** to determine whether the fundamental financial records match.

---

## 3. Exception Detection

MORTAL-FI currently detects five financial exception categories.

| Exception | Meaning |
|---|---|
| `DUPLICATE_PAYMENT` | Multiple payment records represent a duplicate transaction |
| `AMOUNT_MISMATCH` | Payment and settlement amounts do not match |
| `MISSING_SETTLEMENT` | A valid payment does not have the expected settlement |
| `REFERENCE_MISMATCH` | Settlement exists but the reference identifier differs |
| `MISSING_ORDER` | Payment references an order that cannot be found |

These exceptions are passed to the resolution pipeline for further investigation.

---

## 4. Deterministic Financial Reasoner

Before AI reasoning is trusted, MORTAL-FI evaluates deterministic financial evidence.

This includes information such as:

- payment existence,
- order existence,
- settlement existence,
- duplicate status,
- payment amount,
- settlement amount,
- recovered reference information,
- exception type,
- financial risk.

This gives the system a deterministic evidence layer independent of the AI model.

---

## 5. AI Reasoning Agent

The AI reasoning layer receives structured exception context rather than unrestricted raw financial control.

Its role is to help answer questions such as:

- What likely caused this exception?
- Does the available evidence support a safe resolution?
- What action would be appropriate?
- Should the case be escalated?

The AI response is validated before it can influence the final resolution decision.

AI reasoning therefore acts as a **decision-support layer**, not an unrestricted financial executor.

---

## 6. Resolution Agent

The Resolution Agent combines:

```text
Exception Context
       +
Deterministic Reasoning
       +
AI Reasoning
       +
Financial Risk
       +
Guardrails
       ↓
Final Resolution Decision
```

Possible outcomes include:

```text
AUTO_RESOLVE
ESCALATE
REVIEW_REQUIRED
MANUAL_REVIEW_REQUIRED
```

Only validated low-risk cases are eligible for autonomous execution.

---

# 🔒 Guardrails

Guardrails prevent unsafe AI decisions from becoming financial actions.

The system validates conditions including:

- AI response validity,
- deterministic evidence,
- financial risk level,
- exception type,
- allowed resolution action,
- amount consistency,
- settlement existence,
- execution eligibility.

The safety model ensures:

```text
Invalid AI response
        ↓
Never Auto-Resolve

Guardrail violation
        ↓
Never Auto-Resolve

High financial risk
        ↓
Escalate

Validated low-risk case
        ↓
Eligible for Auto-Resolution
```

---

# ⚡ Controlled Resolution Execution

MORTAL-FI includes a controlled execution layer.

The currently supported safe autonomous action is:

```text
LINK_RECOVERED_SETTLEMENT
```

Before executing the action, the system validates:

- settlement exists,
- payment exists,
- payment amount is available,
- settlement gross amount is available,
- payment and settlement amounts match.

Only after these validations pass can the action be executed.

---

# 🔁 Idempotent Financial Execution

Financial systems must be safe during retries.

A network retry, service restart, or repeated agent execution should not perform the same financial operation twice.

MORTAL-FI therefore implements idempotent execution.

First execution:

```text
EXECUTED
```

Repeated attempt:

```text
ALREADY_EXECUTED
```

The second request is recognized without repeating the underlying financial action.

This protects the system from duplicate execution during retry scenarios.

---

# ✅ Post-Execution Verification

Autonomous execution is not considered sufficient proof of success.

After execution, MORTAL-FI independently verifies the resulting financial relationship.

```text
Resolution Decision
        ↓
Execution
        ↓
Independent Verification
        ↓
VERIFIED / FAILED
```

Verification checks that the payment and recovered settlement remain financially consistent.

This creates a closed-loop autonomous workflow:

```text
Detect
  ↓
Reason
  ↓
Decide
  ↓
Execute
  ↓
Verify
  ↓
Audit
```

---

# 📊 Validated Results

The final MORTAL-FI system was tested against **103 payment transactions**.

## Reconciliation Results

| Metric | Result |
|---|---:|
| Total Payments | 103 |
| Automatically Matched | 80 |
| Exceptions Detected | 23 |
| Match Rate | 77.67% |

### Exception Distribution

| Exception Type | Count |
|---|---:|
| `DUPLICATE_PAYMENT` | 6 |
| `AMOUNT_MISMATCH` | 5 |
| `MISSING_SETTLEMENT` | 5 |
| `REFERENCE_MISMATCH` | 4 |
| `MISSING_ORDER` | 3 |
| **Total** | **23** |

---

## AI Agent Results

| Metric | Result |
|---|---:|
| Total Exceptions Investigated | 23 |
| Autonomous Resolutions | 4 |
| Escalations | 19 |
| Manual Reviews | 19 |
| Auto-Resolution Rate | 17.39% |
| Escalation Rate | 82.61% |
| Average AI Confidence | 93.39% |
| Low-Risk Exceptions | 4 |
| High-Risk Exceptions | 19 |

A high escalation rate is intentional in this prototype.

MORTAL-FI optimizes for **safe autonomous resolution**, not maximum autonomous resolution.

---

## Execution & Verification Results

| Metric | Result |
|---|---:|
| Successful Unique Executions | 4 |
| Verified Autonomous Resolutions | 4 |
| Verification Rate | **100%** |
| Duplicate Actual Executions During Retry Testing | **0** |

### Final Result

> **103 transactions processed → 80 automatically matched → 23 exceptions detected → 4 safe exceptions autonomously resolved → 19 high-risk cases escalated → 100% of autonomous resolutions verified → zero duplicate financial executions during retry testing.**

---

# 🧪 Final System Validation

MORTAL-FI includes an automated end-to-end validation suite.

The final validation covered:

- API service health,
- reconciliation totals,
- exception distribution,
- AI decision consistency,
- financial risk controls,
- human-review enforcement,
- AI-response validity,
- guardrail enforcement,
- execution validation,
- execution idempotency,
- post-execution verification,
- agent-performance metrics,
- pipeline completeness,
- payment-ID consistency.

Final result:

```text
Total Tests: 57
Passed:      57
Failed:      0

MORTAL-FI FINAL SYSTEM VALIDATION PASSED
```

Run the validation suite with:

```bash
python -m src.validation.final_testing
```

---

# 🧠 Example Autonomous Resolution

One of the golden-path transactions is:

```text
Payment ID:       PAY0092
Settlement ID:    SET0092
Amount:           ₹799
Exception:        REFERENCE_MISMATCH
Financial Risk:   LOW
```

The system determines that the settlement can be safely recovered using deterministic evidence.

The resulting lifecycle is:

```text
PAY0092
   ↓
REFERENCE_MISMATCH detected
   ↓
Deterministic settlement recovery
   ↓
AI-assisted reasoning
   ↓
LOW financial risk
   ↓
Guardrails passed
   ↓
AUTO_RESOLVE
   ↓
LINK_RECOVERED_SETTLEMENT
   ↓
EXECUTED
   ↓
VERIFIED
```

If the same execution is attempted again:

```text
ALREADY_EXECUTED
```

No duplicate financial operation occurs.

---

# 🖥️ Dashboard

MORTAL-FI includes an interactive Streamlit dashboard for operational monitoring and investigation.

The dashboard contains six major views.

### 🏠 Overview

Displays:

- reconciliation KPIs,
- exception statistics,
- AI-agent performance,
- execution performance,
- verification metrics,
- processing status.

### 🚨 Exceptions

Allows operators to:

- inspect detected exceptions,
- filter by exception type,
- search payment IDs,
- search order IDs.

### 🔍 Investigation

Provides transaction-level explainability including:

- financial evidence,
- deterministic reasoning,
- AI reasoning,
- financial risk,
- guardrail status,
- recommended action,
- final agent decision.

### ⚙️ Execution

Displays:

- execution history,
- execution status,
- validation results,
- idempotent retry events,
- verification results,
- resolution lifecycle.

### 📋 Audit & Explainability

Provides traceability across:

```text
Reconciliation
    ↓
AI Analysis
    ↓
Agent Decision
    ↓
Execution
    ↓
Verification
```

### 🎬 Demo Mode

Provides a simplified end-to-end transaction walkthrough designed for demonstrating MORTAL-FI's autonomous resolution pipeline.

---

# 🔌 REST API

MORTAL-FI exposes system information through FastAPI.

Interactive API documentation is available while the backend is running at:

```text
http://127.0.0.1:8000/docs
```

Important endpoints include:

| Endpoint | Purpose |
|---|---|
| `/` | API health / project information |
| `/metrics` | Core system metrics |
| `/dashboard/kpis` | Dashboard KPI data |
| `/reconciliation` | Reconciliation results |
| `/exceptions` | Detected financial exceptions |
| `/exceptions/{payment_id}` | Transaction-specific exception |
| `/analytics/exceptions` | Exception analytics |
| `/analytics/processing-status` | Pipeline processing status |
| `/ai/resolutions` | AI resolution results |
| `/ai/agent-decisions` | Final agent decisions |
| `/ai/agent-decisions/{payment_id}` | Transaction-level AI decision |
| `/analytics/ai` | AI analytics |
| `/execution/audit` | Resolution execution history |
| `/execution/verification` | Verification history |
| `/analytics/agent-performance` | Resolution-agent metrics |
| `/audit` | End-to-end audit records |

---

# 🛠️ Technology Stack

## Backend

- **Python**
- **FastAPI**
- **Uvicorn**
- **Pandas**

## AI / Decision Layer

- AI-assisted exception reasoning
- deterministic financial reasoning
- risk-based resolution logic
- financial guardrails
- structured AI-response validation

## Frontend

- **Streamlit**
- **Plotly**
- **Pandas**
- **Requests**

## Data

- CSV-based prototype datasets
- synthetic financial transaction data
- append-only execution and verification audit records

## Testing

- automated end-to-end validation suite
- API health testing
- financial consistency testing
- guardrail testing
- idempotency testing
- post-execution verification testing

---

# 📁 Project Structure

```text
MORTAL-FI/
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── reconciliation/
│   ├── ai_resolution/
│   ├── ai_agent/
│   ├── execution/
│   ├── audit/
│   ├── metrics/
│   └── dashboard/
│
├── src/
│   │
│   ├── data/
│   │   └── ETL and data-loading modules
│   │
│   ├── reconciliation/
│   │   ├── reconciliation_engine.py
│   │   ├── duplicate_detector.py
│   │   └── reference_matcher.py
│   │
│   ├── agents/
│   │   ├── context_builder.py
│   │   ├── financial_reasoner.py
│   │   ├── ai_reasoning_agent.py
│   │   ├── resolution_agent.py
│   │   ├── resolution_executor.py
│   │   ├── post_execution_verifier.py
│   │   └── agents_performance.py
│   │
│   ├── api/
│   │   └── app.py
│   │
│   └── validation/
│       └── final_testing.py
│
├── frontend/
│   └── dashboard/
│       └── app.py
│
├── requirements.txt
├── README.md
└── .gitignore
```

---

# 🚀 Installation

## 1. Clone the Repository

```bash
git clone <YOUR-REPOSITORY-URL>
cd MORTAL-FI
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv MORTAL-F
MORTAL-F\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv MORTAL-F
source MORTAL-F/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running MORTAL-FI

The dashboard and API run as separate services.

## Terminal 1 — Start FastAPI

From the project root:

```bash
uvicorn src.api.app:app --reload
```

The backend will be available at:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

## Terminal 2 — Start Streamlit

Open another terminal from the project root:

```bash
streamlit run frontend/dashboard/app.py
```

The dashboard will normally open at:

```text
http://localhost:8501
```

---

# 🧪 Running Post-Execution Verification

To independently verify autonomous executions:

```bash
python -m src.agents.post_execution_verifier
```

Verification records are stored in:

```text
data/execution/verification_audit.csv
```

---

# 📈 Running Agent Performance Analysis

```bash
python -m src.agents.agents_performance
```

This calculates metrics including:

- autonomous resolution rate,
- escalation rate,
- AI confidence,
- financial-risk distribution,
- successful executions,
- verified resolutions,
- verification rate.

---

# 🔍 Running Final Validation

Make sure FastAPI and Streamlit are running.

Then execute:

```bash
python -m src.validation.final_testing
```

Expected final result:

```text
Total Tests: 57
Passed:      57
Failed:      0

MORTAL-FI FINAL SYSTEM VALIDATION PASSED
```

---

# 🗂️ Auditability

Financial automation requires traceability.

MORTAL-FI records evidence across the full pipeline.

Important audit datasets include:

```text
data/audit/end_to_end_audit_trail.csv
data/execution/execution_audit.csv
data/execution/verification_audit.csv
```

This makes it possible to reconstruct:

```text
What happened?
      ↓
Why was it considered an exception?
      ↓
What evidence was available?
      ↓
What did the AI reason?
      ↓
What did deterministic logic conclude?
      ↓
What decision was made?
      ↓
Was an action executed?
      ↓
Was that action independently verified?
```

---

# 🆚 Why MORTAL-FI Is Different

A naive AI financial agent could operate like this:

```text
Transaction
    ↓
LLM
    ↓
Financial Action
```

That architecture creates unnecessary financial risk.

MORTAL-FI instead uses:

```text
Transaction
      ↓
Deterministic Reconciliation
      ↓
Exception Detection
      ↓
Deterministic Evidence
      +
AI Reasoning
      ↓
Financial Risk Assessment
      ↓
Guardrails
      ↓
Controlled Decision
      ↓
Validated Execution
      ↓
Independent Verification
      ↓
Audit Trail
```

The objective is therefore not:

> **“How many financial exceptions can AI automatically resolve?”**

It is:

> **“How many financial exceptions can be resolved autonomously without compromising financial safety?”**

---

# ⚠️ Current Prototype Limitations

MORTAL-FI is currently a hackathon prototype and not a production payment-processing system.

Current limitations include:

- synthetic financial datasets,
- CSV-based storage,
- a limited set of exception categories,
- one intentionally narrow autonomous financial resolution action,
- local API/dashboard deployment,
- no direct production payment-gateway integration,
- no distributed transaction-processing infrastructure,
- no enterprise authentication or authorization layer.

These limitations are deliberate: the prototype focuses on proving the architecture and safety model before expanding autonomous financial capabilities.

---

# 🔮 Future Scope

The architecture can be extended toward production-scale financial operations.

Potential improvements include:

### Real-Time Event Processing

Replace batch CSV processing with event-driven transaction ingestion.

```text
Payment Event
     ↓
Message Queue / Event Stream
     ↓
Real-Time Reconciliation
```

### Production Databases

Move audit, reconciliation, and execution state into transactional databases.

### Expanded Exception Resolution

Safely support additional exception categories after defining deterministic validation and guardrails for each action.

### Human-in-the-Loop Operations

Add reviewer workflows where operators can:

- approve,
- reject,
- modify,
- comment on,
- or investigate escalated resolutions.

### Feedback-Based AI Improvement

Human-review outcomes can become structured feedback for improving future exception reasoning.

### Enterprise Security

Introduce:

- authentication,
- role-based access control,
- approval policies,
- encrypted secrets,
- immutable audit infrastructure.

### Payment Infrastructure Integration

Integrate the reconciliation pipeline with real payment-gateway, order-management, and settlement APIs.

---

# 🏆 Core Engineering Principles

MORTAL-FI was designed around five principles:

**1. Deterministic logic before AI**

Core financial truth should come from financial records and deterministic validation.

**2. AI assists reasoning**

AI helps understand exceptions but does not receive unrestricted financial authority.

**3. Risk determines autonomy**

Low-risk validated cases may be automated. High-risk cases are escalated.

**4. Execution must be idempotent**

Retries must never create duplicate financial operations.

**5. Execution must be verified**

An autonomous action is not considered successful until its financial result is independently checked.

---

# 🎬 Recommended Demo Flow

For a live demonstration:

### 1. Open Overview

Show:

```text
103 Payments
80 Matched
23 Exceptions
4 Autonomous Resolutions
19 Escalations
100% Verification Rate
```

### 2. Open Exceptions

Show the different exception categories detected by the reconciliation engine.

### 3. Investigate `PAY0092`

Explain:

```text
REFERENCE_MISMATCH
        ↓
Recovered Settlement
        ↓
Amount Validation
        ↓
LOW Risk
        ↓
AI + Deterministic Evidence
        ↓
AUTO_RESOLVE
```

### 4. Show Execution

Display:

```text
LINK_RECOVERED_SETTLEMENT
        ↓
EXECUTED
```

Then highlight idempotency:

```text
Repeated execution
        ↓
ALREADY_EXECUTED
```

### 5. Show Verification

```text
PAY0092
   ↓
VERIFIED
```

### 6. Show a High-Risk Exception

Demonstrate that high-risk financial cases are **escalated rather than automatically executed**.

This demonstrates that MORTAL-FI is not simply an AI chatbot around financial data—it is a controlled financial decision and execution pipeline.

---

# 📌 Final Outcome

MORTAL-FI demonstrates that autonomous AI can be introduced into financial reconciliation without giving probabilistic models unrestricted financial control.

The prototype successfully combines:

```text
Reconciliation
     +
Exception Detection
     +
Deterministic Financial Reasoning
     +
AI Reasoning
     +
Risk Assessment
     +
Guardrails
     +
Controlled Execution
     +
Idempotency
     +
Independent Verification
     +
Auditability
```

into a single end-to-end system.

### Validated Prototype Result

**103 transactions processed.  
80 automatically matched.  
23 financial exceptions detected.  
4 low-risk exceptions autonomously resolved.  
19 high-risk cases safely escalated.  
100% of autonomous resolutions independently verified.  
0 duplicate financial executions during retry testing.  
57/57 final system validation tests passed.**

---

## 💳 MORTAL-FI

**AI-Powered Financial Reconciliation & Exception Resolution System**

> **Autonomy where it is safe. Human oversight where it matters.**
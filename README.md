# Email Agent

Automated email processing pipeline for B2B sales teams.
Reads incoming emails from Outlook, classifies intent with GPT-4o mini, decides the next best action using a rules engine, checks compliance, writes a personalized reply, sends it, and logs the activity in Dynamics 365 CRM — all in one API call.

<img width="1000" height="1914" alt="AutoSalesInbox_project_structure_v2(1)" src="https://github.com/user-attachments/assets/a518dad1-1c9a-4d07-b7d8-08c33be22d66" />
---

## Architecture

```
Dynamics 365 CRM  →  FastAPI Gateway  →  LangGraph Orchestrator
                                                  |
                          ┌───────────────────────┼───────────────────────┐
                          ▼                       ▼                       ▼
                    Email Reader         Intent Agent             Decision Agent
                    (Graph API)          (GPT-4o mini)            (Python rules)
                                                  |
                                         Compliance Agent
                                                  |
                                          Email Writer
                                          (GPT-4o mini)
                                                  |
                              ┌───────────────────┴──────────────┐
                              ▼                                   ▼
                    Graph Mail API                        CRM Activity Log
                    (send reply)                          (Dynamics 365)
```

**Flow for each incoming email:**

1. **Email Reader** — fetches the email from Outlook and the lead record from CRM
2. **Intent Agent** — classifies intent: `positive` | `neutral` | `negative` | `no_reply`
3. **Decision Agent** — applies rules to pick `reply` | `schedule` | `no_action`
4. **Compliance Agent** — checks opt-out flags and email frequency limits
5. **Email Writer** — generates a personalized reply draft with GPT-4o mini
6. **Execute** — sends the email and logs the activity in CRM

---

## Prerequisites

- Python 3.12+
- Docker Desktop (for Docker setup)
- An Azure account with:
  - Azure OpenAI resource (GPT-4o mini deployment)
  - Microsoft 365 app registration (Graph API access)
  - Dynamics 365 / CRM instance
  - Azure Service Bus namespace (optional for queue features)

---

## Local Setup (without Docker)

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/agent-email.git
cd agent-email

# 2. Create and activate a virtual environment
python -m venv .venv
.venv\Scripts\Activate.ps1        # Windows PowerShell
# source .venv/bin/activate       # Mac / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment variables
copy .env.example .env            # Windows
# cp .env.example .env            # Mac / Linux
# Then open .env and fill in your credentials

# 5. Run
python main.py
```

Server starts at `http://localhost:8000`.
Interactive API docs at `http://localhost:8000/docs`.

---

## Local Setup (with Docker)

```bash
# 1. Fill in your credentials
copy .env.example .env

# 2. Build and start
docker compose up --build
```

The app mounts your local folder as a volume so code changes reload automatically without rebuilding the image.

---

## Environment Variables

Copy `.env.example` to `.env` and fill in these values:

| Variable | What it is |
|---|---|
| `AZURE_OPENAI_ENDPOINT` | Your Azure OpenAI resource URL |
| `AZURE_OPENAI_API_KEY` | API key from Azure portal |
| `AZURE_OPENAI_DEPLOYMENT_NAME` | Name of your GPT-4o mini deployment |
| `GRAPH_CLIENT_ID` | App registration client ID |
| `GRAPH_CLIENT_SECRET` | App registration client secret |
| `GRAPH_TENANT_ID` | Your Microsoft 365 tenant ID |
| `CRM_BASE_URL` | Dynamics 365 org URL (e.g. `https://org.crm.dynamics.com`) |
| `CRM_CLIENT_ID` | CRM app registration client ID |
| `CRM_CLIENT_SECRET` | CRM app registration client secret |
| `CRM_TENANT_ID` | CRM tenant ID |
| `SERVICE_BUS_CONNECTION_STRING` | Azure Service Bus connection string |
| `LOG_LEVEL` | `INFO` or `DEBUG` |

---

## API

### `POST /api/v1/process-email`

Runs the full pipeline for one email.

**Request body:**
```json
{
  "email_id": "AAMkAGI...",
  "user_id": "seller@company.com",
  "lead_id": "a1b2c3d4-0000-0000-0000-000000000000"
}
```

**Response:**
```json
{
  "email_id": "AAMkAGI...",
  "intent": "positive",
  "next_action": "reply",
  "compliance_approved": true,
  "draft_reply": "Hi John, great to hear from you...",
  "actions_taken": ["email_sent", "crm_logged"],
  "error": null
}
```

### `GET /api/v1/health`

Returns `{"status": "ok"}`. Use this to check the service is running.

---

## Running Tests

```bash
# Install dev dependencies
pip install -r requirements.txt -r requirements-dev.txt

# Run all tests
pytest

# Run only unit tests
pytest tests/unit

# Run with output
pytest -v
```

Unit tests mock all external calls (LLM, Graph API, CRM) so they run without real credentials.

---

## Project Structure

```
agent-email/
├── main.py                        # entry point
├── requirements.txt               # runtime dependencies
├── requirements-dev.txt           # test dependencies
├── Dockerfile
├── docker-compose.yml
│
├── config/
│   └── settings.py                # all env vars loaded here via pydantic-settings
│
├── api/
│   ├── models.py                  # request / response schemas
│   └── routes.py                  # FastAPI endpoints
│
├── orchestrator/
│   ├── state.py                   # LangGraph shared state definition
│   └── graph.py                   # state machine wiring all agents together
│
├── agents/
│   ├── email_reader/              # fetches email + lead from external APIs
│   ├── intent_agent/              # GPT-4o mini → positive/neutral/negative/no_reply
│   ├── decision_agent/            # Python rules → reply/schedule/no_action
│   ├── compliance_agent/          # opt-out + frequency checks
│   └── email_writer/              # GPT-4o mini → personalized reply draft
│
├── services/
│   ├── auth.py                    # shared OAuth2 token helper
│   ├── graph_mail/                # Microsoft Graph Mail API client
│   ├── graph_calendar/            # Microsoft Graph Calendar API client
│   ├── crm/                       # Dynamics 365 client
│   └── service_bus/               # Azure Service Bus client
│
└── tests/
    ├── conftest.py                # shared fixtures
    ├── unit/                      # fast tests, no external calls
    └── integration/               # API tests with mocked graph
```

---

## What is NOT pushed to GitHub

- `.env` — your credentials and secrets
- `.venv/` — Python virtual environment
- `__pycache__/` — compiled bytecode
- `*.log` — runtime logs
- `.coverage` / `htmlcov/` — test coverage reports




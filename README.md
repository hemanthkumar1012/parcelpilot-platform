# ParcelPilot Platform

ParcelPilot is a modern logistics and shipment tracking platform built with FastAPI, PostgreSQL, and Vanilla JS. It features a built-in AI customer support assistant and comprehensive SLA management for logistics operators.

## Features

- **End-to-End Shipment Tracking:** Monitor shipments from origin to destination with real-time status updates.
- **SLA & Support Management:** Track support tickets, carrier faults, and SLA violations internally.
- **AI-Powered Customer Support:** Includes an integrated OpenAI-powered assistant that can lookup shipments, verify SLA policies, and prepare ticket escalations automatically.
- **Secure Architecture:** JWT authentication, strict tenant isolation via account IDs, and a safe read-only "Guest Mode" for demonstrations.

## Tech Stack

- **Backend:** Python 3.10+, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL (defaults to SQLite for local development)
- **Frontend:** HTML, CSS, Vanilla JS (No build step required)
- **AI Integration:** OpenAI Python SDK

## Project Structure

```text
parcelpilot-platform/
├── app/
│   ├── api/          # FastAPI routes
│   ├── core/         # Config, security, and dependencies
│   ├── db/           # SQLAlchemy models
│   ├── schemas/      # Pydantic models
│   ├── services/     # Business logic
│   └── tools/        # Tools exposed to the LLM
├── alembic/          # Database migrations
├── frontend/         # Static web assets
├── scripts/          # Database seeding
└── tests/            # Pytest test suite
```

## Quick Start

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hemanthkumar1012/parcelpilot-platform.git
   cd parcelpilot-platform
   ```

2. **Configure environment:**
   ```bash
   cp .env.example .env
   ```
   Add your `OPENAI_API_KEY` to the `.env` file. You can also specify a custom `DATABASE_URL` if you want to use PostgreSQL instead of the default SQLite.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize database & seed demo data:**
   ```bash
   alembic upgrade head
   python scripts/seed_demo.py
   ```
   *Note: `seed_demo.py` will generate realistic sample shipments and support tickets for testing.*

5. **Run the development server:**
   ```bash
   uvicorn app.main:app --reload
   ```
   The dashboard will be available at `http://localhost:8000`. 
   API documentation is available at `http://localhost:8000/docs`.

## Testing

Run the test suite using `pytest`:

```bash
# Run local tests (SQLite memory DB)
pytest --ignore=tests/test_postgres_integration.py

# Run integration tests against a live PostgreSQL database
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/testdb pytest tests/test_postgres_integration.py
```

## AI Agent Safety

The integrated AI assistant is designed with strict security boundaries:
- **No Direct Writes:** The LLM cannot modify application state directly. State changes (like escalating tickets) are generated as `pending` actions that a human user must confirm.
- **Enforced Isolation:** Authorization (e.g., checking `account_id`) is handled at the database execution layer, not by the LLM. The AI only has access to records owned by the authenticated user.
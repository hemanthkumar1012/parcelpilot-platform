# ParcelPilot Platform

ParcelPilot Platform is a unified logistics and shipment tracking system with an integrated AI customer support assistant. Built with FastAPI and PostgreSQL, it provides a robust API for managing shipments, orders, and support tickets, along with a Vanilla JS frontend dashboard.

## Overview

ParcelPilot manages the entire lifecycle of a shipment, from creation to delivery. It includes:
- **Shipment Tracking:** Customers can track shipments, monitor statuses (e.g., pending, in_transit, delivered), and view historical tracking events.
- **Support & SLA Management:** Customers and admins can manage support tickets, track SLA violations, and monitor carrier faults.
- **AI Customer Support:** An integrated AI assistant that helps customers track their shipments, check SLAs, and prepare escalations automatically using the OpenAI API.
- **Authentication & Guest Access:** Secure JWT-based authentication with strict tenant isolation, plus a robust "Continue as Guest" mode providing access to demo data without risking private customer data.

## Technology Stack

- **Backend:** Python, FastAPI, SQLAlchemy, Alembic
- **Database:** PostgreSQL (with SQLite fallback for local testing)
- **Frontend:** Vanilla HTML/CSS/JavaScript (No frameworks, lightweight)
- **AI Integration:** OpenAI Python SDK (function calling for tools)

## Project Structure

```
parcelpilot-platform/
├── app/
│   ├── api/          # FastAPI routers and endpoints (v1)
│   ├── core/         # Security, JWT, config, middleware
│   ├── db/           # SQLAlchemy models and database setup
│   ├── schemas/      # Pydantic validation schemas
│   ├── services/     # Business logic and AI orchestration
│   └── tools/        # Tools exposed to the AI agent
├── alembic/          # Database migrations
├── data/             # SLA and Policy PDF knowledge base
├── frontend/         # Static HTML/JS/CSS assets
├── scripts/          # Database seeding scripts
└── tests/            # Pytest test suite
```

## Local Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/hemanthkumar1012/parcelpilot-platform.git
   cd parcelpilot-platform
   ```

2. **Environment Variables:**
   Copy the example config and fill in your keys:
   ```bash
   cp .env.example .env
   ```
   *Required variables:*
   - `OPENAI_API_KEY`: Required for the AI chat assistant.
   - `SECRET_KEY`: Used for JWT signing.
   - `DATABASE_URL`: Your PostgreSQL connection string. (Defaults to `sqlite:///./test.db` if omitted for testing).

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Initialize the Database:**
   If using SQLite, the tables are auto-created. For PostgreSQL, run Alembic migrations:
   ```bash
   alembic upgrade head
   ```

5. **Seed Demo Data:**
   To populate the database with demo accounts, shipments, and support tickets (useful for guest mode):
   ```bash
   python -m scripts.seed_ai_data
   ```

6. **Start the Application:**
   ```bash
   uvicorn app.main:app --reload
   ```
   Navigate to `http://localhost:8000` to view the frontend dashboard.
   Navigate to `http://localhost:8000/docs` to view the Swagger API documentation.

## Testing

The project uses `pytest`. Tests can run against an isolated SQLite memory database or a real PostgreSQL instance.

```bash
# Run the fast test suite (SQLite)
pytest --ignore=tests/test_postgres_integration.py

# Run integration tests (Requires PostgreSQL)
TEST_DATABASE_URL=postgresql://user:password@localhost:5432/testdb pytest tests/test_postgres_integration.py
```

## AI Provider Configuration

The AI assistant uses the `openai` Python package. It expects `OPENAI_API_KEY` in the environment. Tools are securely sandboxed: the backend strictly enforces that users (or guests) can only lookup and interact with data they own (`current_user.account_id`). The AI agent does not make authorization decisions.

## Security Considerations

- **Tenant Isolation:** All database queries implicitly filter by the authenticated user's account ID.
- **Guest Restrictions:** Guests cannot perform state-changing mutations (e.g., escalating support tickets).
- **Tool Validation:** The AI tool dispatch layer catches malformed tool arguments safely.

## Security & Agent Safety Design

The platform ensures strict boundary isolation between the LLM logic and application state:

- **Staged-Confirmation Flow:** The AI is strictly barred from modifying sensitive entities directly. Instead, when an LLM requests a state change (like escalating a ticket), it invokes `prepare_escalation` in `app/tools/agent_tools.py`. This generates a secure `pending` record in the `agent_actions` table. A human user must explicitly submit a subsequent `confirm_action` call to formally execute it.
- **Tenant Isolation Enforcement:** The LLM does NOT manage authorization parameters (e.g., `account_id`). When the AI attempts to lookup data, the `_is_authorized` fallback in `app/tools/agent_tools.py` intercepts the retrieved record. It enforces that `current_user.account_id` matching rules apply explicitly at the backend execution layer before passing any data back to the LLM context.
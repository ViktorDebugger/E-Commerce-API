# E-Commerce API

A practice e-commerce API (based on the [roadmap.sh E-Commerce API](https://roadmap.sh/projects/ecommerce-api) project spec): JWT authentication, a product catalog with admin-only management, a shopping cart, and Stripe-powered checkout with webhook-confirmed payments.

## Tech stack

- FastAPI + SQLAlchemy 2.0 + Alembic (migrations)
- PostgreSQL
- JWT auth (`pyjwt` + `bcrypt`)
- Stripe (PaymentIntents + webhooks)
- `uv` for Python dependency management
- `pytest` + `pytest-cov` for testing
- Docker Compose (Postgres + API, orchestrated together)
- GitHub Actions CI

## Project structure

```
.
├── docker-compose.yml
├── .github/workflows/          # CI
│
├── app/main.py                 # FastAPI app, router registration
├── api/
│   ├── deps.py                 # auth dependencies (get_current_user, admin gate)
│   └── routes/                 # auth, products, cart, checkout, orders, webhooks, health
├── core/                       # config (Settings) + security (hashing, JWT)
├── db/                         # SQLAlchemy engine/session, declarative Base
├── models/                     # User, Product, Cart, CartItem, Order, OrderItem
├── schemas/                    # Pydantic request/response schemas
├── alembic/                    # migrations
├── scripts/
│   ├── init-test-db.sql        # auto-creates the test DB on first Postgres init
│   └── seed.py                 # seeds sample products + an admin user
├── tests/                      # pytest suite (one file per route module)
├── Dockerfile
└── pyproject.toml
```

## Installation

**Prerequisites:** Docker Desktop (or Docker Engine + Compose).

1. Clone the repo, then copy the env template:
   ```
   cp .env.example .env
   ```
2. Fill in the required values in `.env`:
   - `SECRET_KEY` — any random string (generate one: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `STRIPE_SECRET_KEY` / `STRIPE_WEBHOOK_SECRET` — see [Stripe setup](#stripe-setup) below
3. Start everything from the project root:
   ```
   docker compose up --build
   ```
4. Run migrations (first time only, or after pulling new migrations):
   ```
   docker compose exec app alembic upgrade head
   ```
5. (Optional) Seed sample data — see [Scripts](#scripts) below.

API + docs are now running at http://localhost:8000/docs.

**Changed a dependency** (`uv add ...`)? Rebuild instead of just restarting, and force-recreate anonymous volumes so stale installed packages don't linger:
```
docker compose up --build -V
```

## Stripe setup

This project uses Stripe's **test mode** — no real payments, no real card required.

1. Create a free Stripe account (or use an existing one) and switch to **Test mode**.
2. Dashboard → Developers → API keys → copy the **Secret key** (`sk_test_...`) into `.env`'s `STRIPE_SECRET_KEY`.
3. **Webhooks (local dev)** — Stripe can't reach `localhost` directly, so use the [Stripe CLI](https://docs.stripe.com/stripe-cli) to forward events:
   ```
   stripe listen --forward-to localhost:8000/webhooks/stripe --api-key sk_test_...
   ```
   Copy the `whsec_...` it prints into `.env`'s `STRIPE_WEBHOOK_SECRET`, then:
   ```
   docker compose up -d --force-recreate app
   ```
   Leave `stripe listen` running in its own terminal — it must be active for orders to actually flip to `"paid"`.
4. **Test the full flow via Swagger** (`/docs`): sign up → log in → add a product to cart → `POST /checkout` → copy the returned `client_secret`'s PaymentIntent id → confirm it with Stripe's test card via the CLI:
   ```
   stripe payment_intents confirm pi_... --payment-method pm_card_visa --api-key sk_test_...
   ```

## Scripts

| Script | Purpose | Run with |
|---|---|---|
| `scripts/init-test-db.sql` | Auto-creates the `ecommerce_test` database on Postgres's first init. Runs automatically — nothing to invoke manually. | — |
| `scripts/seed.py` | Seeds 5 sample products + an admin user (`admin@example.com` / `adminpass123`). Idempotent — safe to re-run. | `docker compose exec app python -m scripts.seed` |
| Alembic migrations | Create/apply schema changes. | `docker compose exec app alembic revision --autogenerate -m "..."` then `docker compose exec app alembic upgrade head` |

## Testing

Tests run on the **host** (not inside Docker — the container's image intentionally excludes dev dependencies to stay production-lean), against a dedicated `ecommerce_test` database reachable via `localhost:5432` (Docker's Postgres port is exposed to the host).

```
uv sync                    # installs dev deps (pytest, httpx, pytest-cov) locally, once
uv run pytest -v
```

The suite is integration-style: `tests/conftest.py` spins up a `TestClient` wired to the real FastAPI app, with `Depends(get_db)` overridden to point at the isolated test database (tables created fresh and dropped after every test). External calls to Stripe are mocked (`unittest.mock.patch`) rather than hitting the real API.

## Coverage

```
uv run pytest --cov=. --cov-report=term-missing
```

For a browsable, file-by-file report:
```
uv run pytest --cov=. --cov-report=html:.coverage_data/htmlcov
start .coverage_data/htmlcov/index.html
```

For inline gutters in VS Code, install the **Coverage Gutters** extension and generate the Cobertura XML format instead:
```
uv run pytest --cov=. --cov-report=xml:.coverage_data/coverage.xml
```
(Both report types can be generated in the same run by passing `--cov-report` twice.)

## CI

`.github/workflows/test.yml` runs the test suite on every push/PR:
- Spins up an ephemeral Postgres service container (never touches real data)
- Installs dependencies via `uv sync` (with dependency caching keyed on `uv.lock`)
- Runs `pytest -v` with dummy `SECRET_KEY`/`STRIPE_*` env vars (sufficient since Stripe calls are mocked in tests, not real)

No deploy pipeline is wired up — this project doesn't have a hosting target yet. If one is added later, it should be a separate job gated on this test job succeeding (`needs: test`), not bundled into the same workflow.

# IntelliRisk — Dengue Risk Monitoring (ESP32 + Flask + MySQL + MQTT)

IntelliRisk is an end-to-end IoT monitoring system designed to collect environmental data (e.g., temperature and humidity), publish telemetry via MQTT, persist readings in a relational database, and provide a web interface for real-time monitoring and interaction.

This repository is organized using a Flask **application factory** pattern with separated web routes, MQTT handlers, and error handlers to improve maintainability and clarity.

> **Note:** Setup and execution instructions are intentionally omitted.

---

## What problem does it solve?

Dengue risk is influenced by environmental conditions. IntelliRisk supports monitoring these conditions by:
- collecting sensor measurements from an IoT device (ESP32),
- persisting historical readings and actuator events,
- presenting real-time values in a web dashboard,
- enabling remote interactions via MQTT topics (e.g., LED control).

---

## Key features

- **Real-time telemetry**
  - Subscribes to MQTT topics and updates in-memory state for live visualization.
- **Persistent history**
  - Saves sensor readings and actuator messages to a database for later analysis.
- **Role-based access**
  - Pages such as admin and publishing dashboards depend on the user role.
- **End-to-end workflow**
  - IoT device → MQTT broker → Flask backend → database → web UI.

---

## System overview

High-level architecture:

1. **ESP32 + sensors** publish measurements to MQTT topics.
2. **MQTT broker** routes messages.
3. **Flask backend** subscribes to topics, decodes payloads, and persists readings.
4. **Database (MySQL via SQLAlchemy)** stores reads/writes and application data.
5. **Web UI** renders dashboards for monitoring and interaction.

---

## Application structure (refactored)

The project follows a modular Flask layout:

- `app/__init__.py` — application factory (`create_app`) and blueprint/handler registration
- `app/extensions.py` — shared Flask extensions (database, login manager, MQTT client)
- `app/web/routes.py` — web routes (dashboards and actions)
- `app/mqtt_handlers.py` — MQTT connect/message handlers (subscription + persistence + state updates)
- `app/error_handlers.py` — centralized HTTP error handlers
- `app/state.py` — in-memory state (`dengue_values`) used for real-time dashboard rendering
- `controllers/` — feature blueprints (auth, users, sensors, reads/writes, etc.)
- `models/` — SQLAlchemy models and persistence helpers
- `views/` — HTML templates
- `static/` — frontend assets
- `docs/` — diagrams and database artifacts (optional)

---

## Web routes (high level)

The web layer provides:
- `/` — home page
- `/login` — login page
- `/adm` — admin dashboard (role-aware)
- `/publish` — publishing/actions page (role-aware)
- `/tempo_real` — real-time dashboard, displaying current values from `dengue_values`
- `/publish_message` — publishes a `{topic, message}` payload to MQTT and records the event
- `/desligar_led` — publishes an "off" command to the actuator topic

---

## MQTT topics (example)

Common topics used by the system include:
- `dengue1`
- `dengue2`
- `dengue3`
- `topico_led`

The MQTT handler:
- subscribes to the topics on connect,
- decodes payloads,
- persists reads/writes,
- updates `dengue_values` for real-time rendering.

> If you standardize payload formats, document `topic → payload type → meaning` here.

---

## Data model (high level)

The system persists:
- **Sensor readings** (topic, timestamp, value, metadata)
- **Actuator events** (topic, timestamp, command/value)
- **Users and roles** (role-based access control)

If you have schema diagrams or SQL exports, place them under `docs/` and reference them here.

---

## Security and configuration notes

- Avoid committing secrets (credentials, tokens, real passwords).
- Keep environment-specific settings outside source code (e.g., via environment variables).
- Database initialization scripts should avoid destructive operations by default (e.g., avoid dropping all tables unless explicitly required).

---

## Roadmap (suggested)

- Add automated tests for core services (topic parsing, persistence, role access)
- Add CI checks (lint + tests)
- Standardize configuration management (environment variables)
- Add short architectural diagrams under `docs/`
- Improve documentation for payload formats and error handling


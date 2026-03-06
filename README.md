# EcoCleanUp

Community cleanup management system for COMP639 project.

## Features

**Volunteer**
- Browse and register for cleanup events
- View participation history
- Submit feedback for attended events
- Login reminders for upcoming events

**Event Leader**
- Create and manage cleanup events
- Track volunteer attendance
- Record event outcomes (bags collected, attendees, etc.)
- View volunteer feedback

**Admin**
- Manage user accounts (activate/deactivate)
- View platform statistics and reports

## Test Accounts

| Role | Username | Password |
|------|----------|----------|
| Volunteer | rudyard | Rudyardpass |
| Event Leader | philip | Philippass |
| Admin | admin01Tanya | Abcd1234 |

## Setup

1. Clone the repository
2. Create virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate` (Mac) or `venv\Scripts\activate` (Windows)
4. Install requirements: `pip install -r requirements.txt`
5. Create PostgreSQL database using `create_myecu_database.sql`
6. Populate with test data using `populate_database.sql`
7. Update database credentials in `loginapp/connect.py`
8. Run: `python run.py`

## GenAI Acknowledgement

This project used the following tools during development (February-March 2026):
- **GitHub Copilot** - Code completion during development 
- **ChatGPT** - Debugging help and code examples
- **generatedata.com** -  Generated test data

Examples of prompts used:
- "Generate 20 New Zealand names, addresses and phone numbers for database test data"
- "Getting KeyError 0 when accessing cursor.fetchone() in Flask with PostgreSQL. How to fix?"
- "List index error in Jinja2 template when displaying query results - template shows 4 items but query returns 2"
- "How to check for overlapping event registrations in SQL for a Flask app"
- "Debug: volunteer history count mismatch between page and database"
# 🤖 University Transport Chatbot

> **An AI-powered Rasa chatbot built as a Final Year Project (FYP) for NUML University, Islamabad.** It provides real-time university transport information by querying a MySQL database — including bus routes, driver details, schedules, and student assignments.

![Python](https://img.shields.io/badge/Python-3.8-blue?logo=python&logoColor=white)
![Rasa](https://img.shields.io/badge/Rasa-3.6.21-5A17EE?logo=rasa&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-8.0-4479A1?logo=mysql&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?logo=docker&logoColor=white)

---

## 📋 Table of Contents

- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [Database Schema](#-database-schema)
- [Getting Started](#-getting-started)
- [Usage](#-usage)
- [NLU Pipeline](#-nlu-pipeline)
- [Custom Actions](#-custom-actions)
- [Deployment](#-deployment)
- [Tech Stack](#-tech-stack)
- [Contributing](#-contributing)
- [License](#-license)

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🚌 **Route Lookup** | Get detailed information about any bus route by route number |
| 👤 **Student Route Finder** | Find your assigned route by providing your student ID |
| 🧑‍✈️ **Driver Information** | View driver name and contact details for any route |
| ⏰ **Schedule & Timing** | Check bus departure and arrival times for each route |
| 📊 **Route Statistics** | View student count, bus number, and shift details |
| 📋 **Student Lists** | List all students assigned to a specific route |
| 🛡️ **Error Handling** | Graceful handling of invalid student IDs, route numbers, and database errors |
| 💬 **Natural Conversation** | Supports greetings, thank you, clarifications, and goodbyes |

---

## 🏗️ Architecture

```
┌──────────────────┐     REST API      ┌──────────────────┐
│                  │ ◄──────────────── │                  │
│   Frontend /     │                   │   Rasa Server    │
│   Chat Client    │ ────────────────► │   (Port 5005)    │
│                  │                   │                  │
└──────────────────┘                   └────────┬─────────┘
                                                │
                                       Webhook  │
                                                ▼
                                       ┌──────────────────┐
                                       │  Rasa Action     │
                                       │  Server          │
                                       │  (Port 5055)     │
                                       └────────┬─────────┘
                                                │
                                       MySQL    │  Connector
                                                ▼
                                       ┌──────────────────┐
                                       │  MySQL 8.0       │
                                       │  Database        │
                                       │  (Port 3306)     │
                                       │                  │
                                       │  transport_      │
                                       │  management      │
                                       └──────────────────┘
```

---

## 📁 Project Structure

```
university-transport-chatbot/
├── .rasa/                        # Rasa cache and global config
├── data/
│   ├── nlu.yml                   # NLU training data (intents & entities)
│   └── stories.yml               # Conversation stories for training
├── models/                       # Trained Rasa model files (.tar.gz)
├── __pycache__/                  # Python bytecode cache
│
├── actions.py                    # Custom Rasa actions (DB queries)
├── config.yml                    # Rasa NLU pipeline & policy configuration
├── domain.yml                    # Intents, entities, slots, responses & actions
├── endpoints.yml                 # Action server endpoint config
├── nlu.yml                       # Additional NLU training examples
├── stories.yml                   # Additional conversation stories
│
├── database_config.py            # MySQL connection configuration
├── create_tables.sql             # Database schema (DDL)
├── import_data.py                # Import data into MySQL
├── import_excel_to_mysql.py      # Import Excel spreadsheets to MySQL
├── fix_database.py               # Database repair/migration utility
├── setup_routes.py               # Route setup script
├── map_students_to_routes.py     # Map students to their routes
│
├── Dockerfile                    # Docker image for Rasa server
├── requirements.txt              # Python dependencies
├── runtime.txt                   # Python runtime version (3.8.16)
├── .gitignore                    # Git ignore rules
├── .gitattributes                # Git LFS tracking for model files
└── README.md                     # Project documentation
```

---

## 🗄️ Database Schema

The chatbot uses a `transport_management` MySQL database with the following schema:

```
┌────────────────┐       ┌────────────────┐
│    routes       │       │    drivers      │
├────────────────┤       ├────────────────┤
│ id (PK)        │◄──┐   │ id (PK)        │
│ route_number   │   │   │ name           │
│ route_shift    │   │   │ contact_number │
│ bus_number     │   └───│ route_id (FK)  │
│ start_time     │       └────────────────┘
│ end_time       │
└───────┬────────┘
        │
        │  ┌──────────────────┐      ┌────────────────┐
        │  │  student_routes   │      │    students     │
        │  ├──────────────────┤      ├────────────────┤
        └──│ route_id (FK)    │      │ id (PK)        │
           │ student_id (FK)  │──────│ system_id      │
           │ id (PK)          │      │ name           │
           └──────────────────┘      │ semester       │
                                     └────────────────┘
```

| Table | Description |
|-------|-------------|
| `routes` | Bus routes with shift, bus number, and timings |
| `drivers` | Driver names and contact info linked to routes |
| `students` | Student records with university system IDs |
| `student_routes` | Many-to-many mapping of students to routes |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.8.x** (required by Rasa 3.6)
- **MySQL 8.0** (local or remote)
- **Docker** (optional, for containerized deployment)

### 1. Clone the Repository

```bash
git clone https://github.com/Ahmedimtiaz-github/university-transport-chatbot.git
cd university-transport-chatbot
```

### 2. Install Dependencies

```bash
pip install rasa==3.6.21
pip install -r requirements.txt
```

### 3. Set Up the Database

```bash
# Create the database schema
mysql -u root -p < create_tables.sql

# Import data from Excel (if available)
python import_excel_to_mysql.py

# Or import data directly
python import_data.py

# Map students to routes
python map_students_to_routes.py
```

### 4. Configure Database Connection

Edit `database_config.py` with your MySQL credentials:

```python
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'your_password',
    'database': 'transport_management',
    'raise_on_warnings': True
}
```

### 5. Train the Model

```bash
rasa train
```

### 6. Run the Chatbot

Open **two terminals**:

**Terminal 1 — Rasa Action Server:**
```bash
rasa run actions
```

**Terminal 2 — Rasa Server:**
```bash
# Interactive shell mode
rasa shell

# OR as an API server
rasa run --enable-api --cors "*" --port 5005
```

---

## 💬 Usage

### Example Conversations

**Finding your bus route:**
```
User: Hi
Bot:  Hello! How can I help you with the bus service today?

User: What is my bus route?
Bot:  Please provide your student ID number.

User: My ID is NUNL-S24-27196
Bot:  Hello [Student Name],
      Your assigned route is R#1:
      Bus Number: BUS-001
      Shift: Morning
      Timing: 07:00 to 17:00
      Driver: [Driver Name] ([Contact])
```

**Getting driver information:**
```
User: Who is the driver for R#1?
Bot:  Driver Information for Route R#1:
      Name: [Driver Name]
      Contact: [Phone Number]
      Bus Number: BUS-001
```

**Checking route timing:**
```
User: What's the schedule for R#2?
Bot:  Route R#2 Timing:
      Shift: Morning
      Start Time: 07:00
      End Time: 17:00
```

### Supported Intents

| Intent | Example Phrases |
|--------|----------------|
| `greet` | "hi", "hello", "good morning" |
| `ask_route` | "what is my bus route?", "which bus do I take?" |
| `provide_student_id` | "NUNL-S24-27196", "my ID is NUMS-F23-1234" |
| `ask_driver_info` | "who drives R#1?", "driver details for R#2" |
| `ask_route_timing` | "when does the bus arrive?", "timing for R#1" |
| `ask_route_students` | "how many students on R#1?", "list students in R#2" |
| `ask_route_stats` | "route statistics for R#1", "show me stats for R#2" |
| `ask_bus_number` | "what's my bus number?", "bus number for R#1" |
| `goodbye` | "bye", "see you later" |
| `thank` | "thanks", "thank you" |

---

## 🧠 NLU Pipeline

The chatbot uses a sophisticated NLU pipeline configured in `config.yml`:

```
Input Text
    │
    ▼
WhitespaceTokenizer ──► RegexFeaturizer ──► LexicalSyntacticFeaturizer
    │
    ▼
CountVectorsFeaturizer (word-level + char n-grams)
    │
    ▼
DIETClassifier (100 epochs) ──► Intent & Entity Recognition
    │
    ▼
EntitySynonymMapper ──► ResponseSelector ──► FallbackClassifier
```

### Policies

| Policy | Purpose |
|--------|---------|
| `MemoizationPolicy` | Remembers exact conversation patterns |
| `RulePolicy` | Handles rule-based conversations |
| `TEDPolicy` | Transformer-based dialogue management (100 epochs) |
| `UnexpecTEDIntentPolicy` | Detects unexpected user intents |
| `FallbackClassifier` | Handles low-confidence predictions (threshold: 0.3) |

---

## ⚡ Custom Actions

All custom actions are defined in `actions.py` and connect to MySQL using connection pooling:

| Action | Description |
|--------|-------------|
| `ActionFetchRoute` | Fetches complete route info (shift, bus, timing, driver, student count) |
| `ActionFetchDriverInfo` | Gets driver name, contact, and bus number for a route |
| `ActionFetchRouteStudents` | Lists all students assigned to a specific route |
| `ActionFetchRouteTiming` | Returns departure and arrival times for a route |
| `ActionFetchTotalRoutes` | Lists all available routes in the system |
| `ActionFetchRouteByStudentId` | Finds the assigned route for a student by their ID |
| `ActionFetchRouteStats` | Provides route statistics including student count |

---

## ☁️ Deployment

### Docker

```bash
# Build the image
docker build -t university-transport-chatbot .

# Run the container
docker run -p 5005:5005 university-transport-chatbot
```

### Render

1. Create a new **Web Service** on [Render](https://render.com).
2. Connect this GitHub repository.
3. Render will auto-detect the `Dockerfile`.
4. Set the `PORT` environment variable (Render provides this automatically).
5. The Rasa API will be available at your Render URL.

### API Endpoints

Once deployed, the Rasa server exposes:

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/webhooks/rest/webhook` | POST | Send messages and get responses |
| `/status` | GET | Check server status |
| `/model/parse` | POST | Parse a message without sending it |

**Example API call:**
```bash
curl -X POST http://localhost:5005/webhooks/rest/webhook \
  -H "Content-Type: application/json" \
  -d '{"sender": "user1", "message": "What is my bus route?"}'
```

---

## 🛠️ Tech Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| **Python** | 3.8.16 | Runtime language |
| **Rasa Open Source** | 3.6.21 | Conversational AI framework |
| **Rasa SDK** | 3.6.21 | Custom action server |
| **MySQL** | 8.0 | Relational database |
| **mysql-connector-python** | Latest | MySQL database driver |
| **SQLAlchemy** | Latest | ORM / database toolkit |
| **Docker** | Latest | Containerization |
| **Gunicorn** | Latest | WSGI HTTP server |

---

## 🤝 Contributing

Contributions are welcome! Here's how to get started:

1. **Fork** the repository
2. **Create** a feature branch: `git checkout -b feature/amazing-feature`
3. **Commit** your changes: `git commit -m 'Add amazing feature'`
4. **Push** to the branch: `git push origin feature/amazing-feature`
5. **Open** a Pull Request

---

## 📄 License

This project is open source and available for educational and personal use.

---

## 👤 Author

**Muhammad Ahmed Imtiaz**
- GitHub: [@Ahmedimtiaz-github](https://github.com/Ahmedimtiaz-github)
- University: NUML, Islamabad
- Project Type: Final Year Project (FYP)

---

<p align="center">
  Made with ❤️ for NUML University Transport Management
</p>
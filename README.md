# Library Management System

CPS510 — Database Systems | Toronto Metropolitan University

## Overview

A web-based library database management system built using Python,
Flask and Oracle Database. The application uses a normalized 3NF/BCNF
database schema and provides an interface for managing library records.

## Features

- Oracle database login
- Create, populate and drop database tables
- Execute predefined SQL queries and advanced reports
- View and search database records
- Add, edit and delete records using data entry forms
- Log out of the application

## Requirements

- Python 3.10 or newer
- Visual Studio Code (recommended)
- Valid Oracle database credentials
- TMU VPN (if required)
- Internet access to install dependencies

## Installation and Setup

### 1. Download the Project

Download the repository from GitHub using **Code > Download ZIP**
and extract the downloaded folder.

### 2. Open the Project in VS Code

Open VS Code and select **File > Open Folder**.

Select the extracted folder containing `app.py` and
`requirements.txt`, then open **Terminal > New Terminal**.

### 3. Create and Activate a Virtual Environment

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

**Windows (PowerShell):**

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

If Windows blocks activation, use the virtual environment's
Python executable directly in the following steps.

### 4. Install Dependencies

```bash
python -m pip install -r requirements.txt
```

For Windows without activation:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

This installs Flask and python-oracledb.

### 5. Connect to Oracle

Connect to the TMU VPN if required.

The Oracle connection string is located in `database.py`:

```python
DSN = "orsrv1.cs.torontomu.ca:1521/orcldb"
```

Users outside TMU must have access to their own Oracle database
and change the DSN accordingly.

### 6. Run the Application

```bash
python app.py
```

For Windows without activation:

```powershell
.\.venv\Scripts\python.exe app.py
```

Open the URL displayed in the terminal, usually:

http://127.0.0.1:5001

Log in using your Oracle username and password.

## Using the Application

### First-Time Setup

1. Log in using your Oracle credentials.
2. Click **Create Tables** to create the database tables and views.
3. Click **Populate Tables** to insert sample records.
4. Click **Query Tables** to execute SQL queries.
5. Select a table from the sidebar to manage its records.

If your database already contains the required tables and records,
you can skip steps 2 and 3.

### Query Tables

Select a predefined query from the dropdown menu and run it.
The application displays the SQL statement and its results.

### Data Entry Forms

Select a table from the sidebar to view, search, add, edit
or delete records.

### Drop Tables

**Warning:** This option permanently deletes the project's
database tables, records and views.

### Exit

Click **Exit** to log out. Press `Ctrl+C` in the terminal
to stop the application.

## Database Structure

| Table | Purpose |
| --- | --- |
| AUTHOR | Author information |
| PUBLISHER | Publisher information |
| BOOKS | Book information |
| BOOK_COPY | Individual book copies |
| POSTAL_LOCATION | Postal codes, cities and provinces |
| MEMBERS_3NF | Normalized member information |
| LIBRARIAN | Librarian information |
| FINE | Member fines |
| WRITES | Author-book relationships |
| BORROWS | Borrowing records |
| RESERVES | Reservation records |

The database also includes three views:

- AVAILABLE_BOOKS
- OUTSTANDING_FINES
- BORROWED_BOOKS

## Project Structure

```text
Library_DBMS/
├── app.py              # Main Flask application
├── database.py         # Oracle connection and SQL execution
├── login.py            # Login and logout
├── tables.py           # Table administration
├── records.py          # Record management
├── reports.py          # SQL queries and reports
├── create.sql          # Database table definitions
├── populate.sql        # Sample records
├── views.sql           # Database views
├── reports.json        # Predefined SQL queries
├── requirements.txt    # Python dependencies
├── README.md           # Project documentation
├── .gitignore
├── static/
│   └── style.css       # Website styling
└── templates/
    ├── base.html
    ├── login.html
    ├── dashboard.html
    ├── records.html
    ├── reports.html
    ├── error.html
    └── missing_table.html
```

## Running the Application Again

Dependencies only need to be installed during the initial setup.

**macOS / Linux:**

```bash
source .venv/bin/activate
python app.py
```

**Windows:**

```powershell
.\.venv\Scripts\python.exe app.py
```

## Group Members

- Neel Jadav
- Nico Ramos
- Mithusa Vasudevan
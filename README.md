# API Testing Lab - 6787004

API testing practice using Python, pytest, requests and pytest-html against
https://quickpizza.grafana.com.

## Requirements

- Python 3.10 or newer
- Git and a GitHub account
- curl (use `curl.exe` in Windows PowerShell)
- Visual Studio Code or another editor with a terminal

## Setup (Windows PowerShell)

Run these commands from the repository folder:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
curl.exe --version
```

Select `.venv\Scripts\python.exe` as the Python interpreter in your editor.
If activation is unavailable, use the environment directly without changing
PowerShell's execution policy:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pip check
.\.venv\Scripts\python.exe -m pytest --version
```

## Running tests

Once the lab test files have been added:

```powershell
.\.venv\Scripts\python.exe -m pytest -v
.\.venv\Scripts\python.exe -m pytest -v --html=report.html --self-contained-html
```

Open `report.html` in a browser to review the report.
The test files and results belong to Part 0, Part A and Part B and have not
been implemented during setup.

## QuickPizza shared-site rules

- Create, change and delete only data created by your own tests.
- Never create or change ratings using the public token `abcdef0123456789`
  or any token not obtained by logging in as your own test user.
- Use made-up usernames and passwords, never real credentials.
- Run the suite only when needed, never in a loop. A complete lab run sends
  approximately 140 requests and takes about a minute.

## Repository

Current public repository: https://github.com/Shiho-py/api-lab-6787004

The handout specifies the name `api-lab`; the existing repository uses
`api-lab-6787004`. Its name has been preserved during setup.
No commit or push is part of this setup task.

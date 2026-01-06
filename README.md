# Domain Hoster

A Python application for hosting/managing domains (project-specific behavior depends on this repository’s source code and configuration).

## Prerequisites

- Python 3.9+ (recommended)
- `pip` (usually included with Python)
- Git

Check versions:

```bash
python --version
pip --version
```

> On some systems you may need to use `python3` and `pip3` instead of `python` and `pip`.

## Getting Started

### 1) Clone the repository

```bash
git clone https://github.com/Wrap-pixelz/domain-hoster.git
cd domain-hoster
```

### 2) Create a virtual environment (recommended)

A virtual environment keeps dependencies isolated per project.

#### macOS / Linux

```bash
python -m venv .venv
source .venv/bin/activate
```

#### Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Windows (Command Prompt)

```bat
python -m venv .venv
.\.venv\Scripts\activate.bat
```

After activation, your terminal prompt usually changes to show `(.venv)`.

### 3) Upgrade pip (optional but recommended)

```bash
python -m pip install --upgrade pip
```

### 4) Install project dependencies

If your repository includes `requirements.txt`:

```bash
pip install -r requirements.txt
```

If it uses `pyproject.toml` (Poetry):

```bash
pip install poetry
poetry install
```

If it uses `Pipfile` (Pipenv):

```bash
pip install pipenv
pipenv install
pipenv shell
```

> Use the method that matches the dependency files present in this repo.

### 5) Run the application

How to run depends on how the project is structured. Common options:

- If there is an entry script like `main.py`:
  ```bash
  python main.py
  ```

- If this is a package with a module entry point:
  ```bash
  python -m domain_hoster
  ```

- If it is a web app (example: Flask):
  ```bash
  flask run
  ```

If you’re unsure, check the repository for files like:
- `main.py`, `app.py`, `run.py`
- `pyproject.toml`
- `requirements.txt`
- `Makefile`
- GitHub Actions workflow documentation

## Deactivating the virtual environment

When you’re done:

```bash
deactivate
```

## Troubleshooting

### `python` not found / wrong Python version
Try:

```bash
python3 --version
python3 -m venv .venv
source .venv/bin/activate
```

### Windows PowerShell activation policy error
If you see an error running `Activate.ps1`, you can run:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then try activating again:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Recreating the environment
If dependencies get messy:

```bash
deactivate  # if active
rm -rf .venv  # macOS/Linux
# or delete the .venv folder on Windows
python -m venv .venv
# activate it again, then:
pip install -r requirements.txt
```

## License

Add license information here (if applicable).

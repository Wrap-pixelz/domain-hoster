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

> Use the method that matches the dependency files present in this repo.

### 5) Configure environment variables

Copy the example environment file and edit as needed:

```bash
cp .env.example .env
# Then edit .env to set your VPS_IP and other values
```

**.env variables:**

- `FLASK_ENV` - Flask environment (development/production)
- `FLASK_HOST` - Host for Flask app (default: 0.0.0.0)
- `FLASK_PORT` - Port for Flask app (default: 5000)
- `SECRET_KEY` - Flask secret key
- `VPS_IP` - Your server's public IP (used for domain validation)
- `NGINX_TEMPLATE_PATH` - Path to NGINX Jinja2 template
- `NGINX_SITES_AVAILABLE` - NGINX sites-available directory
- `NGINX_SITES_ENABLED` - NGINX sites-enabled directory
- `DOMAINS_FILE` - Path to domains JSON file
- `ALLOWED_PORT_MIN`/`ALLOWED_PORT_MAX` - Allowed port range for apps

### 6) Run the application

```bash
python app.py
# or, for development:
flask run
```
## API Endpoints

All endpoints are prefixed by your server's base URL (e.g., `http://localhost:5000`).

### `GET /health`
**Description:** Health check endpoint. Returns `{"status": "ok"}` if the server is running.

### `GET /domains`
**Description:** List all managed domains and their assigned ports/status.

**Response Example:**
```json
{
  "example.com": { "port": 3000, "status": "active" }
}
```

### `POST /domains`
**Description:** Add a new domain and deploy its NGINX config.

**Request Body:**
```json
{
  "domain": "example.com",
  "port": 3000
}
```
**Validations:**
- Domain must have an A record pointing to your VPS IP.
- Port must be within allowed range.

**Response:**
- `201 Created` on success, with domain info.
- Error message if validation or deployment fails.

### `DELETE /domains/<domain>`
**Description:** Remove a domain from management (does not remove NGINX config).

**Response:**
- `200 OK` on success, with confirmation message.
- `404 Not Found` if domain is not managed.


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

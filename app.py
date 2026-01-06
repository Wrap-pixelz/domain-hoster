import os
import json
import socket
import subprocess
from flask import Flask, request, jsonify,redirect, url_for
from dotenv import load_dotenv
from flasgger import Swagger, swag_from

load_dotenv()

FLASK_HOST = os.getenv("FLASK_HOST", "127.0.0.1")
FLASK_PORT = int(os.getenv("FLASK_PORT", 5000))
SECRET_KEY = os.getenv("SECRET_KEY", "change-me")

VPS_IP = os.getenv("VPS_IP")
DOMAINS_FILE = os.getenv("DOMAINS_FILE", "data/domains.json")

ALLOWED_PORT_MIN = int(os.getenv("ALLOWED_PORT_MIN", 2000))
ALLOWED_PORT_MAX = int(os.getenv("ALLOWED_PORT_MAX", 9000))

DEPLOY_SCRIPT = os.getenv("DEPLOY_SCRIPT", "scripts/deploy_nginx.py")

app = Flask(__name__)
app.config["SECRET_KEY"] = SECRET_KEY

swagger_template = {
    "swagger": "2.0",
    "info": {
        "title": "Domain Hoster API",
        "description": "REST API for managing domains and provisioning NGINX on a VPS",
        "version": "1.0.0"
    },
    "basePath": "/",
    "schemes": ["http"],
}

Swagger(app, template=swagger_template)

def load_domains():
    if not os.path.exists(DOMAINS_FILE):
        return {}
    with open(DOMAINS_FILE, "r") as f:
        return json.load(f)

def save_domains(data):
    os.makedirs(os.path.dirname(DOMAINS_FILE), exist_ok=True)
    with open(DOMAINS_FILE, "w") as f:
        json.dump(data, f, indent=2)

def verify_domain_points_to_vps(domain: str) -> bool:
    try:
        resolved_ip = socket.gethostbyname(domain)
        return resolved_ip == VPS_IP
    except Exception:
        return False

def validate_port(port: int) -> bool:
    return ALLOWED_PORT_MIN <= port <= ALLOWED_PORT_MAX

@app.route("/health", methods=["GET"])
@swag_from({
    "tags": ["Health"],
    "responses": {
        200: {
            "description": "Service is healthy"
        }
    }
})
def health_check():
    return jsonify({"status": "ok"}), 200

@app.route("/domains", methods=["GET"])
@swag_from({
    "tags": ["Domains"],
    "responses": {
        200: {
            "description": "List all domains"
        }
    }
})
def list_domains():
    return jsonify(load_domains()), 200

@app.route("/domains", methods=["POST"])
@swag_from({
    "tags": ["Domains"],
    "parameters": [
        {
            "name": "body",
            "in": "body",
            "required": True,
            "schema": {
                "type": "object",
                "required": ["domain", "port"],
                "properties": {
                    "domain": {"type": "string", "example": "example.com"},
                    "port": {"type": "integer", "example": 3000}
                }
            }
        }
    ],
    "responses": {
        201: {"description": "Domain deployed successfully"},
        400: {"description": "Validation error"},
        409: {"description": "Domain already exists"},
        500: {"description": "NGINX deployment failed"}
    }
})
def add_domain():
    data = request.get_json(silent=True)

    if not data:
        return jsonify({"error": "Invalid JSON body"}), 400

    domain = data.get("domain")
    port = data.get("port")

    if not domain or not port:
        return jsonify({"error": "domain and port are required"}), 400

    try:
        port = int(port)
    except ValueError:
        return jsonify({"error": "port must be an integer"}), 400

    if not validate_port(port):
        return jsonify({
            "error": f"Port must be between {ALLOWED_PORT_MIN} and {ALLOWED_PORT_MAX}"
        }), 400

    if not verify_domain_points_to_vps(domain):
        return jsonify({
            "error": "Domain A record does not point to VPS IP"
        }), 400

    domains = load_domains()

    if domain in domains:
        return jsonify({"error": "Domain already exists"}), 409

    try:
        subprocess.run(
            ["sudo", "python3", DEPLOY_SCRIPT, domain, str(port)],
            check=True,
            capture_output=True,
            text=True
        )
    except subprocess.CalledProcessError as e:
        return jsonify({
            "error": "NGINX deployment failed",
            "details": e.stderr
        }), 500

    domains[domain] = {
        "port": port,
        "status": "active"
    }
    save_domains(domains)

    return jsonify({
        "message": "Domain deployed successfully",
        "domain": domain,
        "port": port
    }), 201

@app.route("/domains/<domain>", methods=["DELETE"])
@swag_from({
    "tags": ["Domains"],
    "parameters": [
        {
            "name": "domain",
            "in": "path",
            "type": "string",
            "required": True
        }
    ],
    "responses": {
        200: {"description": "Domain removed"},
        404: {"description": "Domain not found"}
    }
})
def delete_domain(domain):
    domains = load_domains()

    if domain not in domains:
        return jsonify({"error": "Domain not found"}), 404

    del domains[domain]
    save_domains(domains)

    return jsonify({
        "message": "Domain removed",
        "domain": domain
    }), 200

if __name__ == "__main__":
    app.run(
        host=FLASK_HOST,
        port=FLASK_PORT,
        debug=os.getenv("FLASK_ENV") == "development"
    )

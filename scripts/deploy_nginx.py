import os
from dotenv import load_dotenv
from jinja2 import Template
import subprocess
import sys

load_dotenv()

DOMAIN = sys.argv[1]
PORT = sys.argv[2]

TEMPLATE_PATH = os.getenv("NGINX_TEMPLATE_PATH")
SITES_AVAILABLE = os.getenv("NGINX_SITES_AVAILABLE")
SITES_ENABLED = os.getenv("NGINX_SITES_ENABLED")

available_path = f"{SITES_AVAILABLE}/{DOMAIN}"
enabled_path = f"{SITES_ENABLED}/{DOMAIN}"

with open(TEMPLATE_PATH) as f:
    template = Template(f.read())

config = template.render(domain=DOMAIN, port=PORT)

with open(available_path, "w") as f:
    f.write(config)

subprocess.run(["ln", "-sf", available_path, enabled_path])
subprocess.run(["nginx", "-t"], check=True)
subprocess.run(["systemctl", "reload", "nginx"], check=True)

print("NGINX DEPLOYED")

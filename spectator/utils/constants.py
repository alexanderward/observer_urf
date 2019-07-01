import os

if os.environ.get("environment", "local") == 'PROD':
    api_endpoint = ""
else:
    api_endpoint = "http://localhost:8000"

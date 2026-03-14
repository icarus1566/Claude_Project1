import os
import subprocess
import time
import urllib.request
import urllib.error
import argparse

# Configuration
COMPOSE_FILE = r"d:\ALL_AI\Claude_Project1\lfnovo-rag-system\deploy\common\compose.yaml"
API_HEALTH_URL = "http://localhost:8000/api/v1/health"

def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        return None

def check_model_exists():
    model_path = r"d:\ALL_AI\Claude_Project1\lfnovo-rag-system\models\embedding\bge-m3"
    files = ["model.safetensors", "pytorch_model.bin"]
    exists = any(os.path.exists(os.path.join(model_path, f)) for f in files)
    if not exists:
        print(f"WARNING: Model weight files not found in {model_path}")
    return exists

def check_api_health():
    print(f"Checking API health at {API_HEALTH_URL}...")
    try:
        with urllib.request.urlopen(API_HEALTH_URL, timeout=5) as response:
            if response.getcode() == 200:
                print("SUCCESS: API is reachable and healthy.")
                return True
            else:
                print(f"FAILURE: API returned status code {response.getcode()}")
    except urllib.error.URLError as e:
        print(f"FAILURE: Could not reach API. Error: {e}")
    except Exception as e:
        print(f"FAILURE: An unexpected error occurred: {e}")
    return False

def check_port_conflict(port):
    print(f"Checking for port conflict on {port}...")
    try:
        # Using docker ps to find containers using the port
        cmd = f'docker ps --filter "publish={port}" --format "{{{{.ID}}}}:{{{{.Names}}}}"'
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.stdout.strip():
            print(f"CONFLICT: Port {port} is occupied by: {result.stdout.strip()}")
            return result.stdout.strip().split(':')[0]
    except Exception as e:
        print(f"Error checking port conflict: {e}")
    return None

def restart_services():
    print("Restarting services...")
    
    # Check for port 8000 conflict before starting
    conflicting_id = check_port_conflict(8000)
    if conflicting_id:
        print(f"Attempting to stop conflicting container {conflicting_id}...")
        run_command(f"docker stop {conflicting_id}")

    run_command(f"docker compose -f {COMPOSE_FILE} down")
    run_command(f"docker compose -f {COMPOSE_FILE} up -d")
    print("Waiting for services to stabilize (10s)...")
    time.sleep(10)

def main():
    parser = argparse.ArgumentParser(description="lfnovo Docker Management Script")
    parser.add_argument("--check-health", action="store_true", help="Check health of API and services")
    parser.add_argument("--restart", action="store_true", help="Restart all services")
    
    args = parser.parse_args()

    if args.restart:
        if not check_model_exists():
            print("ERROR: Cannot restart. Model files are missing.")
            return
        restart_services()
    
    if args.check_health:
        check_api_health()

if __name__ == "__main__":
    main()

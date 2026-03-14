import subprocess
import os

# Configuration
IMAGES = [
    "rag-api",
    "ollama/ollama:latest",
    "ghcr.io/open-webui/open-webui:main",
    "qdrant/qdrant:latest",
    "minio/minio:latest",
    "postgres:15-alpine"
]

EXPORT_DIR = r"d:\ALL_AI\Claude_Project1\production_images"

def run_command(cmd):
    print(f"Executing: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        return False

def main():
    if not os.path.exists(EXPORT_DIR):
        os.makedirs(EXPORT_DIR)
        print(f"Created directory: {EXPORT_DIR}")

    print("--- Starting Docker Image Export for Air-gapped Deployment ---")
    
    for image in IMAGES:
        # Create a safe filename (replace / and : with _)
        safe_filename = image.replace("/", "_").replace(":", "_") + ".tar"
        export_path = os.path.join(EXPORT_DIR, safe_filename)
        
        print(f"Exporting {image} to {safe_filename}...")
        success = run_command(f'docker save "{image}" -o "{export_path}"')
        
        if success:
            print(f"Successfully exported: {safe_filename}")
        else:
            print(f"FAILED to export: {image}")

    print("\n--- Summary ---")
    print(f"All images have been (attempted to be) saved in: {EXPORT_DIR}")
    print("Next step: Compress this directory along with your source code and move to the target server.")

if __name__ == "__main__":
    main()

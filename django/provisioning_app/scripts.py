import subprocess
import sys

# Mapping of app names to their git URLs
APP_GIT_URLS = {
    "hrms": "https://github.com/frappe/hrms",
    "healthcare": "https://github.com/earthians/marley",
    "education": "https://github.com/frappe/education",
    # Add more as needed
}

def ensure_app_present(app):
    app_path = f"/home/frappe/frappe-bench/apps/{app}"
    # Check if app directory exists in the container
    result = subprocess.run([
        "docker", "exec", "erpnext_saas_backend_1",
        "test", "-d", app_path
    ])
    if result.returncode != 0:
        # App not present, get it using bench get-app
        git_url = APP_GIT_URLS.get(app)
        if not git_url:
            raise Exception(f"Git URL for app '{app}' not found in mapping.")
        subprocess.run([
            "docker", "exec", "erpnext_saas_backend_1",
            "bench", "get-app", app, git_url
        ], check=True)

def provision_site(domain, apps, admin_password):
    print(f"\n[INFO] Starting site provisioning for: {domain}\n")

    try:
        # Step 1: Create a new site
        print("[STEP 1] Creating new site...")
        result = subprocess.run([
            "docker", "exec", "erpnext_saas_backend_1",
            "bench", "new-site", domain,
            "--no-mariadb-socket",
            "--admin-password", admin_password,
            "--mariadb-root-password", "admin"
        ], check=True, capture_output=True, text=True)
        print("[OK] Site created successfully.")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        msg = f"[ERROR] Failed to create new site. STDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        print(msg)
        return False, msg
    except FileNotFoundError:
        msg = "[FATAL] Docker or Bench not found. Is Docker installed and running?"
        print(msg)
        return False, msg
    except Exception as e:
        msg = f"[UNEXPECTED ERROR] {e}"
        print(msg)
        return False, msg

    # Step 2: Install selected apps
    for app in apps:
        try:
            print(f"\n[STEP 2] Installing app '{app}' on site...")
            # Ensure the app is present before installing
            if app != "erpnext":
                ensure_app_present(app)
            result = subprocess.run([
                "docker", "exec", "erpnext_saas_backend_1",
                "bench", "--site", domain, "install-app", app
            ], check=True, capture_output=True, text=True)
            print(f"[OK] App '{app}' installed on site.")
            print(result.stdout)
        except subprocess.CalledProcessError as e:
            msg = f"[ERROR] Failed to install app '{app}' on site. STDOUT: {e.stdout}\nSTDERR: {e.stderr}"
            print(msg)
            return False, msg
        except Exception as e:
            msg = f"[UNEXPECTED ERROR] {e}"
            print(msg)
            return False, msg

    print(f"\n[VERIFY] Checking if site directory exists for '{domain}'...")
    result = subprocess.run([
        "docker", "exec", "erpnext_saas_backend_1",
        "test", "-f", f"/home/frappe/frappe-bench/sites/{domain}/site_config.json"
    ], capture_output=True, text=True)
    if result.returncode == 0:
        msg = f"[SUCCESS] Site '{domain}' was created successfully and is ready to use."
        print(msg)
        return True, msg
    else:
        msg = f"[ERROR] Site directory or site_config.json not found for '{domain}'."
        print(msg)
        return False, msg

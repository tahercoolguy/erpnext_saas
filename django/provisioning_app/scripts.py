import subprocess
import sys

def provision_site(domain, apps):
    print(f"\n[INFO] Starting site provisioning for: {domain}\n")

    try:
        # Step 1: Create a new site
        print("[STEP 1] Creating new site...")
        result = subprocess.run([
            "docker", "exec", "erpnext_saas_backend_1",
            "bench", "new-site", domain,
            "--no-mariadb-socket",
            "--admin-password", "admin",
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

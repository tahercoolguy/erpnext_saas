import subprocess
import sys

def provision_site(domain):
    print(f"\n[INFO] Starting site provisioning for: {domain}\n")

    try:
        # Step 1: Create a new site
        print("[STEP 1] Creating new site...")
        result = subprocess.run([
            "docker", "exec", "erpnext_saas-backend-1",
            "bench", "new-site", domain,
            "--no-mariadb-socket",
            "--admin-password", "admin",
            "--mariadb-root-password", "admin",
            "--install-app", "frappe"
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

    try:
        # Step 2: Install ERPNext on the new site
        print("\n[STEP 2] Installing ERPNext app...")
        result = subprocess.run([
            "docker", "exec", "erpnext_saas-backend-1",
            "bench", "--site", domain, "install-app", "erpnext"
        ], check=True, capture_output=True, text=True)
        print("[OK] ERPNext installed on site.")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        msg = f"[ERROR] Failed to install ERPNext on site. STDOUT: {e.stdout}\nSTDERR: {e.stderr}"
        print(msg)
        return False, msg
    except Exception as e:
        msg = f"[UNEXPECTED ERROR] {e}"
        print(msg)
        return False, msg

    print(f"\n[VERIFY] Checking if site directory exists for '{domain}'...")
    result = subprocess.run([
        "docker", "exec", "erpnext_saas-backend-1",
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

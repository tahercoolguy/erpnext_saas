import subprocess
import sys

def provision_site(domain):
    print(f"\n[INFO] Starting site provisioning for: {domain}\n")

    try:
        # Step 1: Create a new site
        print("[STEP 1] Creating new site...")
        result = subprocess.run([
            "docker", "exec", "backend",
            "bench", "new-site", domain,
            "--no-mariadb-socket",
            "--admin-password", "admin",
            "--mariadb-root-password", "admin",
            "--install-app", "frappe"
        ], check=True, capture_output=True, text=True)
        print("[OK] Site created successfully.")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to create new site.")
        print("[STDOUT]:", e.stdout)
        print("[STDERR]:", e.stderr)
        return False
    except FileNotFoundError:
        print("[FATAL] Docker or Bench not found. Is Docker installed and running?")
        return False
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        return False

    try:
        # Step 2: Install ERPNext on the new site
        print("\n[STEP 2] Installing ERPNext app...")
        result = subprocess.run([
            "docker", "exec", "backend",
            "bench", "--site", domain, "install-app", "erpnext"
        ], check=True, capture_output=True, text=True)
        print("[OK] ERPNext installed on site.")
        print(result.stdout)

    except subprocess.CalledProcessError as e:
        print("[ERROR] Failed to install ERPNext on site.")
        print("[STDOUT]:", e.stdout)
        print("[STDERR]:", e.stderr)
        return False
    except Exception as e:
        print(f"[UNEXPECTED ERROR] {e}")
        return False

    print(f"\n[SUCCESS] Provisioned site '{domain}' with ERPNext.\n")
    return True

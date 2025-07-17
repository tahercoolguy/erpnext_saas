import subprocess
import sys

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

def get_app_git_url(app):
    """Return the git URL for known apps, or None if unknown."""
    app_git_urls = {
        "hrms": "https://github.com/frappe/hrms",
        "education": "https://github.com/frappe/education",
        "healthcare": "https://github.com/earthians/marley",
        # Add more mappings as needed
    }
    return app_git_urls.get(app)

    # Step 2: Install selected apps
    for app in apps:
        if app == "erpnext":
            # Directly install erpnext, do not check or fetch
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
            continue
        # Check if app is present in the container
        app_path = f"/home/frappe/frappe-bench/apps/{app}"
        check_result = subprocess.run([
            "docker", "exec", "erpnext_saas_backend_1",
            "test", "-d", app_path
        ])
        if check_result.returncode != 0:
            # App not present, try to get it
            git_url = get_app_git_url(app)
            if git_url:
                print(f"[INFO] App '{app}' not found. Fetching from {git_url} ...")
                get_app_result = subprocess.run([
                    "docker", "exec", "erpnext_saas_backend_1",
                    "bench", "get-app", git_url
                ], capture_output=True, text=True)
                if get_app_result.returncode != 0:
                    msg = f"[ERROR] Failed to get app '{app}'. STDOUT: {get_app_result.stdout}\nSTDERR: {get_app_result.stderr}"
                    print(msg)
                    return False, msg
            else:
                msg = f"[ERROR] No git URL configured for app '{app}'. Cannot fetch app."
                print(msg)
                return False, msg
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

import subprocess

def provision_site(domain):
    try:
        subprocess.run([
            "docker", "exec", "backend", "bench", "new-site", domain
        ], check=True)

        subprocess.run([
            "docker", "exec", "backend", "bench", "--site", domain, "install-app", "erpnext"
        ], check=True)

        return True
    except subprocess.CalledProcessError as e:
        print("Provisioning failed:", e)
        return False

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Company
from .scripts import provision_site
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
import base64

@require_GET
@csrf_exempt
def check_domain(request):
    subdomain = request.GET.get('subdomain', '').strip().lower()
    if not subdomain:
        return JsonResponse({'available': False, 'error': 'No subdomain provided'}, status=400)
    domain = f"{subdomain}.preciseerp.com"
    exists = Company.objects.filter(domain=domain).exists()
    return JsonResponse({'available': not exists})

def register_company(request):
    if request.method == 'POST':
        print("[LOG] Received POST data:", request.POST)
        name = request.POST.get('name')
        subdomain = request.POST.get('subdomain', '').strip().lower()
        # Accept multiple apps (as list)
        apps = request.POST.getlist('apps')
        admin_password = request.POST.get('admin_password', '').strip() or 'admin'
        # Encode the password for storage (not secure, just obfuscation; replace with encryption in production)
        admin_password_encoded = base64.b64encode(admin_password.encode('utf-8')).decode('utf-8')
        print(f"[LOG] Parsed name: {name}, subdomain: {subdomain}, apps: {apps}, admin_password: {'*' * len(admin_password) if admin_password else '(default)'}")
        if not name or not subdomain or not apps:
            print("[LOG] Missing fields in registration form.")
            return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)
        domain = f"{subdomain}.preciseerp.com"
        print(f"[LOG] Constructed domain: {domain}")
        if Company.objects.filter(domain=domain).exists():
            print(f"[LOG] Domain already taken: {domain}")
            return JsonResponse({'success': False, 'error': 'Domain already taken'}, status=400)
        company = Company.objects.create(name=name, domain=domain, admin_password=admin_password_encoded, installed_apps=','.join(apps))
        print(f"[LOG] Created company object: {company}")
        success, message = provision_site(domain, apps, admin_password)
        print(f"[LOG] Provision site result: success={success}, message={message}")
        company.status = 'created' if success else 'failed'
        company.save()
        print(f"[LOG] Company status updated to: {company.status}")
        return JsonResponse({'success': success, 'message': message})
    return render(request, 'register.html')

from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Company
from .scripts import provision_site
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

@require_GET
@csrf_exempt
def check_domain(request):
    subdomain = request.GET.get('subdomain', '').strip().lower()
    if not subdomain:
        return JsonResponse({'available': False, 'error': 'No subdomain provided'}, status=400)
    domain = f"{subdomain}-erp.preciseerp.com"
    exists = Company.objects.filter(domain=domain).exists()
    return JsonResponse({'available': not exists})

def register_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        subdomain = request.POST.get('subdomain', '').strip().lower()
        if not name or not subdomain:
            return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)
        domain = f"{subdomain}-erp.preciseerp.com"
        if Company.objects.filter(domain=domain).exists():
            return JsonResponse({'success': False, 'error': 'Domain already taken'}, status=400)
        company = Company.objects.create(name=name, domain=domain)
        success = provision_site(domain)
        company.status = 'created' if success else 'failed'
        company.save()
        return JsonResponse({'success': success})
    return render(request, 'register.html')

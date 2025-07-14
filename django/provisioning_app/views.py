from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.http import JsonResponse
from .models import Company
from .scripts import provision_site

def register_company(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        domain = request.POST.get('domain')

        if not name or not domain:
            return JsonResponse({'success': False, 'error': 'Missing fields'}, status=400)

        company = Company.objects.create(name=name, domain=domain)
        success = provision_site(domain)

        company.status = 'created' if success else 'failed'
        company.save()

        return JsonResponse({'success': success})

    return render(request, 'register.html')

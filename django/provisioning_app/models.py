from django.db import models

class Company(models.Model):
    name = models.CharField(max_length=255)
    domain = models.CharField(max_length=255, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='pending')  # pending, created, failed
    admin_password = models.CharField(max_length=255, blank=True, null=True, help_text='Encrypted or encoded admin password for the site (store securely!)')
    installed_apps = models.TextField(blank=True, null=True, help_text='Comma-separated list of installed Frappe apps for this site')

    def __str__(self):
        return self.name

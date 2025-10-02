"""
URL configuration for university_erp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.shortcuts import render

def homepage(request):
    """Homepage view for University ERP System"""
    html_content = """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>University ERP System</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 0; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); min-height: 100vh; }
            .container { max-width: 1200px; margin: 0 auto; background: white; border-radius: 10px; padding: 40px; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }
            h1 { color: #333; text-align: center; margin-bottom: 10px; }
            .subtitle { text-align: center; color: #666; margin-bottom: 40px; }
            .links { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; margin-top: 30px; }
            .link-card { background: #f8f9fa; border: 1px solid #e9ecef; border-radius: 8px; padding: 20px; text-decoration: none; color: #333; transition: transform 0.2s; }
            .link-card:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
            .link-title { font-weight: bold; font-size: 18px; margin-bottom: 8px; color: #007bff; }
            .link-desc { color: #666; font-size: 14px; }
            .status { background: #d4edda; border: 1px solid #c3e6cb; color: #155724; padding: 15px; border-radius: 5px; margin: 20px 0; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 University ERP System</h1>
            <p class="subtitle">Complete Education Management Solution</p>
            
            <div class="status">
                <strong>✅ System Status:</strong> Online and Ready | 
                <strong>📊 Database:</strong> MySQL Connected | 
                <strong>🔧 Server:</strong> Running on Port 8001
            </div>

            <div class="links">
                <a href="/admin/" class="link-card">
                    <div class="link-title">🛠️ Django Admin Panel</div>
                    <div class="link-desc">Complete administrative interface for managing all ERP modules including students, faculty, courses, and more.</div>
                </a>
                
                <a href="/api/students/" class="link-card">
                    <div class="link-title">👨‍🎓 Student Management API</div>
                    <div class="link-desc">REST API endpoints for student enrollment, academic records, attendance, and graduation tracking.</div>
                </a>
                
                <a href="/api/faculty/" class="link-card">
                    <div class="link-title">👩‍🏫 Faculty Management API</div>
                    <div class="link-desc">Manage faculty information, course assignments, workload, and performance evaluations.</div>
                </a>
                
                <a href="/api/admissions/" class="link-card">
                    <div class="link-title">📝 Admissions API</div>
                    <div class="link-desc">Handle student applications, admission process, document verification, and enrollment.</div>
                </a>
                
                <a href="/api/exams/" class="link-card">
                    <div class="link-title">📋 Examination System API</div>
                    <div class="link-desc">Schedule exams, manage results, generate transcripts, and academic performance tracking.</div>
                </a>
                
                <a href="/api/backoffice/" class="link-card">
                    <div class="link-title">💼 Backoffice Operations API</div>
                    <div class="link-desc">Financial management, payroll, fee collection, inventory, and administrative operations.</div>
                </a>
                
                <a href="/api/administration/" class="link-card">
                    <div class="link-title">🏛️ Administration API</div>
                    <div class="link-desc">University governance, policy management, reporting, and institutional administration.</div>
                </a>
                
                <a href="/api/auth/" class="link-card">
                    <div class="link-title">🔐 Authentication API</div>
                    <div class="link-desc">User authentication, authorization, role management, and security features.</div>
                </a>
            </div>

            <div style="margin-top: 40px; padding: 20px; background: #e7f3ff; border-radius: 5px;">
                <h3>🚀 Quick Start Guide:</h3>
                <ol>
                    <li><strong>Access Admin Panel:</strong> Click "Django Admin Panel" above and login with your superuser credentials</li>
                    <li><strong>Create Superuser:</strong> Run <code>python manage.py createsuperuser</code> if you haven't already</li>
                    <li><strong>Explore APIs:</strong> Click any API link above to see available endpoints</li>
                    <li><strong>Database:</strong> Your MySQL database 'university_erp_db' is fully connected and operational</li>
                </ol>
            </div>

            <div style="text-align: center; margin-top: 30px; color: #666;">
                <p>💾 Database: <strong>MySQL (university_erp_db)</strong> | 🌐 Server: <strong>Django 4.2.7</strong> | 🐍 Python: <strong>3.10</strong></p>
            </div>
        </div>
    </body>
    </html>
    """
    return HttpResponse(html_content)

urlpatterns = [
    path('', homepage, name='homepage'),  # Add homepage URL
    path('admin/', admin.site.urls),
    path('api/auth/', include('authentication.urls')),
    path('accounts/', include('allauth.urls')),  # Google OAuth URLs
    path('api/students/', include('students.urls')),
    path('api/faculty/', include('faculty.urls')),
    path('api/exams/', include('exams.urls')),
    path('api/admissions/', include('admissions.urls')),
    path('api/administration/', include('administration.urls')),
    path('api/backoffice/', include('backoffice.urls')),
]

# Serve media files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

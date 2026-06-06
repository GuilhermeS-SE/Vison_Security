from django.shortcuts import render
from datetime import datetime
from .analyzer import analyze_url
from .models import Scan

def landing(request):
    return render(request, 'scanner/landing.html')

def home(request):
    return render(request, 'scanner/home.html')

def run_scan(request):
    if request.method == 'POST':
        target_url = request.POST.get('url')
        analysis = analyze_url(target_url)

        Scan.objects.create(
            url=analysis["url"],
            risk_level=analysis["risk_level_display"],
            risk_percentage=analysis["risk_percentage"]
        )

        context = {
            'url': analysis['url'],
            'scan_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'risk_level': analysis['risk_level'],
            'risk_level_display': analysis['risk_level_display'],
            'risk_percentage': analysis['risk_percentage'],
            'https_status': analysis['https_status'],
            'scripts_status': analysis['scripts_status'],
            'vulnerabilities': analysis['vulnerabilities'],
            'headers': analysis.get('headers', {})
        }

        return render(request, 'scanner/review.html', context)

    return render(request, 'scanner/home.html')

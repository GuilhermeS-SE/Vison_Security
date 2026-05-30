from django.shortcuts import render
from datetime import datetime
from .analyzer import analyze_url

def landing(request):
    """Puxa a página de apresentação (Landing Page)"""
    return render(request, 'scanner/landing.html')

def home(request):
    """Puxa a página com o formulário do scanner (VISION)"""
    return render(request, 'scanner/home.html')

def run_scan(request):
    """Processa o formulário e gera os dados para a tela de relatório"""
    if request.method == 'POST':
        target_url = request.POST.get('url')

        analysis = analyze_url(target_url)

        context = {
            'url': analysis['url'],
            'scan_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'risk_level': analysis['risk_level'],
            'risk_level_display': analysis['risk_level_display'],
            'risk_percentage': analysis['risk_percentage'],
            'https_status': analysis['https_status'],
            'scripts_status': analysis['scripts_status'],
            'vulnerabilities': analysis['vulnerabilities']
        }
        
        return render(request, 'scanner/review.html', context)
        
    # Se alguém tentar acessar essa URL por fora (GET), joga de volta para o formulário
    return render(request, 'scanner/home.html')
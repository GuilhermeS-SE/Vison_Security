from django.shortcuts import render
from datetime import datetime

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

        context = {
            'url': target_url,
            'scan_time': datetime.now().strftime('%d/%m/%Y %H:%M:%S'),
            'risk_level': 'medio',               # Define a classe CSS (baixo, medio, alto)
            'risk_level_display': 'Médio',       # Texto que aparece na tela
            'risk_percentage': 65,               # Preenche a barra de progresso (risk-bar__fill)
            'https_status': 'Ativo (HTTPS)' if target_url.lower().startswith('https') else 'Inativo (HTTP)',
            'scripts_status': '3 scripts dinâmicos encontrados',
            'vulnerabilities': [
                "Formulário de login detectado em página com scripts externos desconhecidos.",
                "Ausência do cabeçalho de segurança 'Content-Security-Policy' (CSP)."
            ]
        }
        
        return render(request, 'scanner/review.html', context)
        
    # Se alguém tentar acessar essa URL por fora (GET), joga de volta para o formulário
    return render(request, 'scanner/home.html')
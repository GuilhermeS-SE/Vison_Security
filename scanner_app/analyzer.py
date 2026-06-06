import requests
from bs4 import BeautifulSoup

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from webdriver_manager.chrome import ChromeDriverManager
    from selenium.webdriver.chrome.service import Service
    SELENIUM_AVAILABLE = True
except Exception:
    SELENIUM_AVAILABLE = False


def analyze_url(url):
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    result = {
        "url": url,
        "https_status": "Desconhecido",
        "scripts_status": "0 scripts encontrados",
        "risk_level": "baixo",
        "risk_level_display": "Baixo",
        "risk_percentage": 0,
        "vulnerabilities": [],
        "headers": {},
        "internal_links": []
    }

    try:
        headers_request = {
            "User-Agent": "Mozilla/5.0"
        }

        response = requests.get(url, headers=headers_request, timeout=5)
        response.raise_for_status()

        headers = response.headers

        result["headers"] = {
            "Server": headers.get("Server", "Não informado"),
            "Content-Type": headers.get("Content-Type", "Não informado"),
            "X-Frame-Options": headers.get("X-Frame-Options", "Ausente"),
            "Content-Security-Policy": headers.get("Content-Security-Policy", "Ausente"),
        }

        result["https_status"] = (
            "Ativo (HTTPS)"
            if url.lower().startswith("https")
            else "Inativo (HTTP)"
        )

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all("script")
        forms = soup.find_all("form")
        iframes = soup.find_all("iframe")

        risk_score = 0

        phishing_keywords = [
            "senha", "password", "login",
            "cpf", "cartao", "credit card",
            "pix", "bank"
        ]

        html_text = soup.get_text().lower()

        for word in phishing_keywords:
            if word in html_text:
                result["vulnerabilities"].append(
                    f"Possível coleta de credenciais: '{word}' encontrada."
                )
                risk_score += 15

        for a in soup.find_all("a", href=True):
            href = str(a.get("href", ""))
            
            if href.startswith("/") or url in href:
                result["internal_links"].append(href)

        result["internal_links"] = result["internal_links"][:20]

        if not url.lower().startswith("https"):
            result["vulnerabilities"].append(
                "Site utiliza HTTP sem criptografia."
            )
            risk_score += 30

        if "Content-Security-Policy" not in headers:
            result["vulnerabilities"].append(
                "Ausência do cabeçalho Content-Security-Policy (CSP)."
            )
            risk_score += 20

        if "X-Frame-Options" not in headers:
            result["vulnerabilities"].append(
                "Ausência do cabeçalho X-Frame-Options."
            )
            risk_score += 20

        if forms:
            result["vulnerabilities"].append(
                f"{len(forms)} formulário(s) encontrado(s) para análise."
            )

        if iframes:
            result["vulnerabilities"].append(
                f"{len(iframes)} iframe(s) detectado(s)."
            )
            risk_score += 10

        if SELENIUM_AVAILABLE:
            try:
                options = Options()
                options.add_argument("--headless")

                driver = webdriver.Chrome(
                    service=Service(ChromeDriverManager().install()),
                    options=options
                )

                driver.get(url)
                page_source = driver.page_source
                driver.quit()

                if "document.cookie" in page_source:
                    result["vulnerabilities"].append(
                        "Possível acesso a cookies detectado."
                    )
                    risk_score += 15

                if "window.location" in page_source:
                    result["vulnerabilities"].append(
                        "Possível redirecionamento automático detectado."
                    )
                    risk_score += 15
            except Exception:
                pass

        result["scripts_status"] = f"{len(scripts)} scripts encontrados"

        if risk_score >= 60:
            result["risk_level"] = "alto"
            result["risk_level_display"] = "Alto"
        elif risk_score >= 30:
            result["risk_level"] = "medio"
            result["risk_level_display"] = "Médio"

        result["risk_percentage"] = min(risk_score, 100)

    except Exception:
        result["risk_level"] = "medio"
        result["risk_level_display"] = "Não analisado"
        result["vulnerabilities"].append(
            "Não foi possível acessar o site informado."
        )

    return result

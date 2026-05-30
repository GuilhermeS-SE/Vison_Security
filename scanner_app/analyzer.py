import requests
from bs4 import BeautifulSoup


def analyze_url(url):
    """
    Realiza análise básica de uma URL.
    """
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
        "vulnerabilities": []
    }

    try:
        headers_request = {
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/136.0 Safari/537.36"
            )
        }

        response = requests.get(
            url,
            headers=headers_request,
            timeout=5
        )
        response.raise_for_status()

        result["https_status"] = (
            "Ativo (HTTPS)"
            if url.lower().startswith("https")
            else "Inativo (HTTP)"
        )

        soup = BeautifulSoup(response.text, "html.parser")

        scripts = soup.find_all("script")
        forms = soup.find_all("form")
        iframes = soup.find_all("iframe")

        headers = response.headers

        risk_score = 0

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


        result["scripts_status"] = (
            f"{len(scripts)} scripts encontrados"
        )

        if risk_score >= 60:
            result["risk_level"] = "alto"
            result["risk_level_display"] = "Alto"

        elif risk_score >= 30:
            result["risk_level"] = "medio"
            result["risk_level_display"] = "Médio"

        else:
            result["risk_level"] = "baixo"
            result["risk_level_display"] = "Baixo"

        result["risk_percentage"] = min(risk_score, 100)

    except Exception:
        result["risk_level"] = "medio"
        result["risk_level_display"] = "Não analisado"
        result["risk_percentage"] = 0

        result["vulnerabilities"].append(
            "Não foi possível acessar o site informado."
        )

    return result
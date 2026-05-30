# Vision - Scanner de Vulnerabilidades

O **Vision** é uma ferramenta de análise preventiva de segurança da informação focada na identificação de ameaças em websites e links suspeitos. O projeto visa combater o "elo fraco" da segurança — o fator humano — mitigando riscos de phishing e scripts maliciosos antes mesmo que o usuário interaja com o conteúdo.

## 🎯 Escopo e Objetivos

O objetivo central é realizar o escaneamento de URLs (HTTP/HTTPS) para detectar padrões de coleta indevida de dados e comportamentos suspeitos.

**As principais funcionalidades incluem:**

* **Mapeamento de Cabeçalhos:** Extração de metadados HTTP e links internos.

* **Simulação de Navegação:** Execução de JavaScript para identificar ameaças dinâmicas.

* **Análise de Segurança:** Busca ativa por padrões de phishing no HTML.
  
* **Geração de Relatórios:** Compilação clara dos resultados com atribuição de nível de risco (Baixo, Médio, Alto).

## ⚙️ Funcionamento e Tecnologias

O sistema foi modelado sob a arquitetura **MTV (Model-Template-View)**, padrão do Django, semelhante ao **MVC**.

### Stack Tecnológica

* **Python:** Linguagem base para toda a lógica de processamento e automação.

* **Selenium:** Utilizado para automação de navegador, permitindo a análise de scripts dinâmicos que ferramentas estáticas não detectariam.

* **BeautifulSoup:** Responsável pela extração e análise detalhada da estrutura HTML suspeita.

* **Requests:** Empregado para requisições HTTP rápidas e eficientes de análise de servidor.

* **Django:** Framework web utilizado para a estrutura MTV e gerenciamento das rotas.

* **HTML & CSS:** Utilizados na construção da interface de usuário (View) para inserção de URLs e exibição de relatórios.

---

## 🚀 Guia de Instalação

Siga os passos abaixo para configurar o ambiente de desenvolvimento em sua máquina.

### 1. Instalação do Python

O Vision requer o Python instalado.

1. Acesse o site oficial [python.org](https://www.python.org/downloads/).
2. Baixe a versão mais recente para o seu sistema operacional.
3. **Importante:** Durante a instalação no Windows, marque a caixa **"Add Python to PATH"**.
4. Verifique a instalação abrindo o terminal e digitando:

```bash
python --version
```

### 2. Configuração do Django e dependências

O projeto utiliza o framework Django para gerenciar a estrutura web e a lógica do Controller.

1. **Crie um ambiente virtual (recomendado):**

```bash
python -m venv venv
```

2. **Ative o ambiente:**
* Windows: `venv\Scripts\activate`
* Linux/Mac: `source venv/bin/activate`

3. **Instale as dependências:**

```bash
pip install django selenium beautifulsoup4 requests
```

### 3. WebDriver (necessário para o Selenium)

O Selenium precisa de um WebDriver compatível com seu navegador.

**Opção recomendada (automática):**
```bash
pip install webdriver-manager
```

**Opção manual:**

- Baixe o ChromeDriver compatível com seu navegador  
- Disponível em: https://chromedriver.chromium.org/  
- Adicione ao PATH ou coloque na raiz do projeto  

### 4. Executar as migrações do banco de dados

Antes de iniciar o servidor, crie as tabelas necessárias:

```bash
python manage.py migrate
```

### 5. Iniciar o servidor

```bash
python manage.py runserver
```

Acesse a aplicação no navegador: **http://127.0.0.1:8000**

---

## 🖥️ Como usar

1. Na página inicial, digite a URL que deseja analisar.
2. Clique em **INICIAR SCAN**.
3. Aguarde alguns segundos.
4. Visualize o relatório com o nível de risco e as vulnerabilidades encontradas.

---

### Equipe Técnica

Guilherme S. Ribeiro - guilherme.devtechno@gmail.com

Thiago Alves - thiagoalvesx.dev@gmail.com

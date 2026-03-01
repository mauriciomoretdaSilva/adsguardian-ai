# Guia Final de Deploy: AdsGuardian AI

Parabéns! O seu SaaS AdsGuardian AI está completo. Este guia consolida tudo o que precisa para colocar o seu projeto online, de forma gratuita e segura.

---

## 1. Organização dos Ficheiros

O projeto já está organizado. O ficheiro mais importante para o deploy é o `requirements.txt`, que lista todas as bibliotecas que o Streamlit Community Cloud e o GitHub Actions precisam de instalar.

**Conteúdo final do `requirements.txt`:**
```
fastapi
uvicorn[standard]
supabase
python-dotenv
streamlit
requests
pandas
facebook_business
openai
stripe
```

---

## 2. Preparar o GitHub

Siga estes passos para colocar o seu projeto num repositório GitHub.

### Passo 1: Criar um Repositório no GitHub

1.  Vá a [github.com/new](https://github.com/new).
2.  Dê um nome ao seu repositório (ex: `adsguardian-ai`).
3.  Escolha se quer que seja **Público** ou **Privado**.
4.  **Não** adicione um `README`, `.gitignore` ou licença. Vamos usar os que já criámos.
5.  Clique em **"Create repository"**.

### Passo 2: Subir os Ficheiros

Na página do seu novo repositório, o GitHub irá mostrar-lhe alguns comandos. Vamos usar a opção "…or push an existing repository from the command line".

1.  Abra o seu terminal (ou `cmd` / `PowerShell` no Windows).
2.  Navegue para a pasta onde descompactou o projeto `adsguardian_ai`.
3.  Copie e cole os seguintes comandos, **um de cada vez**, pressionando Enter após cada um. Substitua `SEU-USUARIO` e `SEU-REPOSITORIO` pelos seus dados.

```bash
# Inicializa o Git na sua pasta
git init

# Adiciona todos os ficheiros para serem enviados
git add .

# Cria o primeiro "save point" (commit)
git commit -m "Versão inicial do AdsGuardian AI"

# Define a branch principal como 'main'
git branch -M main

# Conecta a sua pasta local ao repositório online
git remote add origin https://github.com/SEU-USUARIO/SEU-REPOSITORIO.git

# Envia os ficheiros para o GitHub
git push -u origin main
```

Após executar o último comando, recarregue a página do seu repositório no GitHub. Todos os seus ficheiros estarão lá!

---

## 3. Configuração de Secrets no Streamlit Cloud

Para que a sua aplicação online se conecte ao Supabase, Stripe, etc., precisa de adicionar as suas chaves de API no Streamlit Cloud.

1.  Aceda ao seu workspace em [share.streamlit.io](https://share.streamlit.io/).
2.  Clique em **"New app"** e configure o seu repositório (conforme o guia de deploy anterior).
3.  Antes de fazer o deploy, clique em **"Advanced settings..."**.
4.  Na caixa de texto **"Secrets"**, cole o seguinte bloco de código, substituindo os `COLE_AQUI...` pelas suas chaves reais.

**Código para colar nas Secrets:**
```toml
# Supabase
SUPABASE_URL = "COLE_AQUI_SUA_SUPABASE_URL"
SUPABASE_KEY = "COLE_AQUI_SUA_SUPABASE_KEY"
SUPABASE_SERVICE_KEY = "COLE_AQUI_SUA_SUPABASE_SERVICE_KEY"

# Stripe
STRIPE_SECRET_KEY = "COLE_AQUI_SUA_STRIPE_SECRET_KEY"
STRIPE_WEBHOOK_SECRET = "COLE_AQUI_SUA_STRIPE_WEBHOOK_SECRET"

# Meta (Facebook)
META_APP_ID = "COLE_AQUI_SEU_META_APP_ID"
META_APP_SECRET = "COLE_AQUI_SEU_META_APP_SECRET"
META_ACCESS_TOKEN = "COLE_AQUI_SEU_META_ACCESS_TOKEN"
AD_ACCOUNT_ID = "COLE_AQUI_SEU_AD_ACCOUNT_ID"

# Telegram
TELEGRAM_BOT_TOKEN = "COLE_AQUI_SEU_TELEGRAM_BOT_TOKEN"
TELEGRAM_CHAT_ID = "COLE_AQUI_SEU_TELEGRAM_CHAT_ID"

# OpenAI / LLM
OPENAI_API_KEY = "COLE_AQUI_SUA_OPENAI_API_KEY"
```

5.  Clique em **"Save"** e depois em **"Deploy!"**.

---

## 4. Automação Gratuita (GitHub Actions)

O ficheiro de automação para o CPA Guard já está no seu projeto. Assim que subir os ficheiros para o GitHub, ele será ativado automaticamente.

**Conteúdo do `.github/workflows/monitoramento.yml`:**
```yaml
name: Monitorização de CPA do AdsGuardian AI

on:
  schedule:
    # Executa a cada 15 minutos
    - cron: '*/15 * * * *'
  workflow_dispatch: # Permite execução manual

jobs:
  monitor-cpa:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout do código
        uses: actions/checkout@v3

      - name: Configurar Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'

      - name: Instalar dependências
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt

      - name: Executar o script de monitorização de CPA
        env:
          SUPABASE_URL: ${{ secrets.SUPABASE_URL }}
          SUPABASE_KEY: ${{ secrets.SUPABASE_KEY }}
          META_APP_ID: ${{ secrets.META_APP_ID }}
          META_APP_SECRET: ${{ secrets.META_APP_SECRET }}
          META_ACCESS_TOKEN: ${{ secrets.META_ACCESS_TOKEN }}
          AD_ACCOUNT_ID: ${{ secrets.AD_ACCOUNT_ID }}
          TELEGRAM_BOT_TOKEN: ${{ secrets.TELEGRAM_BOT_TOKEN }}
          TELEGRAM_CHAT_ID: ${{ secrets.TELEGRAM_CHAT_ID }}
        run: python backend/app/cpa_monitor.py

# Este workflow executa o script de monitorização de CPA (CPA Guard) a cada 15 minutos.
```

Para que este workflow funcione, precisa de configurar as **GitHub Secrets** (diferentes das do Streamlit). Vá a `Settings > Secrets and variables > Actions` no seu repositório e adicione as mesmas chaves que usou no Streamlit Cloud.

Com este guia, tem tudo o que precisa para lançar e manter o seu SaaS AdsGuardian AI a funcionar de forma autónoma e gratuita.

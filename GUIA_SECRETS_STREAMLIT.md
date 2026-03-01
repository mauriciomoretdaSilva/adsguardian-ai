
# Guia: Configurar Secrets no Streamlit Community Cloud

Para que a sua aplicação online funcione, ela precisa de aceder às mesmas chaves de API (Supabase, Stripe, Meta, etc.) que usou localmente. O Streamlit Community Cloud tem um sistema de "Secrets" seguro para isso, que substitui o seu ficheiro `.env` local.

## O Formato Correto: TOML

O Streamlit Cloud não usa o formato `.env`. Em vez disso, ele usa o formato **TOML**. A estrutura é muito semelhante.

**Exemplo do formato TOML para as nossas secrets:**

```toml
# Ficheiro de exemplo, não use estas chaves

# Supabase
SUPABASE_URL = "https://seu-projeto.supabase.co"
SUPABASE_KEY = "sua-chave-anon-aqui"

# Stripe
STRIPE_SECRET_KEY = "sk_test_..."
STRIPE_WEBHOOK_SECRET = "whsec_..."

# Meta (Facebook)
META_APP_ID = "1234567890"
META_APP_SECRET = "seu-app-secret"
META_ACCESS_TOKEN = "seu-token-de-longa-duracao"
AD_ACCOUNT_ID = "act_123456789"

# Telegram
TELEGRAM_BOT_TOKEN = "seu-token-de-bot"
TELEGRAM_CHAT_ID = "seu-chat-id"

# OpenAI / LLM
OPENAI_API_KEY = "sua-chave-de-api"
```

## Como Adicionar as Secrets no Streamlit Cloud

Existem duas formas de adicionar as suas secrets:

### Método 1: Durante o Deploy

1.  Ao fazer o deploy da sua app, antes de clicar em "Deploy!", clique em **"Advanced settings..."**.
2.  Irá aparecer uma caixa de texto com o título **"Secrets"**.
3.  **Copie e cole todo o conteúdo** do seu ficheiro de secrets em formato TOML (como o exemplo acima) para dentro desta caixa.
4.  Clique em **"Save"** e depois em **"Deploy!"**.

### Método 2: Após o Deploy (para atualizar)

1.  No seu workspace do Streamlit Cloud, encontre a sua aplicação.
2.  Clique nos três pontos (`...`) ao lado do nome da app e selecione **"Settings"**.
3.  No menu à esquerda, clique em **"Secrets"**.
4.  Aqui pode ver, adicionar, editar ou apagar as suas secrets.

## Como o Código Acede às Secrets

O nosso código já está preparado para isto. A biblioteca `python-dotenv` (que lê o ficheiro `.env`) só funciona localmente. No ambiente do Streamlit Cloud, as secrets que configurou são automaticamente carregadas como variáveis de ambiente, e `os.getenv("SUA_CHAVE")` irá funcionar na perfeição.

**Importante:**

*   **Nunca** coloque as suas chaves diretamente no código.
*   **Nunca** faça commit do seu ficheiro de secrets para o GitHub.
*   As secrets no Streamlit Cloud são encriptadas e seguras.

Ao seguir estes passos, garante que a sua aplicação online tem acesso a todas as APIs de que precisa, mantendo as suas credenciais completamente protegidas.

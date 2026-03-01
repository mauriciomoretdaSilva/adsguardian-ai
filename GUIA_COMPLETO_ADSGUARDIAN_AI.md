
# Guia: Deploy Gratuito no Streamlit Community Cloud

O Streamlit Community Cloud é a forma mais rápida e gratuita de colocar a sua aplicação online, com um link `.streamlit.app` partilhável. Este guia mostra como conectar o seu repositório do GitHub e fazer o deploy.

## Pré-requisitos

1.  **Conta no GitHub:** O seu projeto AdsGuardian AI já deve estar num repositório GitHub.
2.  **Conta no Streamlit Community Cloud:** Crie uma conta gratuita em [share.streamlit.io](https://share.streamlit.io/) usando a sua conta do GitHub.

## Passo a Passo para o Deploy

1.  **Aceda ao seu Workspace:**
    *   Faça login em [share.streamlit.io](https://share.streamlit.io/).
    *   Será direcionado para o seu workspace, onde pode ver todas as suas apps.

2.  **Crie uma Nova App:**
    *   No canto superior direito, clique no botão **"New app"**.

3.  **Configure o Repositório:**
    *   **Repository:** Selecione o seu repositório `adsguardian_ai` na lista. Se não aparecer, verifique se deu permissão ao Streamlit para aceder aos seus repositórios.
    *   **Branch:** Selecione a branch principal do seu projeto (normalmente `main` ou `master`).
    *   **Main file path:** Este é o caminho para o ficheiro principal do seu frontend. Para o nosso projeto, é: `frontend/main.py`.

4.  **Escolha um URL Personalizado (Opcional, mas recomendado):**
    *   No campo **"App URL"**, pode definir um subdomínio personalizado. É muito mais profissional e fácil de lembrar.
    *   Sugestão: `adsguardian` (o que resultaria em `adsguardian.streamlit.app`).

5.  **Clique em "Deploy!":**
    *   O Streamlit irá começar a construir o ambiente, instalar as dependências do `requirements.txt` e iniciar a sua aplicação.
    *   Pode acompanhar o processo em tempo real na janela de logs que aparece.

Em poucos minutos, a sua aplicação estará online e acessível a qualquer pessoa através do link que definiu!

## Manutenção e Atualizações

A melhor parte do Streamlit Community Cloud é a integração contínua:

*   **Atualizações Automáticas:** Sempre que fizer um `git push` para a branch principal do seu repositório no GitHub, o Streamlit deteta a alteração e **atualiza a sua aplicação automaticamente**. Não precisa de fazer deploy novamente.

*   **Hibernação:** As apps no plano gratuito podem "hibernar" após um período de inatividade. Isto significa que o primeiro utilizador a aceder à app após algum tempo pode ter de esperar um pouco mais para que ela "acorde".

Com estes passos, o seu frontend estará totalmente funcional e acessível globalmente, sem qualquer alteração que fizer no código será refletida online assim que a enviar para o GitHub.

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

# Checklist Final de Verificação - AdsGuardian AI

Parabéns por chegar até aqui! Este checklist garante que todos os componentes do seu SaaS estão configurados e a funcionar corretamente antes do lançamento.

## 1. Configuração do Repositório GitHub

- [ ] O projeto completo está no seu repositório GitHub.
- [ ] O ficheiro `.gitignore` está a ignorar a pasta `__pycache__` e ficheiros `.env`.
- [ ] Todas as 11 **GitHub Secrets** estão configuradas em `Settings > Secrets and variables > Actions`.

| Secret | Serviço | Status |
|---|---|---|
| `META_APP_ID` | Meta for Developers | [ ] Adicionada |
| `META_APP_SECRET` | Meta for Developers | [ ] Adicionada |
| `META_ACCESS_TOKEN` | Meta (Token de longa duração) | [ ] Adicionada |
| `AD_ACCOUNT_ID` | Meta Ads | [ ] Adicionada |
| `SUPABASE_URL` | Supabase | [ ] Adicionada |
| `SUPABASE_KEY` | Supabase | [ ] Adicionada |
| `STRIPE_SECRET_KEY` | Stripe | [ ] Adicionada |
| `STRIPE_WEBHOOK_SECRET` | Stripe | [ ] Adicionada |
| `TELEGRAM_BOT_TOKEN` | Telegram | [ ] Adicionada |
| `TELEGRAM_CHAT_ID` | Telegram | [ ] Adicionada |
| `OPENAI_API_KEY` | OpenAI / LLM | [ ] Adicionada |

## 2. Verificação dos GitHub Actions (Automations)

- [ ] **Ação 1: Monitorização de CPA (`cpa_monitor.yml`)**
    - [ ] Vá à aba **"Actions"** do seu repositório.
    - [ ] Encontre o workflow "Monitorização de CPA do AdsGuardian AI".
    - [ ] Verifique se ele está a ser executado **a cada 15 minutos**.
    - [ ] Clique numa das execuções recentes e verifique se o log termina com sucesso (um visto verde ✅).
    - [ ] Para forçar um teste, pode ir à página do workflow e clicar em **"Run workflow"**.

- [ ] **Ação 2: Régua de Comunicação (`trial_expiry_notifier.yml`)**
    - [ ] Na mesma aba "Actions", encontre o workflow "Régua de Comunicação".
    - [ ] Verifique se ele está configurado para rodar diariamente (`schedule: cron: '0 10 * * *'`).
    - [ ] Execute-o manualmente (`Run workflow`) para garantir que não há erros de configuração.

## 3. Verificação do Deploy no Streamlit Community Cloud

- [ ] A sua aplicação está online no URL `.streamlit.app` que escolheu.
- [ ] Consegue fazer login com um utilizador criado no Supabase.
- [ ] A página de dashboard carrega sem erros.
- [ ] A página "Insights de IA" funciona, classificando comentários e gerando roteiros.
- [ ] As **Secrets** foram adicionadas corretamente nas configurações da app no Streamlit Cloud (em formato TOML).

## 4. Verificação dos Serviços Externos

- [ ] **Supabase:**
    - [ ] As tabelas (`meta_connections`, `campaign_data`) e as colunas na tabela `profiles` (`stripe_customer_id`, `subscription_status`) foram criadas.
    - [ ] A autenticação de utilizadores está a funcionar.

- [ ] **Stripe:**
    - [ ] O script `stripe_config.py` foi executado e o produto/preço foram criados no seu dashboard do Stripe.
    - [ ] O endpoint do **Webhook** está configurado para receber os eventos `customer.subscription.*`.
    - [ ] A chave secreta do webhook (`whsec_...`) está configurada tanto no GitHub como no Streamlit Cloud.

- [ ] **Meta for Developers:**
    - [ ] A sua App está em modo "Live" (ou em modo de desenvolvimento, se for apenas para si).
    - [ ] As permissões `ads_read`, `ads_management` e `pages_read_engagement` foram aprovadas.

- [ ] **Telegram:**
    - [ ] O bot foi criado com o @BotFather.
    - [ ] O Token e o Chat ID estão corretos nas secrets.
    - [ ] Recebeu uma notificação de teste ao executar o `cpa_monitor.py` manualmente.

Se todos os itens deste checklist estiverem marcados, o seu SaaS AdsGuardian AI está 100% funcional, automatizado e pronto para ser usado!

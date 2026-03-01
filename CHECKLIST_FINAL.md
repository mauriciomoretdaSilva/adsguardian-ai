
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

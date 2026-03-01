# AdsGuardian AI

**AdsGuardian AI** é um SaaS de monitorização inteligente de anúncios Meta com IA, pausa automática de CPA e notificações Telegram.

## Funcionalidades

- Login e registo de utilizadores via Supabase
- Integração com Meta Ads API (leitura de campanhas e CPA)
- Monitorização automática de CPA a cada 15 minutos
- Pausa automática de anúncios quando CPA sobe 30%
- Classificação de comentários com IA (Dúvida, Crítica, Elogio)
- Geração de roteiros para Reels com IA
- Notificações via Telegram
- Faturação com Stripe (R$ 97/mês, 45 dias trial)
- Painel de Admin exclusivo

## Stack Tecnológica

- **Backend:** FastAPI + Python
- **Frontend:** Streamlit (Dark Mode)
- **Base de Dados:** Supabase (PostgreSQL)
- **IA:** OpenAI API
- **Pagamentos:** Stripe
- **Notificações:** Telegram Bot API
- **Automação:** GitHub Actions

## Instalação

```bash
pip install -r requirements.txt
```

## Execução

```bash
# Backend
cd backend && uvicorn app.main:app --reload

# Frontend
cd frontend && streamlit run main.py
```

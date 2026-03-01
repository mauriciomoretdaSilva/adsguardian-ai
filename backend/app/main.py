
# adsguardian_ai/backend/app/main.py

from fastapi import FastAPI, Depends
from app.subscription_middleware import check_subscription_status
from app.routers import auth, meta, ai_insights

app = FastAPI(
    title="AdsGuardian AI API",
    description="API para o SaaS AdsGuardian AI, com gestão de utilizadores e funcionalidades de IA.",
    version="0.1.0",
    # O middleware será aplicado a todas as rotas, exceto as isentas
    # dependencies=[Depends(check_subscription_status)] # Descomentar para ativar globalmente
)

# Inclui os routers
app.include_router(auth.router)
app.include_router(meta.router)
app.include_router(ai_insights.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bem-vindo à API do AdsGuardian AI"}

# Exemplo de como proteger uma rota específica com o middleware
@app.post("/protected-route", dependencies=[Depends(check_subscription_status)])
async def protected_route(user_id: str):
    return {"message": f"Olá, utilizador {user_id}! A sua subscrição está ativa."}

# Inclui o router de webhook do Stripe
from app.routers import stripe_webhook
app.include_router(stripe_webhook.router)
'''
# Inclui o router de administração
from app.routers import admin
app.include_router(admin.router)
'''

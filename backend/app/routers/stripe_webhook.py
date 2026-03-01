
# adsguardian_ai/backend/app/routers/stripe_webhook.py

from fastapi import APIRouter, Request, HTTPException, Header
import stripe
import os
from app.config import supabase

router = APIRouter()

# Configura a chave secreta do endpoint do webhook
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")
webhook_secret = os.getenv("STRIPE_WEBHOOK_SECRET")

@router.post("/stripe/webhook", tags=["Stripe"])
async def stripe_webhook(request: Request, stripe_signature: str = Header(None)):
    """Endpoint para receber eventos do Stripe e atualizar o status da subscrição no Supabase."""
    if webhook_secret is None:
        raise HTTPException(status_code=500, detail="A chave secreta do webhook do Stripe não está configurada.")

    payload = await request.body()
    
    try:
        event = stripe.Webhook.construct_event(
            payload=payload, sig_header=stripe_signature, secret=webhook_secret
        )
    except ValueError as e: # Assinatura inválida
        raise HTTPException(status_code=400, detail=f"Payload inválido: {e}")
    except stripe.error.SignatureVerificationError as e: # Assinatura inválida
        raise HTTPException(status_code=400, detail=f"Erro na verificação da assinatura: {e}")

    # Lida com o evento
    if event["type"] in ["customer.subscription.created", "customer.subscription.updated", "customer.subscription.deleted"]:
        subscription = event["data"]["object"]
        customer_id = subscription["customer"]
        status = subscription["status"]

        try:
            # Encontra o user_id no Supabase com base no customer_id do Stripe
            response = supabase.table("users")\
                .select("id")\
                .eq("stripe_customer_id", customer_id)\
                .single()\
                .execute()

            if response.data:
                user_id = response.data["id"]
                
                # Atualiza o status da subscrição no Supabase
                supabase.table("users")\
                    .update({"subscription_status": status})\
                    .eq("id", user_id)\
                    .execute()
                
                print(f"Status da subscrição do utilizador {user_id} atualizado para: {status}")

        except Exception as e:
            print(f"Erro ao atualizar o status no Supabase: {e}")
            # Numa app de produção, aqui seria um bom lugar para logar o erro
            # para que possa ser investigado manualmente.

    return {"status": "success"}

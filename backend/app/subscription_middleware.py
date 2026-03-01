
# adsguardian_ai/backend/app/subscription_middleware.py

from fastapi import Request, HTTPException
from app.config import supabase

async def check_subscription_status(request: Request):
    """
    Middleware para verificar o status da subscrição de um utilizador antes de permitir
    a execução de uma ação protegida (como uma automação).
    """
    # Rotas que não precisam de verificação de subscrição
    exempt_paths = ["/docs", "/openapi.json", "/auth/", "/stripe/webhook"]
    if any(request.url.path.startswith(path) for path in exempt_paths):
        return

    # Extrai o user_id do corpo da requisição (ou de um header, se preferir)
    try:
        body = await request.json()
        user_id = body.get("user_id")
    except Exception:
        # Se não houver corpo JSON, ou não tiver user_id, a rota pode ser pública
        return

    if not user_id:
        # Se a rota requer um user_id mas não o tem, é um erro de requisição
        # Mas para um middleware genérico, é melhor deixar passar e a rota lida com isso
        return

    try:
        # Consulta o status da subscrição no Supabase
        response = supabase.table("users")\
            .select("subscription_status")\
            .eq("id", user_id)\
            .single()\
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Utilizador não encontrado.")

        status = response.data.get("subscription_status")
        allowed_statuses = ["active", "trialling"]

        if status not in allowed_statuses:
            raise HTTPException(
                status_code=403, 
                detail=f"A sua subscrição não está ativa. Status atual: {status}. Por favor, atualize a sua subscrição para continuar."
            )

    except HTTPException as http_exc:
        raise http_exc # Re-levanta a exceção para que o FastAPI a trate
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao verificar a subscrição: {e}")

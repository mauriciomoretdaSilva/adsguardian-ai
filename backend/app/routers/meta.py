
# adsguardian_ai/backend/app/routers/meta.py

from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from app.config import supabase
from app.meta_auth import get_authorization_url, get_long_lived_access_token
from app.meta_reader import get_campaign_insights

router = APIRouter()

class MetaConnection(BaseModel):
    user_id: str
    ad_account_id: str

@router.get("/meta/authorize", tags=["Meta Integration"])
async def meta_authorize():
    """Redireciona o utilizador para a página de autorização da Meta."""
    auth_url = get_authorization_url()
    return RedirectResponse(url=auth_url)

@router.get("/meta/callback", tags=["Meta Integration"])
async def meta_callback(code: str, user_id: str, ad_account_id: str):
    """Callback da Meta após autorização. Troca o código por um token e guarda no Supabase."""
    try:
        access_token, expires_in = get_long_lived_access_token(code)
        
        # Guarda o token e o ID da conta de anúncios no Supabase
        # Assumindo que tem uma tabela 'meta_connections' com colunas: user_id, ad_account_id, access_token
        data, count = supabase.table('meta_connections').upsert({
            'user_id': user_id,
            'ad_account_id': ad_account_id,
            'access_token': access_token,
            'expires_in': expires_in
        }).execute()

        return {"message": "Autorização com a Meta concluída com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro na autorização com a Meta: {e}")

@router.post("/meta/sync-campaigns", tags=["Meta Integration"])
async def sync_campaigns(connection: MetaConnection):
    """Sincroniza os dados das campanhas da Meta para o Supabase."""
    try:
        # 1. Obtém o token de acesso do Supabase
        response = supabase.table('meta_connections')\
            .select('access_token')\
            .eq('user_id', connection.user_id)\
            .eq('ad_account_id', connection.ad_account_id)\
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Ligação com a Meta não encontrada para este utilizador.")

        access_token = response.data[0]['access_token']

        # 2. Busca os insights das campanhas
        campaign_data = get_campaign_insights(access_token, connection.ad_account_id)

        if not campaign_data:
            raise HTTPException(status_code=500, detail="Não foi possível obter os dados das campanhas.")

        # 3. Guarda os dados no Supabase
        # Assumindo uma tabela 'campaign_data' para armazenar os insights
        for campaign in campaign_data:
            # Adiciona o ID do utilizador para referência
            campaign['user_id'] = connection.user_id
            supabase.table('campaign_data').insert(campaign).execute()

        return {"message": f"{len(campaign_data)} campanhas sincronizadas com sucesso!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao sincronizar campanhas: {e}")


# adsguardian_ai/backend/app/routers/ai_insights.py

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.config import supabase
from app.meta_comments_reader import get_ad_comments
from app.meta_reader import get_campaign_insights
from app.ai_content_module import classify_and_suggest_response, generate_reels_script
import json

router = APIRouter()

class AIRequest(BaseModel):
    user_id: str
    ad_account_id: str

@router.post("/ai/analyze-comments", tags=["AI Insights"])
async def analyze_comments(request: AIRequest):
    """Busca comentários, classifica-os com IA e retorna as análises."""
    try:
        # 1. Obtém o token de acesso do Supabase
        response = supabase.table("meta_connections")\
            .select("access_token")\
            .eq("user_id", request.user_id)\
            .eq("ad_account_id", request.ad_account_id)\
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Ligação com a Meta não encontrada.")
        access_token = response.data[0]["access_token"]

        # 2. Busca os comentários dos anúncios
        comments = get_ad_comments(access_token, request.ad_account_id)
        if comments is None:
            raise HTTPException(status_code=500, detail="Erro ao buscar comentários da Meta.")

        # 3. Analisa cada comentário com IA
        analyzed_comments = []
        for comment in comments:
            analysis_json = classify_and_suggest_response(comment["message"])
            analysis = json.loads(analysis_json)
            comment.update(analysis)
            analyzed_comments.append(comment)

        return analyzed_comments

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/ai/generate-reel-script", tags=["AI Insights"])
async def get_reel_script(request: AIRequest):
    """Gera um roteiro de Reel com base no anúncio de maior performance (mais cliques)."""
    try:
        # 1. Obtém o token de acesso do Supabase
        response = supabase.table("meta_connections")\
            .select("access_token")\
            .eq("user_id", request.user_id)\
            .eq("ad_account_id", request.ad_account_id)\
            .execute()

        if not response.data:
            raise HTTPException(status_code=404, detail="Ligação com a Meta não encontrada.")
        access_token = response.data[0]["access_token"]

        # 2. Busca os insights das campanhas para encontrar a de maior performance
        campaign_insights = get_campaign_insights(access_token, request.ad_account_id)
        if not campaign_insights:
            raise HTTPException(status_code=404, detail="Nenhum dado de campanha encontrado.")

        # 3. Encontra a campanha com mais cliques
        top_campaign = max(campaign_insights, key=lambda x: int(x.get("clicks", 0)))

        # 4. Gera o roteiro de Reel com base na campanha de topo
        script = generate_reels_script(top_campaign["campaign_name"], top_campaign)

        return {"reel_script": script, "based_on_campaign": top_campaign["campaign_name"]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

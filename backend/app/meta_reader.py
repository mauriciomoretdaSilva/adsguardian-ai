
# adsguardian_ai/backend/app/meta_reader.py

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

def get_campaign_insights(access_token: str, ad_account_id: str):
    """Busca os insights das campanhas de uma conta de anúncios, incluindo o CPA."""
    try:
        FacebookAdsApi.init(app_id=META_APP_ID, app_secret=META_APP_SECRET, access_token=access_token)

        ad_account = AdAccount(f'act_{ad_account_id}')
        
        # Define os campos que queremos obter
        fields = [
            AdsInsights.Field.campaign_name,
            AdsInsights.Field.spend,
            AdsInsights.Field.impressions,
            AdsInsights.Field.clicks,
            AdsInsights.Field.cpc, # Custo por Clique
            AdsInsights.Field.ctr, # Click-Through Rate
            AdsInsights.Field.cost_per_action_type,
            AdsInsights.Field.actions, # Ações (conversões)
        ]

        # Define os parâmetros da consulta
        params = {
            'level': 'campaign',
            'date_preset': 'last_30d', # Últimos 30 dias
        }

        insights = ad_account.get_insights(fields=fields, params=params)

        campaign_data = []
        for insight in insights:
            # Extrai o CPA (Custo por Aquisição) - pode haver vários tipos de ação
            cpa_data = {}
            if insight.get(AdsInsights.Field.cost_per_action_type):
                for cpa in insight[AdsInsights.Field.cost_per_action_type]:
                    cpa_data[cpa['action_type']] = cpa['value']

            campaign_data.append({
                "campaign_name": insight[AdsInsights.Field.campaign_name],
                "spend": insight.get(AdsInsights.Field.spend, 0),
                "impressions": insight.get(AdsInsights.Field.impressions, 0),
                "clicks": insight.get(AdsInsights.Field.clicks, 0),
                "cpc": insight.get(AdsInsights.Field.cpc, 0),
                "ctr": insight.get(AdsInsights.Field.ctr, 0),
                "cpa": cpa_data, # Dicionário com CPAs por tipo de ação
            })
        
        return campaign_data

    except Exception as e:
        print(f"Erro ao buscar insights da campanha: {e}")
        return None

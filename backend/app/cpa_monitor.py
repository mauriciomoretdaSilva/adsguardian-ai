
# adsguardian_ai/backend/app/cpa_monitor.py

import os
import sys
from datetime import datetime, timedelta
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign
from facebook_business.adobjects.adsinsights import AdsInsights
from app.telegram_notifier import send_telegram_message

# --- Configuração Inicial ---

# Carrega as credenciais a partir das GitHub Secrets (variáveis de ambiente)
META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN") # Token de longa duração do utilizador
AD_ACCOUNT_ID = os.getenv("AD_ACCOUNT_ID")

# Define o limiar de aumento do CPA para acionar a pausa (30%)
CPA_INCREASE_THRESHOLD = 1.30

# --- Funções Auxiliares ---

def initialize_api():
    """Inicializa a API da Meta com as credenciais."""
    try:
        FacebookAdsApi.init(app_id=META_APP_ID, app_secret=META_APP_SECRET, access_token=ACCESS_TOKEN)
    except Exception as e:
        print(f"Erro ao inicializar a API da Meta: {e}")
        sys.exit(1)

def get_cpa_for_period(ad_account_id: str, time_range: dict):
    """Busca o CPA médio de todas as campanhas ativas para um determinado período."""
    try:
        ad_account = AdAccount(f'act_{ad_account_id}')
        
        fields = [
            AdsInsights.Field.spend,
            AdsInsights.Field.actions,
        ]
        
        params = {
            'level': 'account',
            'time_range': time_range,
            'filtering': [{'field': 'campaign.effective_status', 'operator': 'IN', 'value': ['ACTIVE']}]
        }

        insights = ad_account.get_insights(fields=fields, params=params)

        if not insights:
            return 0, 0 # Retorna 0 se não houver dados

        total_spend = float(insights[0][AdsInsights.Field.spend])
        
        # Foca numa ação de conversão principal, ex: 'offsite_conversion.fb_pixel_purchase'
        # Se não houver, pode usar 'actions' e pegar o total.
        total_actions = 0
        if insights[0].get(AdsInsights.Field.actions):
            for action in insights[0][AdsInsights.Field.actions]:
                # Tente encontrar uma ação de compra, senão use a primeira que encontrar
                if 'purchase' in action['action_type']:
                    total_actions = int(action['value'])
                    break
            if total_actions == 0: # Se não encontrou compra, usa o total de ações
                 total_actions = sum(int(a['value']) for a in insights[0][AdsInsights.Field.actions])

        if total_actions == 0:
            return 0, total_spend # Evita divisão por zero

        cpa = total_spend / total_actions
        return cpa, total_spend

    except Exception as e:
        print(f"Erro ao buscar CPA para o período {time_range}: {e}")
        return None, None

def pause_campaign(campaign_id: str):
    """Pausa uma campanha de anúncios específica."""
    try:
        campaign = Campaign(campaign_id)
        campaign.remote_update(params={
            'status': Campaign.Status.paused
        })
                print(f"SUCESSO: Campanha {campaign_id} foi pausada devido ao aumento do CPA.")
        # Envia notificação para o Telegram
        alert_message = (
            f"*🚨 Anúncio Pausado pelo AdsGuardian AI 🚨*\n\n"
            f"A campanha *{campaign_id}* foi pausada automaticamente devido a um aumento significativo no CPA."
        )
        send_telegram_message(alert_message)
    except Exception as e:
        print(f"ERRO: Falha ao pausar a campanha {campaign_id}: {e}")

# --- Lógica Principal do Script ---

if __name__ == "__main__":
    print("--- Iniciando Monitorização de CPA do AdsGuardian AI ---")
    initialize_api()

    if not all([META_APP_ID, META_APP_SECRET, ACCESS_TOKEN, AD_ACCOUNT_ID]):
        print("ERRO: As variáveis de ambiente (GitHub Secrets) não estão configuradas.")
        sys.exit(1)

    # Define os períodos de tempo
    today = datetime.now()
    yesterday = today - timedelta(days=1)
    day_before_yesterday = today - timedelta(days=2)

    # Período 1: Últimas 24 horas
    period1_range = {'since': yesterday.strftime('%Y-%m-%d'), 'until': today.strftime('%Y-%m-%d')}
    # Período 2: 24 horas anteriores
    period2_range = {'since': day_before_yesterday.strftime('%Y-%m-%d'), 'until': yesterday.strftime('%Y-%m-%d')}

    print(f"A calcular CPA para o período de {period1_range['since']} a {period1_range['until']}...")
    cpa_period1, spend_period1 = get_cpa_for_period(AD_ACCOUNT_ID, period1_range)

    print(f"A calcular CPA para o período de {period2_range['since']} a {period2_range['until']}...")
    cpa_period2, spend_period2 = get_cpa_for_period(AD_ACCOUNT_ID, period2_range)

    if cpa_period1 is None or cpa_period2 is None:
        print("Não foi possível calcular o CPA. A terminar o script.")
        sys.exit(1)

    print(f"CPA (últimas 24h): ${cpa_period1:.2f} (Gasto: ${spend_period1:.2f})")
    print(f"CPA (24h anteriores): ${cpa_period2:.2f} (Gasto: ${spend_period2:.2f})")

    # Verifica se o CPA do período anterior é válido para evitar falsos positivos
    if cpa_period2 > 0:
        # Calcula a variação do CPA
        cpa_variation = cpa_period1 / cpa_period2
        print(f"Variação do CPA: {cpa_variation:.2%}")

        if cpa_variation >= CPA_INCREASE_THRESHOLD:
            print(f"ALERTA: O CPA aumentou {cpa_variation:.2%}, que é acima do limiar de {CPA_INCREASE_THRESHOLD:.2%}.")
            
            # Lógica para pausar campanhas - aqui pausamos todas as ativas como exemplo
            # Numa implementação real, poderia ser mais seletivo
            try:
                ad_account = AdAccount(f'act_{AD_ACCOUNT_ID}')
                active_campaigns = ad_account.get_campaigns(fields=[Campaign.Field.id], params={'effective_status': ['ACTIVE']})
                
                if not active_campaigns:
                    print("Não foram encontradas campanhas ativas para pausar.")
                else:
                    for campaign in active_campaigns:
                        print(f"A pausar a campanha: {campaign['id']}")
                        pause_campaign(campaign['id'])
            except Exception as e:
                print(f"Erro ao obter a lista de campanhas ativas para pausar: {e}")
        else:
            print("CPA está dentro dos limites aceitáveis. Nenhuma ação necessária.")
    else:
        print("CPA do período anterior é zero. Não é possível calcular a variação.")

    print("--- Monitorização de CPA concluída ---")

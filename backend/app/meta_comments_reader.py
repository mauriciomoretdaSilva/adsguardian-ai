
# adsguardian_ai/backend/app/meta_comments_reader.py

from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.ad import Ad
from facebook_business.adobjects.adcreative import AdCreative

import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")

def get_ad_comments(access_token: str, ad_account_id: str):
    """Busca os comentários dos anúncios de uma conta."""
    try:
        FacebookAdsApi.init(app_id=META_APP_ID, app_secret=META_APP_SECRET, access_token=access_token)
        ad_account = AdAccount(f'act_{ad_account_id}')
        
        # 1. Obter todos os anúncios da conta
        ads = ad_account.get_ads(fields=[Ad.Field.id, Ad.Field.name, Ad.Field.creative])
        
        all_comments = []
        for ad in ads:
            if ad.get(Ad.Field.creative):
                creative_id = ad[Ad.Field.creative]['id']
                creative = AdCreative(creative_id)
                
                # 2. Obter o ID do post associado ao criativo do anúncio
                creative.remote_read(fields=[AdCreative.Field.effective_object_story_id])
                post_id = creative.get(AdCreative.Field.effective_object_story_id)

                if post_id:
                    # 3. Obter os comentários do post
                    # O SDK não tem um método direto para get_comments, então usamos uma chamada de API
                    api = FacebookAdsApi.get_default_api()
                    response = api.call(
                        'GET',
                        f'/{post_id}/comments',
                        params={'fields': 'message,from,created_time'}
                    )
                    comments = response.json().get('data', [])
                    
                    for comment in comments:
                        all_comments.append({
                            'ad_id': ad['id'],
                            'ad_name': ad['name'],
                            'post_id': post_id,
                            'comment_id': comment['id'],
                            'message': comment['message'],
                            'from_user': comment.get('from', {}).get('name', 'Utilizador Desconhecido'),
                            'created_time': comment['created_time']
                        })
        return all_comments

    except Exception as e:
        print(f"Erro ao buscar comentários dos anúncios: {e}")
        return None

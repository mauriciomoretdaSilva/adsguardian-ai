
# adsguardian_ai/backend/app/meta_auth.py

import os
import requests
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configurações da App Meta (a serem preenchidas pelo utilizador no ficheiro .env)
META_APP_ID = os.getenv("META_APP_ID")
META_APP_SECRET = os.getenv("META_APP_SECRET")
META_REDIRECT_URI = os.getenv("META_REDIRECT_URI")

API_VERSION = "v19.0" # Usar a versão mais recente da API

def get_authorization_url():
    """Gera a URL de autorização para o utilizador conceder permissões."""
    scope = "ads_read,ads_management" # Pedir permissões de leitura e gestão
    auth_url = f"https://www.facebook.com/{API_VERSION}/dialog/oauth?"
    auth_url += f"client_id={META_APP_ID}"
    auth_url += f"&redirect_uri={META_REDIRECT_URI}"
    auth_url += f"&scope={scope}"
    auth_url += "&response_type=code"
    return auth_url

def get_long_lived_access_token(code: str):
    """Troca um código de autorização por um token de acesso de longa duração."""
    # 1. Trocar o código por um token de acesso de curta duração
    token_url = f"https://graph.facebook.com/{API_VERSION}/oauth/access_token"
    token_params = {
        "client_id": META_APP_ID,
        "redirect_uri": META_REDIRECT_URI,
        "client_secret": META_APP_SECRET,
        "code": code
    }
    response = requests.get(token_url, params=token_params)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter token de curta duração: {response.json()}")
    
    short_lived_token = response.json().get("access_token")
    if not short_lived_token:
        raise Exception("Não foi possível obter o token de acesso de curta duração.")

    # 2. Trocar o token de curta duração por um de longa duração
    long_lived_token_url = f"https://graph.facebook.com/{API_VERSION}/oauth/access_token"
    long_lived_token_params = {
        "grant_type": "fb_exchange_token",
        "client_id": META_APP_ID,
        "client_secret": META_APP_SECRET,
        "fb_exchange_token": short_lived_token
    }
    response = requests.get(long_lived_token_url, params=long_lived_token_params)
    if response.status_code != 200:
        raise Exception(f"Erro ao obter token de longa duração: {response.json()}")

    long_lived_token_data = response.json()
    return long_lived_token_data.get("access_token"), long_lived_token_data.get("expires_in")

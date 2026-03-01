'''
# adsguardian_ai/backend/app/config.py

import os
from supabase import create_client, Client
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do ficheiro .env
load_dotenv()

# Configurações do Supabase
SUPABASE_URL: str = os.environ.get("SUPABASE_URL")
SUPABASE_KEY: str = os.environ.get("SUPABASE_KEY")
SUPABASE_SERVICE_KEY: str = os.environ.get("SUPABASE_SERVICE_KEY")

# Cria o cliente Supabase para operações normais (com a chave anon)
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Cria um cliente Supabase com a chave de serviço para operações de admin
supabase_admin: Client = create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
'''

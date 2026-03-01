
# adsguardian_ai/frontend/pages/3_Admin.py

import streamlit as st
import requests
import pandas as pd

# --- Configuração da Página ---
st.set_page_config(page_title="Admin - AdsGuardian AI", layout="wide")

# --- Proteção de Acesso ---
ADMIN_EMAIL = "mauricio.expert@gmail.com"

# Verifica se o utilizador está logado e se é o administrador
if 'user' not in st.session_state or st.session_state.user['email'] != ADMIN_EMAIL:
    st.error("Acesso negado. Esta página é exclusiva para administradores.")
    st.stop() # Interrompe a execução da página

# --- Funções da API ---
API_URL = "http://127.0.0.1:8000" # Mudar para o URL de produção quando fizer deploy

def get_all_users():
    response = requests.get(f"{API_URL}/admin/users")
    if response.status_code == 200:
        return response.json()
    return []

def suspend_user(user_id):
    response = requests.post(f"{API_URL}/admin/users/{user_id}/suspend")
    return response.status_code == 200

def delete_user(user_id):
    response = requests.delete(f"{API_URL}/admin/users/{user_id}")
    return response.status_code == 200

# --- Interface da Página de Admin ---

st.title("Painel de Administração")
st.markdown("Gestão de utilizadores e métricas da plataforma.")

# Carrega os dados dos utilizadores
users_data = get_all_users()

if not users_data:
    st.warning("Nenhum utilizador encontrado.")
else:
    df = pd.DataFrame(users_data)

    # --- Contadores ---
    total_users = len(df)
    trial_users = df[df['subscription_status'] == 'trialing'].shape[0]
    active_users = df[df['subscription_status'] == 'active'].shape[0]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Utilizadores", total_users)
    col2.metric("Utilizadores em Trial", trial_users)
    col3.metric("Utilizadores Pagantes", active_users)

    st.divider()

    # --- Tabela de Utilizadores ---
    st.subheader("Lista de Utilizadores")

    # Adiciona colunas para os botões
    df['Ações'] = ""

    # Usa st.data_editor para uma tabela mais interativa
    st.data_editor(df, disabled=True, use_container_width=True)

    st.subheader("Ações de Gestão")
    selected_user_email = st.selectbox("Selecione um utilizador para gerir:", options=df['email'])
    
    if selected_user_email:
        user_id = df[df['email'] == selected_user_email]['id'].iloc[0]
        
        col_suspend, col_delete = st.columns(2)
        
        with col_suspend:
            if st.button("Suspender Acesso", key=f"suspend_{user_id}"):
                if suspend_user(user_id):
                    st.success(f"Acesso do utilizador {selected_user_email} suspenso.")
                    st.experimental_rerun()
                else:
                    st.error("Falha ao suspender o utilizador.")
        
        with col_delete:
            if st.button("Excluir Utilizador", key=f"delete_{user_id}", type="primary"):
                if delete_user(user_id):
                    st.success(f"Utilizador {selected_user_email} excluído permanentemente.")
                    st.experimental_rerun()
                else:
                    st.error("Falha ao excluir o utilizador.")

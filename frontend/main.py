'''# adsguardian_ai/frontend/main.py

import streamlit as st
import requests

# URL da API do backend FastAPI
API_URL = "http://127.0.0.1:8000"

# Configuração da página
st.set_page_config(
    page_title="AdsGuardian AI - Login",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="collapsed",
)

# Função para aplicar o tema Dark Mode
def set_dark_mode():
    st.markdown("""
    <style>
    .stApp {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    </style>
    """, unsafe_allow_html=True)

# Aplica o Dark Mode
set_dark_mode()

# Título e subtítulo
st.title("AdsGuardian AI")
st.subheader("Faça login para aceder ao seu painel de controlo")

# Formulário de login
with st.form("login_form"):
    email = st.text_input("E-mail")
    password = st.text_input("Palavra-passe", type="password")
    submitted = st.form_submit_button("Entrar")

    if submitted:
        if not email or not password:
            st.error("Por favor, preencha todos os campos.")
        else:
            try:
                response = requests.post(f"{API_URL}/login", json={"email": email, "password": password})

                if response.status_code == 200:
                    st.success("Login bem-sucedido!")
                    st.session_state["logged_in"] = True
                    st.session_state["user_email"] = email
                    # Redireciona para o dashboard (o Streamlit trata disso)
                    st.switch_page("pages/dashboard.py")
                else:
                    st.error("E-mail ou palavra-passe inválidos.")
            except requests.exceptions.ConnectionError:
                st.error("Não foi possível conectar à API. Verifique se o backend está em execução.")

# Link para registo
st.markdown("Ainda não tem uma conta? [Registe-se aqui](#)") # Placeholder para a página de registo
'''

# adsguardian_ai/frontend/main.py

import streamlit as st
from supabase import create_client, Client

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

# Conexão com o Supabase
@st.cache_resource
def init_supabase_client():
    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]
    return create_client(supabase_url, supabase_key)

supabase: Client = init_supabase_client()

# Verifica se o utilizador já está logado
if "user" in st.session_state and st.session_state.user:
    st.switch_page("pages/dashboard.py")

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
                user = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = user.user.dict()
                st.session_state.logged_in = True
                st.success("Login bem-sucedido!")
                st.switch_page("pages/dashboard.py")
            except Exception as e:
                st.error(f"E-mail ou palavra-passe inválidos: {e}")

# Link para registo
st.markdown("Ainda não tem uma conta? [Registe-se aqui](#)") # Placeholder para a página de registo

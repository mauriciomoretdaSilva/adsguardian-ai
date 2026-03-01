# adsguardian_ai/frontend/pages/dashboard.py

import streamlit as st

# Verifica se o utilizador está logado
if not st.session_state.get("logged_in"):
    st.error("Acesso negado. Por favor, faça login primeiro.")
    st.stop()

# Título do dashboard
st.title(f"Bem-vindo ao seu Dashboard, {st.session_state.get('user_email')}!")
st.write("Aqui você poderá visualizar e gerir as suas campanhas de anúncios.")

# Placeholder para o conteúdo do dashboard
st.header("Métricas Principais")
col1, col2, col3 = st.columns(3)
col1.metric("Cliques", "1,234", "+5%")
col2.metric("Impressões", "56,789", "+8%")
col3.metric("CTR", "2.17%", "-0.2%")

# Botão de logout
if st.button("Sair"):
    st.session_state["logged_in"] = False
    st.session_state["user_email"] = None
    st.success("Logout bem-sucedido!")
    st.switch_page("main.py")

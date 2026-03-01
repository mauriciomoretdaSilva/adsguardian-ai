
# adsguardian_ai/frontend/pages/2_Insights_de_IA.py

import streamlit as st
import requests
import pandas as pd

# URL da API do backend FastAPI
API_URL = "http://127.0.0.1:8000"

# --- Configuração da Página ---
st.set_page_config(page_title="Insights de IA - AdsGuardian", layout="wide")

# Verifica se o utilizador está logado (assumindo que a session_state é partilhada)
if not st.session_state.get("logged_in"):
    st.error("Acesso negado. Por favor, faça login primeiro.")
    st.stop()

st.title("🤖 Insights de Conteúdo com IA")
st.write("Analise os comentários dos seus anúncios e gere ideias de conteúdo com o poder da IA.")

# --- Análise de Comentários ---
st.header("Análise de Comentários de Anúncios")

if st.button("Analisar Comentários Agora"):
    with st.spinner("A buscar e analisar comentários... Isto pode demorar alguns minutos."):
        try:
            # Assumindo que o user_id e ad_account_id estão guardados na session_state
            # Numa app real, isto seria obtido após o login e conexão com a Meta
            payload = {
                "user_id": st.session_state.get("user_id", "dummy_user_id"), # Substituir por real
                "ad_account_id": st.session_state.get("ad_account_id", "dummy_ad_account_id") # Substituir por real
            }
            response = requests.post(f"{API_URL}/ai/analyze-comments", json=payload)

            if response.status_code == 200:
                comments = response.json()
                if not comments:
                    st.info("Não foram encontrados comentários para analisar.")
                else:
                    st.success(f"{len(comments)} comentários analisados com sucesso!")
                    
                    # Converte para DataFrame para melhor visualização
                    df = pd.DataFrame(comments)
                    
                    # Mostra os resultados em abas
                    tab1, tab2, tab3 = st.tabs(["Dúvidas", "Críticas", "Elogios"])

                    with tab1:
                        st.subheader("Dúvidas dos Clientes")
                        for _, row in df[df["classification"] == "Dúvida"].iterrows():
                            with st.expander(f"**{row['from_user']}** em **{row['ad_name']}**"):
                                st.write(f"_Comentário:_ "{row['message']}"")
                                st.info(f"**Sugestão de Resposta:** {row['suggested_response']}")

                    with tab2:
                        st.subheader("Críticas e Pontos de Melhoria")
                        for _, row in df[df["classification"] == "Crítica"].iterrows():
                            with st.expander(f"**{row['from_user']}** em **{row['ad_name']}**"):
                                st.write(f"_Comentário:_ "{row['message']}"")
                                st.warning(f"**Sugestão de Resposta (Quebra de Objeção):** {row['suggested_response']}")

                    with tab3:
                        st.subheader("Elogios e Feedbacks Positivos")
                        for _, row in df[df["classification"] == "Elogio"].iterrows():
                            with st.expander(f"**{row['from_user']}** em **{row['ad_name']}**"):
                                st.write(f"_Comentário:_ "{row['message']}"")
                                st.success(f"**Sugestão de Resposta:** {row['suggested_response']}")
            else:
                st.error(f"Erro ao analisar comentários: {response.json().get('detail')}")
        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar à API. Verifique se o backend está em execução.")

# --- Geração de Roteiros para Reels ---
st.header("Gerador de Roteiros para Reels")
st.write("Crie um roteiro de 15 segundos para um Reel com base no seu anúncio de maior sucesso (mais cliques).")

if st.button("Gerar Roteiro de Reel"):
    with st.spinner("A IA está a criar o seu próximo viral..."):
        try:
            payload = {
                "user_id": st.session_state.get("user_id", "dummy_user_id"),
                "ad_account_id": st.session_state.get("ad_account_id", "dummy_ad_account_id")
            }
            response = requests.post(f"{API_URL}/ai/generate-reel-script", json=payload)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Roteiro gerado com base na campanha: **{data['based_on_campaign']}**")
                st.markdown(data["reel_script"])
            else:
                st.error(f"Erro ao gerar roteiro: {response.json().get('detail')}")
        except requests.exceptions.ConnectionError:
            st.error("Não foi possível conectar à API. Verifique se o backend está em execução.")

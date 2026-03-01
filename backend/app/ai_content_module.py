
# adsguardian_ai/backend/app/ai_content_module.py

from openai import OpenAI

# Inicializa o cliente OpenAI (a chave API é lida automaticamente das variáveis de ambiente)
client = OpenAI()

# --- Classificação de Comentários e Sugestão de Resposta ---

def classify_and_suggest_response(comment_text: str):
    """Usa um LLM para classificar um comentário e sugerir uma resposta."""
    try:
        system_prompt = (
            "Você é um assistente de IA especialista em redes sociais e atendimento ao cliente."
            "A sua tarefa é analisar um comentário de um anúncio e fazer duas coisas:"
            "1. Classificar o comentário em uma de três categorias: 'Dúvida', 'Crítica' ou 'Elogio'."
            "2. Sugerir uma resposta curta e profissional para quebrar a objeção ou interagir com o cliente."
            "A resposta deve ser concisa e adequada para uma rede social."
            "Retorne o resultado num formato JSON com as chaves 'classification' e 'suggested_response'."
        )

        response = client.chat.completions.create(
            model="gemini-2.5-flash", # Modelo rápido e eficiente para esta tarefa
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Analise o seguinte comentário: '{comment_text}'"}
            ],
            response_format={"type": "json_object"}
        )

        # Extrai o conteúdo JSON da resposta
        result = response.choices[0].message.content
        return result

    except Exception as e:
        print(f"Erro ao comunicar com a API da OpenAI: {e}")
        return {"classification": "Erro", "suggested_response": "Não foi possível analisar o comentário."}

# --- Geração de Roteiros para Reels ---

def generate_reels_script(ad_name: str, ad_performance: dict):
    """Gera um roteiro de 15 segundos para um Reel com base num anúncio de alta performance."""
    try:
        system_prompt = (
            "Você é um copywriter e especialista em vídeos curtos para redes sociais."
            "A sua tarefa é criar um roteiro de 15 segundos para um Instagram Reel com base num anúncio de sucesso."
            "O roteiro deve ser dinâmico, visual e terminar com uma forte chamada para a ação (CTA)."
            "Estruture o roteiro em 3 a 4 cenas curtas, descrevendo a imagem (visual) e a narração (áudio)."
            "O objetivo é capitalizar o sucesso do anúncio original e gerar mais engajamento."
            "Retorne o resultado como um texto simples em Markdown."
        )

        user_prompt = (
            f"Crie um roteiro de 15 segundos para um Reel baseado no seguinte anúncio de sucesso:\n\n"
            f"**Nome do Anúncio:** {ad_name}\n"
            f"**Performance:**\n"
            f"- Cliques: {ad_performance.get('clicks', 'N/A')}\n"
            f"- Impressões: {ad_performance.get('impressions', 'N/A')}\n"
            f"- CTR: {ad_performance.get('ctr', 'N/A')}%\n\n"
            "O roteiro deve capturar a essência do que tornou este anúncio eficaz."
        )

        response = client.chat.completions.create(
            model="gemini-2.5-flash",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ]
        )

        script = response.choices[0].message.content
        return script

    except Exception as e:
        print(f"Erro ao gerar roteiro de Reel: {e}")
        return "Não foi possível gerar o roteiro. Tente novamente mais tarde."

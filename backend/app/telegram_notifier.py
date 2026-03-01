
# adsguardian_ai/backend/app/telegram_notifier.py

import requests
import os

# Carrega as credenciais a partir das variáveis de ambiente
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message: str):
    """Envia uma mensagem para um chat do Telegram através de um bot."""
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("AVISO: As credenciais do Telegram (TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID) não estão configuradas. A mensagem não será enviada.")
        return False

    api_url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": message,
        "parse_mode": "Markdown"  # Permite formatação como negrito, itálico, etc.
    }

    try:
        response = requests.post(api_url, json=payload)
        response.raise_for_status()  # Lança uma exceção para respostas de erro (4xx ou 5xx)
        print(f"Mensagem enviada com sucesso para o Telegram!")
        return True
    except requests.exceptions.RequestException as e:
        print(f"ERRO: Falha ao enviar mensagem para o Telegram: {e}")
        return False

# Exemplo de como usar (para testes)
if __name__ == "__main__":
    test_message = (
        "*🚨 Alerta AdsGuardian AI 🚨*\n\n"
        "Este é um teste do sistema de notificações. Se recebeu esta mensagem, está tudo a funcionar corretamente!"
    )
    send_telegram_message(test_message)

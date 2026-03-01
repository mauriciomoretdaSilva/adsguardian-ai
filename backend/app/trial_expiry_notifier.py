
# adsguardian_ai/backend/app/trial_expiry_notifier.py

import os
import stripe
from datetime import datetime, timedelta
from app.config import supabase
from app.telegram_notifier import send_telegram_message
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a chave da API do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def check_trial_expirations():
    """
    Verifica as subscrições em trial que expiram em 5 dias e envia um aviso.
    """
    if not stripe.api_key:
        print("ERRO: A chave do Stripe não está configurada.")
        return

    print("--- Iniciando verificação de expiração de trials ---")

    try:
        # 1. Busca todas as subscrições ativas e em trial no Stripe
        subscriptions = stripe.Subscription.list(status="trialing", expand=["data.customer"])

        for sub in subscriptions.auto_paging_iter():
            trial_end_date = datetime.fromtimestamp(sub.trial_end)
            days_until_expiry = (trial_end_date - datetime.now()).days

            # 2. Verifica se o trial expira em exatamente 5 dias
            if days_until_expiry == 5:
                customer_id = sub.customer.id
                customer_email = sub.customer.email

                print(f"AVISO: O trial do cliente {customer_email} (ID: {customer_id}) expira em 5 dias.")

                # 3. Envia a notificação para o Telegram
                # (Numa app real, poderia também enviar um email para o cliente)
                message = (
                    f"*🔔 Lembrete de Faturação - AdsGuardian AI 🔔*\n\n"
                    f"O seu período de trial gratuito de 45 dias está a terminar. A sua primeira cobrança de R$ 97,00 será efetuada em 5 dias.\n\n"
                    f"Não é necessária nenhuma ação se desejar continuar. Para gerir a sua subscrição, aceda ao seu painel."
                )
                
                # Para enviar a mensagem para o utilizador, precisaríamos de ter o seu TELEGRAM_CHAT_ID
                # guardado no Supabase. Como não temos, vamos enviar um alerta geral para o admin.
                admin_message = (
                    f"*🔔 Alerta de Expiração de Trial 🔔*\n\n"
                    f"O trial do cliente *{customer_email}* (Stripe ID: {customer_id}) expira em 5 dias."
                )
                send_telegram_message(admin_message)

    except Exception as e:
        print(f"ERRO ao verificar expiração de trials: {e}")

if __name__ == "__main__":
    check_trial_expirations()

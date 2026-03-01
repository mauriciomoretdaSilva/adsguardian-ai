'''
Este script é para ser executado uma única vez para configurar o produto e o preço no Stripe.
Depois de executado, ele imprime o link de pagamento que pode ser usado no frontend.
'''

import stripe
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

# Configura a chave da API do Stripe
stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

def setup_stripe_product_and_price():
    """Cria o produto, o preço e o link de pagamento no Stripe."""
    try:
        # 1. Criar o produto "AdsGuardian AI Pro"
        print("A criar o produto no Stripe...")
        product = stripe.Product.create(
            name="AdsGuardian AI Pro",
            description="Acesso completo a todas as funcionalidades de monitorização e IA do AdsGuardian.",
        )
        print(f"Produto criado com sucesso! ID: {product.id}")

        # 2. Criar o preço de R$ 97,00/mês
        print("A criar o preço no Stripe...")
        price = stripe.Price.create(
            product=product.id,
            unit_amount=9700,  # Em centavos (R$ 97,00)
            currency="brl",
            recurring={"interval": "month"},
        )
        print(f"Preço criado com sucesso! ID: {price.id}")

        # 3. Criar o link de pagamento com 45 dias de trial
        print("A criar o link de pagamento no Stripe...")
        payment_link = stripe.PaymentLink.create(
            line_items=[{"price": price.id, "quantity": 1}],
            subscription_data={
                "trial_period_days": 45,
            },
            # Opcional: redirecionar para uma página de sucesso após a compra
            # after_completion={
            #     "type": "redirect",
            #     "redirect": {"url": "https://oseusite.com/sucesso"},
            # },
        )
        print(f"Link de pagamento criado com sucesso!")
        print("\n--- Link de Assinatura ---")
        print(payment_link.url)
        print("--------------------------\n")

        return payment_link.url

    except Exception as e:
        print(f"Ocorreu um erro ao configurar o Stripe: {e}")
        return None

if __name__ == "__main__":
    print("Iniciando a configuração do produto e preço no Stripe...")
    if not stripe.api_key:
        print("ERRO: A variável de ambiente STRIPE_SECRET_KEY não está definida.")
    else:
        setup_stripe_product_and_price()

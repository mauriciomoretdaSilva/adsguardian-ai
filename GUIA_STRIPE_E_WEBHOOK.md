
# Guia: Configurar o Stripe, Webhooks e Variáveis de Ambiente

Este guia explica como configurar o Stripe para aceitar pagamentos, como criar um webhook para que o Stripe possa comunicar com a sua aplicação, e como gerir as suas chaves de API de forma segura.

## Parte 1: Configurar as Chaves do Stripe

O Stripe usa duas chaves principais: uma **publicável** (para o frontend) e uma **secreta** (para o backend). Para este projeto, focamo-nos na chave secreta.

1.  **Aceda ao seu Dashboard do Stripe:** [dashboard.stripe.com](https://dashboard.stripe.com/)
2.  **Encontre as suas chaves de API:** No menu à esquerda, vá a **Developers** > **API keys**.
3.  **Copie a sua Chave Secreta (Secret key):** Clique em "Reveal test key" para a ver. Copie esta chave.

### Adicionar a Chave Secreta ao seu Projeto

Adicione a chave que copiou às suas variáveis de ambiente. No GitHub, adicione-a como um **Secret** (seguindo o guia anterior). Para desenvolvimento local, adicione-a ao seu ficheiro `.env` na pasta `backend/`:

```
# .env (na pasta backend/)
STRIPE_SECRET_KEY=sk_test_SUA_CHAVE_SECRETA_AQUI
```

## Parte 2: Configurar o Webhook do Stripe

Um webhook é um URL na sua aplicação que o Stripe chama sempre que um evento importante acontece (ex: um pagamento é bem-sucedido, uma subscrição é cancelada). O nosso endpoint ` /stripe/webhook` está pronto para receber estes eventos.

### Passo a Passo para Configurar o Webhook

1.  **Vá à secção de Webhooks no Stripe:** No menu **Developers**, clique em **Webhooks**.

2.  **Adicione um novo endpoint:** Clique em **+ Add endpoint**.

3.  **Preencha os detalhes do endpoint:**
    *   **Endpoint URL:** Este é o URL público da sua API. 
        *   Para **desenvolvimento local**, isto é um desafio, pois o seu computador não é acessível publicamente. A solução é usar a **Stripe CLI** para encaminhar os eventos para a sua máquina local. Siga as instruções abaixo.
        *   Para **produção**, será o URL do seu servidor, ex: `https://api.adsguardian.ai/stripe/webhook`.
    *   **Listen to:** Clique em **Select events** e escolha os seguintes eventos:
        *   `customer.subscription.created`
        *   `customer.subscription.updated`
        *   `customer.subscription.deleted`

4.  **Obtenha a Chave Secreta do Webhook (Signing secret):** Após criar o endpoint, o Stripe irá mostrar-lhe uma chave secreta específica para este webhook (começa com `whsec_...`). **Copie esta chave.**

5.  **Adicione a Chave Secreta do Webhook ao seu Projeto:** Tal como a chave secreta principal, adicione esta chave às suas GitHub Secrets e ao seu ficheiro `.env` local:

    ```
    # .env (na pasta backend/)
    STRIPE_WEBHOOK_SECRET=whsec_SUA_CHAVE_SECRETA_DO_WEBHOOK_AQUI
    ```

### Usar a Stripe CLI para Testes Locais

A Stripe CLI é uma ferramenta de linha de comando que facilita os testes de webhooks.

1.  **Instale a Stripe CLI:** Siga as instruções em [stripe.com/docs/stripe-cli](https://stripe.com/docs/stripe-cli).

2.  **Faça login na sua conta Stripe:**
    ```bash
    stripe login
    ```

3.  **Encaminhe os eventos para a sua API local:** Com a sua API FastAPI a correr (ex: na porta 8000), execute o seguinte comando:
    ```bash
    stripe listen --forward-to localhost:8000/stripe/webhook
    ```

    Este comando irá dar-lhe uma **nova chave secreta de webhook apenas para testes** (começa com `whsec_...`). Use esta chave no seu ficheiro `.env` enquanto estiver a desenvolver localmente.

    Agora, qualquer evento que aconteça na sua conta Stripe de teste será encaminhado para a sua API local, permitindo-lhe depurar o seu endpoint de webhook em tempo real.

## Parte 3: Executar o Script de Configuração do Produto

O ficheiro `backend/app/stripe_config.py` foi criado para configurar o seu produto e preço no Stripe. **Este script só precisa de ser executado uma vez.**

1.  Certifique-se de que a sua `STRIPE_SECRET_KEY` está no seu ficheiro `.env`.
2.  Execute o script a partir da pasta raiz do projeto:
    ```bash
    python backend/app/stripe_config.py
    ```
3.  O script irá imprimir na consola o **link de pagamento** para a sua subscrição de R$ 97,00 com 45 dias de trial. Copie este link e use-o no seu frontend (por exemplo, num botão "Assinar Agora").

Com estes passos, o seu sistema de faturação está totalmente configurado, seguro e pronto para automatizar a gestão de subscrições dos seus clientes.

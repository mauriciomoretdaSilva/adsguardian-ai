
# Guia: Criar um Bot no Telegram e Obter as Credenciais

Este guia explica como criar o seu próprio bot no Telegram para receber as notificações do AdsGuardian AI e como obter o **Token do Bot** e o seu **Chat ID**.

## Parte 1: Criar o seu Bot com o @BotFather

O Telegram tem um "pai de todos os bots" chamado **BotFather**. É com ele que vai interagir para criar e gerir os seus bots.

1.  **Inicie uma conversa com o BotFather:**
    *   Abra a sua aplicação do Telegram (Desktop ou Mobile).
    *   Na barra de pesquisa, procure por `@BotFather` (ele tem um selo de verificação azul).
    *   Clique nele e inicie uma conversa.

2.  **Crie um novo bot:**
    *   Digite o comando `/newbot` e envie.
    *   O BotFather vai pedir um **nome** para o seu bot. Este é o nome que aparece na lista de contactos. Pode ser algo como `AdsGuardian Notificações`.
    *   Depois, ele vai pedir um **username** para o bot. Este tem de ser único e terminar em `bot`. Por exemplo: `AdsGuardianAlertsBot`.

3.  **Receba o seu Token:**
    *   Se o username estiver disponível, o BotFather irá parabenizá-lo e dar-lhe uma mensagem importante que contém o **token de acesso à API HTTP**. 
    *   O token é uma longa sequência de números e letras, algo como `1234567890:AAH...`.
    *   **Guarde este token em segurança!** Ele é a "palavra-passe" do seu bot.

## Parte 2: Obter o seu Chat ID

O `Chat ID` diz ao seu bot *para quem* ele deve enviar a mensagem. Para notificações pessoais, este será o seu ID de utilizador do Telegram.

1.  **Inicie uma conversa com o seu novo bot:**
    *   Encontre o seu bot na pesquisa do Telegram (usando o username que criou, ex: `@AdsGuardianAlertsBot`).
    *   Clique nele e envie o comando `/start`.
    *   Isto é importante para que o bot o reconheça.

2.  **Obtenha o seu Chat ID:**
    *   Agora, abra o seu navegador de internet.
    *   Cole o seguinte URL na barra de endereços, **substituindo `{SEU_TOKEN_AQUI}` pelo token que recebeu do BotFather**:
        ```
        https://api.telegram.org/bot{SEU_TOKEN_AQUI}/getUpdates
        ```
    *   Pressione Enter. O navegador irá mostrar uma resposta em formato JSON.
    *   Procure por `"chat":{"id": ...}`. O número que aparece a seguir a `"id":` é o seu **Chat ID**.

    **Exemplo da resposta JSON:**
    ```json
    {
      "ok": true,
      "result": [
        {
          "update_id": 834572227,
          "message": {
            "message_id": 1,
            "from": { ... },
            "chat": {
              "id": 123456789,  // <-- ESTE É O SEU CHAT ID
              "first_name": "Seu Nome",
              "type": "private"
            },
            "date": 161... ,
            "text": "/start"
          }
        }
      ]
    }
    ```

## Parte 3: Adicionar as Credenciais ao seu Projeto

Agora que tem o **Token do Bot** e o seu **Chat ID**, precisa de os adicionar como variáveis de ambiente para que os scripts os possam usar de forma segura.

Adicione as seguintes chaves às suas **GitHub Secrets** (em `Settings > Secrets and variables > Actions`) e ao seu ficheiro `.env` local:

```
# .env (na pasta backend/)

# ... outras secrets ...

# Credenciais do Telegram
TELEGRAM_BOT_TOKEN=1234567890:AAH...
TELEGRAM_CHAT_ID=123456789
```

Com isto, o seu sistema de notificações está pronto a funcionar. Sempre que um evento for acionado (como um anúncio a ser pausado), receberá uma mensagem instantânea no seu Telegram!

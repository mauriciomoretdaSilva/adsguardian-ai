
# Guia: Deploy Gratuito no Streamlit Community Cloud

O Streamlit Community Cloud é a forma mais rápida e gratuita de colocar a sua aplicação online, com um link `.streamlit.app` partilhável. Este guia mostra como conectar o seu repositório do GitHub e fazer o deploy.

## Pré-requisitos

1.  **Conta no GitHub:** O seu projeto AdsGuardian AI já deve estar num repositório GitHub.
2.  **Conta no Streamlit Community Cloud:** Crie uma conta gratuita em [share.streamlit.io](https://share.streamlit.io/) usando a sua conta do GitHub.

## Passo a Passo para o Deploy

1.  **Aceda ao seu Workspace:**
    *   Faça login em [share.streamlit.io](https://share.streamlit.io/).
    *   Será direcionado para o seu workspace, onde pode ver todas as suas apps.

2.  **Crie uma Nova App:**
    *   No canto superior direito, clique no botão **"New app"**.

3.  **Configure o Repositório:**
    *   **Repository:** Selecione o seu repositório `adsguardian_ai` na lista. Se não aparecer, verifique se deu permissão ao Streamlit para aceder aos seus repositórios.
    *   **Branch:** Selecione a branch principal do seu projeto (normalmente `main` ou `master`).
    *   **Main file path:** Este é o caminho para o ficheiro principal do seu frontend. Para o nosso projeto, é: `frontend/main.py`.

4.  **Escolha um URL Personalizado (Opcional, mas recomendado):**
    *   No campo **"App URL"**, pode definir um subdomínio personalizado. É muito mais profissional e fácil de lembrar.
    *   Sugestão: `adsguardian` (o que resultaria em `adsguardian.streamlit.app`).

5.  **Clique em "Deploy!":**
    *   O Streamlit irá começar a construir o ambiente, instalar as dependências do `requirements.txt` e iniciar a sua aplicação.
    *   Pode acompanhar o processo em tempo real na janela de logs que aparece.

Em poucos minutos, a sua aplicação estará online e acessível a qualquer pessoa através do link que definiu!

## Manutenção e Atualizações

A melhor parte do Streamlit Community Cloud é a integração contínua:

*   **Atualizações Automáticas:** Sempre que fizer um `git push` para a branch principal do seu repositório no GitHub, o Streamlit deteta a alteração e **atualiza a sua aplicação automaticamente**. Não precisa de fazer deploy novamente.

*   **Hibernação:** As apps no plano gratuito podem "hibernar" após um período de inatividade. Isto significa que o primeiro utilizador a aceder à app após algum tempo pode ter de esperar um pouco mais para que ela "acorde".

Com estes passos, o seu frontend estará totalmente funcional e acessível globalmente, sem qualquer alteração que fizer no código será refletida online assim que a enviar para o GitHub.

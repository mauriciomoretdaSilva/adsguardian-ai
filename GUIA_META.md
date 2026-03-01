
# Guia: Configurar a App no Meta for Developers e Obter Permissões

Este guia explica, passo a passo, como configurar a sua aplicação no painel da Meta for Developers para obter as permissões necessárias para que o AdsGuardian AI possa ler os dados das suas campanhas de anúncios.

## Passo 1: Criar uma Aplicação na Meta for Developers

1.  **Aceda ao portal:** Vá a [developers.facebook.com](https://developers.facebook.com/) e inicie sessão com a sua conta do Facebook.

2.  **Crie uma nova App:**
    *   Clique em **As minhas apps** no canto superior direito.
    *   Clique no botão verde **Criar aplicação**.
    *   Selecione o tipo de aplicação **Empresa** e clique em **Seguinte**.
    *   Preencha os detalhes:
        *   **Nome da aplicação:** `AdsGuardian AI` (ou outro nome à sua escolha).
        *   **E-mail de contacto da aplicação:** O seu e-mail.
        *   **Conta do Gestor de Negócios (opcional):** Se tiver uma, pode associá-la. Não é obrigatório para começar.
    *   Clique em **Criar aplicação**. Poderá ter de introduzir a sua palavra-passe do Facebook para confirmar.

## Passo 2: Configurar o Login com o Facebook (OAuth)

Agora que a aplicação está criada, precisa de configurar o produto "Login com o Facebook", que é o responsável pelo fluxo de autorização.

1.  No painel da sua aplicação, no menu à esquerda, procure por **Adicionar produtos** e encontre **Login com o Facebook**. Clique em **Configurar**.

2.  Será levado para as definições do Login com o Facebook. No menu à esquerda, clique em **Definições**.

3.  **Configurar URIs de redirecionamento do OAuth:**
    *   No campo **URIs de redirecionamento do OAuth válidos**, tem de inserir o URL exato para onde a Meta irá redirecionar o utilizador após a autorização. No nosso caso, será o endpoint `/meta/callback` da nossa API FastAPI.
    *   O URL será algo como: `http://127.0.0.1:8000/meta/callback` (para testes locais) ou `https://oseudominio.com/meta/callback` (quando a aplicação estiver online).
    *   **Importante:** Insira este URL e clique em **Guardar alterações** no fundo da página.

## Passo 3: Adicionar as Permissões Necessárias

Por defeito, a sua aplicação tem acesso muito limitado. Precisamos de pedir as permissões corretas para ler os dados dos anúncios.

1.  No menu à esquerda, vá a **Revisão da aplicação** > **Permissões e funcionalidades**.

2.  Procure pelas seguintes permissões e clique em **Obter acesso avançado** para cada uma delas:
    *   `ads_read`: Permite que a sua aplicação **leia** os dados das suas contas de anúncios, incluindo campanhas, conjuntos de anúncios, anúncios e as suas métricas de desempenho (como o CPA).
    *   `ads_management`: Permite que a sua aplicação **leia e modifique** os dados das suas contas de anúncios. Embora o nosso script atual apenas leia dados, é uma boa prática pedir esta permissão caso queira adicionar funcionalidades de gestão no futuro.

3.  **Modo de Desenvolvimento vs. Modo Público:**
    *   Enquanto a sua aplicação estiver em **modo de desenvolvimento**, apenas os administradores, programadores e testadores da aplicação podem conceder estas permissões. Isto é perfeito para testar.
    *   Para que qualquer utilizador possa usar a sua aplicação, terá de passar pelo processo de **Revisão da Aplicação** da Meta, onde terá de explicar como e por que a sua aplicação usa estas permissões. Por agora, pode manter a aplicação em modo de desenvolvimento.

## Passo 4: Obter as Credenciais da Aplicação (App ID e App Secret)

Estas credenciais são essenciais para que o nosso script Python se possa identificar junto da API da Meta.

1.  No menu à esquerda, vá a **Definições** > **Básicas**.

2.  Aqui encontrará:
    *   **ID da aplicação:** O seu `META_APP_ID`.
    *   **Chave secreta da aplicação:** O seu `META_APP_SECRET`. Clique em **Mostrar** para a visualizar.

3.  **Copie estes valores** e cole-os no seu ficheiro `.env` na pasta `backend/`, juntamente com o URI de redirecionamento que configurou:

    ```
    # .env (na pasta backend/)
    SUPABASE_URL=SUA_URL_DO_SUPABASE
    SUPABASE_KEY=SUA_CHAVE_ANON_DO_SUPABASE

    META_APP_ID=O_SEU_ID_DA_APLICAÇÃO
    META_APP_SECRET=A_SUA_CHAVE_SECRETA_DA_APLICAÇÃO
    META_REDIRECT_URI=http://127.0.0.1:8000/meta/callback
    ```

## Resumo das Permissões

| Permissão | Descrição | Por que precisamos dela? |
|---|---|---|
| `ads_read` | Permite ler dados de contas de anúncios. | Essencial para obter o nome da campanha, o gasto e as métricas de desempenho como o CPA. |
| `ads_management` | Permite ler e gerir contas de anúncios. | Recomendado para futuras funcionalidades de otimização ou gestão de campanhas. |
| **Funcionalidade** | **Acesso Standard à Gestão de Anúncios** | Esta é uma funcionalidade que é automaticamente concedida com as permissões acima e é necessária para usar a Marketing API. |

Com estes passos, a sua aplicação na Meta for Developers está configurada para o fluxo de autorização e pronta para que o AdsGuardian AI comece a ler os dados das suas campanhas!

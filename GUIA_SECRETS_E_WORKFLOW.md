
# Guia: Configurar Chaves Secretas e Ativar o Workflow no GitHub

Este guia explica como guardar as suas chaves de API (API Keys) de forma segura no GitHub usando **Secrets** e como garantir que o seu workflow de monitorização de CPA é ativado e executado corretamente.

## Parte 1: Onde Colar as Suas Chaves Secretas (API Keys)

Nunca deve colocar chaves de API, tokens ou palavras-passe diretamente no seu código. O GitHub oferece uma funcionalidade chamada **Secrets** que armazena estas informações de forma encriptada e segura, disponibilizando-as ao seu workflow apenas durante a execução.

### Passo a Passo para Adicionar Secrets

1.  **Navegue até ao seu repositório no GitHub.**

2.  Clique no separador **Settings** (Definições) no menu superior do repositório.

3.  No menu à esquerda, navegue até **Secrets and variables** > **Actions**.

4.  Clique no botão verde **New repository secret** para adicionar a sua primeira chave.

5.  **Adicione as seguintes quatro secrets**, uma a uma. Para cada uma, irá preencher o campo **Name** com o nome exato que fornecemos e o campo **Secret** com o valor correspondente.

| Nome da Secret (Name) | Onde encontrar o valor (Value) |
|---|---|
| `META_APP_ID` | O **ID da aplicação** que obteve no painel da Meta for Developers. |
| `META_APP_SECRET` | A **Chave secreta da aplicação** que obteve no painel da Meta for Developers. |
| `META_ACCESS_TOKEN` | O **token de acesso de longa duração** do utilizador. Terá de o obter uma vez através do fluxo OAuth que criámos (executando a API localmente e autorizando) e depois colar aqui. Este token dura cerca de 60 dias. |
| `AD_ACCOUNT_ID` | O **ID da sua conta de anúncios** da Meta (ex: `1234567890123456`). Pode encontrá-lo no URL quando está a gerir os seus anúncios no Gestor de Anúncios da Meta. |

**Exemplo ao adicionar a primeira secret:**
*   **Name:** `META_APP_ID`
*   **Secret:** `987654321098765` (cole aqui o seu ID da App)

Clique em **Add secret**. Repita o processo para as outras três chaves.

![Exemplo de como adicionar uma secret no GitHub](https://i.imgur.com/example.png) *(Nota: Imagem ilustrativa)*

Depois de adicionar as quatro secrets, a sua secção de Actions secrets deverá estar completa.

## Parte 2: Ativar e Verificar o Workflow de Monitorização

O ficheiro `.github/workflows/cpa_monitor.yml` que criámos já está configurado para ser executado automaticamente. No entanto, há alguns pontos a verificar.

### 1. O Workflow é Ativado Automaticamente

Assim que fizer o *commit* e o *push* do ficheiro `cpa_monitor.yml` para o seu repositório, o GitHub Actions irá detetá-lo e agendá-lo automaticamente. Não precisa de o "ligar" manualmente.

### 2. Como Verificar se o Workflow está a Ser Executado

1.  No seu repositório GitHub, clique no separador **Actions**.

2.  Na barra lateral esquerda, verá o nome do seu workflow: **"Monitorização de CPA do AdsGuardian AI"**. Clique nele.

3.  Aqui verá uma lista de todas as execuções (runs) do seu workflow. Como está agendado para cada 15 minutos, verá uma nova execução a aparecer nesse intervalo.

    *   **Ícone Verde (✔):** A execução foi concluída com sucesso.
    *   **Ícone Vermelho (✖):** A execução falhou. Pode clicar na execução para ver os logs e perceber o que correu mal (por exemplo, uma secret em falta ou um erro no script).
    *   **Ícone Amarelo (●):** A execução está em progresso.

### 3. Executar o Workflow Manualmente

O nosso ficheiro de workflow inclui a opção `workflow_dispatch:`, que lhe permite acionar o script manualmente a qualquer momento, o que é ótimo para testes.

1.  Vá ao separador **Actions** e selecione o workflow na lista.

2.  Verá uma mensagem a dizer **"This workflow has a workflow_dispatch event trigger."** e um botão **Run workflow** à direita.

3.  Clique em **Run workflow** para iniciar uma execução imediata.

## Resumo e Boas Práticas

- **Segurança em Primeiro Lugar:** As GitHub Secrets são a forma correta e segura de gerir credenciais. Nunca as exponha no código.
- **Monitorize os Logs:** Especialmente nas primeiras execuções, verifique os logs na secção **Actions** para garantir que o script está a correr como esperado e a aceder às secrets corretamente.
- **Limites do Plano Gratuito:** O plano gratuito do GitHub oferece 2000 minutos de execução por mês para repositórios privados, o que é mais do que suficiente para este workflow que demora apenas alguns segundos a cada 15 minutos.

Com estes passos, o seu sistema de monitorização de CPA está totalmente automatizado e seguro, a postos para proteger os seus orçamentos de publicidade!

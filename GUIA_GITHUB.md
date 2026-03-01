
# Guia: Como Criar um Repositório no GitHub e Adicionar Ficheiros (Usando Apenas o Navegador)

Este guia destina-se a utilizadores que não estão familiarizados com o Git ou a linha de comandos. Vamos criar um repositório no GitHub e adicionar os ficheiros do projeto **AdsGuardian AI** passo a passo, utilizando apenas a interface web do GitHub.

## Passo 1: Criar uma Conta no GitHub

Se ainda não tiver uma, o primeiro passo é criar uma conta gratuita no [GitHub](https://github.com/join).

## Passo 2: Criar um Novo Repositório

1.  Depois de iniciar sessão, clique no ícone **+** no canto superior direito da página e selecione **New repository**.

2.  **Preencha os detalhes do repositório:**
    *   **Repository name:** `AdsGuardian-AI` (ou outro nome à sua escolha). O GitHub irá verificar se o nome está disponível.
    *   **Description (opcional):** "Projeto SaaS para otimização de anúncios com FastAPI, Streamlit e Supabase."
    *   **Public/Private:** Escolha **Public** se quiser que qualquer pessoa possa ver o seu projeto. Escolha **Private** se quiser controlar quem o pode ver e aceder.
    *   **Initialize this repository with:**
        *   **NÃO** marque a opção "Add a README file". Já criámos um ficheiro `README.md` e vamos adicioná-lo manualmente.

3.  Clique no botão verde **Create repository**.

## Passo 3: Fazer o Upload da Estrutura de Pastas e Ficheiros

O GitHub não permite o upload de pastas vazias diretamente. A forma mais simples de recriar a estrutura é fazer o upload dos ficheiros um a um, e o GitHub criará as pastas automaticamente.

### 3.1. Adicionar o `README.md` e `requirements.txt`

1.  No seu novo repositório, clique no link **uploading an existing file**.

2.  Arraste e solte os ficheiros `README.md` e `requirements.txt` da sua pasta local para a área de upload do GitHub.

3.  No fundo da página, adicione uma mensagem de commit (por exemplo, "Commit inicial: Adiciona README e requirements") e clique em **Commit changes**.

### 3.2. Adicionar os Ficheiros do Backend

Agora, vamos adicionar os ficheiros da pasta `backend/`.

1.  Na página principal do seu repositório, clique no botão **Add file** e selecione **Upload files**.

2.  Arraste e solte os seguintes ficheiros:
    *   `backend/app/main.py`
    *   `backend/app/config.py`
    *   `backend/app/routers/auth.py`

3.  **Importante:** Para que o GitHub crie as pastas `backend/app/` e `backend/app/routers/`, terá de recriar o caminho no nome do ficheiro durante o upload, se necessário, ou fazer o upload para a pasta correta.

    *Uma forma mais fácil é navegar para a pasta `backend` no seu computador e arrastar os ficheiros para a interface do GitHub. O GitHub irá preservar a estrutura.*

    *Se isso não funcionar, pode criar os ficheiros manualmente:*

    a. Clique em **Add file** > **Create new file**.
    b. Na caixa de texto do nome do ficheiro, escreva `backend/app/main.py`. Ao escrever a `/`, o GitHub criará a pasta `backend` e a subpasta `app`.
    c. Cole o conteúdo do seu ficheiro `main.py` local no editor.
    d. Clique em **Commit new file**.
    e. Repita este processo para todos os outros ficheiros do backend.

4.  Adicione uma mensagem de commit (ex: "Adiciona ficheiros do backend") e clique em **Commit changes**.

### 3.3. Adicionar os Ficheiros do Frontend

Repita o processo para os ficheiros do frontend.

1.  Vá para a página principal do repositório, clique em **Add file** > **Upload files**.

2.  Arraste e solte os ficheiros:
    *   `frontend/main.py`
    *   `frontend/pages/dashboard.py`

3.  Tal como no backend, certifique-se de que a estrutura de pastas `frontend/` e `frontend/pages/` é criada.

4.  Adicione uma mensagem de commit (ex: "Adiciona ficheiros do frontend") e clique em **Commit changes**.

## Passo 4: Verificar a Estrutura

Após o upload de todos os ficheiros, a estrutura do seu repositório no GitHub deve ser idêntica à estrutura de pastas local que criámos:

```
AdsGuardian-AI/
├── backend/
│   └── app/
│       ├── main.py
│       ├── config.py
│       └── routers/
│           └── auth.py
├── frontend/
│   ├── main.py
│   └── pages/
│       └── dashboard.py
├── requirements.txt
└── README.md
```

**Parabéns!** O seu projeto está agora no GitHub. Pode partilhar o link do seu repositório com outras pessoas e continuar a fazer alterações utilizando a interface web.

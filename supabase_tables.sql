
-- =============================================
-- AdsGuardian AI - Tabelas do Supabase (v2)
-- =============================================

-- Tabela de utilizadores (gerida pelo Supabase Auth)
-- Vamos adicionar colunas ao perfil público do utilizador

-- Adiciona as colunas relacionadas com o Stripe à tabela de perfis dos utilizadores
-- (Supabase cria uma tabela `profiles` em `public` que espelha `auth.users`)
-- Se a sua tabela de perfis tiver um nome diferente, ajuste aqui.
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS stripe_customer_id TEXT,
ADD COLUMN IF NOT EXISTS subscription_status TEXT DEFAULT 'none';

-- Cria uma política para que os utilizadores possam ler os seus próprios dados de perfil
CREATE POLICY "Utilizadores podem ver os seus próprios perfis" 
ON public.profiles FOR SELECT
USING (auth.uid() = id);

-- Cria uma política para que os utilizadores possam atualizar os seus próprios perfis
CREATE POLICY "Utilizadores podem atualizar os seus próprios perfis" 
ON public.profiles FOR UPDATE
USING (auth.uid() = id);

-- =============================================
-- Tabelas de Integração com a Meta (já existentes)
-- =============================================

-- Tabela para guardar as ligações dos utilizadores com a Meta
CREATE TABLE IF NOT EXISTS meta_connections (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    ad_account_id TEXT NOT NULL,
    access_token TEXT NOT NULL,
    expires_in INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    UNIQUE(user_id, ad_account_id)
);

-- Tabela para guardar os dados das campanhas sincronizadas
CREATE TABLE IF NOT EXISTS campaign_data (
    id BIGSERIAL PRIMARY KEY,
    user_id UUID NOT NULL REFERENCES auth.users(id) ON DELETE CASCADE,
    campaign_name TEXT NOT NULL,
    spend NUMERIC(12, 2) DEFAULT 0,
    impressions BIGINT DEFAULT 0,
    clicks BIGINT DEFAULT 0,
    cpc NUMERIC(10, 4) DEFAULT 0,
    ctr NUMERIC(10, 4) DEFAULT 0,
    cpa JSONB DEFAULT 
'{}'::jsonb,
    synced_at TIMESTAMPTZ DEFAULT NOW()
);

-- Ativar RLS (Row Level Security) se ainda não estiver ativo
ALTER TABLE meta_connections ENABLE ROW LEVEL SECURITY;
ALTER TABLE campaign_data ENABLE ROW LEVEL SECURITY;

-- Políticas RLS (já existentes)
CREATE POLICY "Utilizadores podem ver as suas próprias ligações Meta"
    ON meta_connections FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Utilizadores podem inserir as suas próprias ligações Meta"
    ON meta_connections FOR INSERT
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Utilizadores podem atualizar as suas próprias ligações Meta"
    ON meta_connections FOR UPDATE
    USING (auth.uid() = user_id);

CREATE POLICY "Utilizadores podem ver os seus próprios dados de campanha"
    ON campaign_data FOR SELECT
    USING (auth.uid() = user_id);

CREATE POLICY "Utilizadores podem inserir os seus próprios dados de campanha"
    ON campaign_data FOR INSERT
    WITH CHECK (auth.uid() = user_id);

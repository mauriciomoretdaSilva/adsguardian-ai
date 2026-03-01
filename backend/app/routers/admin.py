'''
# adsguardian_ai/backend/app/routers/admin.py

from fastapi import APIRouter, HTTPException, Depends
from app.config import supabase, supabase_admin
import os

router = APIRouter()

# --- Dependência de Segurança para Rotas de Admin ---

async def verify_admin(admin_email: str = "mauricio.expert@gmail.com"):
    # Numa app de produção, esta verificação seria mais robusta, 
    # por exemplo, verificando um JWT com uma role de 'admin'.
    # Para este caso, vamos usar uma verificação simples baseada num email fixo.
    if admin_email != "mauricio.expert@gmail.com":
        raise HTTPException(status_code=403, detail="Acesso negado. Esta é uma rota de administrador.")

# --- Endpoints de Administração ---

@router.get("/admin/users", tags=["Admin"], dependencies=[Depends(verify_admin)])
async def list_users():
    """Lista todos os utilizadores registados no Supabase."""
    try:
        response = supabase.table("profiles").select("id, email, subscription_status, created_at").execute()
        if not response.data:
            return []
        return response.data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao listar utilizadores: {e}")

@router.post("/admin/users/{user_id}/suspend", tags=["Admin"], dependencies=[Depends(verify_admin)])
async def suspend_user(user_id: str):
    """Suspende o acesso de um utilizador, alterando o seu status para 'canceled'."""
    try:
        response = supabase.table("profiles").update({"subscription_status": "canceled"}).eq("id", user_id).execute()
        if not response.data:
            raise HTTPException(status_code=404, detail="Utilizador não encontrado.")
        return {"message": f"Utilizador {user_id} suspenso com sucesso."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao suspender o utilizador: {e}")

@router.delete("/admin/users/{user_id}", tags=["Admin"], dependencies=[Depends(verify_admin)])
async def delete_user(user_id: str):
    """Exclui um utilizador permanentemente do Supabase Auth."""
    try:
        # Esta operação requer a chave de serviço (admin) do Supabase
        response = supabase_admin.auth.admin.delete_user(user_id)
        return {"message": f"Utilizador {user_id} excluído com sucesso."}
    except Exception as e:
        # A API do Supabase pode não retornar um erro claro se o user não existir, 
        # então tratamos o sucesso como o cenário principal.
        if "user not found" in str(e).lower():
             raise HTTPException(status_code=404, detail="Utilizador não encontrado.")
        print(f"Erro ao excluir utilizador: {e}")
        raise HTTPException(status_code=500, detail=str(e))

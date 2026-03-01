# adsguardian_ai/backend/app/routers/auth.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.config import supabase

router = APIRouter()

class UserCredentials(BaseModel):
    email: str
    password: str

@router.post("/signup", tags=["Authentication"])
async def signup(credentials: UserCredentials):
    """Regista um novo utilizador no Supabase."""
    try:
        user = supabase.auth.sign_up({
            "email": credentials.email,
            "password": credentials.password,
        })
        if user:
            return {"message": "Utilizador registado com sucesso. Verifique o seu e-mail para confirmação."}
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erro no registo: {e}")

@router.post("/login", tags=["Authentication"])
async def login(credentials: UserCredentials):
    """Autentica um utilizador e retorna uma sessão."""
    try:
        session = supabase.auth.sign_in_with_password({
            "email": credentials.email,
            "password": credentials.password,
        })
        return {"message": "Login bem-sucedido", "session": session}
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"E-mail ou palavra-passe inválidos: {e}")

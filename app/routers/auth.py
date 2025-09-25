from fastapi import APIRouter, Depends, Query, Form
from app.services.auth_service import AuthService
from app.schemas.authSChema import LoginRequest, ResendVerificationEmailRequest
from app.services.email_service import EmailService

router = APIRouter()


def get_auth_service() -> AuthService:
    return AuthService()


def get_email_service() -> EmailService:
    return EmailService()


@router.post("/login")
async def login(
    login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):
    return await auth_service.login__user(
        login_request.email, login_request.password, {}
    )


@router.get("/verify-email")
async def verify_email(
    token: str = Query(...), auth_service: AuthService = Depends(get_auth_service)
):
    print(f"token: {token}")

    return await auth_service.verify_email(token)


@router.post("/resend-verification-email")
async def resend_verification_email(
    resend_verification_email_request: ResendVerificationEmailRequest,
    auth_service: AuthService = Depends(get_auth_service),
):
    return await auth_service.resend_verification_email(
        resend_verification_email_request.email
    )

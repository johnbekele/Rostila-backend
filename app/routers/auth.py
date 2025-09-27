from fastapi import APIRouter, Depends, Query, HTTPException, status,Form
from app.services.auth_service import AuthService
from app.schemas.authSChema import LoginRequest, ResendVerificationEmailRequest
from app.services.email_service import EmailService
from app.services.apple_auth import AppleJWTVerifier
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()


def get_auth_service() -> AuthService:
    return AuthService()


def get_email_service() -> EmailService:
    return EmailService()


@router.post("/login")
async def login(
    login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):  
   
    response = await auth_service.login__user(
        login_request.email, login_request.password, {}
    )
    print(f"response: {response}")
    return response


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

@router.post("/login/apple")
async def login_with_apple(token:str):
    user_sub = AppleJWTVerifier.verify_identity_token(token,client_id="com.rosti.app")
    return {"apple_sub":user_sub}


@router.post("/user-info")
async def get_user_info(
    credential: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    print(f"credential: {credential}")
    token = credential.credentials
    print(f"token: {token}")
    
    try:
        user_data = await auth_service.find_user(token)
        return user_data
    except HTTPException:
        # Re-raise HTTP exceptions (like 401, 404) as they are
        raise
    except Exception as e:
        # Handle any other unexpected errors
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )
    

    
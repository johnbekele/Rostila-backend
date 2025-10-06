from fastapi import APIRouter, Depends, Query, HTTPException, status,Form ,Request
from app.services.auth_service import AuthService
from app.schemas.auth_schema import LoginRequest, ResendVerificationEmailRequest
from app.services.email_service import EmailService
from app.services.apple_auth_service import AppleJWTVerifier
from app.core.security import security_manager
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

router = APIRouter()
security = HTTPBearer()


def get_auth_service() -> AuthService:
    return AuthService()


def get_email_service() -> EmailService:
    return EmailService()


@router.post("/login")
async def login(
    client_info: Request,
    login_request: LoginRequest, auth_service: AuthService = Depends(get_auth_service)
):  
   
    response = await auth_service.login__user(
        login_request.email, login_request.password,client_info
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
async def find_user(
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

@router.post("/find/user")
async def find_user_alt(
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

@router.post("/token-info")
async def get_token_info(
    credential: HTTPAuthorizationCredentials = Depends(security),
    auth_service: AuthService = Depends(get_auth_service)
):
    """Get detailed token information including company and IP data"""
    token = credential.credentials
    
    try:
        # Decode the token to get all the information
        response = security_manager.decode_token(token)
        payload = response.get("payload")
        
        if not payload:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token"
            )
        
        return {
            "success": True,
            "token_info": {
                "username": payload.get("sub"),
                "user_id": payload.get("user_id"),
                "email": payload.get("email"),
                "first_name": payload.get("first_name"),
                "last_name": payload.get("last_name"),
                "phone_number": payload.get("phone_number"),
                "company_name": payload.get("company_name"),
                "company_address": payload.get("company_address"),
                "company_phone_number": payload.get("company_phone_number"),
                "company_email": payload.get("company_email"),
                "company_website": payload.get("company_website"),
                "is_verified": payload.get("is_verified"),
                "last_ip": payload.get("last_ip"),
                "last_device": payload.get("last_device"),
                "login_time": payload.get("login_time"),
                "expires_at": payload.get("exp"),
                "issued_at": payload.get("iat")
            }
        }
    except Exception as e:
        print(f"Error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    

    
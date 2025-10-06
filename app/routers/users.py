from fastapi import APIRouter, Depends, HTTPException, Request
from app.services.user_service import UserService
from app.schemas.user_schema import UserCreate
import traceback

router = APIRouter()


def get_user_service() -> UserService:
    return UserService()


@router.get("/")
async def get_users(user_service: UserService = Depends(get_user_service)):
    return await user_service.get_all_users()


@router.post("/signup")
async def create_user(
    user_data: UserCreate, 
    request: Request,
    user_service: UserService = Depends(get_user_service)
):
    try:
        print(f"Received user data: {user_data}")
        
        # Extract client info for tracking
        client_ip = request.headers.get("x-forwarded-for") or request.headers.get("x-real-ip") or request.client.host
        user_agent = request.headers.get("user-agent", "unknown")
        
        print(f"Client IP: {client_ip}")
        print(f"User Agent: {user_agent}")
        
        result = await user_service.create_user(user_data, client_ip, user_agent)
        print(f"User created successfully: {result}")
        return result
    except Exception as e:
        print(f"Error creating user: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Error creating user: {str(e)}")


@router.post("/test-validation")
async def test_validation(request: Request):
    """Test endpoint to debug validation issues"""
    try:
        body = await request.json()
        print(f"Raw request body: {body}")
        
        # Try to parse with UserCreate schema
        user_data = UserCreate(**body)
        print(f"Parsed user data: {user_data}")
        return {"message": "Validation successful", "data": user_data}
    except Exception as e:
        print(f"Validation error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return {"error": str(e), "type": type(e).__name__}

@router.post("/{email}")
async def getUser_byemail(
    email: str, user_service: UserService = Depends(get_user_service)
):
    print("find Function invoked")
    return await user_service.get_user_by_email(email)

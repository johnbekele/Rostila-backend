from fastapi import APIRouter, Depends
from app.services.coffee_service import CoffeeService
from app.schemas.coffee_schema import CoffeeCreate, CoffeeUpdate, CoffeeResponse

router = APIRouter()

def get_coffee_service() -> CoffeeService:
    return CoffeeService()

@router.post("/create-coffee")
async def create_coffee(coffee: CoffeeCreate, coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.create_coffee(coffee)

@router.get("/")
async def get_all_coffees(coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.get_all_coffees()

@router.get("/{coffee_id}")
async def get_coffee_by_id(coffee_id: str, coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.get_coffee_by_id(coffee_id)

@router.get("/name/{coffee_name}")
async def get_coffee_by_name(coffee_name: str, coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.get_coffee_by_name(coffee_name)

@router.get("/origin/{origin}")
async def get_coffees_by_origin(origin: str, coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.get_coffees_by_origin(origin)

@router.get("/region/{region}")
async def get_coffees_by_region(region: str, coffee_service: CoffeeService = Depends(get_coffee_service)):
    return await coffee_service.get_coffees_by_region(region)

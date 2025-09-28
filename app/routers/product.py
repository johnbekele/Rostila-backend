from fastapi import APIRouter, Depends
from app.services.product_service import ProductService
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse

router = APIRouter()

def get_product_service() -> ProductService:
    return ProductService()

@router.post("/create-product")
async def create_product(product: ProductCreate, product_service: ProductService = Depends(get_product_service)):
    return await product_service.create_product(product)

@router.get("/")
async def get_all_products(product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_all_products()

@router.get("/{product_id}")
async def get_product_by_id(product_id: str, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_product_by_id(product_id)

@router.get("/{product_name}")
async def get_product_by_name(product_name: str, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_product_by_name(product_name)

@router.get("/{origin}")
async def get_products_by_origin(origin: str, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_products_by_origin(origin)

@router.get("/{region}")
async def get_products_by_region(region: str, product_service: ProductService = Depends(get_product_service)):
    return await product_service.get_products_by_region(region)
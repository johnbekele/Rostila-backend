from app.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate, ProductResponse
from app.models.product import Product
from typing import List, Optional

class ProductService:
    def __init__(self):
        self.product_repository = ProductRepository()

    async def create_product(self, product: ProductCreate) -> ProductResponse:
        """Create a new product"""
        created_product = await self.product_repository.create_product(product)
        return ProductResponse.model_validate(created_product.model_dump())

    async def update_product(self, product_id: str, product: ProductUpdate) -> ProductResponse:
        """Update an existing product"""
        updated_product = await self.product_repository.update_product(product_id, product)
        return ProductResponse.model_validate(updated_product.model_dump())

    async def delete_product(self, product_id: str) -> bool:
        """Delete a product by ID"""
        return await self.product_repository.delete_product(product_id)

    async def get_product_by_id(self, product_id: str) -> Optional[ProductResponse]:
        """Get a product by ID"""
        product = await self.product_repository.get_product_by_id(product_id)
        if product:
            return ProductResponse.model_validate(product.model_dump())
        return None

    async def get_product_by_name(self, product_name: str) -> Optional[ProductResponse]:
        """Get a product by name"""
        product = await self.product_repository.get_product_by_name(product_name)
        if product:
            return ProductResponse.model_validate(product.model_dump())
        return None

    async def get_all_products(self) -> List[ProductResponse]:
        """Get all products"""
        products = await self.product_repository.get_all_products()
        return [ProductResponse.model_validate(product.model_dump()) for product in products]

    async def get_products_by_origin(self, origin: str) -> List[ProductResponse]:
        """Get products by origin"""
        products = await self.product_repository.get_products_by_origin(origin)
        return [ProductResponse.model_validate(product.model_dump()) for product in products]

    async def get_products_by_region(self, region: str) -> List[ProductResponse]:
        """Get products by region"""
        products = await self.product_repository.get_products_by_region(region)
        return [ProductResponse.model_validate(product.model_dump()) for product in products]
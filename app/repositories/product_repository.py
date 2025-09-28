from app.repositories.base_repository import BaseRepository
from app.models.product import Product
from app.schemas.product_schema import ProductCreate, ProductUpdate
from typing import List

class ProductRepository(BaseRepository):
    def __init__(self):
        super().__init__(Product)

    async def create_product(self, product: ProductCreate) -> Product:
        return await self.create(product.model_dump())
    
    async def update_product(self, product_id: str, product: ProductUpdate) -> Product:
        return await self.update_one(product_id, product.model_dump())
    
    async def delete_product(self, product_id: str) -> bool:
        return await self.delete_By_ID(product_id)
    
    async def get_product_by_id(self, product_id: str) -> Product:
        return await self.find_by_ID(product_id)
    
    async def get_product_by_name(self, product_name: str) -> Product:
        return await self.find_one(name=product_name)
    
    async def get_all_products(self) -> List[Product]:
        return await self.find_all()
    
    async def get_products_by_origin(self, origin: str) -> List[Product]:
        return await self.find_one(origin=origin)
    
    async def get_products_by_region(self, region: str) -> List[Product]:
        return await self.find_one(region=region)
    
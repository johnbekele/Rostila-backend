from app.repositories.base_repository import BaseRepository
from app.models.coffee import Coffee
from app.schemas.coffee_schema import CoffeeCreate, CoffeeUpdate
from typing import List

class CoffeeRepository(BaseRepository):
    def __init__(self):
        super().__init__(Coffee)

    async def create_coffee(self, coffee: CoffeeCreate) -> Coffee:
        return await self.create(coffee.model_dump())
    
    async def update_coffee(self, coffee_id: str, coffee: CoffeeUpdate) -> Coffee:
        return await self.update_one(coffee_id, coffee.model_dump())
    
    async def delete_coffee(self, coffee_id: str) -> bool:
        return await self.delete_By_ID(coffee_id)
    
    async def get_coffee_by_id(self, coffee_id: str) -> Coffee:
        return await self.find_by_ID(coffee_id)
    
    async def get_coffee_by_name(self, coffee_name: str) -> Coffee:
        return await self.find_one(name=coffee_name)
    
    async def get_all_coffees(self) -> List[Coffee]:
        return await self.find_all()
    
    async def get_coffees_by_origin(self, origin: str) -> List[Coffee]:
        return await self.find_one(origin=origin)
    
    async def get_coffees_by_region(self, region: str) -> List[Coffee]:
        return await self.find_one(region=region)

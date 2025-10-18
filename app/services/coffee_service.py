from app.repositories.coffee_repository import CoffeeRepository
from app.schemas.coffee_schema import CoffeeCreate, CoffeeUpdate, CoffeeResponse
from app.models.coffee import Coffee
from typing import List, Optional

class CoffeeService:
    def __init__(self):
        self.coffee_repository = CoffeeRepository()

    async def create_coffee(self, coffee: CoffeeCreate) -> CoffeeResponse:
        """Create a new coffee"""
        created_coffee = await self.coffee_repository.create_coffee(coffee)
        return CoffeeResponse.model_validate(created_coffee.model_dump())

    async def update_coffee(self, coffee_id: str, coffee: CoffeeUpdate) -> CoffeeResponse:
        """Update an existing coffee"""
        updated_coffee = await self.coffee_repository.update_coffee(coffee_id, coffee)
        return CoffeeResponse.model_validate(updated_coffee.model_dump())

    async def delete_coffee(self, coffee_id: str) -> bool:
        """Delete a coffee by ID"""
        return await self.coffee_repository.delete_coffee(coffee_id)

    async def get_coffee_by_id(self, coffee_id: str) -> Optional[CoffeeResponse]:
        """Get a coffee by ID"""
        coffee = await self.coffee_repository.get_coffee_by_id(coffee_id)
        if coffee:
            return CoffeeResponse.model_validate(coffee.model_dump())
        return None

    async def get_coffee_by_name(self, coffee_name: str) -> Optional[CoffeeResponse]:
        """Get a coffee by name"""
        coffee = await self.coffee_repository.get_coffee_by_name(coffee_name)
        if coffee:
            return CoffeeResponse.model_validate(coffee.model_dump())
        return None

    async def get_all_coffees(self) -> List[CoffeeResponse]:
        """Get all coffees"""
        coffees = await self.coffee_repository.get_all_coffees()
        return [CoffeeResponse.model_validate(coffee.model_dump()) for coffee in coffees]

    async def get_coffees_by_origin(self, origin: str) -> List[CoffeeResponse]:
        """Get coffees by origin"""
        coffees = await self.coffee_repository.get_coffees_by_origin(origin)
        return [CoffeeResponse.model_validate(coffee.model_dump()) for coffee in coffees]

    async def get_coffees_by_region(self, region: str) -> List[CoffeeResponse]:
        """Get coffees by region"""
        coffees = await self.coffee_repository.get_coffees_by_region(region)
        return [CoffeeResponse.model_validate(coffee.model_dump()) for coffee in coffees]

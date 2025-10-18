# models/coffee.py
from beanie import Document, Indexed
from pydantic import Field
from datetime import datetime
from typing import Optional, List
from pymongo import IndexModel


class Coffee(Document):
    """
    Coffee model for Ethiopian coffee and related goods.
    Based on the provided schema.
    """

    # Basic identifiers
    name: Indexed(str)
    origin: Optional[str] = None
    region: Optional[str] = None

    # Producer details
    producer_id: Optional[str] = None
    producer_name: Optional[str] = None

    # Pricing
    price: float
    price_per_kg: Optional[float] = None
    currency: str = "USD"

    # Ratings
    rating: Optional[float] = 0.0
    reviews_count: Optional[int] = 0

    # Coffee-specific details
    processing: Optional[str] = Field(
        default=None, description="Washed, Natural, Honey, Semi-washed"
    )
    altitude: Optional[str] = None
    flavor_notes: List[str] = []
    cupping_score: Optional[float] = None
    moisture_content: Optional[str] = None
    density: Optional[str] = None
    screen_size: Optional[str] = None
    harvest_year: Optional[int] = None

    # Inventory
    availability: str = "In Stock"  # In Stock, Limited, Out of Stock
    quantity_available: int = 0
    unit: str = "kg"

    # Media & certifications
    images: List[str] = []
    certifications: List[str] = []  # Organic, Fair Trade, etc.

    # Commerce details
    description: Optional[str] = None
    shipping_time: Optional[str] = None
    min_order_quantity: int = 1
    max_order_quantity: Optional[int] = None

    # Flags
    is_featured: bool = False
    is_verified: bool = False

    # Metadata
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None

    class Settings:
        # MongoDB collection name
        collection = "coffees"

        # Indexes for optimization
        indexes = [
            IndexModel("name"),
            IndexModel("origin"),
            IndexModel("region"),
            IndexModel("producer_id"),
            IndexModel("availability"),
            IndexModel("created_at"),
        ]

# schemas/product_schema.py
from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class ProductBase(BaseModel):
    """Base product schema with common fields"""
    name: str = Field(..., min_length=1, max_length=200, description="Product name")
    origin: Optional[str] = Field(None, max_length=100, description="Country of origin")
    region: Optional[str] = Field(None, max_length=100, description="Region within the country")
    producer_id: Optional[str] = Field(None, max_length=100, description="Producer identifier")
    producer_name: Optional[str] = Field(None, max_length=200, description="Producer name")
    price: float = Field(..., gt=0, description="Price in the specified currency")
    price_per_kg: Optional[float] = Field(None, gt=0, description="Price per kilogram")
    currency: str = Field(default="USD", max_length=3, description="Currency code")
    processing: Optional[str] = Field(None, description="Processing method (Washed, Natural, Honey, Semi-washed)")
    altitude: Optional[str] = Field(None, max_length=50, description="Growing altitude")
    flavor_notes: List[str] = Field(default=[], description="Flavor profile notes")
    cupping_score: Optional[float] = Field(None, ge=0, le=100, description="Cupping score (0-100)")
    moisture_content: Optional[str] = Field(None, max_length=20, description="Moisture content percentage")
    density: Optional[str] = Field(None, max_length=20, description="Bean density")
    screen_size: Optional[str] = Field(None, max_length=20, description="Screen size")
    harvest_year: Optional[int] = Field(None, ge=2000, le=2030, description="Harvest year")
    availability: str = Field(default="In Stock", description="Availability status")
    quantity_available: int = Field(default=0, ge=0, description="Available quantity")
    unit: str = Field(default="kg", max_length=10, description="Unit of measurement")
    images: List[str] = Field(default=[], description="Product image URLs")
    certifications: List[str] = Field(default=[], description="Product certifications")
    description: Optional[str] = Field(None, max_length=2000, description="Product description")
    shipping_time: Optional[str] = Field(None, max_length=100, description="Estimated shipping time")
    min_order_quantity: int = Field(default=1, ge=1, description="Minimum order quantity")
    max_order_quantity: Optional[int] = Field(None, ge=1, description="Maximum order quantity")
    is_featured: bool = Field(default=False, description="Whether product is featured")
    is_verified: bool = Field(default=False, description="Whether product is verified")

    @validator("flavor_notes")
    def validate_flavor_notes(cls, v):
        if len(v) > 20:
            raise ValueError("Maximum 20 flavor notes allowed")
        return v

    @validator("images")
    def validate_images(cls, v):
        if len(v) > 10:
            raise ValueError("Maximum 10 images allowed")
        return v

    @validator("certifications")
    def validate_certifications(cls, v):
        if len(v) > 10:
            raise ValueError("Maximum 10 certifications allowed")
        return v


class ProductCreate(ProductBase):
    """Schema for creating a new product"""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product (all fields optional)"""
    name: Optional[str] = Field(None, min_length=1, max_length=200)
    origin: Optional[str] = Field(None, max_length=100)
    region: Optional[str] = Field(None, max_length=100)
    producer_id: Optional[str] = Field(None, max_length=100)
    producer_name: Optional[str] = Field(None, max_length=200)
    price: Optional[float] = Field(None, gt=0)
    price_per_kg: Optional[float] = Field(None, gt=0)
    currency: Optional[str] = Field(None, max_length=3)
    processing: Optional[str] = Field(None)
    altitude: Optional[str] = Field(None, max_length=50)
    flavor_notes: Optional[List[str]] = Field(None)
    cupping_score: Optional[float] = Field(None, ge=0, le=100)
    moisture_content: Optional[str] = Field(None, max_length=20)
    density: Optional[str] = Field(None, max_length=20)
    screen_size: Optional[str] = Field(None, max_length=20)
    harvest_year: Optional[int] = Field(None, ge=2000, le=2030)
    availability: Optional[str] = Field(None)
    quantity_available: Optional[int] = Field(None, ge=0)
    unit: Optional[str] = Field(None, max_length=10)
    images: Optional[List[str]] = Field(None)
    certifications: Optional[List[str]] = Field(None)
    description: Optional[str] = Field(None, max_length=2000)
    shipping_time: Optional[str] = Field(None, max_length=100)
    min_order_quantity: Optional[int] = Field(None, ge=1)
    max_order_quantity: Optional[int] = Field(None, ge=1)
    is_featured: Optional[bool] = Field(None)
    is_verified: Optional[bool] = Field(None)

    @validator("flavor_notes")
    def validate_flavor_notes(cls, v):
        if v is not None and len(v) > 20:
            raise ValueError("Maximum 20 flavor notes allowed")
        return v

    @validator("images")
    def validate_images(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Maximum 10 images allowed")
        return v

    @validator("certifications")
    def validate_certifications(cls, v):
        if v is not None and len(v) > 10:
            raise ValueError("Maximum 10 certifications allowed")
        return v


class ProductResponse(ProductBase):
    """Schema for product response (includes all fields plus metadata)"""
    id: str = Field(..., description="Product ID")
    rating: Optional[float] = Field(None, ge=0, le=5, description="Average rating")
    reviews_count: Optional[int] = Field(None, ge=0, description="Number of reviews")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        from_attributes = True


class ProductListResponse(BaseModel):
    """Schema for paginated product list response"""
    products: List[ProductResponse] = Field(..., description="List of products")
    total: int = Field(..., description="Total number of products")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Page size")
    pages: int = Field(..., ge=1, description="Total number of pages")


class ProductSearchRequest(BaseModel):
    """Schema for product search request"""
    query: Optional[str] = Field(None, max_length=200, description="Search query")
    origin: Optional[str] = Field(None, max_length=100, description="Filter by origin")
    region: Optional[str] = Field(None, max_length=100, description="Filter by region")
    processing: Optional[str] = Field(None, description="Filter by processing method")
    min_price: Optional[float] = Field(None, ge=0, description="Minimum price filter")
    max_price: Optional[float] = Field(None, ge=0, description="Maximum price filter")
    min_rating: Optional[float] = Field(None, ge=0, le=5, description="Minimum rating filter")
    availability: Optional[str] = Field(None, description="Filter by availability")
    is_featured: Optional[bool] = Field(None, description="Filter featured products")
    is_verified: Optional[bool] = Field(None, description="Filter verified products")
    page: int = Field(default=1, ge=1, description="Page number")
    size: int = Field(default=20, ge=1, le=100, description="Page size")
    sort_by: Optional[str] = Field(default="created_at", description="Sort field")
    sort_order: Optional[str] = Field(default="desc", description="Sort order (asc/desc)")

    @validator("max_price")
    def validate_price_range(cls, v, values):
        if v is not None and "min_price" in values and values["min_price"] is not None:
            if v < values["min_price"]:
                raise ValueError("max_price must be greater than min_price")
        return v

    @validator("sort_by")
    def validate_sort_by(cls, v):
        allowed_fields = [
            "name", "price", "rating", "created_at", "updated_at", 
            "cupping_score", "reviews_count"
        ]
        if v not in allowed_fields:
            raise ValueError(f"sort_by must be one of: {', '.join(allowed_fields)}")
        return v

    @validator("sort_order")
    def validate_sort_order(cls, v):
        if v not in ["asc", "desc"]:
            raise ValueError("sort_order must be 'asc' or 'desc'")
        return v


class ProductReviewRequest(BaseModel):
    """Schema for product review request"""
    rating: float = Field(..., ge=1, le=5, description="Rating from 1 to 5")
    comment: Optional[str] = Field(None, max_length=1000, description="Review comment")
    title: Optional[str] = Field(None, max_length=200, description="Review title")

    @validator("comment")
    def validate_comment(cls, v):
        if v is not None and len(v.strip()) < 10:
            raise ValueError("Comment must be at least 10 characters long")
        return v


class ProductReviewResponse(BaseModel):
    """Schema for product review response"""
    id: str = Field(..., description="Review ID")
    user_id: str = Field(..., description="User ID")
    product_id: str = Field(..., description="Product ID")
    rating: float = Field(..., ge=1, le=5, description="Rating")
    comment: Optional[str] = Field(None, description="Review comment")
    title: Optional[str] = Field(None, description="Review title")
    created_at: datetime = Field(..., description="Review creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Review update timestamp")

    class Config:
        from_attributes = True


class ProductStatsResponse(BaseModel):
    """Schema for product statistics response"""
    total_products: int = Field(..., description="Total number of products")
    featured_products: int = Field(..., description="Number of featured products")
    verified_products: int = Field(..., description="Number of verified products")
    average_rating: Optional[float] = Field(None, description="Average rating across all products")
    total_reviews: int = Field(..., description="Total number of reviews")
    price_range: dict = Field(..., description="Price range statistics")
    origin_distribution: dict = Field(..., description="Distribution by origin")
    processing_distribution: dict = Field(..., description="Distribution by processing method")

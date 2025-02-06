from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime 

# User Model
class User(BaseModel):
    name: str
    title:str
    designation:str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

# Product Model
class Product(BaseModel):
    name: str = Field(..., example="Wireless Headphones")
    description: Optional[str] = Field(None, example="Noise-canceling Bluetooth headphones")
    price: float = Field(..., example=29.99)
    stock: int = Field(..., example=50)
    category: Optional[str] = Field(None, example="Audio Accessories")
    image_url: Optional[str] = Field(None, example="https://example.com/image.jpg")

class ServiceRequest(BaseModel):
    customer_name: str = Field(..., example="John Doe")
    contact: str = Field(..., example="+254799954672")
    service_type: str = Field(..., example="TV Mounting")  # Includes installations & repairs
    item: Optional[str] = Field(None, example="LG 55-inch OLED TV")  # Optional field for the item
    description: str = Field(..., example="Wall mounting a 55-inch Samsung TV")
    assigned_technician: Optional[str] = None  # New field to track technician assignment
    scheduled_date: Optional[datetime] = Field(None, example="2025-02-10T15:30:00")
    status: str = Field(default="Pending", example="Pending")
    payment_status: str = Field(default="Unpaid", example="Unpaid")
    request_date: datetime = Field(default_factory=datetime.utcnow)
    completion_date: Optional[datetime] = None

class Technician(BaseModel):
    name: str = Field(..., example="Kevin Otieno")
    specializations: List[str] = Field(..., example=["TV Mounting", "Laptop Repair"])
    jobs_completed: int = Field(default=0)
    average_rating: float = Field(default=0.0)  # New field for ratings
    total_ratings: int = Field(default=0)  # To calculate average

class TechnicianRating(BaseModel):
    technician_id: str
    rating: int = Field(..., ge=1, le=5)  # 1-5 star rating
    feedback: str = Field(..., example="Great job, very professional!")

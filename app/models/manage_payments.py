from pydantic import BaseModel, Field, EmailStr
from typing import Optional, Dict

class CreatePaymentIntentRequest(BaseModel):
    amount: int = Field(..., gt=0, description="Amount in cents (e.g., 1000 for 10.00 EUR)")
    currency: str = Field(default="eur", description="Currency code (e.g., 'eur', 'usd')")
    metadata: Dict[str, str] = Field(default={}, description="Optional metadata for the payment")
    description: Optional[str] = Field(None, description="Description of the payment")
    receipt_email: Optional[EmailStr] = Field(None, description="Customer email for the receipt")
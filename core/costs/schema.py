from pydantic import BaseModel, Field, field_validator
import re


class CostSchema(BaseModel):
    description: str = Field(..., min_length=1, max_length=50)

    amount: float = Field(..., gt=0)

    @field_validator("description")
    @classmethod
    def validate_description(cls, value):
        pattern = r"^[a-zA-Z0-9\s]+$"

        if not re.match(pattern, value):
            raise ValueError("description cannot contain special characters or symbols")

        return value


class CostResponseSchema(BaseModel):
    id: int
    description: str
    amount: float

    model_config = {"from_attributes": True}

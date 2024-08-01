from datetime import datetime
from decimal import Decimal
from typing import Any
import uuid
from bson import Decimal128
from pydantic import UUID4, BaseModel, Field, model_validator


class CreateBaseModel(BaseModel):
    id: UUID4 = Field(default_factory=uuid.uuid4)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @model_validator(pre=True)
    def set_updated_at(cls, values: dict[str, Any]) -> dict[str, Any]:
        if 'updated_at' in values:
            values['updated_at'] = values['updated_at'] or datetime.now()
        return values

    def set_model(self) -> dict[str, Any]:
        self_dict = self.model_dump()
        for key, value in self_dict.items():
            if isinstance(value, Decimal):
                self_dict[key] = Decimal128(str(value))
        return self_dict

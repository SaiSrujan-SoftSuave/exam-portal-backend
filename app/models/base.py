from bson import ObjectId
from pydantic import BaseModel, Field
from typing import Optional, Any
from pydantic_core import core_schema


class PyObjectId(ObjectId):
    """
    Custom Pydantic type for MongoDB's ObjectId, compatible with Pydantic V2.
    """

    @classmethod
    def __get_pydantic_core_schema__(
            cls, source_type: Any, handler: Any
    ) -> core_schema.CoreSchema:
        """
        Defines the core schema for ObjectId validation.
        - For JSON Schema (OpenAPI), it's represented as a string.
        - For Python validation, it accepts a valid ObjectId string or an existing ObjectId instance.
        - For serialization, it converts the ObjectId to a string.
        """

        def validate_from_str(value: str) -> ObjectId:
            if not ObjectId.is_valid(value):
                raise ValueError("Invalid ObjectId")
            return ObjectId(value)

        from_str_schema = core_schema.chain_schema(
            [
                core_schema.str_schema(),
                core_schema.no_info_plain_validator_function(validate_from_str),
            ]
        )

        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema(
                [
                    core_schema.is_instance_schema(ObjectId),
                    from_str_schema,
                ]
            ),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda instance: str(instance)
            ),
        )


class BaseMongoModel(BaseModel):
    """
    A base model for all MongoDB documents.
    It includes a Pydantic-compatible `id` field that maps to MongoDB's `_id`.
    """
    id: PyObjectId = Field(alias="_id", default=None)

    class Config:
        populate_by_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}

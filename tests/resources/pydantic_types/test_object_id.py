import pytest
from bson import ObjectId
from pydantic import BaseModel

from src.resources.pydantic_types.object_id import PyObjectId


class ClassWithObjectId(BaseModel):
    id_: PyObjectId


def test_object_id_validation():
    valid_object_id = ObjectId()
    ClassWithObjectId(id_=str(valid_object_id))
    invalid_object_id = 'invalid_object_id'
    with pytest.raises(ValueError):
        ClassWithObjectId(id_=invalid_object_id)


def test_json_schema_of_object_id_is_string():
    schema = ClassWithObjectId.schema()
    assert schema['properties']['id_']['type'] == 'string'

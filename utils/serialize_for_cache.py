from pydantic import BaseModel

def get_serialized_for_cache(value: BaseModel | dict | str) -> dict | str:
    if isinstance(value, BaseModel):
        return value.model_dump()
    elif isinstance(value, (dict, str)):
        return value
    else:
        raise TypeError("Unsupported type for redis caching")
from pydantic import BaseModel, Field

class Params(BaseModel):
    unitGroup : str
    key : str
    include : str
    elements: str
    contentType : str 
    locationMode : str
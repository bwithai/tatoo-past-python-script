from pydantic import BaseModel


class SelectedRegion(BaseModel):
    width: int = 0
    height: int = 0
    x: int = 0
    y: int = 0

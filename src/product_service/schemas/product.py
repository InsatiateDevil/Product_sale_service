from pydantic import ConfigDict, BaseModel


# Product schemas
class ProductBase(BaseModel):
    name: str
    description: str
    price: int
    is_active: bool | None = None


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductCreate):
    pass


class ProductPartialUpdate(ProductCreate):
    name: str | None = None
    description: str | None = None
    price: int | None = None
    is_active: bool | None = None


class Product(ProductBase):
    model_config = ConfigDict(from_attributes=True)
    id: int

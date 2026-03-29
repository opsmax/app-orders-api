"""Pydantic models for the Orders API."""

from pydantic import BaseModel


class Order(BaseModel):
    id: int
    customer: str
    product: str
    quantity: int
    price: float
    status: str
    created_at: str


class HealthResponse(BaseModel):
    status: str
    database: str


class StatsResponse(BaseModel):
    total_orders: int
    total_revenue: float
    average_order_value: float
    orders_by_status: dict[str, int]
    top_products: list[dict[str, object]]


class AppInfo(BaseModel):
    app: str
    version: str
    description: str
    platform: str
    endpoints: dict[str, str]
    database: str

"""Orders API — IDP Reference Application."""

import os
from collections import Counter

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .database import is_db_available
from .mock_data import MOCK_ORDERS
from .models import AppInfo, HealthResponse, Order, StatsResponse

APP_VERSION = os.getenv("APP_VERSION", "1.0.0")

app = FastAPI(
    title="Orders API",
    description="IDP Reference Application — Orders API",
    version=APP_VERSION,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def _get_orders() -> list[dict]:
    """Return orders from DB if available, otherwise mock data."""
    if is_db_available():
        # Future: query PostgreSQL here
        pass
    return list(MOCK_ORDERS)


@app.get("/", response_model=AppInfo)
def root():
    """Welcome / info page."""
    db_status = "connected" if is_db_available() else "using mock data"
    return AppInfo(
        app="orders-api",
        version=APP_VERSION,
        description="IDP Reference Application — Orders API",
        platform="Internal Developer Platform",
        endpoints={
            "health": "/health",
            "orders": "/api/orders",
            "order_by_id": "/api/orders/{id}",
            "statistics": "/api/stats",
            "docs": "/docs",
        },
        database=db_status,
    )


@app.get("/health", response_model=HealthResponse)
def health():
    """Health check endpoint."""
    db_status = "connected" if is_db_available() else "unavailable"
    return HealthResponse(status="healthy", database=db_status)


@app.get("/api/orders", response_model=list[Order])
def list_orders():
    """List all orders."""
    return [Order(**o) for o in _get_orders()]


@app.get("/api/orders/{order_id}", response_model=Order)
def get_order(order_id: int):
    """Get a single order by ID."""
    for o in _get_orders():
        if o["id"] == order_id:
            return Order(**o)
    raise HTTPException(status_code=404, detail=f"Order {order_id} not found")


@app.get("/api/stats", response_model=StatsResponse)
def order_stats():
    """Aggregate order statistics."""
    orders = _get_orders()
    total_revenue = sum(o["price"] * o["quantity"] for o in orders)
    avg_value = total_revenue / len(orders) if orders else 0.0

    status_counts: dict[str, int] = dict(Counter(o["status"] for o in orders))

    product_revenue: dict[str, float] = {}
    for o in orders:
        product_revenue[o["product"]] = product_revenue.get(o["product"], 0) + (
            o["price"] * o["quantity"]
        )
    top_products = sorted(
        [{"product": k, "revenue": v} for k, v in product_revenue.items()],
        key=lambda x: x["revenue"],
        reverse=True,
    )

    return StatsResponse(
        total_orders=len(orders),
        total_revenue=round(total_revenue, 2),
        average_order_value=round(avg_value, 2),
        orders_by_status=status_counts,
        top_products=top_products,
    )

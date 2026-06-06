"""Configuration for the Product Routing Worker."""
from __future__ import annotations

import os
from dataclasses import dataclass


@dataclass(frozen=True)
class ProductRoutingWorkerConfig:
    database_url: str
    batch_size: int = 25


def load_config() -> ProductRoutingWorkerConfig:
    database_url = os.environ.get("NC_DATABASE_URL") or os.environ.get("DATABASE_URL")
    if not database_url:
        raise RuntimeError("NC_DATABASE_URL or DATABASE_URL is required")
    return ProductRoutingWorkerConfig(
        database_url=database_url,
        batch_size=int(os.environ.get("NC_PRODUCT_ROUTING_BATCH_SIZE", "25")),
    )

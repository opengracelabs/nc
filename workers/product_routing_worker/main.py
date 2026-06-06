"""Product Routing Worker entrypoint."""
from __future__ import annotations

import asyncio

import asyncpg

from .config import load_config
from .store import claim_routable_commerce_opportunities, load_active_routing_policy, route_commerce_opportunity


async def run_once() -> int:
    config = load_config()
    conn = await asyncpg.connect(config.database_url)
    try:
        routing_policy = await load_active_routing_policy(conn)
        opportunities = await claim_routable_commerce_opportunities(conn, config.batch_size)
        routed = 0
        for opportunity in opportunities:
            routed += len(await route_commerce_opportunity(conn, routing_policy, opportunity))
        return routed
    finally:
        await conn.close()


def main() -> None:
    asyncio.run(run_once())


if __name__ == "__main__":
    main()

import os
import asyncio
import redis.asyncio as aioredis

from judas_ibkr.rebalancer import Rebalancer
from utils.spirit_coin_adapter import SpiritPriceAdapter, SpiritWalletManager

# Ensure data directory exists for Streamlit dashboard
DATA_DIR = os.path.join(os.getcwd(), "data")
os.makedirs(DATA_DIR, exist_ok=True)

async def main():
    # ——— Setup your IBKR Rebalancer ———
    rebalancer = Rebalancer(
        watch_list=["NVDA", "AMD", "MSFT", "AMZN", "GOOG", "PLTR", "SNOW", "AI"],
        leverage=2.0,
        threshold=0.01,
        max_trade_fraction=0.2,
        min_price_points=60,
        ib=None  # your IBKR client instance
    )

    # ——— Wire in SPIRIT price subscription ———
    price_adapter = SpiritPriceAdapter(
        api_url="https://api.coingecko.com/api/v3/simple/price",
        token_id="spirit-token",
        vs_currency="usd"
    )
    asyncio.create_task(
        price_adapter.subscribe_prices(
            callback=rebalancer.update_price,
            interval=15
        )
    )

    # ——— Crypto execution layer ———
    private_key = os.getenv("SPIRIT_PRIVATE_KEY")
    if private_key:
        wallet_mgr = SpiritWalletManager(
            provider_url=os.getenv("WEB3_PROVIDER"),
            private_key=private_key,
            router_address=os.getenv("SPIRIT_ROUTER_ADDRESS"),
            router_abi=[]  # your router ABI list here
        )

        # Override safe_execute for SPIRIT
        original_execute = rebalancer.safe_execute
        def unified_execute(ib, symbol, delta, price_ref, guessed=False):
            if symbol == "SPIRIT":
                return wallet_mgr.safe_execute_crypto(
                    amount_in=delta,
                    path=[os.getenv("SPIRIT_TOKEN_ADDRESS"), os.getenv("USD_TOKEN_ADDRESS")]
                )
            return original_execute(ib, symbol, delta, price_ref, guessed)

        rebalancer.safe_execute = unified_execute
    else:
        print("[Warning] SPIRIT_PRIVATE_KEY not set; SPIRIT trades will be skipped.")

    # ——— Create Redis pub/sub client ———
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")
    client = aioredis.from_url(redis_url)
    ps = client.pubsub()
    await ps.subscribe("T.AAPL", "T.SPIRIT")

    # ——— Start streaming & rebalance loop ———
    await rebalancer.stream_and_rebalance(ps)

if __name__ == "__main__":
    asyncio.run(main())

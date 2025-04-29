import os
import asyncio

import redis.asyncio as aioredis
from judas_ibkr.rebalancer import Rebalancer
from utils.spirit_coin_adapter import SpiritPriceAdapter, SpiritWalletManager

# Ensure data directory exists for Streamlit dashboard
DATA_DIR = os.path.join(os.getcwd(), "data")
(os.makedirs(DATA_DIR, exist_ok=True))

async def main():
    # ——— Setup your IBKR Rebalancer ———
    rebalancer = Rebalancer(
        watch_list=[
            "NVDA", "AMD", "MSFT", "AMZN", "GOOG",AMD", "MSFT", "AMZN", "GOOG",
            "PLTR", "SNOW", "AI"  # Core AI stocksOW", "AI"  # Core AI stocks
        ],
        leverage=2.0,
        threshold=0.01,
        max_trade_fraction=0.2,   max_trade_fraction=0.2,
        min_price_points=60,    # one-minute gate        min_price_points=60,    # one-minute gate
        ib=None  # your IBKR client instance
    )

    # ——— Wire in SPIRIT price subscription ———ubscription ———
    price_adapter = SpiritPriceAdapter(tPriceAdapter(
        api_url="https://api.coingecko.com/api/v3/simple/price",   api_url="https://api.coingecko.com/api/v3/simple/price",
        token_id="spirit-token",-token",
        vs_currency="usd"
    )
    asyncio.create_task((
        price_adapter.subscribe_prices(rice_adapter.subscribe_prices(
            callback=rebalancer.update_price,       callback=rebalancer.update_price,
            interval=15            interval=15
        )
    )

    # ——— Crypto execution layer ———
    private_key = os.getenv("SPIRIT_PRIVATE_KEY")
    if private_key:
        wallet_mgr = SpiritWalletManager(
            provider_url=os.getenv("WEB3_PROVIDER"),
            private_key=private_key,   private_key=private_key,
            router_address=os.getenv("SPIRIT_ROUTER_ADDRESS"),IT_ROUTER_ADDRESS"),
            router_abi=[]  # your router ABI list herehere
        )
        # Override safe_execute for SPIRITr SPIRIT
        original_execute = rebalancer.safe_execute
        def unified_execute(ib, symbol, delta, price_ref, guessed=False):ol, delta, price_ref, guessed=False):
            if symbol == "SPIRIT":
                return wallet_mgr.safe_execute_crypto(eturn wallet_mgr.safe_execute_crypto(
                    amount_in=delta,
                    path=[os.getenv("SPIRIT_TOKEN_ADDRESS"), os.getenv("USD_TOKEN_ADDRESS")]_ADDRESS"), os.getenv("USD_TOKEN_ADDRESS")]
                )       )
            return original_execute(ib, symbol, delta, price_ref, guessed)
        rebalancer.safe_execute = unified_execute        rebalancer.safe_execute = unified_execute
    else:
        print("[Warning] SPIRIT_PRIVATE_KEY not set; SPIRIT trades will be skipped.")es will be skipped.")

    # ——— Create Redis pub/sub client ———ub/sub client ———
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379")s://localhost:6379")
    client = aioredis.from_url(redis_url)    client = aioredis.from_url(redis_url)
    ps = client.pubsub()
    await ps.subscribe("T.AAPL", "T.SPIRIT")

    # ——— Start streaming & rebalance loop ———& rebalance loop ———
    await rebalancer.stream_and_rebalance(ps)ream_and_rebalance(ps)




    asyncio.run(main())if __name__ == "__main__":if __name__ == "__main__":
    asyncio.run(main())

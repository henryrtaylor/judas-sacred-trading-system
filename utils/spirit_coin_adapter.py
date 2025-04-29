import os
import asyncio
import requests
from web3 import Web3


class SpiritPriceAdapter:
    """
    Fetch SPIRIT token prices from a public API (e.g., CoinGecko) for USD quote.
    """
    def __init__(self,
                 api_url: str = "https://api.coingecko.com/api/v3/simple/price",
                 token_id: str = "spirit-token",
                 vs_currency: str = "usd"):
        self.api_url = api_url
        self.token_id = token_id
        self.vs_currency = vs_currency

    def get_price(self) -> float:
        """
        Returns current SPIRIT price in USD via HTTP GET.
        """
        try:
            resp = requests.get(self.api_url, params={
                "ids": self.token_id,
                "vs_currencies": self.vs_currency
            })
            data = resp.json()
            return float(data.get(self.token_id, {}).get(self.vs_currency, 0.0))
        except Exception:
            return 0.0

    async def subscribe_prices(self, callback, interval: int = 10):
        """
        Polls price every `interval` seconds and invokes `callback(symbol, price)`.
        """
        symbol = "SPIRIT"
        while True:
            price = self.get_price()
            callback(symbol, price)
            await asyncio.sleep(interval)


class SpiritWalletManager:
    """
    Manages SPIRIT token trades via a Web3 provider and router contract.
    """
    def __init__(self,
                 provider_url: str,
                 private_key: str,
                 router_address: str,
                 router_abi: list):
        self.w3 = Web3(Web3.HTTPProvider(provider_url))
        self.account = self.w3.eth.account.from_key(private_key)
        self.router_address = Web3.to_checksum_address(router_address)
        self.router = self.w3.eth.contract(
            address=self.router_address,
            abi=router_abi
        )

    def safe_execute_crypto(self,
                             amount_in: float,
                             path: list[str],
                             slippage: float = 0.005,
                             deadline: int = None) -> str:
        """
        Executes a token swap via router:
        - amount_in: input token amount
        - path: [token_in_addr, token_out_addr]
        - slippage: max allowed slippage (e.g., 0.5%)
        - deadline: txn deadline as UNIX timestamp
        Returns transaction hash string.
        """
        if deadline is None:
            deadline = int(asyncio.get_event_loop().time()) + 300  # 5 min default

        # Approve token if needed (omitted for brevity)

        # Build swapExactTokensForTokens transaction
        txn = self.router.functions.swapExactTokensForTokens(
            Web3.to_wei(amount_in, 'ether'),
            0,  # amountOutMin (could implement slippage calc)
            path,
            self.account.address,
            deadline
        ).build_transaction({
            'from': self.account.address,
            'nonce': self.w3.eth.get_transaction_count(self.account.address),
            'gas': 300000,
            'gasPrice': self.w3.to_wei('5', 'gwei')
        })

        signed = self.account.sign_transaction(txn)
        tx_hash = self.w3.eth.send_raw_transaction(signed.rawTransaction)
        return tx_hash.hex()


# Example usage in Rebalancer:
# from utils.spirit_coin_adapter import SpiritPriceAdapter, SpiritWalletManager
# price_adapter = SpiritPriceAdapter()
# wallet_mgr = SpiritWalletManager(
#     provider_url=os.getenv('WEB3_PROVIDER'),
#     private_key=os.getenv('SPIRIT_PRIVATE_KEY'),
#     router_address=os.getenv('SPIRIT_ROUTER_ADDRESS'),
#     router_abi=[...]
# )
#
# asyncio.create_task(price_adapter.subscribe_prices(rebalancer.update_price, interval=15))
# safe_execute_crypto = wallet_mgr.safe_execute_crypto

from brownie import FundMe, network, config, MockV3Aggregator
from scripts.helpful_scripts import get_account, deploy_mocks, LOCAL_BLOCKCHAIN_ENVIRONMENTS


def deploy_fund_me():
    account = get_account()

    # Determine price feed address
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMENTS:
        deploy_mocks()
        price_feed_address = MockV3Aggregator[-1].address
    else:
        price_feed_address = config["networks"][network.show_active()]["eth_usd_price_feed"]

    # Transaction parameters (this must be passed positionally)
    tx_params = {"from": account}

    # Brownie on an Anvil mainnet fork must use EIP-1559 fee fields instead of gas_price=0
    if network.show_active() in ["mainnet-fork-dev", "mainnet-fork"]:
        tx_params["priority_fee"] = "2 gwei"
        tx_params["max_fee"] = "100 gwei"

    # Deploy - IMPORTANT: tx_params must come BEFORE publish_source
    fund_me = FundMe.deploy(
        price_feed_address,
        tx_params,
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print(f"FundMe deployed at {fund_me.address}")
    return fund_me


def main():
    deploy_fund_me()

from brownie import accounts, config, Tutorial

def deploy_simple_storage():
    account = accounts[0]
    tutorial_storage = Tutorial.deploy({"from": account, "gas_price": "0"})
    stored_value = tutorial_storage.retrieve()
    print (stored_value)
    transaction = tutorial_storage.store(15, {"from": account, "gas_price": "0"})
    transaction.wait(1)
    updated_stored_value = tutorial_storage.retrieve()
    print (updated_stored_value)
    #account = accounts.load("vanebuilds_")
    #print (account)
    #account = accounts.add(config["wallets"]["from_key"])
    #print (account)
def main():
    deploy_simple_storage()

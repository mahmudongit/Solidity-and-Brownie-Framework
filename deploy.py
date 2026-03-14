from web3 import Web3
import json
import os

from dotenv import load_dotenv
load_dotenv()

# connect to Ethereum sepolia testnet
w3 = Web3(Web3.HTTPProvider("https://eth-sepolia.g.alchemy.com/v2/EWOtfnP8eEX1ES0pVqSy1"))

CHAIN_ID = 11155111  # Sepolia chain ID
MY_ADDRESS = "0x1157fEa8690C2BA2a23fb33Fa650c665527e7F53"
PRIVATE_KEY = os.getenv("PRIVATE_KEY")

# Read compiled contract (solcx output)
with open("./compiled_code.json", "r") as f:
    compiled_sol = json.load(f)
    
# 3. Extract ABI + bytecode

bytecode = compiled_sol["contracts"]["tutorial.sol"]["Tutorial"]["evm"]["bytecode"]["object"]
abi = compiled_sol["contracts"]["tutorial.sol"]["Tutorial"]["abi"]

#  Deploying the contract

# Create contract object
Tutorial = w3.eth.contract(abi=abi, bytecode=bytecode)

# Nonce
nonce = w3.eth.get_transaction_count(MY_ADDRESS)

# Build deployment tx
tx = Tutorial.constructor().build_transaction({
    "from": MY_ADDRESS,
    "nonce": nonce,
    "gas": 3000000,
    "gasPrice": w3.eth.gas_price,
    "chainId": CHAIN_ID
})

# Sign tx
signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

# Send tx
tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)

print("Deploying...")

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_hash)
print("Contract deployed to:", tx_receipt.contractAddress)

# ---- Interacting with deployed contract ---- #

contract = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

# Example: store()
store_tx = contract.functions.store(15).build_transaction({
    "from": MY_ADDRESS,
    "nonce": nonce + 1,
    "gas": 300000,
    "gasPrice": w3.eth.gas_price,
    "chainId": CHAIN_ID
})

signed_store = w3.eth.account.sign_transaction(store_tx, PRIVATE_KEY)
print ("Storing 15...")
store_hash = w3.eth.send_raw_transaction(signed_store.raw_transaction)
w3.eth.wait_for_transaction_receipt(store_hash)

print("Stored!")
print("Retrieving:", contract.functions.retrieve().call())
print("Retrieved:", contract.functions.retrieve().call())

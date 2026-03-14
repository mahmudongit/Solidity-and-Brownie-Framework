from brownie import accounts, Tutorial

def test_deploy():
    # Arrange 
    account = accounts[0]
    
    # Act
    tutorial_storage = Tutorial.deploy({"from": account, "gas_price": "0"})
    starting_value = tutorial_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected
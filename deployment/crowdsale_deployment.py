#!/usr/bin/env python3

from web3_interface import Web3Interface
import json
from unlock import Unlock
import os, errno
from datetime import datetime
from deployer import Deployer
import sys

# web3.py instance
web3 = Web3Interface(middleware=True).w3
miner = web3.miner
unlocker = Unlock()
sender_account = web3.eth.accounts[0]
gas = 5000000
address_log_path = "./address_log/"
compiled_path = "./build/"

pending_configuration = True

while pending_configuration:
  try:
    if __name__ != '__main__' or sys.argv[1] == 'test':
      unlocker.unlock()
      miner.start(1)
      contract_name = "Crowdsale"
      gas_price = 20000000000
      pending_configuration = False
    else:
      print("Enter 'test' as a parameter or no parameter for MainNet deployment")
  except IndexError:
    contract_name = input("\nEnter contract's name: ")
    gas_price = input("\nEnter gas price: ")
    pending_configuration = False

if compiled_path[len(compiled_path)-1] != "/":
  compiled_path += "/"

deployer = Deployer()

print("\nDeploying contract...")
(crowdsale_contract, receipt) = deployer.deploy(compiled_path, contract_name, sender_account, {"from": sender_account, "value": 0, "gas": gas, "gasPrice": gas_price},)

print("Deployment successful: " + str(receipt.status == 1),
      "\n\nDeployment hash: " + receipt.transactionHash.hex(),
      "\nCrowdsale address: " + crowdsale_contract.address,
      "\nGas used: " + str(receipt.gasUsed) + "\n")

def write_to_address_log(address_log_path):
  # Write json file with contract's address into address_log folder
  try:
    if __name__ != "__main__" or sys.argv[1] == 'test':
      deployment_name = "test"
  except IndexError:
    deployment_name = input('Enter name of deployment: ')
  
  local_time = datetime.now()
  json_file_name = "Contract-Address" + '--' + local_time.strftime('%Y-%m-%d--%H-%M-%S') + '--' + deployment_name
  
  try:
    if not os.path.exists(address_log_path):
      os.makedirs(address_log_path)
  except OSError as e:
    if e.errno != errno.EEXIST:
      raise
  
  file_path_name_w_ext = address_log_path + json_file_name + '.json'
  address_for_file = {'contract_address': crowdsale_contract.address}
  with open(file_path_name_w_ext, 'w') as fp:
    json.dump(address_for_file, fp, sort_keys=True, indent=2)

write_to_address_log(address_log_path)
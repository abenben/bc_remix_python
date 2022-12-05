from web3 import Web3

account_1 = '0x2044E11CeeBA8dbeaFaA37f61c9F7EeCa994b34b'
account_2 = '0xD70C23F6f2b174d714c52399AbE7C86331dfdBe8'
account_3 = '0x350d426eA41051ab33e543a5826490e0DdE3c89a'

private_key_1 = '0x636dad935aca38288fb3f6262d945ab0a0802d7afb902774ace597024f2fa9c8'
private_key_2 = '0x32981336a053501949a5415a5f31fc67ff71772bc9f10855ac5c3ccc53c169a3'
private_key_3 = '0xc4aeb0559cc91d6f1ec5477b388569d839db98b9ea05baded4b53b9b99a3409f'

# Ganacheに接続する
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.isConnected()

# ここにRemixでコンパイルしたABIのコピーを貼り付ける
abi = '''
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "to",
				"type": "address"
			}
		],
		"name": "delegate",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "voter",
				"type": "address"
			}
		],
		"name": "giveRightToVote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "bytes32[]",
				"name": "proposalNames",
				"type": "bytes32[]"
			}
		],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "proposal",
				"type": "uint256"
			}
		],
		"name": "vote",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "chairperson",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"name": "proposals",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "name",
				"type": "bytes32"
			},
			{
				"internalType": "uint256",
				"name": "voteCount",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"name": "voters",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "weight",
				"type": "uint256"
			},
			{
				"internalType": "bool",
				"name": "voted",
				"type": "bool"
			},
			{
				"internalType": "address",
				"name": "delegate",
				"type": "address"
			},
			{
				"internalType": "uint256",
				"name": "vote",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "winnerName",
		"outputs": [
			{
				"internalType": "bytes32",
				"name": "winnerName_",
				"type": "bytes32"
			}
		],
		"stateMutability": "view",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "winningProposal",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "winningProposal_",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''

# ここにRemixでデプロイしたコントラクトのアドレスを貼り付ける
contract_address = '0xC08dfBe16b0C78607FeE9a38F5a936582fE1AEAC'
contract_instace = w3.eth.contract(address=contract_address, abi=abi)

print("#" * 50)
print("初期状態")
print("#" * 50)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("議長に投票権を付与する")
print("#" * 50)
try:
    # 議長に投票権を付与する
    txn = contract_instace.functions.giveRightToVote(account_1).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(1)')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("議長投票後")
print("#" * 50)
try:
    # 議長の投票
    txn = contract_instace.functions.vote(2).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(2)')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("議長の二重投票後")
print("#" * 50)
try:
    # 二重投票する
    txn = contract_instace.functions.vote(2).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(3)')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("投票権のないアカウント（2人目）による投票")
print("#" * 50)
try:
    # 2人目のアカウントの投票
    txn = contract_instace.functions.vote(0).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_2,
        'nonce': w3.eth.getTransactionCount(account_2),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_2)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(4):投票権がないことを期待')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("2人目のアカウントに投票権を付与")
print("#" * 50)
try:
    # 2人目のアカウントに投票権を付与
    txn = contract_instace.functions.giveRightToVote(account_2).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(5)')
    print(e)

print(contract_instace.functions.winningProposal().call())
print(contract_instace.functions.winnerName().call())

print("#" * 50)
print("2人目のアカウントによる投票")
print("#" * 50)
try:
    # 2人目のアカウントの投票
    txn = contract_instace.functions.vote(0).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_2,
        'nonce': w3.eth.getTransactionCount(account_2),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_2)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(6)')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案

print("#" * 50)
print("3人目のアカウントに投票権を付与")
print("#" * 50)
try:
    # 3人目のアカウントに投票権を付与
    txn = contract_instace.functions.giveRightToVote(account_3).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(7)')
    print(e)

print("#" * 50)
print("3人目のアカウントによる委任投票（議長と同じ投票）")
print("#" * 50)
try:
    txn = contract_instace.functions.delegate(account_1).buildTransaction({
        'gas': 170000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_3,
        'nonce': w3.eth.getTransactionCount(account_3),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_3)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です(8)')
    print(e)

print(contract_instace.functions.winningProposal().call())  # 当選したインデックス
print(contract_instace.functions.winnerName().call())  # 当選案
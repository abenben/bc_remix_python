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
abi='''
[
	{
		"inputs": [
			{
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "changeOwner",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"stateMutability": "nonpayable",
		"type": "constructor"
	},
	{
		"anonymous": false,
		"inputs": [
			{
				"indexed": true,
				"internalType": "address",
				"name": "oldOwner",
				"type": "address"
			},
			{
				"indexed": true,
				"internalType": "address",
				"name": "newOwner",
				"type": "address"
			}
		],
		"name": "OwnerSet",
		"type": "event"
	},
	{
		"inputs": [],
		"name": "getOwner",
		"outputs": [
			{
				"internalType": "address",
				"name": "",
				"type": "address"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''

# ここにRemixでデプロイしたコントラクトのアドレスを貼り付ける
contract_address='0x2c4dDe47E2836Ef4dA928AB7267C13CA228cdD4E'
contract_instace = w3.eth.contract(address=contract_address,abi=abi)

# 現在のオーナーのアカウントアドレスを確認する。
print("最初のオーナー （アカウントアドレス）: {}".format(contract_instace.functions.getOwner().call()))

# 現在のオーナーを変更する。
try:
    txn = contract_instace.functions.changeOwner(account_2).buildTransaction({
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です')
    print(e)

# 新しいオーナーのアカウントアドレスを確認する。
print("新しいのオーナー （アカウントアドレス）: {}".format(contract_instace.functions.getOwner().call()))

# 前のオーナーが、オーナーを自分に変更する。
try:
    txn = contract_instace.functions.changeOwner(account_1).buildTransaction({
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_1,
        'nonce': w3.eth.getTransactionCount(account_1),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です')
    print(e)

# 新しいオーナーによって、オーナーを前回のオーナーに変更する。
try:
    txn = contract_instace.functions.changeOwner(account_1).buildTransaction({
        'gas': 70000,
        'gasPrice': w3.toWei('1', 'gwei'),
        'from': account_2,
        'nonce': w3.eth.getTransactionCount(account_2),
    })
    signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_2)
    w3.eth.sendRawTransaction(signed_txn.rawTransaction)
except Exception as e:
    print('例外です')
    print(e)

# オーナーのアカウントアドレスを確認する。
print("現在のオーナー（アカウントアドレス） : {}".format(contract_instace.functions.getOwner().call()))

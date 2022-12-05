from web3 import Web3

account_1 = '0x2044E11CeeBA8dbeaFaA37f61c9F7EeCa994b34b'
account_2 = '0xD70C23F6f2b174d714c52399AbE7C86331dfdBe8'
account_3 = '0x350d426eA41051ab33e543a5826490e0DdE3c89a'

private_key_1 = '0x636dad935aca38288fb3f6262d945ab0a0802d7afb902774ace597024f2fa9c8'
private_key_2 = '0x32981336a053501949a5415a5f31fc67ff71772bc9f10855ac5c3ccc53c169a3'
private_key_3 = '0xc4aeb0559cc91d6f1ec5477b388569d839db98b9ea05baded4b53b9b99a3409f'

Web3.EthereumTesterProvider

# Ganacheに接続する
w3 = Web3(Web3.HTTPProvider('http://127.0.0.1:7545'))
w3.isConnected()

# ここにRemixでコンパイルしたABIのコピーを貼り付ける
abi='''
[
	{
		"inputs": [
			{
				"internalType": "uint256",
				"name": "num",
				"type": "uint256"
			}
		],
		"name": "store",
		"outputs": [],
		"stateMutability": "nonpayable",
		"type": "function"
	},
	{
		"inputs": [],
		"name": "retrieve",
		"outputs": [
			{
				"internalType": "uint256",
				"name": "",
				"type": "uint256"
			}
		],
		"stateMutability": "view",
		"type": "function"
	}
]
'''

# ここにRemixでデプロイしたコントラクトのアドレスを貼り付ける
contract_address='0x3fc44cd135BD12c4627085C4f6674A668187F5A2'
contract_instace = w3.eth.contract(address=contract_address,abi=abi)

# Storageコントラクトのretrieve（取り出す）メソッドの呼びだし
print("初期値：retrieve : {}".format(contract_instace.functions.retrieve().call()))

# Storageコントラクトのstore（格納する）メソッドの呼びだし
txn = contract_instace.functions.store(123456789).buildTransaction({
  'gas': 170000,
  'gasPrice': w3.toWei('1', 'gwei'),
  'from': account_1,
  'nonce' : w3.eth.getTransactionCount(account_1),
})
signed_txn = w3.eth.account.signTransaction(txn, private_key=private_key_1)
w3.eth.sendRawTransaction(signed_txn.rawTransaction)

# Storageコントラクトのretrieve（取り出す）メソッドの呼びだし
print("変更後：retrieve : {}".format(contract_instace.functions.retrieve().call()))

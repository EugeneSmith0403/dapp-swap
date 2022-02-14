# dapp-swap


Install ganache framework for creating testing ethereum environment.

```
https://trufflesuite.com/ganache/

```
install open openzeppelin https://docs.openzeppelin.com/contracts/4.x/
```
 npm install @openzeppelin/contracts
```
Change constants in settings.py.

```
OPEN_ZEPPELIN_URL = ''

ETHEREUM_NETWORK = ''

CONTRACT_OWNER_WALLET_ADDRESS = ''

PRIVATE_KEY = ''

```

Optional install requirements, if it's necessary.

```
 pip3 install -r requirements.txt
```

Change wallet field in User table for superuser.
Change wallet field in Client table or add new row.
These fields must be equal CONTRACT_OWNER_WALLET_ADDRESS.





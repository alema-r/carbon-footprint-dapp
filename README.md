## Install the solidity compiler

### Linux
1. Download the compiler and save it in /usr/local/bin/ with the name solc:

`sudo curl -L https://github.com/ethereum/solidity/releases/download/v0.8.12/solc-static-linux -o /usr/local/bin/solc`

2. Make it executable:


`chmod +x /usr/local/bin/solc`

### Windows
1. Download the compiler from https://github.com/ethereum/solidity/releases.
2. Either add it to PATH or move it in the project directory

## Compile contract files
In order to compile contracts you have to download @openzeppelin contracts. To do this run the command:

`npm install @openzeppelin/contracts`

Then, run compile.py:

`python3 compile.py`

Now in the `solc_output` folder there are three json files:
- UserContract.json: the User.sol contract compiled
- CFContract.json: the CarbonFootprint.sol contract compiled
- errors.json: any error/warning from SMTChecker
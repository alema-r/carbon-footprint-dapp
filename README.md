# Progetto software cyberscurity (gruppo 9)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## Table of contents
1. [Prerequisites](#prerequisites)
2. [Setup](#setup)
3. [Usage](#usage)

## Prerequisites

To run this program you must have the following installed:
- [Node.js/npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) 10 or higher
- Java 11 or higher
- Python 3.8 or higher

## Setup
Clone this repo:

```
git clone https://github.com/alema-r/progetto-software-cybersecurity.git
cd progetto-software-cybersecurity
```

In order to compile the contracts you have to 
- download @openzeppelin contracts 
- install the solidity compiler. 

You can download the @openzeppelin contracts by executing the command:

`npm install`

To install the compiler, follow the instructions for your OS.

### Installing the compiler

**Linux**
1. Download the compiler and save it in /usr/local/bin/ with the name solc:

`sudo curl -L https://github.com/ethereum/solidity/releases/download/v0.8.12/solc-static-linux -o /usr/local/bin/solc`

2. Make it executable:

`chmod +x /usr/local/bin/solc`

**Windows**
1. Download the compiler from https://github.com/ethereum/solidity/releases.
2. Either add it to PATH or move it in the project directory

### Guided installation (recommended method)

You can execute the `setup.sh` script and specify the flags.
```
usage: setup.sh [-dmrv] [-s|-t]
  -d, --deploy            deploy a new blockchain
  -m, --model-checker     compile with SMTCHECKER
  -s, --seeding           creates a demo scenario in the blockchain, 
                          only use with -d option
  -t, --run-test          run all python tests (do not use with -s)
  -r, --req               install python requirements
  -v, --venv              initialize a python virtual environment
  -h, --help              shows this message and exit
```

For example you can run:

`./setup.sh -v -r -d -t`

This will create a python virtual environment under the env folder, install all python requirements, create a test blockchain, compile all the contracts and then it will run the tests.


### Manual installation
Install python requirements:

`pip install -r requirements.txt`

Deploy a test blockchain:

`npx quorum-wizard -q`

Start the blockchain:

**Linux**

```
cd network/3-nodes-quickstart
./start.sh
```

**Windows**

```
cd network/3-nodes-quickstart
start.cmd
```

Create a directory named "solc_output" in the project root directory.

Lastly, execute the following (from within the scripts folder):

```
python3 compile.py
python3 deploy_contracts.py
```

If you want to seed the blockchain, run:

`python3 seeding.py`

Otherwise, if you want to run tests, you can execute:

**Linux**

`./test.sh`

**Windows**

`./test.bat`

_Note: you cannot run the seeding script after executing the tests and viceversa._

## Usage
To start the application execute the `main.py` script.

`python3 main.py`

The application is a CLI application, so you will perform actions using only your keyboard.
- You can navigate a list by pressing the up and down arrow keys and you can select the option by pressing enter.
- Some input are lists of checkboxes: you can select/unselect an option by pressing space and press enter to confirm the selection.
- Finally in a text input, you simply have to answer the question and press enter when you're done.

Here you can see a demo of the application, with key presses on screen:

https://user-images.githubusercontent.com/79423643/168593985-c4e11072-ee0d-4f0a-acac-10614c8257b7.mp4


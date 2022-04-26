#!/bin/bash
usage()
{
    echo "usage: setup.sh [-dmr] [-s|-t]"
    echo "  -d, --deploy            deploy a new blockchain"
    echo "  -m, --model-checker     compile with SMTCHECKER"
    echo "  -s, --seeding           creates a demo scenario in the blockchain, only use with -d option"
    echo "  -t, --run-test          run all python tests"
    echo "  -r, --req               install python requirements"
    echo "  -h, --help              shows this message and exit"
}
deploy=0
smt=0
seeding=0
run_test=0
req=0
while [ "$1" != "" ]; do
    case $1 in
        -d | --deploy)              deploy=1
                                    ;;
        -m | --model-checker)       smt=1
                                    ;;
        -h | --help)                usage
                                    exit
                                    ;;
        -r | --req)                 req=1
                                    ;;
        -s | --seeding)             seeding=1
                                    ;;
        -t | --run-test)            run_test=1
                                    ;;
        * )                         usage
                                    exit 1
    esac
    shift
done

if [[ $seeding == 1 && $run_test == 1 ]]; then
    echo 'You cannot choose both -s and -t options.'
    echo 'Exiting'
    exit 1
fi

echo '{"address":""}' > address.json
if [[ $req == 1 ]]; then
    echo 'Installing python requirements...'
    pip install -r requirements.txt
fi

if [[ $deploy == 1 ]]; then
    echo 'Creating test blockchain...'
    npx quorum-wizard -q
    echo 'Starting blockchain...'
    cd network/3-nodes-quickstart/; ./stop.sh; ./start.sh 
    cd ../../
fi

if [[ ! -d "solc_output/" ]]; then
    mkdir solc_output
fi

cd scripts
if [[ $smt == 1 ]]; then
    python3 compile.py -m
else
    python3 compile.py
fi

python3 deploy_contracts.py

if [[ $seeding == 1 ]]; then
    echo 'Starting seeding...'
    python3 seeding.py
fi

if [[ $run_test == 1 ]]; then
    echo "Running tests..."
    cd ..
    ./test.sh
fi

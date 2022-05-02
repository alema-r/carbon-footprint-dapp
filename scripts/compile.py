#!/usr/bin/env python3
"""
Script used to compile solidity contracts.
"""

import getopt
import json
import shutil
import subprocess
import sys
from telnetlib import OUTMRK

NODE_MOD_PATH = "../node_modules/"


def usage():
    print(
        """Script to compile solidity contracts
    Usage: compile.py [options]
    options:
        -m, --model-checker     compile with SMTCHECKER (don't use if you are on Windows)
        -h, --help              shows this message and exit
    """
    )


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hm", ["help", "model-checker"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    smt = False
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-m", "--model-checker"):
            smt = True

    solc_bin = shutil.which("solc")
    if solc_bin is None:
        print("Cannot find solidity executable.")
        sys.exit(1)

    if smt:
        print("Compiling with SMTChecker...")
        solc_options = "solc_options_smt.json"
        cmd = f"{solc_bin} --base-path ../ --include-path {NODE_MOD_PATH} --standard-json {solc_options} --pretty-json"
        output = subprocess.check_output(cmd.split(" "))
        output = json.loads(output)

        with open("../solc_output/errors.json", "w", encoding="utf-8") as errors:
            json.dump(obj=output["errors"], fp=errors, indent=4)
        print("Done! The output of SMTChekcker can be found in solc_output/errors.json")
    else:
        print("Compiling...")
        solc_options = "solc_options.json"
        cmd = f"{solc_bin} --base-path ../ --include-path {NODE_MOD_PATH} --standard-json {solc_options} --pretty-json"
        output = subprocess.check_output(cmd.split(" "))
        output = json.loads(output)
        print("Done!")

    with open("../solc_output/CFContract.json", "w", encoding="utf-8") as cf_contract:
        json.dump(
            obj=output["contracts"]["../contracts/CarbonFootprint.sol"][
                "CarbonFootprint"
            ],
            fp=cf_contract,
        )
    with open(
        "../solc_output/UserContract.json", "w", encoding="utf-8"
    ) as user_contract:
        json.dump(
            obj=output["contracts"]["../contracts/User.sol"]["User"], fp=user_contract
        )


if __name__ == "__main__":
    main()

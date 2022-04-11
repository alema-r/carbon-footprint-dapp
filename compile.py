"""
Script used to compile solidity contracts.
"""

import json
import shutil
import subprocess
import inquirer

NODE_MOD_PATH = "node_modules/"


def main():
    choices = [
        "Compile with SMTChecker (don't choose this option if you are using Windows)",
        "Only compile",
    ]

    choice = inquirer.list_input(message="Choose an option", choices=choices)
    solc_bin = shutil.which("solc")
    if solc_bin is None:
        print("Cannot find solidity executable.")
        exit(1)

    print("Compiling...")
    if choice == choices[0]:
        solc_options = "solc_options_smt.json"
        cmd = f"{solc_bin} --base-path . --include-path {NODE_MOD_PATH} --standard-json {solc_options} --pretty-json"
        output = subprocess.check_output(cmd.split(" "))
        output = json.loads(output)

        with open("solc_output/errors.json", "w", encoding="utf8") as errors:
            json.dump(obj=output["errors"], fp=errors, indent=4)

    else:
        solc_options = "solc_options.json"
        cmd = f"{solc_bin} --base-path . --include-path {NODE_MOD_PATH} --standard-json {solc_options} --pretty-json"
        output = subprocess.check_output(cmd.split(" "))
        output = json.loads(output)

    print("Done!")
    with open("solc_output/CFContract.json", "w", encoding="utf8") as cf_contract:
        json.dump(
            obj=output["contracts"]["contracts/CarbonFootprint.sol"]["CarbonFootprint"],
            fp=cf_contract,
        )
    with open("solc_output/UserContract.json", "w", encoding="utf8") as user_contract:
        json.dump(
            obj=output["contracts"]["contracts/User.sol"]["User"], fp=user_contract
        )


if __name__ == "__main__":
    main()

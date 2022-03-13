import json
import shutil
import subprocess

solc_bin = shutil.which("solc")
if solc_bin == "":
    print("Eseguibile solc non trovato.")
    exit(1)
solc_options = "solc_options.json"
cmd = f"{solc_bin} --base-path . --include-path .deps/npm/ --standard-json {solc_options} --pretty-json"
output = subprocess.check_output(cmd.split(" "))
output = json.loads(output)

with open("solc_output/errors.json", "w") as errors:
    json.dump(obj=output["errors"], fp=errors)

with open("solc_output/CFContract.json", "w") as cf_contract:
    json.dump(
        obj=output["contracts"]["contracts/CarbonFootprint.sol"]["CarbonFootprint"],
        fp=cf_contract,
    )

with open("solc_output/UserContract.json", "w") as user_contract:
    json.dump(obj=output["contracts"]["contracts/User.sol"]["User"], fp=user_contract)

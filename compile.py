import json
import shutil
import subprocess

solc_bin = shutil.which('solc')
if solc_bin == '':
    print("Eseguibile solc non trovato.")
    exit(1)
solc_options = "solc_options.json"
cmd = f"{solc_bin} --base-path . --include-path .deps/npm/ --standard-json {solc_options} --pretty-json"
with open("solc_output/out.json", 'w') as out:
    subprocess.call(cmd.split(' '), stdout=out)

with open("solc_output/out.json", 'r') as infile:
    errors = json.load(infile)['errors']

print(errors)
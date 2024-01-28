import json
import os
import sys
import urllib.request

if len(sys.argv) < 3:
    print(f"Usage: {os.path.filename(sys.argv[0])} <token> <url>", file=sys.stderr)
    exit(1)

module = None
with urllib.request.urlopen(sys.argv[2]) as f:
    module = json.load(f)

request = {
    "id": module["id"],
    "dry-run": True,
    "release": {
        "version": module["version"],
        "manifest": sys.argv[2],
    }
}

notes = module.get("changelog")
if notes:
    request["release"]["notes"] = notes

moduleCompat = module.get("compatibility")
if moduleCompat:
    compat = {}
    min = moduleCompat.get("minimum")
    if min:
        compat["minimum"] = min
    max = moduleCompat.get("maximum")
    if max:
        compat["maximum"] = max
    verified = moduleCompat.get("verified")
    if verified:
        moduleCompat["verified"] = verified
    request["compatibility"] = compat

requestJson = json.dumps(request)

print(requestJson, file=sys.stderr)

print("response-code=200")
print("result=This is some output!")

import json
import os
import sys
import urllib.request

API_URL = "https://api.foundryvtt.com/_api/packages/release_version/"


def main() -> int:
    if len(sys.argv) < 3:
        printErr(f"Usage: {os.path.filename(sys.argv[0])} <token> <url>")
        return 1

    token, moduleUrl = sys.argv[1:3]

    module = getModule(moduleUrl)
    requestJson = constructRequestJson(module, moduleUrl)

    printErr(requestJson)

    status, reason, responseJson = sendRequest(requestJson, token)

    printErr(f"Response: {status} {reason}")
    printErr(responseJson)

    print(f"response-code={status}")
    print("response-json<<EOF")
    print(responseJson)
    print("EOF")

    return 0 if status == 200 else 2


def printErr(*args, **kwargs):
    """Print to stderr"""
    print(*args, **kwargs, file=sys.stderr)


def getModule(url: str) -> dict:
    """Read the module.json from the URL"""
    with urllib.request.urlopen(url) as f:
        return json.load(f)


def constructRequestJson(module: dict, url: str) -> str:
    """Construct the JSON API request"""
    request = {
        "id": module["id"],
        "release": {
            "version": module["version"],
            "manifest": url,
            "compatibility": {
                "minimum": module["compatibility"]["minimum"],
                "verified": module["compatibility"]["verified"],
            }
        }
    }

    if notes := module.get("changelog"):
        request["release"]["notes"] = notes

    if verified := module["compatibility"].get("verified"):
        request["release"]["compatibility"]["verified"] = verified

    return json.dumps(request, separators=(',', ':'))


def sendRequest(requestJson: str, token: str) -> (int, str, str):
    """Send the API request to Foundry website"""
    try:
        response = urllib.request.urlopen(urllib.request.Request(
            API_URL, method="POST",
            data=requestJson.encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": token
            }
        ))
    except urllib.error.HTTPError as e:
        response = e

    return int(response.status), response.reason, response.read().decode()


if __name__ == '__main__':
    sys.exit(main())

import json
import os
import sys
import urllib.request

API_URL = "https://api.foundryvtt.com/_api/packages/release_version/"


def main() -> int:
    if len(sys.argv) < 3:
        print(f"Usage: {os.path.filename(sys.argv[0])} <token> <url>", file=sys.stderr)
        return 1

    module = getModule(sys.argv[2])
    requestJson = constructRequestJson(module)

    print(requestJson, file=sys.stderr)

    status, result = sendRequest(requestJson)
    status = int(status)
    result = result.decode()

    print(f"Response: {status}", file=sys.stderr)
    print(result, file=sys.stderr)

    print(f"response-code={status}")
    print("result<<EOF")
    print(result)
    print("EOF")

    return 0 if status == 200 else status


def getModule(url) -> dict:
    with urllib.request.urlopen(sys.argv[2]) as f:
        return json.load(f)


def constructRequestJson(module) -> str:
    request = {
        "id": module["id"],
        "dry-run": True,
        "release": {
            # "version": module["version"],
            "version": "1.18.0",
            "manifest": sys.argv[2],
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


def sendRequest(requestJson):
    try:
        result = urllib.request.urlopen(urllib.request.Request(
            API_URL, method="POST",
            data=requestJson.encode(),
            headers={
                "Content-Type": "application/json",
                "Authorization": sys.argv[1]
            }
        ))
    except urllib.error.HTTPError as e:
        result = e

    return result.status, result.read()


if __name__ == '__main__':
    sys.exit(main())

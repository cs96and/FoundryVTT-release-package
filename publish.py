#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# FoundryVTT-release-package
# https://github.com/cs96and/FoundryVTT-release-package
#
# Copyright (c) 2022-2025 Alan Davies - All Rights Reserved.
#
# You may use, distribute and modify this code under the terms of the MIT license.
#
# You should have received a copy of the MIT license with this file. If not, please visit:
# https://mit-license.org/


import inspect
import json
import os
import sys
import urllib.request

API_URL = "https://api.foundryvtt.com/_api/packages/release_version/"


def main() -> int:
    # Make sure we can open the github output stream before continuing
    githubOutputFile = os.fdopen(3, mode='w+')

    # Get the required parameters from the environment
    token = getMandatoryEnv("INPUT_PACKAGE-TOKEN")
    manifestUrl = getMandatoryEnv("INPUT_MANIFEST-URL")
    version = os.environ.get("INPUT_VERSION")
    notesUrl = os.environ.get("INPUT_NOTES-URL")
    dryRun = os.environ.get("INPUT_DRY-RUN")
    dryRun = (dryRun and dryRun != "0" and dryRun.lower() != "false")

    manifest = getManifest(manifestUrl)
    requestJson = constructRequestJson(manifest, manifestUrl, version, notesUrl, dryRun)

    print(requestJson)

    status, reason, responseJson = sendRequest(requestJson, token)

    print(f"Response: {status} {reason}")
    print(responseJson)

    # Use inspect.cleandoc to remove the initial new-line and indentation from the string
    githubOutputFile.write(inspect.cleandoc(f"""
        response-code={status}
        response-json<<EOF
        {responseJson}
        EOF
        """))

    return 0 if status == 200 else 2


def getMandatoryEnv(name: str) -> str:
    """Get an environment variable and quit if it's not defined"""
    try:
        value = os.environ[name]
    except KeyError:
        print(f"ERROR: {name} not defined")
        exit(1)

    return value


def getManifest(url: str) -> dict:
    """Read the JSON manifest from the URL"""
    with urllib.request.urlopen(url) as f:
        return json.load(f)


def constructRequestJson(manifest: dict, manifestUrl: str, version: str, notesUrl: str, dryRun: bool) -> str:
    """Construct the JSON API request"""
    request = {
        "id": manifest["id"],
        "dry-run": dryRun,
        "release": {
            "version": version if version else manifest["version"],
            "manifest": manifestUrl,
            "compatibility": {
                "minimum": manifest["compatibility"]["minimum"],
                "verified": manifest["compatibility"]["verified"],
            }
        }
    }

    # Use provided notes URL first.  If that is not provided, use the changelog from the manifest
    if notesUrl := notesUrl if notesUrl else manifest.get("changelog"):
        request["release"]["notes"] = notesUrl

    if maximum := manifest["compatibility"].get("maximum"):
        request["release"]["compatibility"]["maximum"] = maximum

    return json.dumps(request, separators=(',', ':'))


def sendRequest(requestJson: str, token: str) -> tuple[int, str, str]:
    """Send the API request to Foundry website"""
    try:
        response = urllib.request.urlopen(urllib.request.Request(
            API_URL,
            method="POST",
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

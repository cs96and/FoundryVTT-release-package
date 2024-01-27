import os
import sys

if len(sys.argv) < 3:
	print("Usage: {os.path.filename(sys.argv[0])} <token> <url>")
	exit(1)

print(sys.argv[1], sys.argv[2])

outputFilename = os.environ["GITHUB_OUTPUT"]
print("result=This is some output!", file=open(outputFilename, "a"))
print("response-code=200", file=open(outputFilename, "a"))

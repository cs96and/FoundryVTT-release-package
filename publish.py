import sys

if len(sys.argv) < 3:
	print("Usage: {os.path.filename(sys.argv[0])} <token> <url>", file=sys.stderr)
	exit(1)

print(sys.argv[1], sys.argv[2], file=sys.stderr)

print("result=This is some output!")
print("response-code=200")

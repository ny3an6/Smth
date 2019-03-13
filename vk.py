import requests


def main():
	res = requests.get("https://api.fixer.io/latest?base=USD&symbols=EUR")
	f = res.json()
	print(f)

main()
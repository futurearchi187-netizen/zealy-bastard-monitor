import requests

url = "https://zealy.io/cw/bastard/questboard"

r = requests.get(
    url,
    headers={"User-Agent": "Mozilla/5.0"}
)

print("Status:", r.status_code)
print(r.text[:5000])

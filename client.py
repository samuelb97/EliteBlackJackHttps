import requests

URL = "http://127.0.0.1:5000/"

p = requests.post(url = URL + "WA", json = {"wager" : 5, "seatNo" : 1})

r = requests.get(url = URL + "status")

print(r.text)

print("\n")


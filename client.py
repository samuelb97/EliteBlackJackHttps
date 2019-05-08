import requests
import json

URL = "http://127.0.0.1:5000/"

requests.post(url = URL + "WA", json = {"wager" : 5, "seatNo" : 1})

data = requests.get(url = URL + "status").json()

player1 = data["gameState"]

print(player1)

print("\n=======================\n")

requests.post(url = URL + "QG", json = {"seatNo" : 1})

r = requests.get(url = URL + "status")

r = r.json()

# player1 = r["player1"]

# print(player1.text)

print("\n")


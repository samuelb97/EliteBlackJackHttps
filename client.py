import requests
import json

URL = "http://127.0.0.1:5000/"

alias = "Sam"
seat = requests.get(url = URL + "GE/" + alias)
seat = seat.text
seat = int(seat)
print("Sams Seat: ", seat)
print("\n")

requests.post(url = URL + "WA", json = {"wager" : 5, "seatNo" : seat})

data = requests.get(url = URL + "status").json()
data = json.loads(data)
player1 = data['players']['player1']
print(player1)

print("\n=======================\n")

requests.post(url = URL + "AC", json = {"seatNo" : seat, "action" : "HT"} )

data = requests.get(url = URL + "status").json()
data = json.loads(data)
player1 = data['players']['player1']
print(player1)

requests.post(url = URL + "AC", json = {"seatNo" : seat, "action" : "ST"} )

data = requests.get(url = URL + "status").json()
data = json.loads(data)
player1 = data['players']['player1']
dealer = data['dealer']
print(player1)
print(dealer)



print("\n=======================\n")

requests.post(url = URL + "QG", json = {"seatNo" : seat})

r = requests.get(url = URL + "status").json()
r = json.loads(r)
player1 = r['players']['player1']
print(player1)



import requests

example_data = {
  "player_id": "duck2",
  "score": "1",
  "operation": "set"
}

r = requests.post("https://keepthescore.com/api/lhblmfdgyjlye/score/", json=example_data)
print(r.status_code)
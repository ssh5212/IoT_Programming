import json
import requests

#kauth.kakao.com/oauth/authorize?client_id=54c5cab1281a3eb65941610939813a65&redirect_uri=https://localhost.com&response_type=code
url = "https://kauth.kakao.com/oauth/token"

data = {
    "grant_type" : "authorization_code",
    "client_id" : "client_id",
    "redirect_url" : "https://localhost.com",
    "code" : "code"
}

response = requests.post(url, data=data)
tokens = response.json()
print(tokens)
with open("kakao_code.json", "w") as fp:
    json.dump(tokens, fp)
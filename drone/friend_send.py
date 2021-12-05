# -*- coding: utf-8 -*-
import json
import requests
with open("kakao_code.json", "r") as fp:
    tokens = json.load(fp)

print(tokens["access_token"])

url = "https://kapi.kakao.com/v1/api/talk/friends" # 친구 목록 가져오기
header = {"Authorization": 'Bearer ' + tokens["access_token"]}

result = json.loads(requests.get(url, headers=header).text)
friends_list = result.get("elements")

print(friends_list)
friend_id = friends_list[0].get("uuid")
print(friend_id)
test = 'test_code'


data = {
    'receiver_uuids': '["{}"]'.format(friend_id),
    "template_object": json.dumps({
        "object_type":"text",
        "text":"인식을 위해 드론에 QR코드를 보여주세요.",
        "link":{
            "web_url" : "https://raw.githubusercontent.com/ssh5212/IoT_OS/main/img/dr.png",
            "mobile_web_url" : "https://raw.githubusercontent.com/ssh5212/IoT_Programming/main/img/dr.png"
        },
        "button_title": "QR코드 보기"
    })
}

url= "https://kapi.kakao.com/v1/api/talk/friends/message/default/send"
header = {"Authorization": 'Bearer ' + tokens["access_token"]}
response = requests.post(url, headers=header, data=data)
response.status_code


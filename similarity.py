#-*- coding:utf-8 -*-
import urllib3
import json
 
openApiURL = "http://aiopen.etri.re.kr:8000/WiseWWN/WordRel"
accessKey = 

firstWord = "개"
# firstSenseId = 'FIRST_SENSE_ID'
secondWord = "강아지"
# secondSenseId = 'SECOND_SENSE_ID'
 
requestJson = {   
    "argument": {
        'first_word': firstWord,
        # 'first_sense_id': firstSenseId,
        'second_word': secondWord
        # 'second_sense_id': secondSenseId
    }
}
 
http = urllib3.PoolManager()
response = http.request(
    "POST",
    openApiURL,
    headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
    body=json.dumps(requestJson)
)
 
print("[responseCode] " + str(response.status))
print("[responBody]")
print(str(response.data,"utf-8"))

# with open("입학식_연설_preprocessed_text.txt", "r", encoding='UTF8') as file:
    # text = file.read()
# keyword = ['신입생', '봄', '봄동산', '축하', '학부', '겨울', '실감', '자랑', '오늘', '환영', '호기심', '시인', '입학', '생각', '사랑', '전공', '가천대학교', '가능']
# 
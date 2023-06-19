import os
import urllib3
import json
import base64

#-------------------------------PARAMETER-------------------------------------
directory = "C:\\Users\\sejung\\Desktop\\raw\\"
testTextFile = "recognized_text.txt"
#-----------------------------------------------------------------------------


from concurrent.futures import ThreadPoolExecutor

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor"  # 한국어
accessKey = "5add8bbc-36cd-4dd6-9819-6f934fc90dd8"
languageCode = "korean"


r_txt_path = os.path.join(directory, testTextFile)

http = urllib3.PoolManager()

def process_segment(segment_number, script):
    audioFilePath = os.path.join(directory, f"5_segment_{segment_number}.pcm")
    file = open(audioFilePath, "rb")
    audioContents = base64.b64encode(file.read()).decode("utf8")
    file.close()

    requestJson = {
        "argument": {
            "language_code": languageCode,
            "script": script,
            "audio": audioContents
        }
    }

    response = http.request(
        "POST",
        openApiURL,
        headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
        body=json.dumps(requestJson),
        timeout=60  # Increase the timeout to 60 seconds
    )

    if response.status != 200:
        print(f"Request failed with status {response.status}")
        return

    response_data = json.loads(response.data.decode("utf-8"))
    score = response_data["return_object"]["score"]
    print(f"[Segment {segment_number}] score: {score}")
    print("----------------------")


with open(r_txt_path, "r", encoding="utf-8") as file:
    segments = file.read().split("[Segment")

    with ThreadPoolExecutor(max_workers=len(segments)) as executor:
        for i in range(1, len(segments)):
            segment_number = segments[i].split("]")[0].strip()
            script = segments[i].split("]")[1].strip()

            executor.submit(process_segment, segment_number, script)

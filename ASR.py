# -*- coding:utf-8 -*-
import urllib3
import json
import base64
import noisereduce as nr
from pydub import AudioSegment
import os
import librosa
import soundfile as sf

#-------------------------------PARAMETER-------------------------------------
audioFilePath = "C:\\Users\\sejung\\Desktop\\raw\\test.mp3"
generatedTextFile = "C:\\Users\\sejung\\Desktop\\raw\\recognized_text.txt"
#-----------------------------------------------------------------------------


def reduce_noise(data, sample_rate):
    reduced_noise = nr.reduce_noise(y=data, sr=sample_rate, prop_decrease=0.7)
    return reduced_noise



def preprocess_audio(file_path):
    if not file_path.endswith('.pcm'):
        audio = AudioSegment.from_file(file_path)
        file_path_temp = file_path.rsplit('.', 1)[0] + '.wav'
        audio.export(file_path_temp, format='wav')

        data, sample_rate = librosa.load(file_path_temp, sr=None)
        file_path = file_path.rsplit('.', 1)[0] + '.pcm'

        sf.write(file_path, data, sample_rate, format='RAW', subtype='PCM_16')

    else:
        data, sample_rate = sf.read(file_path, format='RAW', channels=1, samplerate=16000, subtype='PCM_16')

    data = reduce_noise(data, sample_rate)  # Apply noise reduction here

    if sample_rate != 16000:
        data = librosa.resample(data, orig_sr=sample_rate, target_sr=16000)
        sample_rate = 16000

    segments = []
    for start in range(0, len(data), 15 * sample_rate):
        end = start + 15 * sample_rate
        segment = data[start:end]
        segments.append(segment)

    return segments, sample_rate

openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = "5add8bbc-36cd-4dd6-9819-6f934fc90dd8"
languageCode = "korean"

segments, sample_rate = preprocess_audio(audioFilePath)

http = urllib3.PoolManager()
with open(generatedTextFile, 'w', encoding='utf8') as f:
    for i, segment in enumerate(segments):
        file_path = f"{audioFilePath.rsplit('.', 1)[0]}_segment_{i}.pcm"
        sf.write(file_path, segment, sample_rate, format='RAW', subtype='PCM_16')

        file = open(file_path, "rb")
        audioContents = base64.b64encode(file.read()).decode("utf8")
        file.close()

        requestJson = {
            "argument": {
                "language_code": languageCode,
                "audio": audioContents
            }
        }

        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
            body=json.dumps(requestJson)
        )

        result_json = json.loads(response.data.decode('utf-8'))
        recognized_text = result_json['return_object']['recognized']
        print(f"Recognized text for segment {i}: {recognized_text}")  # Print the recognized text

        # Check if the recognized text is not empty
        if recognized_text.strip():
            f.write(f"[Segment {i}]\n")
            f.write(recognized_text + '\n')
            f.flush()
            os.fsync(f.fileno())
        else:
            print(f"No recognized text for segment {i}.")


print("finished")
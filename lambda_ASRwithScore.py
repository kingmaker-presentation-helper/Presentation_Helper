# 좋아요 잘 작동하네요.
# 그런데 전체적을 너무 느립니다...
# 조금 더 빠르게 할 수 있는 방법이 있을까요?
# 예를 들면 병렬처리요.
# -*- coding:utf-8 -*-
import time

import boto3
import urllib3
import json
import base64
import noisereduce as nr
from pydub import AudioSegment
import librosa
import soundfile as sf
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

# Boto3 S3 클라이언트 초기화
s3 = boto3.client(
    's3',
    aws_access_key_id='',
    aws_secret_access_key=''
)

max_workers=1
time_out = 10
#-------------------------------PARAMETER-------------------------------------
openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/Recognition"
accessKey = ""
languageCode = "korean"
#-----------------------------------------------------------------------------



def reduce_noise(data, sample_rate):
    reduced_noise = nr.reduce_noise(y=data, sr=sample_rate, prop_decrease=0.7)
    return reduced_noise

def preprocess_audio(file_path, local_directory):
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
        segment_file_path = os.path.join(local_directory,
                                         f"{os.path.basename(file_path).rsplit('.', 1)[0]}_segment_{len(segments) - 1}.pcm")
        sf.write(segment_file_path, segment, sample_rate, format='RAW', subtype='PCM_16')

    return segments, sample_rate



def evaluate_pronunciation_parallel(segment_paths, segment_texts):
    with ThreadPoolExecutor(max_workers) as executor:
        results = executor.map(evaluate_pronunciation, segment_paths, segment_texts)
    return list(results)



#음성인식
def recognize_speech(audio_path, http_manager, language_code, open_api_url, access_key):
    try:
        with open(audio_path, "rb") as file:
            audio_contents = base64.b64encode(file.read()).decode("utf8")

        request_json = {
            "argument": {
                "language_code": language_code,
                "audio": audio_contents
            }
        }

        response = http_manager.request(
            "POST",
            open_api_url,
            headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": access_key},
            body=json.dumps(request_json)
        )

        response_data = json.loads(response.data.decode('utf-8'))

        if 'return_object' in response_data:
            recognized_text = response_data['return_object']['recognized']
            return recognized_text
        else:
            print(f"API response does not contain 'return_object': {response_data}")
            return None

    except Exception as e:
        print(f"An error occurred during speech recognition: {e}")
        return None

#발음 평가
valid_segments = 0
def evaluate_pronunciation(audio_path, segment_text):
    try:
        openApiURL = "http://aiopen.etri.re.kr:8000/WiseASR/PronunciationKor"
        languageCode = "korean"
        script = segment_text

        with open(audio_path, "rb") as file:
            audioContents = base64.b64encode(file.read()).decode("utf8")

        requestJson = {
            "argument": {
                "language_code": languageCode,
                "script": script,
                "audio": audioContents
            }
        }

        http = urllib3.PoolManager()
        response = http.request(
            "POST",
            openApiURL,
            headers={"Content-Type": "application/json; charset=UTF-8", "Authorization": accessKey},
            body=json.dumps(requestJson),
            timeout = time_out
        )

        response_data = json.loads(response.data.decode('utf-8'))
        if 'return_object' in response_data:  # 'result' 대신 'return_object'를 확인

            return response_data['return_object'].get('score')  # 'score' 값을 가져옴
        else:
            print("API response does not contain 'return_object' key")
            return None
    except Exception as e:
        print(f"An error occurred during pronunciation evaluation: {e}")
        return None


def handler(event, context):
    # S3 버킷 이름
    s3_bucket_name = "kingmaker-s3-bucket"

    # event에서 정보 추출
    user_id = event['id']
    file_id = event['file_id']
    file_number = event['file_number']
    input_key = f"{user_id}/{file_id}{file_number}.mp4"
    output_key = f"{user_id}/{file_id}{file_number}.txt"

    # 로컬 경로 설정
    local_directory = f"/tmp/{user_id}"
    if not os.path.exists(local_directory):
        os.makedirs(local_directory)

    local_audio_path = os.path.join(local_directory, f"{file_id}{file_number}.mp4")

    # 처리된 텍스트를 저장할 경로 설정
    local_text_path = os.path.join(local_directory, f"{file_id}{file_number}.txt")

    segments = []  # 초기화
    try:
        # S3에서 오디오 파일 다운로드
        with open(local_audio_path, 'wb') as f:
            s3.download_fileobj(s3_bucket_name, input_key, f)

        # 오디오 전처리 및 세그먼트 생성
        segments, sample_rate = preprocess_audio(local_audio_path, local_directory)

        # 음성 인식 및 발음 평가 실행
        results = process_audio_segments(local_audio_path, segments, sample_rate, languageCode, openApiURL, accessKey)

        total_score = 0.0
        valid_segments = 0
        with open(local_text_path, 'w', encoding='utf8') as f:
            for i, (segment_path, recognized_text, pronunciation_score) in enumerate(results):
                if recognized_text is not None:
                    f.write(f"{recognized_text} ")

                    if pronunciation_score is not None:
                        print(f"{i}: {recognized_text}: {pronunciation_score}")
                        total_score += float(pronunciation_score)  # pronunciation_score를 float로 변환하여 더함
                        valid_segments += 1
                    elif pronunciation_score == 0:
                        print("0점이요!")
                        valid_segments -= 1
                    else:
                        print(f"Pronunciation evaluation error for segment {i}.")
                else:
                    print(f"Speech recognition error for segment {i}.")

            # 평균 점수 계산 및 기록
            if valid_segments > 0:
                average_score = total_score / valid_segments
                f.write(f"\n{average_score}")
            else:
                f.write("\nNo valid segments to calculate average pronunciation score.\n")
            print(average_score)
        # 결과 파일을 S3에 업로드
        with open(local_text_path, 'rb') as f:
            try:
                s3.upload_fileobj(f, s3_bucket_name, output_key)
            except Exception as e:
                print(f"An error occurred during file upload to S3: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # 임시 파일 삭제
        if os.path.exists(local_audio_path):
            os.remove(local_audio_path)
        if os.path.exists(local_text_path):
            os.remove(local_text_path)
        # 임시 PCM 파일 삭제
        for segment_file in os.listdir(local_directory):
            if segment_file.endswith(".pcm"):
                os.remove(os.path.join(local_directory, segment_file))


def process_segment(segment_path, language_code, open_api_url, access_key):
    http_manager = urllib3.PoolManager()
    recognized_text = recognize_speech(segment_path, http_manager, language_code, open_api_url, access_key)
    if recognized_text and recognized_text.strip():
        pronunciation_score = evaluate_pronunciation(segment_path, recognized_text)
        if pronunciation_score is not None:
            return recognized_text, pronunciation_score
    return recognized_text, None



def process_audio_segments(local_audio_path, segments, sample_rate, language_code, open_api_url, access_key):
    segment_paths = [f"{local_audio_path.rsplit('.', 1)[0]}_segment_{i}.pcm" for i in range(len(segments))]
    results = []

    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for segment_path in segment_paths:
            # time.sleep(0.5)  # 쓰레드 실행 간 0.5초 지연
            futures.append(executor.submit(process_segment, segment_path, language_code, open_api_url, access_key))

        for future in as_completed(futures):
            try:
                recognized_text, pronunciation_score = future.result()  # Future 객체의 결과를 가져옴
                results.append((segment_path, recognized_text, pronunciation_score))
            except Exception as exc:
                print(f'A segment processing generated an exception: {exc}')

    return results


# 테스트 데이터 생성
test_event = {
    "id": "king",
    "file_id": "ex",
    "file_number": "3"
}

# 더미 컨텍스트 객체
class DummyContext:
    def __init__(self):
        self.function_name = 'test_lambda_function'
        self.memory_limit_in_mb = 128

dummy_context = DummyContext()

# `handler` 함수 호출
handler(test_event, dummy_context)
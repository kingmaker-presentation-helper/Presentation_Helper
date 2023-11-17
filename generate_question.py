import openai

# 발급받은 API 키 설정
OPENAI_API_KEY = 

# openai API 키 인증
openai.api_key = OPENAI_API_KEY

# 모델 - GPT 3.5 Turbo 선택
model = "gpt-3.5-turbo"

# 질문 작성하기
# query = "다음은 발표문이야. 예상되는 질문 10가지를 말해줘. [발표문] "
query = "다음은 발표문이야. 예상되는 질문 10가지와 주요한 키워드 15개를 뽑아줘. [발표문] "
# 발표문 불러오기
with open("환영사_22_preprocessed_text.txt", "r", encoding='UTF8') as file:
    statement = file.read()

# 메시지 설정하기
messages = [{
    "role": "system",
    "content": "You are a helpful assistant."
}, {
    "role": "user",
    "content": query + statement
}]

# ChatGPT API 호출하기
response = openai.ChatCompletion.create(model=model, messages=messages)
answer = response['choices'][0]['message']['content']
print(answer)
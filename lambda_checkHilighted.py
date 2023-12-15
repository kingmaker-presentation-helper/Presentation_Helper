from kiwipiepy import Kiwi

# kiwipiepy 객체 초기화
kiwi = Kiwi(num_workers=4)

import json
from kiwipiepy import Kiwi

# kiwipiepy 객체 초기화
kiwi = Kiwi(num_workers=4)

def handler(event, context):
    # 입력 데이터와 비교할 단어 목록을 이벤트에서 추출
    input_text = event.get('text', '')
    comparison_words = event.get('comparison_words', '').split()

    # Kiwi로 텍스트에서 명사 추출
    nouns = []
    for res in kiwi.analyze(input_text):
        nouns.extend(token.form for token in res[0] if token.tag in ["NNG", "NNP", "NNB", "NR", "NP"])

    # Exact Match 점수 계산
    match_count = sum(word in nouns for word in comparison_words)
    em_score = match_count / len(comparison_words) if comparison_words else 0

    # 결과 로그 출력 및 반환
    result = {
        'extracted_nouns': nouns,
        'em_score': em_score
    }
    print(result)

    return result  # JSON 문자열 변환 없이 바로 Python 딕셔너리 반환

from keybert import KeyBERT
from kiwipiepy import Kiwi
from transformers import BertModel
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')
import numpy as np


def reserve_list_pop(keyword_list, pop_list):
    for idx in reversed(pop_list):
        keyword_list.pop(idx)
    return keyword_list

def delete_included_word(keyword_list):
    for idx, keyword in enumerate(keyword_list):
        pop_list = []
        for idx2, keyword2 in enumerate(keyword_list[idx + 1:]):
            idx2 += idx + 1
            # print(keyword, keyword2)
            # print(keyword_list[idx], keyword_list[idx2])
            if idx == idx2:
                continue

            if (keyword in keyword2) or (keyword2 in keyword):
                pop_list.append(idx2)
        keyword_list = reserve_list_pop(keyword_list, pop_list)
    return keyword_list

def list_be_unique(my_list):
    unique_list = []
    for item in my_list:
        if item not in unique_list:
            unique_list.append(item)
    return unique_list

def delete_included_word2(keyword_list):
    keyword_list = list_be_unique(keyword_list)
    result_list = []
    for keyword1 in keyword_list:
        include = False
        for keyword2 in keyword_list:
            if keyword1 == keyword2:
                continue  # 같은 키워드는 무시하고 다음으로 넘어감
            if keyword2 in keyword1:
                include = True
                break  # 포함되는 경우 반복문 종료
        if not include:
            result_list.append(keyword1)
    return result_list

def delete_included_word3(keyword_list):
    keyword_list = list_be_unique(keyword_list)
    result_list = []
    for keyword1 in keyword_list:
        include = False
        for keyword2 in keyword_list:
            if keyword1 == keyword2:
                continue  # 같은 키워드는 무시하고 다음으로 넘어감
        if not include:
            result_list.append(keyword1)
    return result_list


def count_word_occurrences(text, target_word):
    words = text.split()
    count = 0

    for word in words:
        print("[", word, "] [", target_word, "]")
        if target_word in word or target_word == word:
            print("!!!!!!!")
            count += 1
    return count


def count_word_list(text, word_list, visualize=True):
    count_list = []
    for word in word_list:
        count = count_word_occurrences(text, word)
        count_list.append(count)

    if visualize:
        # 시각화를 위한 색상 맵 설정
        cmap = plt.get_cmap('viridis', len(word_list))

        # 그래프 크기 설정
        plt.figure(figsize=(10, 6))

        # 각 단어와 해당 단어의 빈도를 바 그래프로 그리기
        plt.bar(word_list, count_list, color=cmap(np.arange(len(word_list))))

        # 축 및 제목 설정
        plt.xlabel('Words')
        plt.ylabel('Occurrences')
        plt.title('Word Occurrences')

        # 그래프 표시
        plt.xticks(rotation=45)
        plt.show()
    print(word_list)
    print(count_list)
    return count_list

def extract_keyword(text):
    keyword_list = []

    model = BertModel.from_pretrained('skt/kobert-base-v1')
    kw_model = KeyBERT(model)
    kiwi = Kiwi()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=50)
    print(keywords)

    for keyword in keywords:
        if keyword == "":
            continue
        # keyword_list.append(keyword[0])
        result = kiwi.analyze(keyword[0])
        keyword_str = ''

        for idx, (token, pos, _, _ )in enumerate(result[0][0]):
            # print(token, pos)

            # '갑자기'와 같은 부사가 중간에 나오면 그 앞까지만 사용
            # if pos.startswith('MAG'):
            #     break
            # 처벌'하'어야와 같이 중간에 동사 파생 접미사가 나오면 그 앞까지만 사용
            if pos.startswith('XSV') or pos.startswith('XSA') or pos.startswith('XSM'):
                break
            # 조사가 단어 중간에 나오면 그 앞까지만 사용
            if pos.startswith('J'):
                if idx != 0 or idx != len(result[0][0]):
                    break
                # 만약 조사가 단어 앞이나 끝에 나오면 조사는 결과에 포함하지 않음.
            # 만약 대명사로 시작하면, 사용 X
            if pos.startswith('NP'):
                keyword_str = ""
                break
            # 어
            if pos.startswith('EP') or pos.startswith('EF') or pos.startswith('EC'):
                keyword_str = ""
                break
            # 부사는 사용 X
            if pos.startswith("MA"):
                break
            keyword_str = keyword_str + token
        
        # 결과가 ""이면 키워드로 저장하지 않기
        if keyword_str == "":
            continue

        keyword_list.append(keyword_str)

    # print(delete_included_word3(keyword_list.copy()))
    
    # return keyword_list

    return delete_included_word3(keyword_list.copy())



# NP만 사용
def extract_keyword2(text):
    keyword_list = []

    model = BertModel.from_pretrained('skt/kobert-base-v1')
    # model = BertModel.from_pretrained('xlm-roberta-large')
    
    kw_model = KeyBERT(model)
    kiwi = Kiwi()
    keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=50)
    print(keywords)

    for keyword in keywords:
        result = kiwi.analyze(keyword[0])
        keyword_str = ''

        for _, (token, pos, _, _ )in enumerate(result[0][0]):
            # print(token, pos,end=" | ")
            if pos.startswith("SN"):
                keyword_str = keyword_str + token
            if pos.startswith("NN") and not(pos.startswith("NNB")): 
                keyword_str = keyword_str + token
            if keyword_str != "" and pos.startswith("XSN"):
                keyword_str = keyword_str + token
        # 결과가 ""이면 키워드로 저장하지 않기
        if keyword_str == "":
            continue

        keyword_list.append(keyword_str)

    # print(delete_included_word3(keyword_list.copy()))
    
    # return keyword_list

    return delete_included_word3(keyword_list.copy())


with open("입학식_연설_preprocessed_text.txt", "r", encoding='UTF8') as file:
    text = file.read()
# print(text)

print()
print(extract_keyword2(text))
# # ---------------------
# # Ko - GPT
# # ---------------------
# from transformers import PreTrainedTokenizerFast
# tokenizer = PreTrainedTokenizerFast.from_pretrained("skt/kogpt2-base-v2",
#   bos_token='</s>', eos_token='</s>', unk_token='<unk>',
#   pad_token='<pad>', mask_token='<mask>')
# import torch
# from transformers import GPT2LMHeadModel

# model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')
# text = '키워드 추출: ' + "자랑스러운 신입생 여러분 여러분의 입학을 진심으로 환영합니다 겨울이 깊으면 봄도 멀지 않으리한 시인은 그렇게 말했습니다 마침내 오늘 따사로운 봄을 맞이합니다 겨울처럼 길고 혹독했던 입시 터을 헤치고 이곳에 이르렀습니다 고통과 인내의 여정 끝에 봄동산의 승자로 오른 여러분을 축하합니다사랑하는 신입생 여러분 요즘 무엇에 감동하고 어느 분야에 호기심을 갖고 있습니까 저는 한 세기를 호기심으로살며 오늘에 이르렀습니다 그런데 최근 두 가지 혁신 제품에 가슴 설레고 있습니다 그것은 다름 아닌인공지능을 활용한 기계와 채팅 로봇, 즉 책 GPT 이 두 가지입니다. 문명의 거대한 변곡점이것을 실감합니다 먼저 인공지능 센서를 이용해서 논밭의 작물에만 골라서 비료를 뿌리는 이것의 뜻 샷입니다.잡초와 고랑에 허비하는 비료를 60%나 아낍니다. 또 AI 센서가 농작물인지 잡초인지를 구별하여 잡초에만농약을 살포하여 그 비용을 70% 이상 줄인다고 합니다. 인공지능은 마침내 1차 산업인 농업문명의 뿌리까지도 바꿨습니다.가 두 번째는 책 GPT입니다 질문이 그 무엇이건 AI가 척척 답변해 주는 책보시입니다을 얼마 전 대통령이 우리말로 신전사를 써보게 했더니 생각보다 그럴 듯했다고 감탄한 바로 그것입니다.또 언어로 문제풀이를 하고 숫자 계산, 주어진 문장에 따른 포딩, 주관식 가만 작성이 가능합니다 기사를 쓰기도.하고 철학을 주제로 한 글쓰기에서 최우수 작품을 내놨다고도 합니다 사랑하는 신입생 여러분 꿈 같고 기적 같은 인인공지능 문명은 숨가쁘게 진화하며 우리를 설레게 만듭니다. 여기에 호기심을 불태우고 심화하여 각자의 미래를 향해 시를꾸려 나가십시오 모두가 컴퓨터 공학을 하거나 앱 개발자가 될 필요는 없습니다 다만 전공 취미 목표가 무엇이건AI를 손에 넣어야 진척과 성취가 있을 것입니다. 이제 AI는 우리 삶의 산소 같은 존재입니다. 여러분.AI 시대에는 경쟁 패턴도 다릅니다 같은 경쟁에서 다름의 경쟁으로 가야 합니다 과거 공업과 제조업 시대에는표준화, 규격화로 같은 중에서 비교 우위를 겨뤘습니다. 그러나 이것은 모조리 인공지능과 자동화가 만들어냅니다.의 AI 시대에는 뜨거운 호기심 상상과 창의에서 비롯되는 철저한 발음과 격차만이 승자의 조건이 됩니다가천대학교는 국내 최초로 학부에 인공지능학과를 만들었습니다 그리고 상상과 창의력을 기르기 위해 엔트리 과정을 만들고3, 4학년 과정에 국내 최초로 창업대학을 세웠습니다. 같은을 버리고 발음을 추구하는 AI 시대의 유일한 온리완대학을 꿈꿉니다 오늘부터 사년 간 우리 모두 호기심을 불태워 인공 지능 세상 초격차 사회의 선도에 나서기를 바랍니다여러분의 입학을 다시 한 번 진심으로 환영합니다."
# input_ids = tokenizer.encode(text, return_tensors='pt')
# gen_ids = model.generate(input_ids,
#                            max_length=1024,
#                            repetition_penalty=2.0,
#                            pad_token_id=tokenizer.pad_token_id,
#                            eos_token_id=tokenizer.eos_token_id,
#                            bos_token_id=tokenizer.bos_token_id,
#                            use_cache=True)
# generated = tokenizer.decode(gen_ids[0])
# print(generated)

# ---------------------
# t5 summarization
# # ---------------------
# import nltk
# nltk.download('punkt')
# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

# model = AutoModelForSeq2SeqLM.from_pretrained('eenzeenee/t5-base-korean-summarization')
# tokenizer = AutoTokenizer.from_pretrained('eenzeenee/t5-base-korean-summarization')

# prefix = "summarize: "
# sample = """
#     자랑스러운 신입생 여러분 여러분의 입학을 진심으로 환영합니다 겨울이 깊으면 봄도 멀지 않으리한 시인은 그렇게 말했습니다 마침내 오늘 따사로운 봄을 맞이합니다 겨울처럼 길고 혹독했던 입시 터을 헤치고 이곳에 이르렀습니다 고통과 인내의 여정 끝에 봄동산의 승자로 오른 여러분을 축하합니다사랑하는 신입생 여러분 요즘 무엇에 감동하고 어느 분야에 호기심을 갖고 있습니까 저는 한 세기를 호기심으로살며 오늘에 이르렀습니다 그런데 최근 두 가지 혁신 제품에 가슴 설레고 있습니다 그것은 다름 아닌인공지능을 활용한 기계와 채팅 로봇, 즉 책 GPT 이 두 가지입니다. 문명의 거대한 변곡점이것을 실감합니다 먼저 인공지능 센서를 이용해서 논밭의 작물에만 골라서 비료를 뿌리는 이것의 뜻 샷입니다.잡초와 고랑에 허비하는 비료를 60%나 아낍니다. 또 AI 센서가 농작물인지 잡초인지를 구별하여 잡초에만농약을 살포하여 그 비용을 70% 이상 줄인다고 합니다. 인공지능은 마침내 1차 산업인 농업문명의 뿌리까지도 바꿨습니다.가 두 번째는 책 GPT입니다 질문이 그 무엇이건 AI가 척척 답변해 주는 책보시입니다을 얼마 전 대통령이 우리말로 신전사를 써보게 했더니 생각보다 그럴 듯했다고 감탄한 바로 그것입니다.또 언어로 문제풀이를 하고 숫자 계산, 주어진 문장에 따른 포딩, 주관식 가만 작성이 가능합니다 기사를 쓰기도.하고 철학을 주제로 한 글쓰기에서 최우수 작품을 내놨다고도 합니다 사랑하는 신입생 여러분 꿈 같고 기적 같은 인인공지능 문명은 숨가쁘게 진화하며 우리를 설레게 만듭니다. 여기에 호기심을 불태우고 심화하여 각자의 미래를 향해 시를꾸려 나가십시오 모두가 컴퓨터 공학을 하거나 앱 개발자가 될 필요는 없습니다 다만 전공 취미 목표가 무엇이건AI를 손에 넣어야 진척과 성취가 있을 것입니다. 이제 AI는 우리 삶의 산소 같은 존재입니다. 여러분.AI 시대에는 경쟁 패턴도 다릅니다 같은 경쟁에서 다름의 경쟁으로 가야 합니다 과거 공업과 제조업 시대에는표준화, 규격화로 같은 중에서 비교 우위를 겨뤘습니다. 그러나 이것은 모조리 인공지능과 자동화가 만들어냅니다.의 AI 시대에는 뜨거운 호기심 상상과 창의에서 비롯되는 철저한 발음과 격차만이 승자의 조건이 됩니다가천대학교는 국내 최초로 학부에 인공지능학과를 만들었습니다 그리고 상상과 창의력을 기르기 위해 엔트리 과정을 만들고3, 4학년 과정에 국내 최초로 창업대학을 세웠습니다. 같은을 버리고 발음을 추구하는 AI 시대의 유일한 온리완대학을 꿈꿉니다 오늘부터 사년 간 우리 모두 호기심을 불태워 인공 지능 세상 초격차 사회의 선도에 나서기를 바랍니다여러분의 입학을 다시 한 번 진심으로 환영합니다.
#     """

# inputs = [prefix + sample]


# inputs = tokenizer(inputs, max_length=1024+512, truncation=True, return_tensors="pt")
# output = model.generate(**inputs, num_beams=3, do_sample=True, min_length=128, max_length=256)
# decoded_output = tokenizer.batch_decode(output, skip_special_tokens=True)[0]
# result = nltk.sent_tokenize(decoded_output.strip())[0]

# print('RESULT >>', result)
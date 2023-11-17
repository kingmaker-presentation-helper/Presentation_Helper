r_f = open("입학식_연설_recognized_text.txt", 'r', encoding='UTF8')
w_f = open("입학식_연설_preprocessed_text.txt", "w", encoding='UTF8')

lines = r_f.readlines()
for line in lines:
    if line.startswith("[Segment"):
        continue
    if line.startswith("에 "):
        w_f.write(line[2:].split("\n")[0])
        continue
    # print(line.split("\n")[0], end="")
    # w_f.write(line.split("\n")[0])
    w_f.write(line)
r_f.close()
import os

def isFind(line,question):
    result = len(question)
    for q in question:
        if line.find(q) != -1:
            result -= 1
    return result

question = ['匈奴', '劉邦', '破', '漢', '圧迫']

def splitQuestion(question):
    result = []
    for i,val in enumerate(question):
        tmpArr = []
        for q in question:
            tmpArr.append(q)
        tmpArr.pop(i)
        result.append(tmpArr)
    return result

questions = splitQuestion(question)

results = [0 for j in range(len(questions))]

with open("noblank_jawiki.txt") as f:
    for i,line in enumerate(f):
        for qindex, question in enumerate(questions):
            if isFind(line, question) == 0:
                results[qindex] += 1
                print("-------------", i)
                print(question)
                print(line)
                print("-------------", i)

print(results)

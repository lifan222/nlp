import os
import math

def isFind(line,question):
    result = len(question)
    for q in question:
        if line.find(q) != -1:
            result -= 1
    return result

question = ["ヴェルサイユ宮殿","バロック様式"]

results = []

with open("noblank_jawiki.txt") as f:
    for i,line in enumerate(f):
        if isFind(line, question) == 0:
            results.append(math.fabs(line.find(question[0])-line.find(question[1])))
            print("-------------", i)
            print(question)
            print(line)
            print("-------------", i)

results.sort()
newResult = []
average1 = sum(results) / float(len(results))

for val in results:
    if val < average1:
        newResult.append(val)
    else:
        break

average2 = sum(newResult) / float(len(newResult))

print(results)
print(average1)
print(average2)

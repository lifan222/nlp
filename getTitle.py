import os
import codecs
import string
import math
import bisect

wikiArr = []
with open("finalWiki.txt") as f:
    for line in f:
        wikiArr.append(line)
# wikiTitleLineArr = []
# wikiTitleArr = []
# with open("wikiTitle.txt") as f:
#     for line in f:
#         wikiTitleLineArr.append(int(line.split("-->>")[1]))
#         wikiTitleArr.append(line.split("-->>")[0])

def isFind(line,question):
    result = len(question)
    for q in question:
        if line.find(q) != -1:
            result -= 1
    return result

def splitQuestion(question):
    result = [question]
    for i in range(len(question)):
        result.append([question[i]])
    return [result]

def calFrequecny(arr):
    arr.sort()
    a1 = arr[0]
    a2 = arr[1]
    a3 = arr[2]
    try:
        return [0.6*math.log(a1,a2)+0.1*math.log(a2,a3)+0.3*math.log(a1,a3),float(a1)/a2]
    except:
        return 0

def output(question):
    questionArrs = splitQuestion(question)
    print(questionArrs)
    results = []
    docResults = []
    docFrenq = []
    for qs in questionArrs:
        results.append([0 for j in range(len(qs))])
        docResults.append([0 for j in range(len(qs))])
        docFrenq.append([0 for j in range(len(qs))])
    for (i,questions) in enumerate(questionArrs):
        for (qindex,question) in enumerate(questions):
            tmpDocCount = 0
            tmpCount = 0
            tmpMax = 0
            for (windex,line) in enumerate(wikiArr):
                if line[:2] == "[[":
                    if tmpCount >= tmpMax:
                        tmpMax = tmpCount
                    tmpCount = 0
                    tmpBool = 1
                if isFind(line, question) == 0:
                    results[i][qindex] += 1
                    tmpCount += 1
                    if tmpBool == 1:
                        tmpDocCount += 1
                        tmpBool = 0
            docResults[i][qindex] = tmpMax
            docFrenq[i][qindex] = tmpDocCount
    print(results)
    print(docResults)
    print(docFrenq)
    for freq in results:
        print(calFrequecny(freq))

questions1 = [["アルハンブラ", "宮殿"], \
            ["ヴェルサイユ", "宮殿"], \
            ["イルハン", "国"], \
            ["ローマカトリック", "教会"], \
            ["イスラーム", "様式"],\
            ["ヒンドゥー", "教"],\
            ["マジャール", "人"],\
            ["モンゴル","軍"],\
            ["ブルガリア","王国"],\
            ["アッバース","朝"]]

questions2 = [["ナポレオン", "3世"], \
            ["ヴィルヘルム", "2世"], \
            ["大陸", "封鎖令"], \
            ["キリル", "文字"], \
            ["征服", "地"],\
            ["共和政", "ローマ"],\
            ["則天", "武后"],\
            ["アラビア","語"],\
            ["玄奘","三蔵"],\
            ["新約","聖書"]]

questions3 = [["アメンホテプ4世", "一神教"], \
            ["カージャール", "バーブ"], \
            ["イルハン", "バーブ"], \
            ["ツヴィングリ", "プラハ"], \
            ["ツヴィングリ", "チューリヒ"],\
            ["白蓮教", "明代"],\
            ["白蓮教", "清代"],\
            ["明代","消滅"],\
            ["清代","反乱"],\
            ["白蓮教","消滅"],\
            ["白蓮教","反乱"]]

questions4 = [["ナポレオン3世", "大陸封鎖令"], \
            ["ナポレオン3世", "発布"], \
            ["大陸封鎖令", "発布"], \
            ["ナポレオン", "大陸封鎖令"], \
            ["ナポレオン", "発布"],\
            ["ヴィルヘルム2世", "社会主義者鎮圧法"],\
            ["ヴィルヘルム2世", "制定"],\
            ["社会主義者鎮圧法","制定"],\
            ["ビスマルク","社会主義者鎮圧法"],\
            ["ビスマルク","制定"]]

questions5 = [["北京", "紫禁城"], \
            ["紫禁城", "宮殿"], \
            ["宋", "皇帝"], \
            ["皇帝", "宮殿"], \
            ["紫禁城", "宋"],\
            ["宋", "宮殿"],\
            ["明", "皇帝"],\
            ["明","宮殿"],\
            ["紫禁城","明"]]

questions = [['明', '紫禁城'],['明朝', '紫禁城']]
for q in questions:
    output(q)
########################################################
# count = 0
# with open("finalWiki.txt") as f:
#     for (i,line) in enumerate(f):
#         if line.find("征服地") != -1:
#             count += 1
# print(count)

 # 1/(1+m.exp(-m.log((float(fs.count("寺院"))/fs.count("ヒンドゥー教")),10)))

##########################################################
# count = 0
# with open("wikiTitle.txt") as f:
#     for (i,line) in enumerate(f):
#         count += 1
#         # if line.find("バックプロパゲーション") != -1:
#         #     print(line)
# print(count)

def getImpWord(a,b,c):
    s1 = [float(a[j])/c[j] for j in range(len(a))]
    s2 = [float(b[j])/c[j] for j in range(len(a))]
    s3 = [math.log(a[j],c[j]) for j in range(len(a))]
    s4 = [math.log(b[j],c[j]) for j in range(len(a))]
    result = [0 for j in range(len(a))]
    result[s1.index(min(s1))] += 1
    result[s2.index(min(s2))] += 1
    result[s3.index(min(s3))] += 1
    result[s4.index(min(s4))] += 1
    result[c.index(max(c))] += 1
    print(s1)
    print(s2)
    print(s3)
    print(s4)
    print(a)
    print(result)

def regetImpWord(a,b,c):
    result1 = [math.log(10241062,b[j]) for j in range(len(a))]
    result2 = [math.log(10241062,a[j]) for j in range(len(a))]
    result3 = [result1[j]*c[j] for j in range(len(a))]
    result4 = [result2[j]*c[j] for j in range(len(a))]
    print(a)
    print(b)
    print(c)
    print(result1)
    print(result2)
    print(result3)
    print(result4)

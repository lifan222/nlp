import os
import subprocess
import codecs
import xml.etree.ElementTree as ET
from gensim.models import word2vec
import math
import re
wikiArr = []
with open("finalWiki.txt") as f:
    for lineWiki in f:
        wikiArr.append(lineWiki)
#------------------------------------- OS環境変数が Windows_NT の場合のみデフォルトの文字コードを shift-jis にする
if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
    default_encoding='shift-jis'
else:
    default_encoding='utf-8'
#---------- -----------------------------環境に依存しない行単位での文字列分割
def line_split(text):
    return text.splitlines()
#---------------------------------------------------ASAコマンド
def res_cmd(cmd,input):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    return process.communicate(input=input)[0];
def getdata(input_file):
    fin = open(input_file)
    fin_lines = fin.readlines()
    fin.close()
    data_books = []
    link_books = []
    fin_str = ''

    for line in fin_lines:
        if "（" in line and "）" in line:
            tmpLine = re.split("\（|\）", line)
            fin_str += tmpLine[0] + tmpLine[-1]
        else:
            fin_str += line

    cmd = 'java -jar ASA20150617.jar -x'
    cmd_str = res_cmd(cmd, fin_str.encode(default_encoding))
    xml_str = cmd_str.decode(default_encoding)
    xml_list = line_split(xml_str)

    fout = codecs.open('data.xml', 'w', 'utf-8')
    for line in xml_list:
        if line != 'input':
            if line == '起動中':
                fout.write('<data>'+'\n')
            else:
                fout.write(line+'\n')
    fout.write('</data>')
    fout.close()

    #XMLからリストに変換
    data_tree = ET.parse('data.xml')
    data_roots = data_tree.getroot()
    for data_root in data_roots:
        data_lists = []
        waitEnd = 1
        tmpLinkArr = []
        for (iw, child) in enumerate(data_root):
            if child.tag == "sentence":
                tmp_sentence = child.text
            elif child.tag != 'sentence':
                #chunkごとに要素を抽出
                tmp_bool = 0
                tmp_verb = 0
                tmpNounSurface = ""
                tmp_morph = []
                for subchild in child:
                    if subchild.text == 'copula':
                        tmp_bool = 1
                    elif subchild.text == 'verb':
                        tmp_verb = 1
                    elif subchild.tag == 'morph' and tmp_verb == 1 and waitEnd == 1:
                         data_lists.append(subchild[0].text)
                         break
                    elif subchild.tag == 'link':
                        tmpLinkArr.append(int(subchild.text))
                    elif subchild.tag == 'surface':
                        if "「" in subchild.text and "」" in subchild.text:
                            waitEnd = 1
                            tmp_the = re.split("\「|\」",tmp_sentence)
                            data_lists.append(tmp_the[1])
                            break
                        elif subchild.text.find("「") != -1:
                            waitEnd = 0
                            break
                        elif subchild.text.find("」") != -1:
                            waitEnd = 1
                            tmp_the = re.split("\「|\」",tmp_sentence)
                            data_lists.append(tmp_the[1])
                            break
                        elif "『" in subchild.text and "』" in subchild.text:
                            waitEnd = 1
                            tmp_the = re.split("\『|\』",tmp_sentence)
                            data_lists.append(tmp_the[1])
                            break
                        elif subchild.text.find("『") != -1:
                            waitEnd = 0
                            break
                        elif subchild.text.find("』") != -1:
                            waitEnd = 1
                            tmp_the = re.split("\『|\』",tmp_sentence)
                            data_lists.append(tmp_the[1])
                            break
                    elif subchild.tag == 'noun_surface':
                        tmp_bool = 1
                        tmpNounSurface = subchild.text
                    elif subchild.tag == "category" and subchild.text == "動作":
                        tmpLinkArr[-1] = tmpLinkArr[-1] * -1
                    elif subchild.tag == 'morph' and tmp_bool == 1 and waitEnd == 1:
                        for subsubchild in subchild:
                            if subsubchild.tag == 'surface' and tmpNounSurface.find(subsubchild.text) != -1:
                                tmp_morph.append(subsubchild.text)
                if len(tmp_morph) > 1:
                    data_lists.append(tmp_morph)
                elif len(tmp_morph) == 1:
                    data_lists.append(tmp_morph[0])
        data_books.append(data_lists)
        link_books.append(tmpLinkArr)
    print("******questionData*********")
    print([data_books,link_books])
    print("***************************")
    return [data_books,link_books]
def isFind(line,question):
    result = len(question)
    for q in question:
        if line.find(q) != -1:
            result -= 1
    return result
def splitQuestion(question):
    result = []
    for i in range(len(question)-1):
        result.append([[question[i], question[i+1]], [question[i]], [question[i+1]]])
    return result
def calFrequecny(arrData):
    freqData = []
    for arrs in arrData:
        tmpArr = []
        if len(arrs) == 0:
            tmpArr.append(1)
        else:
            for arr in arrs:
                arr.sort()
                a1 = arr[0]
                a2 = arr[1]
                a3 = arr[2]
                try:
                    # tmpArr.append(0.6*math.log(a1,a2)+0.1*math.log(a2,a3)+0.3*math.log(a1,a3))
                    tmpArr.append()
                except:
                    tmpArr.append(0)
        freqData.append(tmpArr)
    return freqData
def calLinkFreq(arr):
    arr.sort()
    a1 = arr[0]
    a2 = arr[1]
    a3 = arr[2]
    try:
        return 0.6*math.log(a1,a2)+0.1*math.log(a2,a3)+0.3*math.log(a1,a3)
    except:
        return 0
def updateDataByTitle(questionData):
    fin = open("wikiTitle.txt")
    fs = fin.read()
    for (s,sentence) in enumerate(questionData):
        tmpWords = []
        for (w,word) in enumerate(sentence):
            if type(word) == list:
                tmps = "".join(word)
                tmpCount = 0
                for line in wikiArr:
                    tmpCount += line.count(tmps)
                titleIndex = fs.find(tmps)
                print(tmps, tmpCount)
                if (titleIndex != -1 and fs[titleIndex-1] == "\n" and fs[titleIndex+len(tmps)] == "-") or tmpCount > 500:
                    questionData[s][w] = tmps
    fin.close()
    print("******updateDataByTitle*********")
    print(questionData)
    print("***************************")
    return questionData

def selectLeastWord(linkPart):
    wordFreq = [0 for j in range(len(linkPart))]
    resultArr = []
    docResults = [0 for j in range(len(linkPart))]
    for (w,word) in enumerate(linkPart):
        tmpCount = 0
        tmpMax = 0
        for (windex,line) in enumerate(wikiArr):
            if line[:2] == "[[":
                if tmpCount >= tmpMax:
                    tmpMax = tmpCount
                tmpCount = 0
            if isFind(line, word) == 0:
                wordFreq[w] += line.count(word)
                tmpCount += 1
        docResults[w] = tmpMax
    wordDF = [(float(wordFreq[j])/docResults[j]) for j in range(len(wordFreq))]
    return linkPart[wordDF.index(min(wordDF))]

def selectLinkPart(linkPart, verbWord, isLast):
    if isLast == 1:
        linkPart.append(verbWord)
    wordFreq = [0 for j in range(len(linkPart))]
    pairFreq = []
    pairArr = []
    resultArr = []
    docResults = [0 for j in range(len(linkPart))]
    docFreq = [0 for j in range(len(linkPart))]
    for (w,word) in enumerate(linkPart):
        tmpCount = 0
        tmpMax = 0
        tmpDocBool = 0
        if w < len(linkPart)-1:
            pairArr.append([linkPart[w],linkPart[w+1]])
        for (windex,line) in enumerate(wikiArr):
            if line[:2] == "[[":
                if tmpCount >= tmpMax:
                    tmpMax = tmpCount
                tmpCount = 0
                tmpDocBool = 1
            if word in line:
                wordFreq[w] += line.count(word)
                tmpCount += 1
                if tmpDocBool == 1:
                    docFreq[w] += 1
                    tmpDocBool = 0
        docResults[w] = tmpMax
    for p in pairArr:
        tmpPairCount = 0
        for line in wikiArr:
            countP1 = line.count(p[0])
            countP2 = line.count(p[1])
            tmpPairCount += min(countP1,countP2)
        pairFreq.append(tmpPairCount)
    for i in range(len(pairArr)):
        resultArr.append(calLinkFreq([pairFreq[i], wordFreq[i], wordFreq[i+1]]))
    docResults.pop(-1)
    wordFreq.pop(-1)
    docFreq.pop(-1)
    wordDF = [(float(docFreq[j])/docResults[j]) for j in range(len(docFreq))]
    # wordDF = [math.log(docResults[j],docFreq[j]) for j in range(len(docFreq))]
    result = [linkPart[wordDF.index(min(wordDF))], min(resultArr)]
    print("******linkPart*********")
    print(linkPart)
    print("******wordFreq*********")
    print(wordFreq)
    print("******docFreq*********")
    print(docFreq)
    # print("******pairFreq*********")
    # print(pairFreq)
    print("******docResults*********")
    print(docResults)
    print("******wordDF*********")
    print(wordDF)
    print("******linkResult*********")
    print(result)
    print("***************************")
    return result
def linkQuestion(question, linkArr):
    tmpArr = []
    tmpLink = 0
    result = []
    for (i,v) in enumerate(linkArr):
        if v < -1:
            linkArr[i] = math.fabs(v)
    for (i,l) in enumerate(linkArr):
        if math.fabs(l) == max(linkArr):
            tmpArr.append(i+1)
        elif l == -1:
            tmpLink = i
    result.append(question[0:tmpArr[0]])
    for j in range(len(tmpArr)-1):
        result.append(question[tmpArr[j]:tmpArr[j+1]])
    result.append(question[tmpLink])
    return result
def moreUpdateDataByTitle(questionData, linkArr):
    fin = open("wikiTitle.txt")
    fs = fin.read()
    for isentece in range(len(questionData)):
        questionData[isentece] = linkQuestion(questionData[isentece], linkArr[isentece])
    print(questionData)
    for (s,sentence) in enumerate(questionData):
        verbWord = sentence[-1]
        for (l, linkPart) in enumerate(sentence):
            if type(linkPart) == list:
                for i in range(len(linkPart)):
                    if (type(linkPart[i]) != list):
                        if i < len(linkPart) - 1:
                            if (type(linkPart[i+1]) != list) and (linkPart[i] != ""):
                                linkPartStr = linkPart[i]+linkPart[i+1]
                                linkPartFindIndex = fs.find(linkPartStr)
                                if linkPartFindIndex != -1 and \
                                fs[linkPartFindIndex+len(linkPartStr)] == "-" and \
                                fs[linkPartFindIndex-1] == "\n":
                                    linkPart[i] = linkPart[i]+linkPart[i+1]
                                    linkPart[i+1] = ""
                    else:
                        linkPart[i] = selectLeastWord(linkPart[i])
                questionData[s][l] = list(filter(None, linkPart))
    print("******moreUpdateDataByTitle*********")
    print(questionData)
    print("***************************")
    return questionData

def selectLastLinkPart(linkPart):
    wordFreq = [0 for j in range(len(linkPart))]
    pairFreq = []
    pairArr = []
    resultArr = []
    for (w,word) in enumerate(linkPart):
        if w < len(linkPart)-1:
            pairArr.append([linkPart[w],linkPart[w+1]])
        for line in wikiArr:
            wordFreq[w] += line.count(word)
    for p in pairArr:
        tmpPairCount = 0
        for line in wikiArr:
            countP1 = line.count(p[0])
            countP2 = line.count(p[1])
            tmpPairCount += min(countP1,countP2)
        pairFreq.append(tmpPairCount)
    for i in range(len(pairArr)):
        resultArr.append(calLinkFreq([pairFreq[i], wordFreq[i], wordFreq[i+1]]))
    print(resultArr)
    result = min(resultArr)
    print("******linkPart*********")
    print(linkPart)
    print("******pairFreq*********")
    print("******wordFreq*********")
    print(wordFreq)
    print("******pairFreq*********")
    print(pairFreq)
    print("******lastlinkResult*********")
    print(resultArr)
    print(result)
    return result

def getLinkId(linkPart, question, linkArr):
    newQuestion = []
    for (i,q) in enumerate(question):
        if type(q) == list:
            for nq in q:
                newQuestion.append(nq)
        else:
            newQuestion.append(q)
    return [linkArr[newQuestion.index(linkPart[0])],linkArr[newQuestion.index(linkPart[1])]]
def output_result(question_txt, output_txt):
    getDataCouple = getdata(question_txt)
    questionData = moreUpdateDataByTitle(updateDataByTitle(getDataCouple[0]), getDataCouple[1])
    lastFreqResultArr = []
    for (s,sentence) in enumerate(questionData):
        newSentence = []
        freqResult = []
        verbWord = sentence[-1]
        for linkPart in sentence:
            if type(linkPart) == list:
                # linkArr = getLinkId(linkPart, getDataCouple[0][s], getDataCouple[1][s])
                print(linkPart)
                if len(linkPart) <= 1:
                    newSentence.append(linkPart[0])
                else:
                    linkPartCoupleArr = selectLinkPart(linkPart, verbWord, 1)
                    newSentence.append(linkPartCoupleArr[0])
                    freqResult.append(linkPartCoupleArr[1])
        freqResult.append(selectLastLinkPart(newSentence))
        lastFreqResultArr.append(min(freqResult))

    print("******lastFreqResultArr*********")
    print(lastFreqResultArr)
    print("***************************")
output_result('question.txt', 'output.txt')
# questionData = moreUpdateDataByTitle(updateDataByTitle(getdata("question1.txt")))
# print(len(wikiArr))

import os
import subprocess
import codecs
import xml.etree.ElementTree as ET

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

def isFind(line,question):
    result = len(question)
    for q in question:
        if line.find(q) != -1:
            result -= 1
    return result

#---------------------------------------------------wikiのtitleを取得
def getTitleName(title_txt):
    results = []
    with open(title_txt) as f:
        for line in f:
            results.append(line.split("-->>")[0])
    return results

#---------------------------------------------------wikiのtitleの行数を取得
def getTitlePos(title_txt):
    results = []
    with open(title_txt) as f:
        for line in f:
            results.append(int(line.split("-->>")[1][:-1]))
    return results

#---------------------------------------------------固有名詞判定
def isTitle(s,titleNameArr):
    if s in titleNameArr:
        return True
    else:
        return False


#---------------------------------------------------とも表記(固有名詞同義語判別)
def sameTitle(i,line,s,arr1,arr2):
    question = ["とも表記", s]
    pos = 0
    if isFind(line,question) == 0:
        arr2.append(i)
        arr2.sort()
        pos = arr2.index(i)-1
        return arr1[pos]

def getdata(input_file):
    fin = open(input_file)
    fin_lines = fin.readlines()
    fin.close()
    data_books = []
    fin_str = ''
    lineRecord = []
    for line in fin_lines:
        tmpLineArr = line.split("-->>")
        tmpStr = tmpLineArr[0]
        if tmpStr.find(")") != -1:
            newTmpStr = ""
            go = 1
            for s in tmpStr:
                if s == "（":
                    go = 0
                elif s == "）":
                    go = 1
                    continue
                if go == 1:
                    newTmpStr += s
            fin_str += newTmpStr+"\n"
        else:
            fin_str += tmpStr+"\n"
        lineRecord.append(tmpLineArr[1][:-1])

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
    for (i,data_root) in enumerate(data_roots):#data
        data_lists = []
        for child in data_root:#sent
            tmp_bool = 0
            if child.tag != 'sentence':#chunk
                tomokeyBool = 0
                if child[0].text.find("とも") != -1:
                    tomokeyBool = 1
                data_arr = []
                for subchild in child:
                    if subchild.tag == 'link':
                        data_arr.append(subchild.text)
                        if tomokeyBool == 1:
                            tomoLink = subchild.text
                    if subchild.tag == 'noun_surface':
                        data_arr.append(subchild.text)
                        if tomokeyBool == 1:
                            tomoText = subchild.text
                data_lists.append(data_arr)
        data_lists.append(lineRecord[i])
        data_lists.append([tomoLink,tomoText])
        data_books.append(data_lists)
    return data_books

titleNameArr = getTitleName("wikiTitle.txt")
titlePosArr = getTitlePos("wikiTitle.txt")
tmpSameTitleArrs = getdata("tomohyoki.txt")
results = []
for titleSent in tmpSameTitleArrs:
    result = []
    linkID = int(titleSent[-1][0])
    lineNum = int(titleSent[-2])
    linkArr = titleSent[-1]
    result.append(linkArr[1])
    titleSent = titleSent[:-2]
    titleSent.reverse()
    for (i,titleArr) in enumerate(titleSent):
        if linkID - int(titleArr[0]) == 1:
            result.append(titleArr[1])
            linkID -= 1
    titlePosArr.append(lineNum)
    titlePosArr.sort()
    pos = titlePosArr.index(lineNum)-1
    result.insert(0, titleNameArr[pos])
    results.append(result)
    titlePosArr.remove(lineNum)

fout = codecs.open("sameTitle.txt", 'w', 'utf-8')
for (i,arr) in enumerate(results):
    try:
        fout.write(",".join(arr)+"\n")
    except Exception as e:
        print(e)

import os
import subprocess
import codecs
import xml.etree.ElementTree as ET
from gensim.models import word2vec

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

#-------------------------------------------教科書と問題文の読み取り
def getdata(input_file):
    fin = open(input_file)
    fin_lines = fin.readlines()
    fin.close()
    data_books = []
    fin_str = ''

    for line in fin_lines:
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
        data_list = ['', {}]
        for child in data_root:
            tmp_bool = 0
            if child.tag != 'sentence':
                #chunkごとに要素を抽出
                for subchild in child:
                    if subchild.text == 'copula' or subchild.text == 'verb' :
                        tmp_bool = 1
                    if subchild.tag == 'morph' and tmp_bool == 1:
                        for subsubchild in subchild:
                            if subsubchild.tag == 'surface':
                                data_lists.append(subsubchild.text)
                                tmp_bool = 0
                    if subchild.tag == 'noun_surface' and tmp_bool == 0:
                        data_lists.append(subchild.text)
        data_books.append(data_lists)
    print(data_books)
    return data_books

def isFind(line,question):
    tmpBool = True
    for q in question:
        getLine = line.find(q)
        if getLine == -1:
            tmpBool = False
    return tmpBool

def output_result(input_txt, question_txt, output_txt):
    questions = getdata(question_txt)
    results = [[],[],[],[]]
    fout = codecs.open(output_txt, 'w', 'utf-8')
    with open(input_txt) as f:
        for i,line in enumerate(f):
            print(i)
            for qindex, question in enumerate(questions):
                if isFind(line, question):
                    print(line)
                    results[qindex].append(line)
    return results

print(output_result("jawiki_wakati.txt", 'question.txt', 'output.txt'))
#

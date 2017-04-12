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
                    if subchild.text == 'verb':
                        break
                    if subchild.text == 'copula' :
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

def output_result(question_txt, output_txt):
    model = word2vec.Word2Vec.load("jawiki_wakati.model")
    questions = getdata(question_txt)
    results = []
    fin = open(question_txt)
    fin_lines = fin.read().splitlines()
    fin.close()
    fout = codecs.open(output_txt, 'w', 'utf-8')
    for question in questions:
        result = []
        for i in range(len(question)):
            if i < len(question)-1:
                try:
                    result.append(model.similarity(question[i], question[i+1]))
                except :
                    print(question)
        try:
            result.append(sum(result)/len(result))
        except:
            result.append(0.5) 

        results.append(result)
    print(results)
    # for idx, val in enumerate(fin_lines):
    #     fout.write(val+','+results[idx]+'\n')

# def output_result(question_txt, output_txt):
#     questions = getdata(question_txt)
#     result = []
#     fin = open(question_txt)
#     fin_lines = fin.read().splitlines()
#     fin.close()
#     fout = codecs.open(output_txt, 'w', 'utf-8')
#     for question in questions:
#         if question in textbooks:
#             result.append('1')
#         else:
#             result.append('0')
#     for idx, val in enumerate(fin_lines):
#         fout.write(val+','+result[idx]+'\n')
#
# #----------------------------------------------main
#
output_result('question.txt', 'output.txt')
#

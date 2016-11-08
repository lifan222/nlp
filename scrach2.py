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


#-------------------------------------------教科書と問題文の読み取り
def getdata(input_file):
    fin = open(input_file)
    fin_lines = fin.readlines()
    fin.close()
    data_dicts = {}
    line_num = 0

    for fin_line in fin_lines:
        fin_list = fin_line.split(",")
        fin_num = fin_list[0]
        fin_str = fin_list[1]
        line_num += 1
        #中間XMLを生成する
        cmd = 'java -jar ASA20150617.jar -x'
        cmd_str = res_cmd(cmd, fin_str.encode(default_encoding))
        xml_str = cmd_str.decode(default_encoding)
        xml_list = line_split(xml_str)
        del xml_list[0]
        del xml_list[0]
        del xml_list[-1]
        fout = codecs.open('data.xml', 'w', 'utf-8')
        for line in xml_list:
            fout.write(line+'\n')
        fout.close()

        #XMLからリストに変換
        data_lists = []
        data_list = ['', {}]
        data_tree = ET.parse('data.xml')
        data_root = data_tree.getroot()

        for child in data_root:
            tmp_dict = {}
            tmp_link = ""
            if child.tag != 'sentence':
                #chunkごとに要素を抽出
                for subchild in child:
                    if subchild.tag == 'semrole':
                        tmp_dict['semrole'] = subchild.text
                    elif subchild.tag == 'noun_surface':
                        tmp_dict['noun_surface'] = subchild.text
                    elif subchild.tag == 'type':
                        tmp_dict['type'] = subchild.text
                    elif subchild.tag == 'link':
                        tmp_dict['link'] = subchild.text

                if tmp_dict['type'] == 'verb':
                    data_list[0] = tmp_dict['noun_surface']
                    data_lists.append(data_list)
                    data_list = ['', {}]
                else:
                    if 'semrole' in tmp_dict:
                        data_list[1][tmp_dict['semrole']] = tmp_dict['noun_surface']
                    else:
                        data_list[1]['link'+tmp_dict['link'] ] = tmp_dict['noun_surface']

        if len(fin_list) > 2:
            data_dicts["問"+str(line_num)] = data_lists
            answer["問"+str(line_num)] = fin_list[2]
            if textbook_list[fin_num] == data_lists:
                result["問"+str(line_num)] = 1
            else:
                result["問"+str(line_num)] = 0
            if result["問"+str(line_num)] == answer["問"+str(line_num)]:
                score += 1
        else:
            data_dicts[fin_num] = data_lists

    return data_dicts

#----------------------------------------------main
result = {}
answer = {}
score = 0
textbook_list = getdata('input.txt')
question_list = getdata('question.txt')
print(textbook_list)
print(question_list)
print(result)
print(answer)
print("点数："+str(score))






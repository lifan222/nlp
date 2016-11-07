import os
import subprocess
import xml.etree.ElementTree as ET

#---------------------------------------------------ASA command----------------------------------------------------------------
def res_cmd(cmd,input):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    return process.communicate(input=input)[0];
#-------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------from txt to list--------------------------------------------------------------
def getdata(input_file):
    #---------------------------------------------------read input file----------------------------------------
    fin = open(input_file)
    fin_str = fin.read()
    fin.close()
    #----------------------------------------------------------------------------------------------------------------

    #----------------------------------------output ASA result as xml--------------------------------
    cmd = 'java -jar ASA20150617.jar -x'
    cmd_str = res_cmd(cmd, fin_str.encode('utf-8'))
    xml_str = cmd_str.decode('utf-8')
    xml_list = xml_str.split('\n')
    del xml_list[0]
    del xml_list[-1]
    del xml_list[-1]
    fout = open('data.xml', 'w')
    for line in xml_list:
        fout.write(line+'\n')
    fout.close()
    #----------------------------------------------------------------------------------------------------------------

    #--------------------------------------------------- get result as list-----------------------------------
    data_list = ['', {}]
    data_tree = ET.parse('data.xml')
    data_root = data_tree.getroot()
    for child in data_root:
        if child.tag != 'sentence':
            if child[1].text == '-1':
                data_list[0] = child[3].text
            else:
                data_list[1][child[6].text] = child[3].text
    return data_list
    #print(data_list)
    #----------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------------------------

def check(textbook, question):
    textbook_list = getdata(textbook)
    question_list = getdata(question)
    print(textbook_list)
    print(question_list)

    if textbook_list == question_list:
        print ('正解！')
    else:
        print('残念！')

check('input.txt', 'question.txt')

print(getdata("input.txt"))






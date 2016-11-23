import os
import subprocess
import codecs
import xml.etree.ElementTree as ET

if 'OS' in os.environ and os.environ['OS'] == 'Windows_NT':
    default_encoding='shift-jis'
else:
    default_encoding='utf-8'

def line_split(text):
    return text.splitlines()

def res_cmd(cmd,input):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    return process.communicate(input=input)[0];

fin = open('input.txt')
fin_lines = fin.readlines()
fin.close()

fin_str = ''

for line in fin_lines:
    fin_str += line

print(fin_str)

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

data_tree = ET.parse('data.xml')
data_roots = data_tree.getroot()
print(data_roots)



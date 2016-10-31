import os
import subprocess

f = open('data.txt', 'w')

def res_cmd(cmd,input):
    process = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,shell=True)
    return process.communicate(input=input)[0];
def res_cmd_stdin(cmd):
    popen = subprocess.Popen(cmd, stdout=subprocess.PIPE,shell=True)
    return popen.communicate()[0];

input_str = '太郎はこの本を二郎を見た女性に渡した。'
cmd = 'java -jar ASA20150617.jar -x'

cmd_str = res_cmd(cmd, input_str.encode('utf-8'))
output_str = cmd_str.decode('utf-8')

f.write(output_str)
